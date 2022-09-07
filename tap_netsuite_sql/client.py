# import requests
import os
import json
from requests_oauthlib import OAuth1Session


class Client:
    def __init__(self, config):
        self._account_id = str(
            config.get("account_id") or os.environ.get("TAP_NETSUITE_ACCOUNT")
        )

        self._oauth = OAuth1Session(
            client_key=config.get("consumer_key")
            or os.environ.get("TAP_NETSUITE_CONSUMER_KEY"),
            client_secret=config.get("consumer_secret")
            or os.environ.get("TAP_NETSUITE_CONSUMER_SECRET"),
            resource_owner_key=config.get("token_key")
            or os.environ.get("TAP_NETSUITE_TOKEN_KEY"),
            resource_owner_secret=config.get("token_secret")
            or os.environ.get("TAP_NETSUITE_TOKEN_SECRET"),
            realm=self._account_id,
            signature_method="HMAC-SHA256",
        )

        self._headers = {"Content-Type": "application/json", "Prefer": "transient"}

    def send(self, query):
        payload = {"q": query}

        url = f"https://{self._account_id}.suitetalk.api.netsuite.com/services/rest/query/v1/suiteql"

        hasMore = True
        items = []

        while hasMore:
            resp = self._oauth.post(
                url, headers=self._headers, data=json.dumps(payload)
            )
            data = json.loads(resp.text)
            hasMore = data["hasMore"]
            url = next(
                iter([l["href"] for l in data["links"] if l["rel"] == "next"]), None
            )
            items += data["items"]

        return items
