pipeline {
  agent any

  stages {
    stage("Init") {
      steps {
        script {
          sh "env >> context_env"
          archiveArtifacts artifacts: 'context_env'
        }
      }
    }
    stage("Trigger Builder") {
      steps {
        build job: 'evently-builder'
      }
    }
  }
}
