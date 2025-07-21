import pulumi
import pulumi_aws as aws
import json

# Set regions
source_region = "us-east-1"
destination_region = "us-west-2"

# Create the source bucket in the source region
source_bucket = aws.s3.Bucket(
    "source-bucket",
    bucket="pulumi-multi-region-drc-bucket-ng1",
    force_destroy=True,
    opts=pulumi.ResourceOptions(provider=aws.Provider("drc", region=source_region)),
)

# Create the destination bucket in the destination region
# Use a separate provider for the destination region
aws_dest = aws.Provider("dest", region=destination_region)
destination_bucket = aws.s3.Bucket(
    "destination-bucket",
    bucket="pulumi-multi-region-dest-bucket-ng1",
    force_destroy=True,
    opts=pulumi.ResourceOptions(provider=aws_dest),
)

# Enable versioning on both buckets
source_versioning = aws.s3.BucketVersioningV2(
    "source-bucket-versioning",
    bucket=source_bucket.id,
    versioning_configuration={"status": "Enabled"},
    opts=pulumi.ResourceOptions(provider=aws.Provider("prc", region=source_region)),
)

destination_versioning = aws.s3.BucketVersioningV2(
    "destination-bucket-versioning",
    bucket=destination_bucket.id,
    versioning_configuration={"status": "Enabled"},
    opts=pulumi.ResourceOptions(provider=aws_dest),
)

# IAM Role for S3 Replication
replication_role = aws.iam.Role(
    "replication-role",
    assume_role_policy=json.dumps({
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"Service": "s3.amazonaws.com"},
                "Action": "sts:AssumeRole"
            }
        ]
    })
)

# IAM Policy for Replication Role
replication_policy = aws.iam.RolePolicy(
    "replication-policy",
    role=replication_role.id,
    policy=pulumi.Output.all(
        source_bucket.arn,
        destination_bucket.arn
    ).apply(lambda arns: json.dumps({
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "s3:GetReplicationConfiguration",
                    "s3:ListBucket"
                ],
                "Resource": arns[0]
            },
            {
                "Effect": "Allow",
                "Action": [
                    "s3:GetObjectVersion",
                    "s3:GetObjectVersionAcl",
                    "s3:GetObjectVersionForReplication",
                    "s3:GetObjectLegalHold",
                    "s3:GetObjectVersionTagging",
                    "s3:GetObjectRetention"
                ],
                "Resource": f"{arns[0]}/*"
            },
            {
                "Effect": "Allow",
                "Action": [
                    "s3:ReplicateObject",
                    "s3:ReplicateDelete",
                    "s3:ReplicateTags",
                    "s3:GetObjectVersionTagging",
                    "s3:ObjectOwnerOverrideToBucketOwner"
                ],
                "Resource": f"{arns[1]}/*"
            }
        ]
    }))
)

# Replication configuration on the source bucket
replication_config = aws.s3.BucketReplicationConfig(
    "replication-config",
    bucket=source_bucket.id,
    role=replication_role.arn,
    rules=[{
        "id": "replicate-all",
        "status": "Enabled",
        "destination": {
            "bucket": destination_bucket.arn,
        },
        # Optionally, you can add filters, delete marker replication, etc.
    }],
    opts=pulumi.ResourceOptions(provider=aws.Provider("wrc", region=source_region)),
)

# Export bucket names
pulumi.export("source_bucket_name", source_bucket.bucket)
pulumi.export("destination_bucket_name", destination_bucket.bucket)
