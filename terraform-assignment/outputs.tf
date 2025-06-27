output "vpc_id" {
  value = aws_vpc.main.id
}

output "s3_bucket_name" {
  value = aws_s3_bucket.terraform_bucket.bucket
}

output "rds_endpoint" {
  value = aws_db_instance.mysql.endpoint
}

output "ecs_cluster_name" {
  value = aws_ecs_cluster.main.name
}

output "eks_cluster_name" {
  value = aws_eks_cluster.eks.name
}