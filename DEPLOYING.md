
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
heroku config:set HEADLESS_MODE="true"
heroku config:set SECRET_KEY="my-secret" # use your own secret value

heroku config:set CHROME_BINARY_PATH="/app/.apt/usr/bin/google-chrome"
heroku config:set CHROMEDRIVER_PATH="/app/.chromedriver/bin/chromedriver"

heroku config:set GA_TRACKER_ID="G-__________" # use your own google analytics
```

Deploying:

```sh
git push heroku main
#git push heroku web:main
```
