terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.100.0"
    }
    awscc = {
      source  = "hashicorp/awscc"
      version = "~> 1.45.0"
    }
  }
}

provider "aws" {
  region  = var.aws_region
  profile = "terraform"
}

provider "awscc" {
  region  = var.aws_region
  profile = "terraform"
} 