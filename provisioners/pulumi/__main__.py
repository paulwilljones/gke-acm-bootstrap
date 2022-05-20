import pulumi
import pulumi_gcp as gcp

cluster = gcp.container.get_cluster(name="gke-acm-bootstrap",
    location="europe-west2")

membership = gcp.gkehub.Membership("membership",
    membership_id="gke-acm-bootstrap",
    endpoint=gcp.gkehub.MembershipEndpointArgs(
        gke_cluster=gcp.gkehub.MembershipEndpointGkeClusterArgs(
            resource_link=f"//container.googleapis.com/{cluster.id}",
        ),
    ),
)

feature = gcp.gkehub.Feature(name="configmanagement",
    resource_name="configmanagement",
    location="global",
)

feature_member = gcp.gkehub.FeatureMembership("featureMember",
    location="global",
    feature=feature.name,
    membership=membership.membership_id,
    configmanagement=gcp.gkehub.FeatureMembershipConfigmanagementArgs(
        config_sync=gcp.gkehub.FeatureMembershipConfigmanagementConfigSyncArgs(
            git=gcp.gkehub.FeatureMembershipConfigmanagementConfigSyncGitArgs(
                sync_repo="https://github.com/paulwilljones/gke-acm-bootstrap",
                sync_branch="develop",
                policy_dir="config-root",
                sync_wait_secs="5",
                secret_type="none"
            ),
            source_format="unstructured"
        ),
    ),
)
