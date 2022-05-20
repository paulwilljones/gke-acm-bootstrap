# `gcloud`

```sh
gcloud container fleet memberships register gke-acm-bootstrap --gke-cluster=gke-acm-bootstrap --enable-workload-identity
gcloud services enable anthos.googleapis.com
gcloud beta container hub config-management enable
gcloud beta container hub config-management apply --membership=gke-acm-bootstrap --config=apply-spec.yaml
```

## Cleanup

```sh
gcloud beta container hub config-management unmanage --membership gke-acm-bootstrap
gcloud beta container hub config-management disable
gcloud beta container hub memberships unregister gke-bootstrap --gke-cluster=europe-west2/gke-acm-bootstrap
```

```sh
gcloud container fleet memberships delete gke-acm-bootstrap
```

## Links

<https://cloud.google.com/sdk/gcloud/reference/beta/container/hub/config-management/enable>
<https://cloud.google.com/sdk/gcloud/reference/beta/container/hub/config-management/apply>
