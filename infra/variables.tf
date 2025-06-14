variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "ap-northeast-2"
}

variable "environment" {
  description = "환경 (dev, prod 등)"
  type        = string
  default     = "dev"
}

variable "project_name" {
  description = "프로젝트 이름"
  type        = string
  default     = "recommendation-system"
} 