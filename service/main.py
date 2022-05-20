import os
import json
import googlemaps
from fastapi import FastAPI
from cxwebhooks import WebhookRequest, WebhookResponse

# Webhook.site [TESTING]: https://webhook.site/#!/de2a6e79-94bc-43bf-b571-5affeaf4f2ca
# Webhook.site [TESTING] - Endpoint: https://webhook.site/de2a6e79-94bc-43bf-b571-5affeaf4f2ca

# https://googlemaps.github.io/google-maps-services-python/docs/index.html

API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY')
gmaps = googlemaps.Client(key=API_KEY)

app = FastAPI()

def staging(path_fn):
    async def call(webhook: WebhookRequest, 
        response=None, params=None):
        response = WebhookResponse()
        params = webhook.sessionInfo.parameters
        return await path_fn(webhook,
            response=response, params=params)
    return call

@app.post("/verify-address")
@staging
async def verify_address(webhook: WebhookRequest,
    response=..., params=...):
    query = params.get('provided_address', {}).get('original')
    street_address = params.get('provided_address', {}).get('street-address')
    resp = gmaps.places(query=query)
    place = resp['results'][0]
    formatted_address = place.get('formatted_address')
    response.add_text_response(f'Your validated address is: {formatted_address}.  Is that correct?')
    response.add_session_params({
        'types': place.get('types'),
        'place_id': place.get('place_id'),
        'formatted_address': formatted_address,
        'street_address': street_address,
        'query': query,
        'gmaps_result': place
    })
    return response

@app.post("/verify-address-with-zip-code")
@staging
async def verify_address_with_zip_code(webhook: WebhookRequest,
    response=..., params=...):
    street_address = params.get('provided_address', {}).get('street-address')
    formatted_address = params.get('formatted_address')
    zip_code = params.get('zip_code')
    query = f'{street_address}, {zip_code}'
    resp = gmaps.places(query=query)
    place = resp['results'][0]
    new_formatted_address = place.get('formatted_address')
    if new_formatted_address == formatted_address:
        response.add_text_response("Uh oh, that really didn't help... sorry!")
    else:
        response.add_text_response(f'Your validated address is: {new_formatted_address}.  Is that correct?')
        response.add_session_params({
            'types': place.get('types'),
            'place_id': place.get('place_id'),
            'formatted_address': new_formatted_address,
            'query': query,
            'gmaps_result': place
        })
    return response