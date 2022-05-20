# Config Connector

## Setup

```sh
 gcloud container clusters update admin-cluster \
    --update-addons ConfigConnector=ENABLED
```

```sh
gcloud iam service-accounts create configconnector
gcloud projects add-iam-policy-binding jetstack-paul \
    --member="serviceAccount:configconnector@jetstack-paul.iam.gserviceaccount.com" \
    --role="roles/editor"
gcloud iam service-accounts add-iam-policy-binding \
    configconnector@jetstack-paul.iam.gserviceaccount.com \
    --member="serviceAccount:jetstack-paul.svc.id.goog[cnrm-system/cnrm-controller-manager]" \
    --role="roles/iam.workloadIdentityUser"
kubectl apply -f configconnector.yaml
kubectl annotate namespace configconnector cnrm.cloud.google.com/project-id=jetstack-paul
```

## Deployment

```sh
kubectl apply -f configconnector.yaml
kubectl apply -f gkehubfeature.yaml -f gkehubfeaturemembership.yaml -f gkehubmembership.yaml
```

```sh
kubectl get gkehubfeature
kubectl get gkehubmembership
kubectl get gkehubfeaturemembership
```

<https://cloud.google.com/config-connector/docs/reference/resource-docs/gkehub/gkehubfeaturemembership>
<https://cloud.google.com/config-connector/docs/how-to/install-upgrade-uninstall>
