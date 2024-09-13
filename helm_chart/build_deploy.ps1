helm lint .
helm package .

$PACKAGE = Resolve-Path "*.tgz" | Select-Object -ExpandProperty Path
helm upgrade --install app $PACKAGE -n datawave