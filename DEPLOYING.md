



# Deploying to Heroku

JK Heroku is dead.

# Deploying to Digital Ocean


https://docs.digitalocean.com/tutorials/app-deploy-flask-app/


Oh JK it's not free either.

https://www.digitalocean.com/pricing


# Deploying to ...

Cool the Anaconda folks?

https://www.pythonanywhere.com/pricing/

Oh only one app? Maybe education deal...

# Deploying to Render

https://render.com/docs/deploy-flask


New Python 3 web service.

Start Command:

    gunicorn "web_app:create_app()"


Has environment variables, and secret config file creation (can probably be used with "google-credentials.json" file approach).

Has GitHub integration with auto-deploy capabilities. Can deploy from branch.

Starting with auto deploy for now.

Build is very slow. They say it gets faster if you pay.

No CLI installation required so far.

Cron Jobs require payment of $1/mo (or perhaps fractional part thereof only when processes are running?)

We are seeing some errors due to old version of Python. Need to specify python version via env var:

    PYTHON_VERSION=3.8.2
    PYTHON_VERSION=3.10.4

Build is ... so ... slow ...

OK Looks good, but how to install chromedriver though?

Maybe need to use a Docker environment instead of Python 3.

Let's try setting up the proper Docker environment in development first, to get it right. Especially because the build is so slow we can't be experimenting in prod.

### Docker in Development

See "Dockerfile" in root directory of the repo (which needs to be capitalized exactly the same), which is supposed to install chromedriver, as well as python and packages.

Let's create a local image and run it:

```sh
docker build . -t my_python_chromedriver_image # builds a new docker image

docker run -it my_python_chromedriver_image /bin/bash # starts up a new container of a docker image

# mess around inside the container, to confirm installations:
which chromedriver
#> /usr/local/bin/chromedriver
# OK great it is installed
pip list
#> OK great

HEADLESS_MODE=true SUBJECT_IDS="FILM,NRSC, CSCI, EMSE, BADM, ISTM" python -m app.multisubject
#> great, it works.

# then exit
```

Once the image has been built, can come back to it like this:

```sh

docker container ls --all # find all container names and IDs

docker start <container id> # starts a paused docker container

docker attach <container id> # reconnects to a running docker container
```
