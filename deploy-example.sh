export API_NAME="ai-audio-bot-rest-api"
export AWS_DEFAULT_REGION=$(aws configure get region)
export ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
export BEDROCK_MODEL_ID="anthropic.claude-3-sonnet-20240229-v1:0"
export BEDROCK_INFERENCE_MODEL_ID="us.anthropic.claude-3-sonnet-20240229-v1:0"

if ! aws s3 ls s3://$API_NAME-$AWS_DEFAULT_REGION-$ACCOUNT_ID; then
    aws s3 mb s3://$API_NAME-$AWS_DEFAULT_REGION-$ACCOUNT_ID
    aws s3api put-bucket-tagging --bucket $API_NAME-$AWS_DEFAULT_REGION-$ACCOUNT_ID --tagging 'TagSet=[{Key=workload,Value=ai-audio-bot-rest-api}]'
    aws s3api put-bucket-versioning --bucket $API_NAME-$AWS_DEFAULT_REGION-$ACCOUNT_ID --versioning-configuration Status=Enabled
fi

sls deploy \
    --stage=v1 \
    --param="API_NAME=$API_NAME" \
    --param="BEDROCK_MODEL_ID=$BEDROCK_MODEL_ID" \
    --param="BEDROCK_INFERENCE_MODEL_ID=$BEDROCK_INFERENCE_MODEL_ID"

rm -rf src/layers