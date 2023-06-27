import json

import httpx

from utils.logger.log import log


class ClientApi:
    def __init__(self, config):
        self.config = config
        self.headers = {
            "Content-Type": "application/json",
            "Connection": "keep-alive",
            "Accept": "application/json",
        }
        self.url = self.config["url"] + "/client"

    @log
    def sign_in(self, data: json) -> httpx.Response:
        """
        POST /sign-in \n
        :param data: data for sign in.
        :return: json data.
        """
        return httpx.put(f"{self.url}/sign-in/", headers=self.headers, json=data)

    @log
    def sign_up(self, data: json) -> httpx.Response:
        """
        POST /sign-up \n
        :param data: data for sign up.
        :return: json data.
        """
        return httpx.post(f"{self.url}/sign-up/", headers=self.headers, json=data)

    @log
    def logout(self, data: json) -> httpx.Response:
        """
        POST /sign-up \n
        :param data: data for sign up.
        :return: json data.
        """
        return httpx.put(f"{self.url}/logout/", headers=self.headers, json=data)
