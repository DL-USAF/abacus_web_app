# abacus_web_app

[![Package](https://github.com/DL-USAF/abacus_web_app/actions/workflows/python_package.yaml/badge.svg)](https://github.com/DL-USAF/abacus_web_app/actions/workflows/python_package.yaml)

## Building an Image
To build the web app as a image, Docker is required. By running the `local_build.ps1` script
you will run the linting process along with a docker build to locally build the image. Currently this will
always create an image with the `latest` tag.

## Helm Charts
To build a helm package, navigate to `helm_chart` then run the `build_pkg.ps1` script. 

To deploy to your kubeconfig environment, run the `build_deploy.ps1` script.

## Configuration
Currently you are able to configure what authorization service the web app utilizes via the environment
variable `AUTH_SERVICE`. We currently only support Keycloak, Dex, and a Mock Identity Providers. 
You can specify a config file by placing a `<IdP>_config.json` in a `configs` folder in the directory 
you are running from. The app will check for the file and if found, read it in as the values to 
configure the OIDC.
