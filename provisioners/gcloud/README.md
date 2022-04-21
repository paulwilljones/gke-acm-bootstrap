# `gcloud`

```sh
gcloud container hub memberships register gke-bootstrap --gke-cluster=europe-west2/config-sync --enable-workload-identity
gcloud beta container hub config-management enable
gcloud beta container hub config-management apply --membership=gke-bootstrap --config=apply-spec.yaml
```

[https://cloud.google.com/sdk/gcloud/reference/beta/container/hub/config-management/enable]
[https://cloud.google.com/sdk/gcloud/reference/beta/container/hub/config-management/apply]
