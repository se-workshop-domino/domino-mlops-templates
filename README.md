# Domino MLOps Templates

Welcome to the Domino MLOps solution repository! This project serves as a comprehensive starting point for implementing MLOps within Domino.

MLOps entails a collection of repeatable, automated, and collaborative workflows, incorporating best practices. It empowers teams of ML professionals to efficiently deploy their machine learning models into production after approval from various stages of the ML ops pipeline.

## Project Overview

This solution offers a modular end-to-end approach for MLOps within Domino, covering Jobs, Models, and Apps publishing.

## Prerequisites

- A Domino subscription with host endpoint URL and user API access key.
- A GitHub account capable of creating environments and adding corresponding variables to them.
- Understanding of GitHub workflows.

Ensure you have GitHub CLI installed: [GitHub CLI](https://cli.github.com/)

## Methodology

This project template demonstrates the usage of GitHub Actions workflows for CI/CD and employs Domino Data Planes, representing different dataplanes for different stages of the OPS pipeline.

For this template project, we would establish three stages in the Domino experiment manager and create three GitHub environments, each mapping to the corresponding stage in the experiment manager of Domino. Progressing through the CI/CD pipeline involves changing the stage in the experiment manager and approving the stage in GitHub to advance it to the next stage.

## GitHub

The project utilizes GitHub Actions workflows located in the `.github/workflows/` folder for Jobs, Apps, and Models to deploy them to different hardware tiers, representing various stages of ML pipelines.

Users need to register different environments in the github project and the environment variables representing appropriate hardware tiers for that stage in Domino Data Plane.

### Workflow:

1. User creates a branch of the project from the main branch and works on the code using Domino workspaces.
2. When the user intends to push the code to production, they merge the code to the main branch, triggering the CI/CD pipeline via GitHub Actions workflows.
3. The approval process from one stage to another involves approving the stage change in the experiment manager and approving it in GitHub as well.
