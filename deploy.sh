#!/bin/bash

# Stop the script if any command fails
set -e

# Function to prompt user confirmation
confirm() {
    while true; do
        read -r -p "$1 [y/n]: " response
        case "$response" in
            [yY][eE][sS]|[yY])
                break
                ;;
            [nN][oO]|[nN])
                echo "Exiting..."
                exit 1
                ;;
            *)
                echo "Please enter y or n."
                ;;
        esac
    done
}

# Display current AWS configuration
echo "Current AWS Configuration:"
echo "AWS Profile: $AWS_PROFILE"
echo "AWS Default Region: $AWS_DEFAULT_REGION"
echo "AWS Region: $AWS_REGION"
echo ""

# Ask user for confirmation
confirm "Do you want to continue with this AWS configuration for deployment?"


# Get the AWS account ID
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query "Account" --output text)
echo 'Will deploy to AWS Account:' $AWS_ACCOUNT_ID

# Deploy SAM Deployment Role
echo "Deploying SAM Deployment Role CloudFormation"
aws cloudformation deploy --template-file deployment-role.yaml --stack-name sam-deployment-role --capabilities CAPABILITY_NAMED_IAM
echo ""

# SAM build
echo "Building SAM application..."
sam build
echo ""

# Deploy using the AWS SAM CLI
echo "Deploying SAM application..."
sam deploy --role-arn arn:aws:iam::$AWS_ACCOUNT_ID:role/SAMDeploymentRole
echo ""

echo "Deployment completed successfully."
