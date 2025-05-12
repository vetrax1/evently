pipeline {
  agent any

  environment {
    DOCKER_IMAGE_BACKEND = 'anunukemsam/evently-backend'
    DOCKER_IMAGE_FRONTEND = 'anunukemsam/evently-frontend'
    TAG = "${GIT_COMMIT.take(8)}"
    DOCKER_CREDENTIALS_ID = 'dockerhub-creds'
    SNYK_TOKEN = credentials('snyk-token')
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
    stage('Build Backend Image') {
      steps {
        script {
          echo "Building backend image from ${env.BRANCH_NAME}..."
          sh """
            docker build -f ${env.DOCKERFILE_BACKEND} -t ${env.DOCKER_IMAGE_BACKEND}:${TAG} evently-backend
          """
          echo "Backend image successfully build and tagged: ${env.DOCKER_IMAGE_BACKEND}:${TAG}"
        }
      }
    }
    stage('Build Frontend Image') {
      steps {
        script {
          echo "Building frontend image from ${env.BRANCH_NAME}..."
          sh """
            docker build -f ${env.DOCKERFILE_FRONTEND} -t ${env.DOCKER_IMAGE_FRONTEND}:${TAG} evently-frontend
          """
          echo "Frontend image successfully build and tagged: ${env.DOCKER_IMAGE_FRONTEND}:${TAG}"
        }
      }
    }
    stage('Scan Docker Images') {
      steps {
        script {
          echo "Starting vulnerability scan on Docker Images..."
          sh """
            snyk auth ${SNYK_TOKEN}
            snyk container test ${DOCKER_IMAGE_BACKEND}:${TAG} --severity-threshold=high
            snyk container test ${DOCKER_IMAGE_FRONTEND}:${TAG} --severity-threshold=high
          """
          echo "Both backend and frontend images scanned successfully."
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
