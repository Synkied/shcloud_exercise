# Compatibility
Tested on Python 3.8

# Installation
- Get Docker
https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository
- Get Docker Compose
https://docs.docker.com/compose/install/#install-compose-on-linux-systems

If you want to run Docker without sudo:
https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user

Then create a network proxy:
`docker network create proxy`

Then proceed to project installation:
`make`

# Tests
`python manage.py test`

# Use application
Go to http://localhost:8061