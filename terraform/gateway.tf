resource "aws_api_gateway_rest_api" "gateway" {
  name        = "klaus-strava-ai"
  description = "Klaus Strava AI API"
}

resource "aws_api_gateway_resource" "proxy" {
  rest_api_id = aws_api_gateway_rest_api.gateway.id
  parent_id   = aws_api_gateway_rest_api.gateway.root_resource_id
  path_part   = "{proxy+}"
}

resource "aws_api_gateway_method" "proxy" {
  rest_api_id   = aws_api_gateway_rest_api.gateway.id
  resource_id   = aws_api_gateway_resource.proxy.id
  http_method   = "ANY"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "lambda" {
  rest_api_id = aws_api_gateway_rest_api.gateway.id
  resource_id = aws_api_gateway_method.proxy.resource_id
  http_method = aws_api_gateway_method.proxy.http_method

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.lambda-function.invoke_arn
}

resource "aws_api_gateway_deployment" "klaus-strava-ai" {
  depends_on = [
    aws_api_gateway_integration.lambda,
  ]

  rest_api_id = aws_api_gateway_rest_api.gateway.id
}

resource "aws_api_gateway_stage" "crud_stage" {
  deployment_id = aws_api_gateway_deployment.klaus-strava-ai.id
  rest_api_id   = aws_api_gateway_rest_api.gateway.id
  stage_name    = "prod"
}

resource "aws_lambda_permission" "apigw" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda-function.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_api_gateway_rest_api.gateway.execution_arn}/*/*"
}

# Output the API Gateway URL
output "api_url" {
  value = "${aws_api_gateway_stage.crud_stage.invoke_url}/strava/webhook"
}
