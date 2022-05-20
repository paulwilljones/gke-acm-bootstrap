#!/usr/bin/env bash

aws eks describe-cluster --name gke-acm-bootstrap --region eu-west2 --query "cluster.identity.oidc.issuer" --output text
gcloud container hub memberships register gke-acm-bootstrap \
    --context=KUBECONFIG_CONTEXT \
    --kubeconfig=KUBECONFIG_PATH \
    --enable-workload-identity \
    --public-issuer-url=OIDC_URL
gcloud beta container hub config-management apply --membership=gke-acm-bootstrap --config=apply-spec.yaml
