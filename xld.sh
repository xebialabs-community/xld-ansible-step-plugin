package=$1
environment=$2

echo "
apiVersion: xl-deploy/v1
kind: Deployment
spec:
  package: ${package}
  environment: ${environment}
  onSuccessPolicy: ARCHIVE
  orchestrators:
    - sequential-by-deployed
" > /tmp/deploy.yaml

cat /tmp/deploy.yaml
./xlw --config ./config.yaml preview  -f /tmp/deploy.yaml
./xlw --config ./config.yaml  apply  -f /tmp/deploy.yaml
