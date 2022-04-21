import pulumi
import pulumi_gcp as gcp

cluster = gcp.container.Cluster("cluster",
    location="us-central1-a",
    initial_node_count=1,
    opts=pulumi.ResourceOptions(provider=google_beta))

membership = gcp.gkehub.Membership("membership",
    membership_id="my-membership",
    endpoint=gcp.gkehub.MembershipEndpointArgs(
        gke_cluster=gcp.gkehub.MembershipEndpointGkeClusterArgs(
            resource_link=cluster.id.apply(lambda id: f"//container.googleapis.com/{id}"),
        ),
    ),
    opts=pulumi.ResourceOptions(provider=google_beta))

feature = gcp.gkehub.Feature("feature",
    location="global",
    labels={
        "foo": "bar",
    },
    opts=pulumi.ResourceOptions(provider=google_beta))

feature_member = gcp.gkehub.FeatureMembership("featureMember",
    location="global",
    feature=feature.name,
    membership=membership.membership_id,
    configmanagement=gcp.gkehub.FeatureMembershipConfigmanagementArgs(
        version="1.6.2",
        config_sync=gcp.gkehub.FeatureMembershipConfigmanagementConfigSyncArgs(
            git=gcp.gkehub.FeatureMembershipConfigmanagementConfigSyncGitArgs(
                sync_repo="https://github.com/hashicorp/terraform",
            ),
        ),
    ),
    opts=pulumi.ResourceOptions(provider=google_beta))
