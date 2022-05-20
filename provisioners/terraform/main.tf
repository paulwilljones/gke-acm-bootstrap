data "google_container_cluster" "cluster" {
  name     = "gke-acm-bootstrap"
  location = "europe-west2"
  project  = "jetstack-paul"
}

resource "google_gke_hub_membership" "membership" {
  project    = "jetstack-paul"
  membership_id = "gke-acm-bootstrap"
  endpoint {
    gke_cluster {
      resource_link = "//container.googleapis.com/${data.google_container_cluster.cluster.id}"
    }
  }
  provider = google-beta
}

resource "google_gke_hub_feature" "configmanagement_acm_feature" {
  name     = "configmanagement"
  location = "global"
  project  = "jetstack-paul"
  provider = google-beta
}

resource "google_gke_hub_feature_membership" "feature_member" {
  project    = "jetstack-paul"
  location   = "global"
  feature    = google_gke_hub_feature.feature.name
  membership = google_gke_hub_membership.membership.membership_id
  configmanagement {
    config_sync {
      git {
        sync_repo      = "https://github.com/paulwilljones/gke-acm-bootstrap"
        sync_branch    = "develop"
        secret_type    = "none"
        policy_dir     = "config-root"
        sync_wait_secs = 5
      }
      source_format = "unstructured"
    }
    policy_controller {
      enabled                    = true
      template_library_installed = true
      referential_rules_enabled  = true
      exemptable_namespaces = ["kube-system", "config-management-system", "config-management-monitoring", "resource-group-system", "asm-system", "gke-connect"]
    }
  }
  depends_on = [
    google_gke_hub_feature.configmanagement_acm_feature
  ]
  provider = google-beta
}
