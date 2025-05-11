pipeline {
  agent any

  environment {
    DOCKER_IMAGE_BACKEND = 'anunukemsam/evently-backend'
    DOCKER_IMAGE_FRONTEND = 'anunukemsam/evently-frontend'
    TAG = "${GIT_COMMIT.take(8)}"
    DOCKER_CREDENTIALS_ID = 'dockerhub-creds'
    SNYK_TOKEN = credentials('snyk-api-token')
    SSH_CREDENTIALS_ID = 'vm-ssh-key'
    VM_USER = 'your-vm-user'
    VM_HOST = 'your.vm.ip.address'
    VM_DEPLOY_DIR = '/home/your-vm-user'
  }

  stages {
    stage('Init Stage') {
      steps {
        script {
          echo "Branch detected: ${env.BRANCH_NAME}"
          if (env.BRANCH_NAME == 'main') {
            env.DOCKER_IMAGE_BACKEND == 'Dockerfile.prod'
            env.DOCKER_IMAGE_FRONTEND == 'Dockerfile'
          } else {
            env.DOCKER_IMAGE_BACKEND == 'Dockerfile'
            env.DOCKER_IMAGE_FRONTEND == 'Dockerfile'
          }
          echo "Backend Dockerfile: ${env.DOCKERFILE_BACKEND}"
          echo "Frontend Dockerfile: ${env.DOCKERFILE_FRONTEND}"
        }
      }
    }
  }

  post {
    always {
      echo "Pipeline completed for branch: ${env.BRANCH_NAME}"
    }
  }
}
