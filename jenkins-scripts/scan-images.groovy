withCredentials([string(credentialsId: 'snyk-token', variable: 'SNYK_TOKEN')]) {
  echo "Starting vulnerability scan on Docker Images..."
  sh """
    snyk auth $SNYK_TOKEN
    snyk container test ${DOCKER_IMAGE_BACKEND}:${TAG} --severity-threshold=high
    snyk container test ${DOCKER_IMAGE_FRONTEND}:${TAG} --severity-threshold=high
  """
  echo "Both backend and frontend images scanned successfully."
}