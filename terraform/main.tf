terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region = "us-west-1"
}

resource "aws_s3_bucket" "bucket" {
  bucket = "klaus-strava-ai"
  region = "us-west-1"

  tags = {
    App         = "klaus-strava-ai"
    Environment = "Production"
  }
}

# IAM role for Lambda execution
data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "lambda-iam-role" {
  name               = "lambda_execution_role"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

# IAM policy for Lambda to access S3
data "aws_iam_policy_document" "lambda_s3_policy" {
  statement {
    effect = "Allow"
    actions = [
      "s3:GetObject"
    ]
    resources = [
      "${aws_s3_bucket.bucket.arn}/*"
    ]
  }
}

resource "aws_iam_role_policy" "lambda_s3_policy" {
  name   = "lambda_s3_access"
  role   = aws_iam_role.lambda-iam-role.id
  policy = data.aws_iam_policy_document.lambda_s3_policy.json
}

# Attach basic execution role for CloudWatch logs
resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role       = aws_iam_role.lambda-iam-role.name
}

# Package the Lambda function code
data "archive_file" "deployment" {
  type        = "zip"
  source_dir  = "${path.module}/../api"
  output_path = "${path.module}/../function.zip"
}

# Upload the Lambda deployment package to S3
resource "aws_s3_object" "lambda_zip" {
  bucket = aws_s3_bucket.bucket.id
  key    = "lambda/function.zip"
  source = data.archive_file.deployment.output_path
  etag   = filemd5(data.archive_file.deployment.output_path)

  tags = {
    App         = "klaus-strava-ai"
    Environment = "Production"
  }
}

# Lambda function
resource "aws_lambda_function" "lambda-function" {
  s3_bucket        = aws_s3_bucket.bucket.id
  s3_key           = aws_s3_object.lambda_zip.key
  function_name    = "klaus-strava-ai"
  role             = aws_iam_role.lambda-iam-role.arn
  handler          = "main.handler"
  source_code_hash = data.archive_file.deployment.output_base64sha256

  runtime = "python3.10"

  environment {
    variables = {
      ENVIRONMENT = "production"
      LOG_LEVEL   = "info"
    }
  }

  tags = {
    Environment = "production"
    Application = "klaus-strava-ai"
  }
}
