# GKE initialisation pattern

## Abstract

GKE clusters created by `gcloud` or Terraform require subsequent post-install steps or bootstrapping processes in order to then orchestrate the deployment of cluster configuration and applications.

These bootstrapping steps occur after a clusters has been provisioned, requiring access to the API Server to deploy components (ie. GitOps tools, operators).
Consequently, this 'push' operation to the newly provisioned cluster often is how the initial components are deployed, before any level of hardening, configuration or security controls have been initialised.

What is required is a pattern for initialising clusters as part of the provisioning process using components that are first-class citizens in GKE, thus configured via GCP APIs not the API Server.

## Motivations



## TL;DR

This is a pattern to bootstrap GKE configuration during cluster provisioning using GKE Hub and Config Sync.

## [Provisioners](./provisioners/)

- [gcloud](./provisioners/gcloud/)
- [terraform](./provisioners/terraform/)
- [config-connector](./provisioners/config-connector/)
- [pulumi](./provisioners/pulumi/)


## References

[https://cloud.google.com/anthos-config-management/docs/how-to/installing-config-sync]
[https://cloud.google.com/anthos-config-management/docs/concepts/configs]
[https://cloud.google.com/blog/topics/developers-practitioners/running-anthos-inside-google]
[https://github.com/GoogleCloudPlatform/anthos-config-management-samples]
