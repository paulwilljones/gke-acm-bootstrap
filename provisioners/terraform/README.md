# Terraform

```
resource "google_container_cluster" "cluster" {
  name               = "my-cluster"
  location           = "us-central1-a"
  initial_node_count = 1
  provider = google-beta
}

resource "google_gke_hub_membership" "membership" {
  membership_id = "my-membership"
  endpoint {
    gke_cluster {
      resource_link = "//container.googleapis.com/${google_container_cluster.cluster.id}"
    }
  }
  provider = google-beta
}

resource "google_gke_hub_feature_membership" "feature_member" {
  location = "global"
  feature = google_gke_hub_feature.feature.name
  membership = google_gke_hub_membership.membership.membership_id
  configmanagement {
    version = "1.6.2"
    config_sync {
      git {
        sync_repo = "https://github.com/hashicorp/terraform"
      }
    }
  }
  provider = google-beta
}
```

[https://registry.terraform.io/providers/hashicorp/google-beta/latest/docs/resources/gke_hub_feature_membership]
