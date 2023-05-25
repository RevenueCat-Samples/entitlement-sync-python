# entitlement-sync-python

Sample app + SDK for entitlement sync via webhooks and RevenueCat API

# Quickstart

### Prerequisites

* Python 3
* pipenv
* Network tunnel to consume webhooks on your dev machine
* Mobile app that allows IAP
* RevenueCat account w/ Admin dashboard access

## Steps to install & run

1. Clone this repository & `cd` into it
2. [Install pipenv](https://pipenv.pypa.io/en/latest/installation/):  `pip install --user pipenv`
3. `pipenv install` to install this project's dependencies
4. Launch your network tunnel and point it to `localhost:8080`
5. Copy `example-config.json` to `config.json` and add the values from
   your [RevenueCat dashboard](https://app.revenuecat.com/)
    1. Create a webhook and set the Authorization header value, which must be prefixed with `Bearer `
    2. Generate a V1 API *secret* key
    3. Get your project ID from the URL by
        1. Clicking the `Projects` dropdown, then select your preferred project
        2. Copy the ID from the URL: `/projects/{PROJECT ID}/apps`
6. `python3 main.py`
    1. You should see `Listening on http://localhost:8080` in the console
7. Try out a test webhook in the dashboard!
    1. `https://app.revenuecat.com/projects/{PROJECT ID}/integrations/webhooks`
