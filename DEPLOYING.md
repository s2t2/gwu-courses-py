



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
