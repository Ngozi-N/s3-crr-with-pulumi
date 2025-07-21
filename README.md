# S3 Cross-Region Replication (CRR) with Pulumi

This project automates the creation of **S3 Cross-Region Replication (CRR)** using **Pulumi** and **Python**. It provisions two S3 buckets in different AWS regions, configures replication between them, and manages the necessary IAM roles and permissions—all through Infrastructure as Code.

## What’s in the Project?

- Source and Destination S3 Buckets (Different Regions)
- IAM Role & Policy for Replication
- Replication Configuration
- Pulumi Python Code

## How to Use

1. **Setup AWS CLI, Pulumi, Python**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
3. **Configure Pulumi stack**
4. **Deploy**
5. **Test replication**
6. **Destroy resources when done**

Architecture Overview
Pulumi provisions:
- 2 S3 Buckets across regions
- IAM Role for replication
- Replication configuration

Everything is fully automated and reusable using Pulumi's code-based approach.

Learn More
Read the detailed Medium guide: [Medium](https://medium.com/@nwadialongozi/automating-s3-cross-region-replication-crr-with-pulumi-step-by-step-guide-03a81e1ec8e9)

Author
Ngozi Nwadialo – [GitHub](https://github.com/Ngozi-N)


