resource "aws_s3_bucket" "data_bucket" {
  bucket = "wnwogus-${var.project_name}-data-${var.environment}"
}

resource "aws_s3_bucket_versioning" "data_bucket_versioning" {
  bucket = aws_s3_bucket.data_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_object" "users_folder" {
  bucket = aws_s3_bucket.data_bucket.id
  key    = "users/"
  content_type = "application/x-directory"
}

resource "aws_s3_object" "items_folder" {
  bucket = aws_s3_bucket.data_bucket.id
  key    = "items/"
  content_type = "application/x-directory"
}

resource "aws_s3_object" "interactions_folder" {
  bucket = aws_s3_bucket.data_bucket.id
  key    = "interactions/"
  content_type = "application/x-directory"
}

resource "aws_s3_object" "users_data" {
  bucket = aws_s3_bucket.data_bucket.id
  key    = "users/users.csv"
  source = "${path.module}/data/users.csv"
  content_type = "text/csv"
  depends_on = [aws_s3_object.users_folder]
}

resource "aws_s3_object" "items_data" {
  bucket = aws_s3_bucket.data_bucket.id
  key    = "items/items.csv"
  source = "${path.module}/data/items.csv"
  content_type = "text/csv"
  depends_on = [aws_s3_object.items_folder]
}

resource "aws_s3_object" "interactions_data" {
  bucket = aws_s3_bucket.data_bucket.id
  key    = "interactions/interactions.csv"
  source = "${path.module}/data/interactions.csv"
  content_type = "text/csv"
  depends_on = [aws_s3_object.interactions_folder]
}

resource "aws_s3_bucket_policy" "data_bucket_policy" {
  bucket = aws_s3_bucket.data_bucket.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AllowPersonalizeAccess"
        Effect = "Allow"
        Principal = {
          Service = "personalize.amazonaws.com"
        }
        Action = [
          "s3:GetObject",
          "s3:ListBucket"
        ]
        Resource = [
          aws_s3_bucket.data_bucket.arn,
          "${aws_s3_bucket.data_bucket.arn}/*"
        ]
      }
    ]
  })
} 