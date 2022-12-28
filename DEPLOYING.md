



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

### Build Script

Was able to get docker with chromedriver running locally, but the render build was still failing. Tech support suggests using a build script ("build.sh"):

  + https://render.com/docs/deploy-django#create-a-build-script

See also:

  + https://community.render.com/t/installing-headless-chromium-w-o-docker/5185
  + https://gist.github.com/BigAlRender/41f4c4d87df3e25770e3db8db728443e


Ensure the script is executable:

```sh
chmod a+x build.sh
```


Change the build command from "pip install -r requirements.txt" to "./build.sh" to invoke the build script (and add the pip installation command in there to complete the process).

Set env var:
    CHROMEDRIVER_PATH="/opt/render/project/.render/chrome"

### SSH

Render has SSH capabilities, but only for paid plans. It would be easier to SSH onto the server the first time only, to figure out what the build script needs to be, rather than trying lots of options via deployment process.

```sh
ssh USERNAME@ssh.REGION.render.com
```

Looks like [RSA keys don't work](https://render.com/docs/ssh-troubleshooting#avoid-rsa-keys), so need to [generate a new key](https://render.com/docs/ssh-generating-keys) and use that:

```sh
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519
#> update permissions so it will work
#chmod 400 ~/.ssh/id_ed25519.pub
#> NOPE

cat ~/.ssh/id_ed25519.pub | pbcopy
# > then paste into the render settings
```

```sh
ssh USERNAME@ssh.REGION.render.com -i ~/.ssh/id_ed25519.pub
```

There is an issue with the key permissions and/or format. Need to revisit.
