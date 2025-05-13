properties([
  parameters([
    booleanParam(
      name: 'ROLLBACK',
      defaultValue: false,
      description: 'Check this box to trigger a rollback on the production Kubernetes deployment.'
    )
  ])
])

pipeline {
  agent any

  environment {
    DOCKER_IMAGE_BACKEND = 'anunukemsam/evently-backend'
    DOCKER_IMAGE_FRONTEND = 'anunukemsam/evently-frontend'
    TAG = "${GIT_COMMIT.take(8)}"
    SNYK_TOKEN = credentials('snyk-token')
    VM_USER = 'your-vm-user'
    VM_HOST = 'your.vm.ip.address'
    VM_DEPLOY_DIR = '/home/vetrax'
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
    stage('Push Docker Images to Docker Hub') {
      when {
        anyOf {
          branch 'main'
          branch 'develop'
        }
      }
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds',usernameVariable: 'DOCKER_USER',passwordVariable: 'DOCKER_PASS')]) {
          script {
            echo "Authenticating with DockerHub..."
            sh """
              echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
            """
            echo "Pushing backend image: ${DOCKER_IMAGE_BACKEND}:${TAG}"
            echo "Pushing frontend image: ${DOCKER_IMAGE_FRONTEND}:${TAG}"
            sh """
              docker push ${DOCKER_IMAGE_BACKEND}:${TAG}
              docker push ${DOCKER_IMAGE_FRONTEND}:${TAG}
            """
            echo "Images successfully pushed to dockerhub"
          }
        }
      }
    }
    stage('Deploy to Staging') {
      when {
        branch 'develop'
      }
      steps {
        sshagent(['vm-ssh-key']) {
          script {
            sh """
              ssh -o StrictHostKeyChecking=no ${VM_USER}@${VM_HOST} << EOF
                echo "Starting deploy on staging VM..."
                cd ${VM_DEPLOY_DIR}/evently
                docker compose pull
                docker compose up -d --remove-orphans
                docker image prune -f || true
                echo "Staging deployment complete!"
              EOF
            """
          }
        }
      }
    }
    stage('Deploy to Prod-k8s') {
      when {
        branch 'main'
      }
      steps {
        sshagent(['vm-ssh-key']) {
          script {
            echo "Copying Kubernetes manifest to production VM..."
            sh """
              scp -o StrictHostKeyChecking=no -r k8s ${VM_USER}@${VM_HOST}:${VM_DEPLOY_DIR}
            """
            sh """
              ssh -o StrictHostKeyChecking=no ${VM_USER}@${VM_HOST} << EOF
                cd ${VM_DEPLOY_DIR}/k8s
                sed -i 's|<IMAGE_TAG>|${TAG}|g' backend-deployment.yaml
                kubectl apply -f backend-deployment.yaml
                kubectl apply -f backend-service.yaml
                kubectl apply -f hpa.yaml
                echo "Waiting for rollout to complete..."
                kubectl rollout status deployment/evently-backend

                echo "Deploying frontend..."
                sed -i 's|<IMAGE_TAG>|${TAG}|g' frontend-deployment.yaml
                kubectl apply -f frontend-deployment.yaml
                kubectl apply -f frontend-service.yaml
                echo "Waiting for rollout to complete..."
                kubectl rollout status deployment/evently-frontend
                echo "Production deployment complete!"
              EOF
            """
          }
        }
      }
    }
    stage('Rollback') {
      when {
        branch 'main'
        expression { return params.ROLLBACK == true }
      }
      steps {
        sshagent(['vm-ssh-key']) {
          script {
            echo "Initiating rollback on production Kubernetes cluster..."
            sh """
              ssh -o StrictHostKeyChecking=no ${VM_USER}@${VM_HOST} << EOF
                echo "Rolling back backend deployment..."
                kubectl rollout undo deployment/evently-backend
                echo "Rolling back frontend deployment..."
                kubectl rollout undo deployment/evently-frontend
                echo "Rollback complete."
              EOF
            """
          }
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
