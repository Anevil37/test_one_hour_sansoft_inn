import json

import requests

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
    def sign_in(self, data: json) -> requests.Response:
        """
        POST /sign-in \n
        :param data: data for sign in.
        :return: json data.
        """
        with requests.put(f"{self.url}/sign-in/", headers=self.headers, json=data) as response:
            return response

    @log
    def sign_up(self, data: json) -> requests.Response:
        """
        POST /sign-up \n
        :param data: data for sign up.
        :return: json data.
        """
        with requests.post(f"{self.url}/sign-up/", headers=self.headers, json=data) as response:
            return response

    @log
    def logout(self, data: json) -> requests.Response:
        """
        POST /sign-up \n
        :param data: data for sign up.
        :return: json data.
        """
        with requests.put(f"{self.url}/logout/", headers=self.headers, json=data) as response:
            return response
