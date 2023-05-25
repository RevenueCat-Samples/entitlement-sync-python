# Overview

Sample app to demonstrate the entire flow of keeping mobile entitlements up-to-date
with RevenueCat.

The primary goal for this sample code is to be easy to understand and get setup with minimal dependencies.

The only third-party dependencies required are:
- `Bottle` - lightweight WSGI framework for receiving HTTP webhooks from RevenueCat
- `requests` - make HTTP request to RevenueCat API
- `certifi` - keeps the TLS certificate bundles up to date

The example uses sqlite so that the database can be created automatically, and should work wherever you can run Python code.
Versions of the dependencies shouldn't matter since we're only using some of the most basic functionality.

### Files
* `main.py` - Entry point for program and where all business logic takes place
* `api_client.py` - HTTP client interface to fetch from the RevenueCat API
* `db_interface.py` - Simple functions for interacting with the database using raw SQL
* `example-config.json` - Template for config. More details in quickstart steps.

# Quickstart

### Prerequisites

* Python 3
* pipenv _(optional)_
* Network tunnel to consume webhooks on your dev machine
* Mobile app that allows IAP
* RevenueCat account w/ Admin dashboard access

## Steps to install & run

* Clone this repository & `cd` into it
* Install _without_ `pipenv`:
   1. `pip install -r requirements.txt`
* **OR** Install _with_ `pipenv` 
   1. [Install pipenv](https://pipenv.pypa.io/en/latest/installation/):  `pip install --user pipenv`
   2. `pipenv install` to install this project's dependencies
* If running locally on your own computer, launch your network tunnel and point it to `localhost:8080`
* Copy `example-config.json` to `config.json` and add the values from
   your [RevenueCat dashboard](https://app.revenuecat.com/)
    1. Create a webhook and set the Authorization header value, which must be prefixed with `Bearer `
    2. Generate a V1 API *secret* key
    3. Get your project ID from the URL by
        1. Clicking the `Projects` dropdown, then select your preferred project
        2. Copy the ID from the URL: `/projects/{PROJECT ID}/apps`
* `python3 main.py`
    1. You should see `Listening on http://localhost:8080` in the console, which means your webhook server is up and listening for webhooks from RevenueCat
* Try out a test webhook in the dashboard!
    1. `https://app.revenuecat.com/projects/{PROJECT ID}/integrations/webhooks`


# Architecture
This diagram illustrates how the flow originates with RevenueCat webhooks, then moves through this sample app. 

The TLS tunnel is optional, but typically the easiest way (vs port forwarding, etc.) to get HTTP requests to your `localhost`. If you're running this behind a server that can already accept HTTP requests over the web, then you can skip this entirely. 



<img src="https://github.com/RevenueCat-Samples/entitlement-sync-python/assets/2552485/fff42d7b-91c3-4222-80bf-a3b336f33f89" width="500px">



