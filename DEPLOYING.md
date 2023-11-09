
# Deploying to Heroku

Heroku got rid of their free tier, but Render is unable to help resolve chromedriver installation issues, so let's deploy to heroku in the meantime :-/



```sh
heroku create gwu-courses
# git remote add heroku git@github.com:s2t2/gwu-courses-py.git
```

Set buildpacks, including to facilitate chromedriver installation:

  + https://github.com/heroku/heroku-buildpack-chromedriver
  + https://github.com/heroku/heroku-buildpack-google-chrome



```sh
heroku buildpacks:set heroku/python
heroku buildpacks:add https://github.com/heroku/heroku-buildpack-chromedriver.git
heroku buildpacks:add https://github.com/heroku/heroku-buildpack-google-chrome.git
```

Config vars:

```sh
heroku config:set APP_ENV="production"
heroku config:set HEADLESS_MODE="true"
heroku config:set SECRET_KEY="my-secret" # use your own secret value


heroku config:set CHROMEDRIVER_PATH="/app/.chromedriver/bin/chromedriver"
heroku config:set CHROME_BINARY_PATH="/app/.apt/usr/bin/google-chrome"
```

Deploying:

```sh
git push heroku main
#git push heroku web:main
```


<hr>


## Render Env Vars

Env vars:

```sh
CHROME_BINARY_PATH="/opt/render/project/bin/chrome/opt/google/chrome"
CHROMEDRIVER_PATH="/opt/render/project/bin/chromedriver"
HEADLESS_MODE="true"
SECRET_KEY="choose your own secret here"
```

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



...

OK here is the process, from start to finish:

```sh
# GENERATION / SETUP:
# h/t: https://stackoverflow.com/questions/42863913/key-load-public-invalid-format

ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519

sudo chmod 600 ~/.ssh/id_ed25519.pub

ssh-add  ~/.ssh/id_ed25519

# LOGIN:
sudo ssh srv-cekgudhgp3jlcsktih8g@ssh.ohio.render.com -i ~/.ssh/id_ed25519.pub
```

And we are able to connect via SSH!

### Render Server Filesystem

Default dir is "/opt/render/project/src" where the repo files are.

In "/opt/render/project", we have ".render" (chrome), "python" (Python-3.10.4 installation), "src" (repo), and "nodes" (empty).

In "/opt/render" we have ".bash_profile", ".cache", ".ssh_env", and "project".

In "opt" we have "render" and "render-ssh".

In the home folder we have:

    bin  boot  dev	etc  home  lib	lib64  media  mnt
    opt  proc  root  run  sbin  srv  sys  tmp  usr  var

We can't make directories in "usr", but we can make them in the "/opt/render/project" folder.

Able to install chromedriver executable with:

```sh

wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip

unzip /tmp/chromedriver.zip chromedriver -d /opt/render/project/bin

rm /tmp/chromedriver.zip
```

But we need to also add to path perhaps:

```sh
export PATH="${PATH}:${CHROMEDRIVER_PATH}"
```

Original path is:

```sh
echo $PATH

/opt/render/project/src/.venv/bin:
/opt/render/project/src/.venv/bin:
/home/render/.python-poetry/bin:
/usr/local/sbin:
/usr/local/bin:
/usr/sbin:
/usr/bin:
/sbin:
/bin:
/opt/render-ssh/session/bin

```


Remember to set env var to match:

    CHROMEDRIVER_PATH="/opt/render/project/bin/chromedriver"

To overcome "cannot find Chrome binary", also install chrome binary (see "build.sh").

Set:

    CHROME_BINARY_PATH="/opt/render/project/bin/chrome/opt/google/chrome"

Need to resolve:

    "Chrome failed to start: exited abnormally. (unknown error: DevToolsActivePort file doesn't exist) (The process started from chrome location /opt/render/project/bin/chrome/opt/google/chrome is no longer running, so ChromeDriver is assuming that Chrome has crashed.)
