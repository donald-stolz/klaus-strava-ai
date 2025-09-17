terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

# Variable declarations
variable "strava_client_id" {
  description = "Strava API Client ID"
  type        = string
  sensitive   = true
}

variable "strava_client_secret" {
  description = "Strava API Client Secret"
  type        = string
  sensitive   = true
}

variable "strava_refresh_token" {
  description = "Strava API Refresh Token"
  type        = string
  sensitive   = true
}

variable "strava_base_url" {
  description = "Strava API Base URL"
  type        = string
  default     = "https://www.strava.com/api/v3"
}

variable "gemini_api_key" {
  description = "Gemini API Key"
  type        = string
  sensitive   = true
}

variable "gemini_model_name" {
  description = "Gemini Model Name"
  type        = string
  default     = "gemini-2.5-flash"
}

variable "environment" {
  description = "Application Environment"
  type        = string
  default     = "production"
}

variable "log_level" {
  description = "Application Log Level"
  type        = string
  default     = "info"
}


# Configure the AWS Provider
provider "aws" {
  region = "us-west-1"
  alias  = "klaus-strava-ai"
}

# AWS Application
resource "aws_servicecatalogappregistry_application" "klaus-strava-ai" {
  provider    = aws.klaus-strava-ai
  name        = "klaus-strava-ai"
  description = "Klaus Strava AI application"
}

# 
# Configure Resources
# 
# provider "aws" {
#   default_tags {
#     
#   }
# }
# AWS S3 Bucket
resource "aws_s3_bucket" "bucket" {
  bucket = "klaus-strava-ai"
  region = "us-west-1"
  tags   = aws_servicecatalogappregistry_application.klaus-strava-ai.tags
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
  tags               = aws_servicecatalogappregistry_application.klaus-strava-ai.tags
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
# data "archive_file" "deployment" {
#   type        = "zip"
#   source_dir  = "${path.module}/.."
#   excludes    = ["${path.module}/../terraform", "${path.module}/../.github", "${path.module}/../.vscode", "${path.module}/../.cursor"]
#   output_path = "${path.module}/../function.zip"
# }

# Upload the Lambda deployment package to S3
resource "aws_s3_object" "lambda_zip" {
  bucket = aws_s3_bucket.bucket.id
  key    = "lambda/function.zip"
  source = "${path.module}/../function.zip"
  etag   = filemd5("${path.module}/../function.zip")
  tags   = aws_servicecatalogappregistry_application.klaus-strava-ai.tags
}

# Lambda function
resource "aws_lambda_function" "lambda-function" {
  s3_bucket        = aws_s3_bucket.bucket.id
  s3_key           = aws_s3_object.lambda_zip.key
  function_name    = "klaus-strava-ai"
  role             = aws_iam_role.lambda-iam-role.arn
  handler          = "main.handler"
  source_code_hash = filemd5("${path.module}/../function.zip")

  runtime = "python3.12"

  environment {
    variables = {
      ENVIRONMENT          = var.environment
      LOG_LEVEL            = var.log_level
      STRAVA_CLIENT_ID     = var.strava_client_id
      STRAVA_CLIENT_SECRET = var.strava_client_secret
      STRAVA_REFRESH_TOKEN = var.strava_refresh_token
      STRAVA_BASE_URL      = var.strava_base_url
      GEMINI_API_KEY       = var.gemini_api_key
      GEMINI_MODEL_NAME    = var.gemini_model_name
    }
  }
  tags = aws_servicecatalogappregistry_application.klaus-strava-ai.tags
}
