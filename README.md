# Modernisation Platform Incident Response ⚡

Modernisation Platform Incident Response is a Django app based on [Monzo's Response tool](https://github.com/monzo/response), and OPG integrations with tools they use and a reskin to meet GOV.UK design standards.
Further changes to the app will be to make it work for the Modernisation Platform. Especially the deployment of the application, which most likely will be hosted on the Cloud Platform.

## Local Development

Refer to the diagram in this [README](https://github.com/monzo/response/blob/master/demo/README.md) to see what components the response app is made of, when running locally.

# Step 1 - create a slack app

Create a slack app using this [README](https://github.com/monzo/response/blob/master/docs/slack_app_create.md).

# Step 2 - configure your local environment

Copy `env.dev.example` to `.env` and configure the environment variables inside. All environment variables need to be set, but some can be set to nonsense values (i.e. `ENV_VAR=...`) as detailed in the table below.

# Step 3 - set ngrok token

Ngrok is a tool that allows an application that is run locally to be publicly accessible, by exposing a public endpoint on your local machine.
In your browser, navigate to [ngrok website](https://dashboard.ngrok.com/get-started/setup), register or sign in and make a note of your personal token.
Set `NGROK_TOKEN` as an environment variable. This will be further used when building a Docker image or running the Docker compose.
`export NGROK_TOKEN=<your_personal_ngrok_token>`

# Step 4 - manually create Docker images for the response, cron, response-nginx and ngrok containers (Optional)

Run the following `docker build` commands in order to create Docker images for the response, cron, response-nginx and ngrok containers:

```
docker build -t response:latest -f ./Dockerfile.response .
docker build -t cron:latest -f ./Dockerfile.cron .
docker build -t response-nginx:latest -f ./Dockerfile.nginx .
docker build -t ngrok:latest -f ./Dockerfile.ngrok --build-arg NGROK_TOKEN .
```

Refer to [Docker build documentation](https://docs.docker.com/engine/reference/commandline/build/) on the build options.

# Step 5 - set ECR account number (Optional)

If you are planning to use images that are published on a remote ECR repository, set `ECR_ACCOUNT_NUMBER` as follow:
`export ECR_ACCOUNT_NUMBER=<ECR_account_number>`
where you can retrieve your `<ECR_account_number>` by following [Cloud Platform user manual](https://user-guide.cloud-platform.service.justice.gov.uk/documentation/getting-started/ecr-setup.html#accessing-the-credentials),
e.g.
`cloud-platform decode-secret -n incident-management-dev -s ecr-repo-incident-management-dev`

# Step 6 - version incompatibility workaround (Optional)

If your docker version is >= `Docker version 20.10.17, build 100c701` you may need this workaround to avoid docker compose failures in the next step:

```
export DOCKER_BUILDKIT=0
export COMPOSE_DOCKER_CLI_BUILD=0
```

# Step 7 - run docker compose

Edit compose.yml following comments inside the file.
In order to start the application run the `docker-compose up -d`.

Refer to Docker compose [specification](https://docs.docker.com/compose/compose-file/) and [file build](https://docs.docker.com/compose/compose-file/build/) documentation for more options.

# Step 8 - verify the local deployment

To confirm ngrok token was configured correctly, see on the ngrok container the content of the `ngrok.yml` file and whether the `authtoken` value is populated:
`cat ngrok.yml`

In your browser, navigate to:
http://localhost/
http://localhost:4040/inspect/http

Make a note of the ngrok URL, it will look something like:
`https://<IP>.ngrok.io`

# Step 9 - configure the slack app

In your browser, navigate to https://api.slack.com/apps and configure slack app setup using this [README](https://github.com/monzo/response/blob/master/docs/slack_app_config.md).

# Step 10 - test the app

In your slack channel, try `/incident test` and see if it works.

## Versions and Releases

This project uses [SemVer for](https://semver.org) versoning.

By default, any merge to main will be a MINOR release. You can control which version number to increment by add `#major`, `#minor` or `#patch` to the commit message that goes into main.

### Configuring Slack

In order to avoid polluting our real Slack workspace, and to give you full control over permissions, you should configure your local copy of the app with [your own Slack workspace](#slack-create).

You now need to [create a Slack app](#slack-app-create) and [configure it](#slack-app-config). Note that you'll need your public ngrok URL to configure endpoints for Slack to use, which you can find by running `docker-compose logs ngrok`.

After you've configured your app, Slack will provide you with bot OAuth token (starting `xoxb-`) and a signing secret, which should be used for the `SLACK_TOKEN` and `SLACK_SIGNING_SECRET` environment variables, respectively. You'll also need to set `SLACK_TEAM_ID` to the team ID of your Slack workspace.

Finally, you'll need to set `INCIDENT_BOT_ID` and `INCIDENT_BOT_NAME` to your bot's ID and public name; and `INCIDENT_CHANNEL_NAME` and `INCIDENT_REPORT_CHANNEL_NAME` to the central channel that you want to report all incidents to (e.g. `opg-incident`).

If you restart ngrok, it will generate a new public URL and you'll have to reconfigure the Slack app to reference that.

### Configuring additional integrations

#### GitHub signin

GitHub signin is turned off in dev mode, but you can enable it by enabling the `RESPONSE_LOGIN_REQUIRED` setting in `dev.py`.

To connect to GitHub, you'll need to create a GitHub OAuth App and set the environment variables `SOCIAL_AUTH_GITHUB_KEY` and `SOCIAL_AUTH_GITHUB_SECRET` to its the app's key and secret respectively. There is already an app called "opg-response-development" which is set up in the ministryofjustice organization for local development.

#### Statuspage

As with Slack, local development shouldn't interfere with our real Statuspage so you'll need to set up your own account. You should then set `STATUSPAGEIO_API_KEY` to [your API key](#statuspage-api-key) and `STATUSPAGEIO_PAGE_ID` to your team ID.

### Environment variables

| Variable                     | Real value required?           | Details                                                                                             |
| ---------------------------- | ------------------------------ | --------------------------------------------------------------------------------------------------- |
| SECRET_KEY                   | Yes                            | Used by Django, can be set to anything                                                              |
| DJANGO_SETTINGS_MODULE       | Yes                            | Specifies which settings to use. Should be `opgincidentresponse.settings.dev` in local environments |
| SOCIAL*AUTH*\*               | Only if testing authentication | There's already a dev/localhost and production GitHub app you can use                               |
| SLACK_TOKEN                  | Yes                            | Provided when you create a Slack app                                                                |
| SLACK_SIGNING_SECRET         | Yes                            | Provided when you create a Slack app                                                                |
| SLACK_TEAM_ID                | Yes                            | You should test in a private team, not MOJD&T                                                       |
| INCIDENT_BOT_ID              | Yes                            | The ID of your test app                                                                             |
| INCIDENT_BOT_NAME            | Yes                            | The name of your test app                                                                           |
| INCIDENT_CHANNEL_NAME        | Yes                            | The channel to post new live incidents to                                                           |
| INCIDENT_REPORT_CHANNEL_NAME | Yes                            | The channel to post new incident reports to                                                         |
| STATUSPAGEIO_API_KEY         | Only if testing Statuspage     | Provided by Statuspage                                                                              |
| STATUSPAGEIO_PAGE_ID         | Only if testing Statuspage     | Provided by Statuspage                                                                              |
| PAGERDUTY_API_KEY            | Only if testing PagerDuty      | Provided by Pagerduty                                                                               |
| PAGERDUTY_EMAIL              | Only if testing PagerDuty      | Provided by Pagerduty                                                                               |
| PAGERDUTY_SERVICE            | Only if testing PagerDuty      | Provided by Pagerduty                                                                               |

## Resources

### django-createsuperuser

[https://docs.djangoproject.com/en/3.1/ref/django-admin/#createsuperuser](https://docs.djangoproject.com/en/3.1/ref/django-admin/#createsuperuser)

### slack-create

[https://slack.com/get-started#/create](https://slack.com/get-started#/create)

### slack-app-create

[https://github.com/monzo/response/blob/master/docs/slack_app_create.md](https://github.com/monzo/response/blob/master/docs/slack_app_create.md)

### slack-app-config

[https://github.com/monzo/response/blob/master/docs/slack_app_config.md](https://github.com/monzo/response/blob/master/docs/slack_app_config.md)

### statuspage-api-key

[https://support.atlassian.com/statuspage/docs/create-and-manage-api-keys/](https://support.atlassian.com/statuspage/docs/create-and-manage-api-keys/)
