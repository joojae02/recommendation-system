output "dataset_group_arn" {
  description = "The ARN of the Personalize Dataset Group"
  value       = awscc_personalize_dataset_group.recommendation_group.dataset_group_arn
}

output "dataset_group_name" {
  description = "The name of the Personalize Dataset Group"
  value       = awscc_personalize_dataset_group.recommendation_group.name
}

output "users_dataset_name" {
  description = "The name of the Users Dataset"
  value       = awscc_personalize_dataset.users.name
}

output "items_dataset_name" {
  description = "The name of the Items Dataset"
  value       = awscc_personalize_dataset.items.name
}

output "interactions_dataset_name" {
  description = "The name of the Interactions Dataset"
  value       = awscc_personalize_dataset.interactions.name
}

output "role_arn" {
  description = "The ARN of the IAM role for Personalize"
  value       = aws_iam_role.personalize_role.arn
}

output "bucket_name" {
  description = "The name of the S3 bucket for data"
  value       = aws_s3_bucket.data_bucket.id
} 