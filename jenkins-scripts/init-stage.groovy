echo "Branch detected: ${env.BRANCH_NAME}"
if (env.BRANCH_NAME == 'main') {
  env.DOCKERFILE_BACKEND = 'Dockerfile.prod'
  env.DOCKERFILE_FRONTEND = 'Dockerfile'
} else {
  env.DOCKERFILE_BACKEND = 'Dockerfile'
  env.DOCKERFILE_FRONTEND = 'Dockerfile'
}
echo "Backend Dockerfile: ${env.DOCKERFILE_BACKEND}"
echo "Frontend Dockerfile: ${env.DOCKERFILE_FRONTEND}"