# Integrating Bump My Version with CI/CD

Bump My Version is a powerful tool for managing version numbers in your projects. Integrating it into your Continuous Integration and Continuous Deployment (CI/CD) pipeline can automate the versioning process, ensuring consistency and reducing manual errors. This guide will walk you through the process of integrating Bump My Version into various CI/CD platforms and provide best practices for automating version bumping.

## Table of Contents

1. [General Integration Steps](#general-integration-steps)
2. [GitHub Actions Integration](#github-actions-integration)
3. [GitLab CI Integration](#gitlab-ci-integration)
4. [Jenkins Integration](#jenkins-integration)
5. [Best Practices](#best-practices)
6. [Handling Version Control System Integration](#handling-version-control-system-integration)

## General Integration Steps

To integrate Bump My Version into your CI/CD pipeline, you'll typically follow these steps:

1. Install Bump My Version in your CI/CD environment
2. Configure Bump My Version for your project
3. Run Bump My Version as part of your CI/CD process
4. Commit and push the changes (if desired)

Let's look at how to implement these steps in different CI/CD platforms.

## GitHub Actions Integration

GitHub Actions provides a powerful and flexible way to automate your software workflows. Here's an example of how to integrate Bump My Version into a GitHub Actions workflow:

```yaml
name: Bump Version

on:
  workflow_dispatch:
    inputs:
      bump-type:
        description: 'Bump type'
        required: true
        default: 'patch'
        type: choice
        options:
        - major
        - minor
        - patch

jobs:
  bump-version:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'

      - name: Install Bump My Version
        run: pip install bump-my-version

      - name: Bump version
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          git config user.name 'GitHub Action'
          git config user.email 'action@github.com'
          bump-my-version bump ${{ github.event.inputs.bump-type }}

      - name: Push changes
        run: git push --follow-tags
```

This workflow:

1. Can be manually triggered with a choice of bump type (major, minor, or patch)
2. Checks out the code and sets up Python
3. Installs Bump My Version
4. Runs the version bump command
5. Pushes the changes back to the repository

## GitLab CI Integration

For GitLab CI, you can use a similar approach. Here's an example `.gitlab-ci.yml` configuration:

```yaml
bump-version:
  image: python:3.9
  script:
    - pip install bump-my-version
    - git config user.name "GitLab CI"
    - git config user.email "gitlab-ci@example.com"
    - bump-my-version bump $BUMP_TYPE
    - git push --follow-tags
  only:
    - main
  when: manual
  variables:
    BUMP_TYPE: patch
```

This job:

1. Uses a Python image
2. Installs Bump My Version
3. Configures Git user information
4. Runs the version bump command
5. Pushes the changes back to the repository

You can manually trigger this job and override the `BUMP_TYPE` variable to choose major, minor, or patch.

## Jenkins Integration

For Jenkins, you can create a pipeline script that integrates Bump My Version. Here's an example `Jenkinsfile`:

```groovy
pipeline {
    agent any

    parameters {
        choice(name: 'BUMP_TYPE', choices: ['patch', 'minor', 'major'], description: 'Type of version bump')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup') {
            steps {
                sh 'pip install bump-my-version'
            }
        }

        stage('Bump Version') {
            steps {
                sh """
                    git config user.name "Jenkins"
                    git config user.email "jenkins@example.com"
                    bump-my-version bump ${params.BUMP_TYPE}
                """
            }
        }

        stage('Push Changes') {
            steps {
                sh 'git push --follow-tags'
            }
        }
    }
}
```

This pipeline:

1. Allows you to choose the bump type when running the job
2. Checks out the code
3. Installs Bump My Version
4. Runs the version bump command
5. Pushes the changes back to the repository

## Best Practices

When integrating Bump My Version into your CI/CD pipeline, consider these best practices:

1. **Automate sensibly**: While it's possible to automatically bump versions on every commit, it's often better to trigger version bumps manually or at specific points in your workflow (e.g., when merging to a release branch).

2. **Use consistent configurations**: Ensure your Bump My Version configuration (`.bumpversion.toml` or in `pyproject.toml`) is consistent across all environments.

3. **Version control your configuration**: Keep your Bump My Version configuration file in version control to ensure all team members and CI/CD systems use the same settings.

4. **Use meaningful commit messages**: When bumping versions, use clear and informative commit messages. Bump My Version allows you to customize these messages in your configuration.

5. **Handle errors gracefully**: In your CI/CD scripts, make sure to handle potential errors from Bump My Version and provide clear output for troubleshooting.

6. **Secure your workflows**: When pushing changes from CI/CD systems, ensure you're using secure methods to authenticate with your version control system.

## Handling Version Control System Integration

Bump My Version integrates with Git and Mercurial version control systems. When using it in a CI/CD environment, keep these points in mind:

1. **Authentication**: Ensure your CI/CD system has the necessary permissions to push changes to your repository. This often involves setting up SSH keys or access tokens.

2. **Commit authorship**: Configure the Git user name and email in your CI/CD environment to accurately reflect the automated nature of the commits.

3. **Tagging**: Bump My Version can create tags for your new versions. Ensure your CI/CD system is configured to push tags along with commits.

4. **Branch protection**: If you have branch protection rules (e.g., on the main branch), you may need to adjust these or use special access tokens to allow your CI/CD system to push directly to protected branches.

5. **Handling conflicts**: In rare cases, concurrent updates might cause conflicts. Implement retry mechanisms or manual intervention processes for these situations.

By following these guidelines and examples, you can effectively integrate Bump My Version into your CI/CD pipeline, automating your versioning process and ensuring consistent version management across your projects.