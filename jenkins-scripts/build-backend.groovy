echo "Building backend image from ${env.BRANCH_NAME}..."
sh """
  docker build -f evently-backend/${env.DOCKERFILE_BACKEND} -t ${DOCKER_IMAGE_BACKEND}:${TAG} evently-backend
"""
echo "Backend image successfully built and tagged: ${DOCKER_IMAGE_BACKEND}:${TAG}"