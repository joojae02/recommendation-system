#!/bin/bash

# 스크립트의 절대 경로 설정
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
INFRA_DIR="$(dirname "$SCRIPT_DIR")"

echo "SCRIPT_DIR: $SCRIPT_DIR"
echo "INFRA_DIR: $INFRA_DIR"

cd "$INFRA_DIR"

# Terraform outputs 가져오기
DATASET_GROUP_NAME=$(terraform output -raw dataset_group_name)
USERS_DATASET_NAME=$(terraform output -raw users_dataset_name)
ITEMS_DATASET_NAME=$(terraform output -raw items_dataset_name)
INTERACTIONS_DATASET_NAME=$(terraform output -raw interactions_dataset_name)
ROLE_ARN=$(terraform output -raw role_arn)
BUCKET_NAME=$(terraform output -raw bucket_name)
PROFILE=terraform

echo "DATASET_GROUP_NAME: $DATASET_GROUP_NAME"
echo "USERS_DATASET_NAME: $USERS_DATASET_NAME"
echo "ITEMS_DATASET_NAME: $ITEMS_DATASET_NAME"
echo "INTERACTIONS_DATASET_NAME: $INTERACTIONS_DATASET_NAME"
echo "ROLE_ARN: $ROLE_ARN"
echo "BUCKET_NAME: $BUCKET_NAME"

# Dataset Group ARN 가져오기
DATASET_GROUP_ARN=$(aws personalize list-dataset-groups --profile $PROFILE --no-cli-pager --query "datasetGroups[?name=='$DATASET_GROUP_NAME'].datasetGroupArn" --output text)

if [ -z "$DATASET_GROUP_ARN" ]; then
    echo "Dataset group not found: $DATASET_GROUP_NAME"
    exit 1
fi

# Dataset ARN 가져오기
USERS_DATASET_ARN=$(aws personalize list-datasets --profile $PROFILE --no-cli-pager --dataset-group-arn $DATASET_GROUP_ARN --query "datasets[?name=='$USERS_DATASET_NAME'].datasetArn" --output text)
ITEMS_DATASET_ARN=$(aws personalize list-datasets --profile $PROFILE --no-cli-pager --dataset-group-arn $DATASET_GROUP_ARN --query "datasets[?name=='$ITEMS_DATASET_NAME'].datasetArn" --output text)
INTERACTIONS_DATASET_ARN=$(aws personalize list-datasets --profile $PROFILE --no-cli-pager --dataset-group-arn $DATASET_GROUP_ARN --query "datasets[?name=='$INTERACTIONS_DATASET_NAME'].datasetArn" --output text)

if [ -z "$USERS_DATASET_ARN" ]; then
    echo "Users dataset not found: $USERS_DATASET_NAME"
    exit 1
fi

if [ -z "$ITEMS_DATASET_ARN" ]; then
    echo "Items dataset not found: $ITEMS_DATASET_NAME"
    exit 1
fi

if [ -z "$INTERACTIONS_DATASET_ARN" ]; then
    echo "Interactions dataset not found: $INTERACTIONS_DATASET_NAME"
    exit 1
fi

# Import job 생성
echo "Creating import jobs..."

# Users import job
aws personalize create-dataset-import-job \
    --profile $PROFILE \
    --no-cli-pager \
    --job-name "recommendation-system-users-dataset-import-dev" \
    --dataset-arn $USERS_DATASET_ARN \
    --data-source "dataLocation=s3://$BUCKET_NAME/users/users.csv" \
    --role-arn $ROLE_ARN

# Items import job
aws personalize create-dataset-import-job \
    --profile $PROFILE \
    --no-cli-pager \
    --job-name "recommendation-system-items-dataset-import-dev" \
    --dataset-arn $ITEMS_DATASET_ARN \
    --data-source "dataLocation=s3://$BUCKET_NAME/items/items.csv" \
    --role-arn $ROLE_ARN

# Interactions import job
aws personalize create-dataset-import-job \
    --profile $PROFILE \
    --no-cli-pager \
    --job-name "recommendation-system-interactions-dataset-import-dev" \
    --dataset-arn $INTERACTIONS_DATASET_ARN \
    --data-source "dataLocation=s3://$BUCKET_NAME/interactions/interactions.csv" \
    --role-arn $ROLE_ARN

echo "Import jobs created. Check AWS Console for status." 