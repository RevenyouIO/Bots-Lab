####################################
# Facilitates accessing the BNF API
# Version: 0.0.1
# contact: marjan@revenyou.io
# (C) Bots by RevenYOU
####################################

import hashlib
import hmac
import json
import os

import requests


class BNF_API:
    """
    BNF API Wrapper
    """

    def __init__(self):
        self.host = "https://signal.revenyou.io/api/signal/v3"
        self.session = requests.Session()

        self.secret = os.environ.get("BOT_SECRET")

    def available_symbols(self):
        return self._make_request(endpoint="/symbols")

    def balance(self):
        return self._make_request(endpoint="/balance")

    def balance_in_bot_base_asset(self):
        return self._make_request(endpoint="/balance/total")

    def list_open_orders(self, params):
        return self._make_request(endpoint="/orders/list-open", params=params)

    def get_order_by_id(self, params):
        return self._make_request(endpoint="/orders/status", params=params)

    def create_order(self, data):
        return self._make_request(endpoint="/orders/place", data=data)

    def cancel_order(self, data):
        return self._make_request(endpoint="/orders/cancel", data=data)

    def borrow(self, data):
        return self._make_request(endpoint="/loans/borrow", data=data)

    def repay(self, data):
        return self._make_request(endpoint="/loans/repay", data=data)

    def _make_request(self, endpoint, params=None, data=None):
        if not params:
            params = {}
        if not data:
            data = {}

        if params:
            params["signature"] = self.sign_request(data)
        if data:
            data["signature"] = self.sign_request(data)

        endpoints = {
            "/symbols": self.session.get,

            "/balance": self.session.get,
            "/balance/total": self.session.get,

            "/orders/status": self.session.get,
            "/orders/list-open": self.session.get,
            "/orders/create": self.session.post,
            "/orders/cancel": self.session.post,

            "/loans/repay": self.session.post,
            "/loans/take": self.session.post,
        }

        response = endpoints[endpoint](
            url=f"{self.host}{endpoint}",
            params=params,
            data=json.dumps(data),
        )

        return response.json()

    def sign_request(self, data: dict):
        qs_data = "&".join([f"{k}={v}" for k, v in data.items()])

        return hmac.new(
            self.secret.encode(
                "utf-8"
            ),
            qs_data.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
