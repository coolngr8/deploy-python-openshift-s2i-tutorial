# Openshift - Deploying Python Service From Local Codebase

## Required files
- Dockerfile

## Steps
- Source: [Binary Builds](https://docs.openshift.com/container-platform/3.6/dev_guide/dev_tutorials/binary_builds.html)
  - `oc login`
  - Change to directory containing codebase locally
  - Create a `Dockerfile` there for exposing a Python service
  - Use following commands
```
oc new-build --strategy docker --binary --docker-image python:latest --name ahmedabad01
oc start-build ahmedabad01 --from-dir . --follow
oc new-app ahmedabad01
oc expose dc/ahmedabad01 --port=8080
```
  - Using Openshift web-based interface (browser), navigate to Developer -> Advanced -> Search -> Route
    - Create a route for above service
