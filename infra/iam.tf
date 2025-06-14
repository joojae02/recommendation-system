resource "aws_iam_role" "personalize_role" {
  name = "${var.project_name}-personalize-role-${var.environment}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "personalize.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy" "personalize_policy" {
  name = "${var.project_name}-personalize-policy-${var.environment}"
  role = aws_iam_role.personalize_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:ListBucket"
        ]
        Resource = [
          "${aws_s3_bucket.data_bucket.arn}/*",
          aws_s3_bucket.data_bucket.arn
        ]
      }
    ]
  })
} 