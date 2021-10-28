import requests
import yaml

from eth_account.messages import encode_defunct
from datetime import datetime, timedelta
from web3.auto import w3

with open('secrets.yaml') as f:
    accounts = yaml.safe_load(f)

headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
    "Authorization": ""}


def get_random_message():
    body = {"operationName": "CreateRandomMessage", "variables": {}, "query": "mutation CreateRandomMessage {\n  createRandomMessage\n}\n"}

    response = requests.post("https://axieinfinity.com/graphql-server-v2/graphql", headers=headers, json=body)

    if response.status_code != 200:
        print(response.text)

    if response.status_code == 200:
        return response.json()['data']['createRandomMessage']


def get_signed_message(random_message, private_key):
    message = encode_defunct(text=random_message)
    message_signed = w3.eth.account.sign_message(message, private_key=private_key)
    return message_signed['signature'].hex()


def get_access_token(address, private_key):
    random_message = get_random_message()
    signed_message = get_signed_message(random_message, private_key)

    payload = {
        "operationName": "CreateAccessTokenWithSignature",
        "variables": {
            "input": {
                "mainnet": "ronin",
                "owner": f"{address}",
                "message": f"{random_message}",
                "signature": f"{signed_message}"
            }
        },
        "query": "mutation CreateAccessTokenWithSignature($input: SignatureInput!) {    createAccessTokenWithSignature(input: $input) {      newAccount      result      accessToken      __typename    }  }  "
    }

    response = requests.post("https://axieinfinity.com/graphql-server-v2/graphql", headers=headers, json=payload)

    if response.status_code != 200:
        print(response.text)

    if response.status_code == 200:
        return response.json()['data']['createAccessTokenWithSignature']['accessToken']


def get_unclaimed_slp(address):
    response = requests.get(f"https://game-api.skymavis.com/game-api/clients/{address}/items/1", headers=headers, data="")

    if response.status_code == 200:
        result = response.json()
        last_claimed_date = datetime.utcfromtimestamp(result["last_claimed_item_at"])
        claimable_slp = result["total"]
    else:
        print(response.text)

    if datetime.utcnow() + timedelta(days=-14) < last_claimed_date:
        claimable_slp = 0

    return claimable_slp


def get_profile(address):
    response = requests.get(f"https://game-api.axie.technology/api/v1/{address}", headers=headers, json="")

    profile = response.json()
    profile['last_claim'] = datetime.fromtimestamp(profile['last_claim'])
    profile['next_claim'] = datetime.fromtimestamp(profile['next_claim'])

    return profile


def get_remaining_energy(address, access_token):
    headers['Authorization'] = f"Bearer {access_token}"

    response = requests.get(f"https://game-api.axie.technology/player/{address}", headers=headers)
    energy_stats = response.json()

    return energy_stats

def get_daily_mission(address, access_token):
    headers['Authorization'] = f"Bearer {access_token}"

    response = requests.get(f"https://game-api.axie.technology/missions/{address}", headers=headers)
    daily_mission = response.json()

    return daily_mission