pipeline {
  agent any

  environment {
    GIT_URL = "https://github.com/vetrax1/evently.git"
  }

  stages {
    stage("Init") {
      steps {
        echo "Branch: ${env.BRANCH_NAME}"
        echo "Commit: ${env.GIT_COMMIT}"
      }
    }

    stage("Trigger Builder") {
      steps {
        build job: 'evently-builder',
        parameters: [
          string(name: 'GIT_URL', value: env.GIT_URL),
          string(name: 'GIT_BRANCH', value: env.BRANCH_NAME),
          string(name: 'GIT_COMMIT', value: env.GIT_COMMIT)
        ]
      }
    }
  }
}
