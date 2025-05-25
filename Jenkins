pipeline {
  agent any
  parameters {
    booleanParam(
      name: 'ROLLBACK',
      defaultValue: false,
      description: 'Check this box to trigger a rollback on the production Kubernetes deployment.'
    )
  }

  environment {
    DOCKER_IMAGE_BACKEND = 'anunukemsam/evently-backend'
    DOCKER_IMAGE_FRONTEND = 'anunukemsam/evently-frontend'
    TAG = "${GIT_COMMIT.take(8)}"
    VM_USER = 'vetrax'
    STAGING_VM_HOST = '192.168.4.127'
    PROD_VM_HOST = '192.168.4.93'
    VM_DEPLOY_DIR = '/home/vetrax'
  }

  stages {
    stage('Build Info') {
      steps {
        load 'jenkins-scripts/build-info.groovy'
      }
    }
    stage('Init Stage') {
      steps {
        script {
          load 'jenkins-scripts/init-stage.groovy'
        }
      }
    }
    stage('Build Backend Image') {
      steps {
        script {
          load 'jenkins-scripts/build-backend.groovy'
        }
      }
    }
    stage('Build Frontend Image') {
      steps {
        script {
          load 'jenkins-scripts/build-frontend.groovy'
        }
      }
    }
    stage('Scan Docker Images') {
      steps {
        script {
          load 'jenkins-scripts/scan-images.groovy'
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
              ssh -o StrictHostKeyChecking=no ${VM_USER}@${STAGING_VM_HOST} << "
                echo "Starting deploy on staging VM..."
                echo 'TAG=${TAG}' > ${VM_DEPLOY_DIR}/evently/.env
                cd ${VM_DEPLOY_DIR}/evently
                docker compose pull
                docker compose up -d --remove-orphans
                docker image prune -f || true
                echo "Staging deployment complete!"
              "
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
              scp -o StrictHostKeyChecking=no -r k8s ${VM_USER}@${PROD_VM_HOST}:${VM_DEPLOY_DIR}
            """
            sh """
              ssh -o StrictHostKeyChecking=no ${VM_USER}@${PROD_VM_HOST} '
                cd ${VM_DEPLOY_DIR}/k8s &&
                sed -i "s|<IMAGE_TAG>|${TAG}|g" backend-deployment.yaml &&
                kubectl apply -f backend-deployment.yaml &&
                kubectl apply -f backend-service.yaml &&
                kubectl apply -f hpa.yaml &&
                echo "Waiting for rollout to complete..." &&
                kubectl rollout status deployment/backend-deployment &&

                echo "Deploying frontend..." &&
                sed -i "s|<IMAGE_TAG>|${TAG}|g" frontend-deployment.yaml &&
                kubectl apply -f frontend-deployment.yaml &&
                kubectl apply -f frontend-service.yaml &&
                echo "Waiting for rollout to complete..." &&
                kubectl rollout status deployment/frontend-deployment &&
                echo "Production deployment complete!"
              '
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
              ssh -o StrictHostKeyChecking=no ${VM_USER}@${PROD_VM_HOST} << '
                echo "Rolling back backend deployment..."
                kubectl rollout undo deployment/evently-backend
                echo "Rolling back frontend deployment..."
                kubectl rollout undo deployment/evently-frontend
                echo "Rollback complete."
              '
            """
          }
        }
      }
    }
  }

  post {
    success {
      echo "Build & deploy succeeded."
    }
    failure {
      echo "Pipeline failed. Please check logs."
    }
    always {
      echo "Pipeline completed for branch: ${env.BRANCH_NAME}"
    }
  }
}
