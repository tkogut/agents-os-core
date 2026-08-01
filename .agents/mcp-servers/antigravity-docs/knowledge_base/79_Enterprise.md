# Enterprise
Source URL: https://antigravity.google/docs/enterprise

Enterprise
Getting Started with Antigravity and Gemini Enterprise Agent Platformlink

Supported products: Antigravity 2.0Antigravity CLI

This guide is for administrators setting up the Google Cloud environment to enable Antigravity integration with Gemini Enterprise Agent Platform. This integration allows enterprise developers to use Antigravity with models hosted in your own Google Cloud project, under Google Cloud Terms of Service, satisfying private networking and data residency requirements, and utilizing consumption-based billing.

info
Note: Integration is only supported for Antigravity 2.0 and Antigravity CLI. Antigravity IDE is not supported for enterprise customers.
Supported Models
Basic Setuplink
Prerequisiteslink

Before you begin, ensure you have:

A Google Cloud account.
Access to the Google Cloud console.
Step 1: Select or Create a Google Cloud Projectlink

In the Google Cloud console, on the project selector page, select or create a Google Cloud project.

Roles Required to Select or Create a Projectlink

Select a project: Selecting a project doesn’t require a specific IAM role—you can select any project that you’ve been granted a role on.

info
Note: To switch to a different Google Cloud project or location, you must first log out of the Antigravity CLI or Hub, then log back in and select your new project/location. Directly changing the project or location while logged in is currently not supported.

Create a project: To create a project, you need the Project Creator role (roles/resourcemanager.projectCreator), which contains the resourcemanager.projects.create permission. Learn how to grant roles.

info
Note: If you don’t plan to keep the resources that you create in this procedure, create a new project instead of selecting an existing project. After you finish these steps, you can delete the project to remove all associated resources.

Go to project selector

Step 2: Verify Billinglink

Verify that billing is enabled for your Google Cloud project. You can check the billing status in the Google Cloud Billing Console. For detailed instructions, see Verify the billing status of your projects.

Step 3: Enable the Agent Platform APIlink

To use Antigravity with Gemini Enterprise Agent Platform, you must enable the Agent Platform API (aiplatform.googleapis.com).

Roles Required to Enable APIslink

To enable APIs, you need the Service Usage Admin IAM role (roles/serviceusage.serviceUsageAdmin), which contains the serviceusage.services.enable permission. Learn how to grant roles.

Enable the APIlink

Enable the Agent Platform API in the API Library

User Permissionslink

To get the permissions that you need to use Gemini Enterprise Agent Platform, ask your administrator to grant you the Agent Platform User (roles/aiplatform.user) IAM role on your project. For more information about granting roles, see Manage access to projects, folders, and organizations.

You might also be able to get the required permissions through custom roles or other predefined roles.

Advanced Configurationlink
Request and Response Logginglink

For detailed instructions on how to enable and configure request and response logging for the Gemini Enterprise Agent Platform, please refer to the official documentation:

Request and Response Logging Documentation

VPC Service Controls (VPC-SC)link

If your organization has a service perimeter, then you must add the following resources to your perimeter:

Agent Platform API

For detailed instructions on how to configure VPC Service Controls, please refer to the official documentation:

VPC Service Controls Documentation

Complementary Resourceslink
Consumption Optionslink

Gemini Enterprise Agent Platform offers different consumption options to suit your needs.

For detailed information on consumption options, please refer to the official documentation:

Consumption Options Documentation

Deployments and Endpoints Locationslink

For now, Antigravity CLI and 2.0 offer 3 endpoints: global, multi-region eu, and multi-region us.

info
Note: Image generation is currently not available in eu and us locations.

For a full list of available locations and deployment endpoints, please refer to the official documentation:

Deployment Endpoints Documentation

Firebase Studio Migration
Plans