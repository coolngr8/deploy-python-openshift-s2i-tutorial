# Use S2I to build a new docker image using sources and a builder image.

## Introduction
- Building a Python-based service on Openshift without any docker or template config. file

## Steps
- Create a public repository on github.com
  - It should contain two files
    - *app.py*: Flask-based REST service
      - Port `8080` should be exposed against IP address `0.0.0.0`
    - *requirements.txt* : list, line by line, all the pip installables required to execute app.py in format `package==version`
      - Refer pypi.org for latest version number of each package
- Download and install *oc* client for Openshift and keep it on system path
- Execute following oc commands on system prompt
  - `oc login`
  - `oc new-app https://github.com/<user>/<repo>`
    - This command should output as follows
```
...
--> Creating resources ...
    buildconfig.build.openshift.io "<repo>" created
    deploymentconfig.apps.openshift.io "<repo>" created
    service "<repo>" created
--> Success
    Build scheduled, use 'oc logs -f bc/<repo>' to track its progress.
    Application is not exposed. You can expose services to the outside world by executing one or more of the commands below:
     'oc expose svc/<repo>'
    Run 'oc status' to view your app.
```
    - `oc expose svc/<repo>`
- However, there could be errors
  - To check those, check *logs* using Openshift web-page (Developer -> Advanced -> Search)
    - If so we need to manually delete all of the following:
      - BuildConfig
      - DeploymentConfig
      - Service
    - There are two more artifacts created (but they are automatically handled by Openshift)
      - Pods
      - Route
    - Route should be created manually to expose the service
      - It contains port mappings too
- Database (Postgres)
  - Connect to terminal via pod and use `psql` command-line utility
    - [PostgreSQL: Documentation: 12: 1.4. Accessing a Database](https://www.postgresql.org/docs/12/tutorial-accessdb.html)
  - [Connecting to a Database Using Port Forwarding in OpenShift](https://blog.openshift.com/openshift-connecting-database-using-port-forwarding)
    - `oc port-forward <postgres-pod> 12345:5432`
      - Now, for Postgres, pgAdmin can be configured to connect on 127.0.0.1:12345
   
