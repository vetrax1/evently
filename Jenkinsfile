pipeline {
  agent any
  stages {
    stage('Capture Environment') {
      steps {
        sh 'env > $JENKINS_HOME/workspace/context_env'
      }
    }
    stage('Trigger Builder') {
      steps {
        build job: 'evently-builder'
      }
    }
  }
}
