# OPG Incident Response ⚡

OPG Incident Response is a Django app based on [Monzo's Response tool](https://github.com/monzo/response), with some additional integrations with tools we use and a reskin to meet GOV.UK design standards.

## Local Development

To start the application locally, copy `env.dev.example` to `.env` and configure the environment variables inside. All environment variables need to be set, but some can be set to nonsense values (i.e. `ENV_VAR=...`) as detailed in the table below.

You will need to configure a Slack app following the instructions below, and can then start the application with `docker-compose up -d`.

Note if you are using ngrok, they have now introduced auth tokens so you'll need to add one to the `ngrok.yml` in the ngrok container

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
