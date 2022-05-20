# Attached Clusters

Anthos Attached Clusters enables managed Kubernetes across [AWS, Azure another other providers](https://cloud.google.com/anthos/docs/setup/attach-kubernetes-clusters#supported_kubernetes_clusters) to leverage GKE Hub features and become first-class citizens in GCP.

## Register cluster

```sh
OIDC_URL=$(aws eks describe-cluster --name gke-acm-bootstrap --region AWS_REGION --query "cluster.identity.oidc.issuer" --output text)
gcloud container hub memberships register gke-acm-bootstrap \
    --context=KUBECONFIG_CONTEXT \
    --kubeconfig=KUBECONFIG_PATH \
    --enable-workload-identity \
    --public-issuer-url=OIDC_URL
```

## Deploy Config Sync

```sh
gcloud beta container hub config-management apply --membership=gke-acm-bootstrap --config=apply-spec.yaml
```

## Cleanup

```sh
gcloud beta container hub config-management unmanage --membership gke-acm-bootstrap
gcloud beta container hub memberships unregister gke-acm-bootstrap --gke-cluster=europe-west2/gke-acm-bootstrap
```

## Links

<https://cloud.google.com/anthos/docs/setup/attach-kubernetes-clusters>
<https://cloud.google.com/anthos-config-management/docs/how-to/installing-config-sync#configuring-config-sync>
