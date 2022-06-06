# gke-acm-bootstrap

## TL;DR

This is a pattern to bootstrap GKE clusters to with components and configuration using GKE Hub and Config Sync as part of cluster provisioning.

## Abstract

Once GKE clusters are created by our provisioner of choice, subsequent post-install steps or bootstrapping processes are required to orchestrate the deployment of cluster configuration, addons and applications.

These bootstrapping steps occur after a cluster has been provisioned, requiring some entity to access to the API Server to deploy these components (ie. via `kubectl`, Helm).

Consequently, this 'push' operation to the newly provisioned cluster often is how the initial components are deployed, before any level of hardening, configuration or security controls have been initialised.

What this pattern encourages is for cluster initialisation to be part of the provisioning process using components that are first-class citizens in GCP and GKE, thus are configured via GCP APIs not the Kubernetes API Server.

## Design

![gke-acm-bootstrap](./assets/gke-acm-bootstrap.png)

## [Provisioners](./provisioners/)

- [gcloud](./provisioners/gcloud/)
- [terraform](./provisioners/terraform/)
- [config-connector](./provisioners/config-connector/)
- [pulumi](./provisioners/pulumi/)

## Multi-cloud

### Anthos Attached Clusters

## References

<https://cloud.google.com/anthos-config-management/docs/how-to/installing-config-sync>

<https://cloud.google.com/anthos-config-management/docs/concepts/configs>

<https://cloud.google.com/blog/topics/developers-practitioners/running-anthos-inside-google>

<https://github.com/GoogleCloudPlatform/anthos-config-management-samples>

## Issues

### external-dns

- bitnami/external-dns fails to render
    - chart contains namespaced `ClusterRole` and `ClusterRoleBinding` which fails `nomos`
        - can be disabled by setting `rbac.clusterRole: false`
    - `hydration-controller` fails to pull bitnami/external-dns:0.6.3 chart
        - `kubectl logs -n config-management-system root-reconciler -c hydration-controller`
            ```sh
            E0520 20:35:15.205562       1 controller.go:244] rendering error for commit 4a51456092638039a8ebeb07b99147bd6ddf43d2: failed to run kustomize build in /repo/source/4a51456092638039a8ebeb07b99147bd6ddf43d2/config-root/base, stdout: : Error: : unable to run: 'helm pull --untar --untardir /repo/source/4a51456092638039a8ebeb07b99147bd6ddf43d2/config-root/base/charts --repo https://charts.bitnami.com/bitnami external-dns --version 6.3.0' with env=[HELM_CONFIG_HOME=/tmp/kustomize-helm-575312248/helm HELM_CACHE_HOME=/tmp/kustomize-helm-575312248/helm/.cache HELM_DATA_HOME=/tmp/kustomize-helm-575312248/helm/.data] (is 'helm' installed?)
            ```
    - running `helm pull --repo https://charts.bitnami.com/bitnami external-dns --version 6.3.0` manually in the `hydration-controller` container returns `Killed`
    - bitnami/nginx-ingress-controller also fails
        - `kubectl logs -n config-management-system root-reconciler -c hydration-controller`
            ```sh
            E0521 18:06:21.265805       1 controller.go:244] rendering error for commit a8e4e0e9ce8cc0fd2aa3c1545d9b24412f2b0bdd: failed to run kustomize build in /repo/source/a8e4e0e9ce8cc0fd2aa3c1545d9b24412f2b0bdd/config-root/base, stdout: : Error: : unable to run: 'helm pull --untar --untardir /repo/source/a8e4e0e9ce8cc0fd2aa3c1545d9b24412f2b0bdd/config-root/base/charts --repo https://charts.bitnami.com/bitnami nginx-ingress-controller --version 9.2.1' with env=[HELM_CONFIG_HOME=/tmp/kustomize-helm-783478784/helm HELM_CACHE_HOME=/tmp/kustomize-helm-783478784/helm/.cache HELM_DATA_HOME=/tmp/kustomize-helm-783478784/helm/.data] (is 'helm' installed?)
            ```
- kubernetes-sigs/external-dns:1.9.0 only gets applied to `default` namespace
    - setting `helmCharts.namespace` only getting applied to `.Release.Namespace`
    - kubernetes-sigs/external-dns resources don't include a `metadata.namespace` field in the templates
    - therefore the hydrated manifests don't get namespaced and get applied to `default` namespace

### `depends_on`

- `depends_on` annotation fails when referencing Policy Controller resources
    - `config.kubernetes.io/depends-on: admissionregistration.k8s.io/ValidatingWebhookConfiguration/gatekeeper-validating-webhook-configuration`
        - `kubectl logs -n config-management-system root-reconciler -c reconciler`
        ```sh
        [2] KNV2009: invalid object: "_cert-manager__Namespace": invalid "config.kubernetes.io/depends-on" annotation: external dependency: /Namespace/cert-manager -> admissionregistration.k8s.io/ValidatingWebhookConfiguration/gatekeeper-validating-webhook-configuration  For more information, see https://g.co/cloud/acm-errors#knv2009        
        ```
    - `config.kubernetes.io/depends-on: apps/namespaces/gatekeeper-system/Deployment/gatekeeper-controller-manager`
        - `kubectl logs -n config-management-system root-reconciler -c reconciler`
        ```sh
        [2] KNV2009: invalid object: "_cert-manager__Namespace": invalid "config.kubernetes.io/depends-on" annotation: external dependency: /Namespace/cert-manager -> apps/namespaces/gatekeeper-system/Deployment/gatekeeper-controller-manager  For more information, see https://g.co/cloud/acm-errors#knv2009
        ```
