"""
Sample app to demonstrate the entire flow of keeping mobile entitlements up-to-date
with RevenueCat.

The primary goal for this sample code is to be easy to understand.

The only third-party dependencies required are:
- Bottle - lightweight WSGI framework for receiving HTTP webhooks from RevenueCat
- requests - make HTTP request to RevenueCat API
- certifi - keeps the TLS certificate bundles up to date
- pipenv - for installing the above dependencies
"""
import json
from datetime import datetime
from pprint import pprint
from sqlite3 import Connection, connect as db_connect

from bottle import Bottle, Response, request, run

from db_interface import db_create_ent_table, db_dict_factory, db_insert_entitlement, db_fetch_entitlements, \
    db_update_entitlement
from api_client import RevenueCatClient

# Define the WSGI web app globally so we can attach the /webhook endpoint
APP = Bottle()


def load_config():
    """Load variables from config.json. See README for details on how to acquire the values needed"""
    global CONFIG
    try:
        CONFIG = json.load(open('config.json', 'r'))
        # All of these values should be populated from the RevenueCat dashboard
        _required_config_vals = [
            # "API_SECRET_KEY_V2", # Don't need V2 for this sample yet
            "API_SECRET_KEY_V1",
            "RC_PROJECT_ID",
            "WEBHOOK_TOKEN"
        ]
        for _config_key in _required_config_vals:
            assert _config_key in CONFIG, f'{_config_key} missing from config.json'
    except FileNotFoundError:
        raise FileNotFoundError('No config file found in current directory.'
                                ' Please create one with your values based on example-config.json')


def sync_user_entitlements(client: RevenueCatClient, db_conn: Connection, app_user_id: str):
    """
    Sync user entitlements from RevenueCat into our local database.

    Can be called on-demand, but typically is triggered from a webhook for a given user.
    """
    response = client.get_subscriber(app_user_id)
    subscriber = response['subscriber']
    existing_ents = db_fetch_entitlements(db_conn, app_user_id)
    # Make existing entitlements easy to lookup while we iterate over server response
    ent_map = {row['entitlement']: row for row in existing_ents}
    # Ignorantly update all the entitlements without checking for changes.
    # In a more complex scenario, we probably want to calculate the difference between the up-to-date
    # entitlements/subscriptions from RevenueCat with what's in our database
    # You *always* want to  update the `last_sync` field, though.
    for ent_name, entitlement in subscriber['entitlements'].items():
        row = {
            'user_id': app_user_id,
            'entitlement': ent_name,
            'expiration': entitlement['expires_date'],
            'last_sync': datetime.utcnow().timestamp(),
            'source': 'revenuecat',
        }
        if ent_name in ent_map:
            # We already have this entitlement, so just update it
            db_update_entitlement(db_conn, row)
        else:
            # New entitlement we haven't seen before
            db_insert_entitlement(db_conn, row)


@APP.post('/webhook')
def webhook_endpoint() -> Response:
    """
    HTTP endpoint to handle requests from RevenueCat.
    We recommend you use an SSH tunnel for testing purposes on your local machine
    """
    # Authenticate the request coming from RevenueCat
    # This is 100% necessary for any production webhook server to:
    # 1. Help prevent getting (D)DoS'd
    # 2. Block attackers from sending crafted messages to exploit your server
    # 3. or to potentially corrupt the data you're storing (make it inaccurate, etc.)
    auth_header: str = request.headers.get('Authorization', '')
    auth_token = auth_header.split('Bearer ')
    if len(auth_token) != 2 or auth_token[1] != CONFIG['WEBHOOK_TOKEN']:
        print('Authorization error - ensure your webhook token matches what you configured in the dashboard.'
              'You need to specify "Bearer {YOUR_TOKEN}" in the dashboard')
        return Response(status=401)

    pprint(request.json)
    event = request.json['event']
    # NOTE: In production, you should process the webhook asynchronously
    sync_user_entitlements(APP.config['client'], APP.config['db_conn'], event['app_user_id'])
    print('Successfully processed webhook event')
    # Return a 200 so RevenueCat knows we were able to consume it
    return Response(status=200)


def main():
    load_config()
    # Making these global to keep the definitions here in main(), but still usable in
    db_conn = db_connect('entitlements.sqlite')
    db_conn.row_factory = db_dict_factory

    client = RevenueCatClient(CONFIG['API_SECRET_KEY_V1'], CONFIG['RC_PROJECT_ID'])
    # Add these to the Bottle request config so we can access them inside
    # our webhook endpoint
    APP.config['db_conn'] = db_conn
    APP.config['client'] = client
    db_create_ent_table(db_conn)
    # Blocking call to host the webserver to consume webhooks from RevenueCat
    # See webhook_endpoint(..) for rest of program flow
    run(APP, host='localhost', port=8080, debug=True)


if __name__ == '__main__':
    main()
