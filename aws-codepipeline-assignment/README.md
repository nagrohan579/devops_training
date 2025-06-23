# AWS CodePipeline Assignment

In this assignment, I used the same application from my Jenkins and GitHub Actions assignments, but this time I set it up with AWS CodePipeline. Here’s how I did it, step by step, with screenshots from my journey.

---

## Setting up ECR

First, I went to the AWS console and searched for ECR.

![Searching for ECR](images/aws_searched_ecr.png)

The ECR page opened up.

![ECR Page](images/aws_ecr_page.png)

I clicked the create button to make a new repository. I named it `guess-number-app` and didn’t set any namespace.

![Creating ECR Repository](images/aws_creating_ecr_repository.png)

Repository created!

![ECR Repository Created](images/aws_ecr_repository_created.png)

---

## Setting up CodePipeline

Next, I searched for CodePipeline.

![Searching for CodePipeline](images/aws_searched_codepipeline.png)

The CodePipeline page opened.

![CodePipeline Page](images/aws_codepipeline_page.png)

I clicked on the create pipeline button. First, I was asked to choose a creation option. There were four options:
- Deployment
- Continuous Integration
- Automation
- Build custom pipeline

I chose **Build custom pipeline**.

![Choosing Build Custom Pipeline](images/aws_choose_build_custom_pipeline_option.png)

Next, I set the pipeline settings:
- Pipeline name: `GuessNumberAppPipeline`
- Execution mode: Queued
- Service role: Create new service role
- Role name: `AWSCodePipelineServiceRole-us-east-1-GuessNumberAppPipeline`
- Permission: Allowed AWS CodePipeline to create the service role

![Pipeline Settings](images/aws_choose_pipeline_settings.png)

---

## Adding Source Stage

In the next step, I needed to add my GitHub repository as the source.

![Connecting to GitHub](images/aws_connecting_to_github.png)

![GitHub Authorize](images/aws_connector_github_authorize.png)

![GitHub Install and Authorize](images/aws_connector_install_and_authorize.png)

All done with the source stage configuration!

![Source Stage Added](images/aws_added_source_stage.png)

---

## Adding Build Stage

Next, I added a build stage:
- Build provider: AWS CodeBuild (from "Other build providers")
- Project name: Not yet selected/created
- Buildspec override: Enabled
- Buildspec override type: Use a buildspec file
- Buildspec name: `buildspec.yml`
- Build type: Single build
- Region: United States (N. Virginia)
- Input artifacts: SourceArtifact
- Automatic retry: Enabled

I needed a CodeBuild project, so I created one.

![CodeBuild Project Created](images/aws_created_codebuild_project.png)

### My buildspec.yml file

Here is the `buildspec.yml` file I used for the build stage:

```yaml
version: 0.2

phases:
  pre_build:
    commands:
      - echo Logging in to Amazon ECR...
      - aws --version
      - aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin 677276117957.dkr.ecr.us-east-1.amazonaws.com
      - REPOSITORY_URI=677276117957.dkr.ecr.us-east-1.amazonaws.com/guess-number-app
      - COMMIT_HASH=$(echo $CODEBUILD_RESOLVED_SOURCE_VERSION | cut -c 1-7)
      - IMAGE_TAG=${COMMIT_HASH:=latest}
  build:
    commands:
      - echo "Starting build of maven project"
      - mvn -B package --file pom.xml
      - echo "Build completed successfully"
      - echo Build started on `date`
      - echo Building the Docker image...
      - docker build -t $REPOSITORY_URI:latest .
      - docker tag $REPOSITORY_URI:latest $REPOSITORY_URI:$IMAGE_TAG
  post_build:
    commands:
      - echo Build completed on `date`
      - echo Pushing the Docker images...
      - docker push $REPOSITORY_URI:latest
      - docker push $REPOSITORY_URI:$IMAGE_TAG
      - echo Writing image definitions file...
      - printf '[{"name":"guess-number-app","imageUri":"%s"}]' $REPOSITORY_URI:$IMAGE_TAG > imagedefinitions.json
artifacts:
  files: imagedefinitions.json
```

#### Explanation of the buildspec.yml

- **version: 0.2**: This specifies the buildspec version.
- **phases**: The build process is divided into three phases:
  - **pre_build**: 
    - Logs in to Amazon ECR using the AWS CLI.
    - Sets environment variables for the repository URI and image tag (using the commit hash or 'latest').
  - **build**: 
    - Builds the Maven project (`mvn -B package --file pom.xml`).
    - Builds the Docker image and tags it with both `latest` and the commit hash.
  - **post_build**: 
    - Pushes both tags of the Docker image to ECR.
    - Writes an `imagedefinitions.json` file, which is used by ECS for deployment.
- **artifacts**: 
  - Specifies that `imagedefinitions.json` should be included as a build artifact for the deploy stage.

---

## Skipping Test and Deploy Stages (for now)

I skipped the test and deploy stages for now.

After running the pipeline, I saw that the source stage worked, but the build failed.

![Source Done, Build Failed](images/aws_codepipeline_source_done_build_fail.png)

I checked the logs and saw it had trouble authenticating with ECR.

![Build Stage Logs](images/aws_codepipeline_build_stage_logs.png)

---

## Fixing Permissions for CodeBuild

I needed to add a policy to the service role of the CodeBuild project.

![CodeBuild Service Role Page](images/aws_codebuild_service_role_page.png)

I clicked Attach policies and added the `AmazonEC2ContainerRegistryPowerUser` policy.

![Adding Policy to Service Role](images/aws_codebuild_service_role_adding_policy.png)

I went back to the pipeline and retried the build stage. This time, it worked!

![Source and Build Done](images/aws_codepipeline_source_and_build_done.png)

I checked ECR and saw the image was pushed.

![ECR Image Pushed](images/aws_ecr_image_pushed.png)

---

## Setting up ECS

Next, I searched for ECS.

![Searching for ECS](images/aws_searched_ecs.png)

The ECS page opened.

![ECS Page](images/aws_ecs_page.png)

I clicked Get Started and created a cluster named `guess-number-app-cluster`, keeping other configurations as default.

![Creating ECS Cluster](images/aws_creating_ecs_cluster.png)

Cluster created!

![ECS Cluster Created](images/aws_ecs_cluster_created.png)

---

## Creating Task Definition

Next, I created a task definition.

![Task Definition Page](images/aws_ecs_task_definition_page.png)

I clicked on create new task definition.

![Creating Task Definition](images/aws_ecs_creating_task_definition.png)

Task definition created!

![Task Definition Created](images/aws_ecs_task_definition_created.png)

---

## Creating a Service in the Cluster

Now, I created a service in the `guess-number-app-cluster`.

![Creating Service in Cluster](images/aws_ecs_creating_a_service_in_the_cluster.png)

Service created!

![Service in Cluster Created](images/aws_ecs_service_in_cluster_created.png)

---

## Adding Deploy Stage to CodePipeline

I went back to CodePipeline, edited my pipeline, and added a new deploy stage, configuring it for ECS.

![Adding Deploy Stage Details](images/aws_codepipeline_adding_deploy_stage_details.png)

The deploy stage was failing due to a permission issue. I added the `AmazonECS_FullAccess` policy to the CodePipeline service role, retried the deploy stage, and it worked! All stages were running successfully.

![Source, Build, Deploy Done](images/aws_codepipeline_source_build_deploy_done.png)

---

## Summary

I successfully set up AWS CodePipeline to build, push, and deploy my application using ECR and ECS, fixing permission issues along the way. The screenshots above show each step I took. This was a great hands-on experience with AWS CI/CD services!
