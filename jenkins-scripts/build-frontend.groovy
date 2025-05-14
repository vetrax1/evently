echo "Building frontend image from ${env.BRANCH_NAME}..."
sh """
  docker build -f evently-frontend/${env.DOCKERFILE_FRONTEND} -t ${DOCKER_IMAGE_FRONTEND}:${TAG} evently-frontend
"""
echo "Frontend image successfully built and tagged: ${DOCKER_IMAGE_FRONTEND}:${TAG}"