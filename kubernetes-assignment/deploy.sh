#!/bin/bash

# Colors for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if minikube is running
check_minikube() {
    echo -e "${BLUE}Checking if minikube is running...${NC}"
    if ! minikube status | grep -q "Running"; then
        echo -e "${YELLOW}Minikube is not running. Starting minikube...${NC}"
        minikube start
        if [ $? -ne 0 ]; then
            echo -e "${RED}Failed to start minikube. Please check your installation.${NC}"
            exit 1
        fi
    else
        echo -e "${GREEN}Minikube is already running!${NC}"
    fi
}

# Check if Helm is installed
check_helm() {
    echo -e "${BLUE}Checking if Helm is installed...${NC}"
    if ! command -v helm &> /dev/null; then
        echo -e "${YELLOW}Helm is not installed. Installing Helm...${NC}"
        
        # Create a temporary directory
        TMP_DIR=$(mktemp -d)
        
        # Download and install Helm
        echo -e "${BLUE}Downloading Helm...${NC}"
        curl -fsSL -o $TMP_DIR/get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
        chmod 700 $TMP_DIR/get_helm.sh
        
        echo -e "${BLUE}Installing Helm...${NC}"
        $TMP_DIR/get_helm.sh
        
        # Clean up
        rm -rf $TMP_DIR
        
        # Verify installation
        if ! command -v helm &> /dev/null; then
            echo -e "${RED}Failed to install Helm. Please install it manually:${NC}"
            echo -e "${YELLOW}https://helm.sh/docs/intro/install/${NC}"
            exit 1
        else
            echo -e "${GREEN}Helm installed successfully!${NC}"
        fi
    else
        echo -e "${GREEN}Helm is already installed!${NC}"
    fi
}

# Build Docker images inside Minikube
build_images() {
    echo -e "${BLUE}Building Docker images inside Minikube...${NC}"
    eval $(minikube docker-env)
    
    echo -e "${BLUE}Building backend image...${NC}"
    docker build -t chat-app-backend:latest ./backend
    
    echo -e "${BLUE}Building frontend-a image...${NC}"
    docker build -t chat-app-frontend-a:latest ./frontend
    
    echo -e "${BLUE}Building frontend-b image...${NC}"
    docker build -t chat-app-frontend-b:latest ./frontend

    # Build proxy images
    echo -e "${BLUE}Building proxy-a image...${NC}"
    docker build -t chat-app-proxy-a:latest ./proxy
    
    echo -e "${BLUE}Building proxy-b image...${NC}"
    docker build -t chat-app-proxy-b:latest ./proxy
    
    echo -e "${GREEN}All images built successfully!${NC}"
}

# Deploy using Kubernetes manifests
deploy_k8s() {
    echo -e "${BLUE}Deploying application using Kubernetes manifests...${NC}"
    kubectl apply -f manifests/
    
    echo -e "${BLUE}Waiting for all pods to be ready...${NC}"
    kubectl wait --for=condition=ready pods --all --timeout=300s
    
    echo -e "${GREEN}Application deployed successfully!${NC}"
}

# Deploy using Helm chart
deploy_helm() {
    echo -e "${BLUE}Deploying application using Helm chart...${NC}"
    check_helm
    
    helm upgrade --install chat-app ./helm-chart
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}Failed to deploy with Helm. Check the error messages above.${NC}"
        exit 1
    fi
    
    echo -e "${BLUE}Waiting for all pods to be ready...${NC}"
    if ! kubectl wait --for=condition=ready pods --all --timeout=300s 2>/dev/null; then
        echo -e "${YELLOW}Not all pods are ready. Continuing anyway, but there might be issues.${NC}"
    else
        echo -e "${GREEN}All pods are ready.${NC}"
    fi
    
    echo -e "${GREEN}Application deployed with Helm!${NC}"
}

# Create port-forwarding scripts
create_port_forward_scripts() {
    local deployment_type=$1
    local service_prefix=""
    
    # Set service prefix based on deployment type
    if [ "$deployment_type" == "helm" ]; then
        service_prefix="chat-app-"
    fi
    
    # Create port forwarding script for User A
    cat > port_forward_a.sh << EOF
#!/bin/bash
# Kill existing processes using port 3000
lsof -ti:3000 | xargs kill -9 2>/dev/null || true
# Start port forwarding
kubectl port-forward service/${service_prefix}proxy-a-service 3000:3000
EOF
    chmod +x port_forward_a.sh
    
    # Create port forwarding script for User B
    cat > port_forward_b.sh << EOF
#!/bin/bash
# Kill existing processes using port 3001
lsof -ti:3001 | xargs kill -9 2>/dev/null || true
# Start port forwarding
kubectl port-forward service/${service_prefix}proxy-b-service 3001:3000
EOF
    chmod +x port_forward_b.sh
    
    echo -e "${GREEN}Port forwarding scripts created:${NC}"
    echo -e "  - ./port_forward_a.sh for User A on port 3000"
    echo -e "  - ./port_forward_b.sh for User B on port 3001"
}

# Set up port forwarding
setup_port_forwarding() {
    local auto_open=$1
    local deployment_type=$2
    
    # Clean up any existing port forwarding
    echo -e "${BLUE}Setting up port forwarding...${NC}"
    pkill -f "kubectl port-forward" || true
    
    # Create port forwarding scripts
    create_port_forward_scripts $deployment_type
    
    # Start port forwarding in background
    echo -e "${BLUE}Starting port forwarding for User A (port 3000)...${NC}"
    ./port_forward_a.sh > /dev/null 2>&1 &
    PID_A=$!
    
    # Wait a moment to ensure the first port-forward is established
    sleep 3
    
    echo -e "${BLUE}Starting port forwarding for User B (port 3001)...${NC}"
    ./port_forward_b.sh > /dev/null 2>&1 &
    PID_B=$!
    
    # Wait for port forwarding to be fully established
    sleep 5
    
    # Check if port forwarding is running
    if ! ps -p $PID_A > /dev/null; then
        echo -e "${RED}Port forwarding for User A failed.${NC}"
        echo -e "${YELLOW}Try running ./port_forward_a.sh manually to see the error.${NC}"
        PID_A=""
    else
        echo -e "${GREEN}Port forwarding for User A is running (PID: $PID_A).${NC}"
    fi
    
    if ! ps -p $PID_B > /dev/null; then
        echo -e "${RED}Port forwarding for User B failed.${NC}"
        echo -e "${YELLOW}Try running ./port_forward_b.sh manually to see the error.${NC}"
        PID_B=""
    else
        echo -e "${GREEN}Port forwarding for User B is running (PID: $PID_B).${NC}"
    fi
    
    # Show access information
    echo -e "\n${GREEN}Access URLs:${NC}"
    echo -e "User A: http://localhost:3000"
    echo -e "User B: http://localhost:3001"
    
    # Open in browser if requested
    if [ "$auto_open" = true ] && [ -n "$PID_A" ] && [ -n "$PID_B" ]; then
        echo -e "${BLUE}Opening chat interfaces in browser...${NC}"
        
        # Wait a moment to ensure services are ready
        sleep 2
        
        # Open browsers based on platform
        if command -v xdg-open >/dev/null 2>&1; then
            # Linux
            xdg-open http://localhost:3000 >/dev/null 2>&1 &
            sleep 1
            xdg-open http://localhost:3001 >/dev/null 2>&1 &
        elif command -v open >/dev/null 2>&1; then
            # macOS
            open http://localhost:3000
            sleep 1
            open http://localhost:3001
        elif command -v start >/dev/null 2>&1; then
            # Windows
            start http://localhost:3000
            sleep 1
            start http://localhost:3001
        else
            echo -e "${YELLOW}Could not automatically open browser.${NC}"
            echo -e "${YELLOW}Please manually open:${NC}"
            echo -e "  - http://localhost:3000"
            echo -e "  - http://localhost:3001"
        fi
    fi
    
    echo -e "\n${YELLOW}Press enter to stop port forwarding and return to the command line...${NC}"
    read -r
    
    # Clean up port forwarding
    echo -e "${BLUE}Stopping port forwarding...${NC}"
    [ -n "$PID_A" ] && kill $PID_A 2>/dev/null || true
    [ -n "$PID_B" ] && kill $PID_B 2>/dev/null || true
    pkill -f "kubectl port-forward" || true
    
    echo -e "${GREEN}Port forwarding stopped.${NC}"
}

# Display access information
show_access_info() {
    local auto_open=$1
    local deployment_type=$2
    
    echo -e "${GREEN}============================================${NC}"
    echo -e "${GREEN}      Chat Application Access Information    ${NC}"
    echo -e "${GREEN}============================================${NC}"
    
    # Show service and pod information
    echo -e "\n${BLUE}Displaying all services:${NC}"
    kubectl get services
    
    echo -e "\n${BLUE}Displaying all pods:${NC}"
    kubectl get pods
    
    # Set up port forwarding
    setup_port_forwarding $auto_open $deployment_type
}

# Main execution
main() {
    # Check if auto-open flag is set
    local auto_open=false
    if [[ "$*" == *"--auto-open"* ]]; then
        auto_open=true
        # Remove --auto-open from args for further processing
        set -- "${@//--auto-open/}"
    fi
    
    case "$1" in
        build)
            check_minikube
            build_images
            ;;
        deploy)
            check_minikube
            if [ "$2" == "helm" ]; then
                deploy_helm
                show_access_info $auto_open "helm"
            else
                deploy_k8s
                show_access_info $auto_open "k8s"
            fi
            ;;
        all)
            check_minikube
            build_images
            if [ "$2" == "helm" ]; then
                deploy_helm
                show_access_info $auto_open "helm"
            else
                deploy_k8s
                show_access_info $auto_open "k8s"
            fi
            ;;
        run)
            check_minikube
            show_access_info true "k8s"
            ;;
        clean)
            echo -e "${BLUE}Cleaning up resources...${NC}"
            # Kill any port forwarding processes
            pkill -f "kubectl port-forward" || true
            # Remove port forwarding scripts
            rm -f port_forward_*.sh
            # Delete the resources
            kubectl delete -f manifests/ || true
            echo -e "${GREEN}Cleanup completed!${NC}"
            ;;
        *)
            echo -e "${BLUE}Chat Application Deployment Helper${NC}"
            echo -e "Usage: $0 [command] [options]"
            echo -e "\nCommands:"
            echo -e "  build              Build Docker images"
            echo -e "  deploy [helm]      Deploy using Kubernetes manifests (or Helm if specified)"
            echo -e "  all [helm]         Build images and deploy (with Helm if specified)"
            echo -e "  run                Open frontend services in browser"
            echo -e "  clean              Delete resources"
            echo -e "\nOptions:"
            echo -e "  --auto-open        Automatically open frontend services in browser"
            ;;
    esac
}

main "$@"