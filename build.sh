#!/bin/sh
set -x

export _ARTIFACT_REGISTRY="us-east4-docker.pkg.dev"
export _ARTIFACT_REGISTRY_REPO="quickstart-docker-repo"
#export _BUCKET_NAME="lcef-ui-code/testlogs"
export _VERSION="1"
export _REGIONSVC="us-east4"
export _SVC_IMAGE="greet-img"
export _SVC_NAME="greet-svc"
export _DB_INSTANCE_NAME="greetingsql"
export _DB_IAM_USER="sa-lcef-idp"
export _DB_DATABASE="greeting-db"
export _SERVERLESS_VPC_CONNECTOR="cymbalconnector"
export _SA_NAME="sa-lcef-idp"

gcloud builds submit --config ./cloudbuild.yaml \
        --substitutions _VERSION=${_VERSION},_ARTIFACT_REGISTRY=${_ARTIFACT_REGISTRY},_ARTIFACT_REGISTRY_REPO=${_ARTIFACT_REGISTRY_REPO},_REGIONSVC=${_REGIONSVC},_DB_INSTANCE_NAME=${_DB_INSTANCE_NAME},_DB_IAM_USER=${_DB_IAM_USER},_DB_DATABASE=${_DB_DATABASE},_SERVERLESS_VPC_CONNECTOR=${_SERVERLESS_VPC_CONNECTOR},_SA_NAME=${_SA_NAME},_SVC_IMAGE=${_SVC_IMAGE},_SVC_NAME=${_SVC_NAME}

