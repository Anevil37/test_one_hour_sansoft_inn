import json

import requests

from utils.logger.log import log


class BookingApi:
    def __init__(self, config):
        self.config = config
        self.headers = {
            "Authorization": f"Bearer {self.config['token']}",
            "Content-Type": "application/json",
            "Connection": "keep-alive",
            "Accept": "application/json",
        }

        self.url = self.config["url"] + "/booking"

    @log
    def post_booking(self, data: json) -> requests.Response:
        """
        POST /booking/ \n
        :param data: data for create booking.
        :return: json data.
        """
        with requests.post(f"{self.url}/", headers=self.headers, json=data) as response:
            return response

    @log
    def get_booking_tenant(self) -> requests.Response:
        """
        GET /booking/tenant/ \n
        :return: json data.
        """
        with requests.get(f"{self.url}/tenant/", headers=self.headers) as response:
            return response

    @log
    def get_booking_owner(self) -> requests.Response:
        """
        GET /booking/owner/ \n
        :return: json data.
        """
        with requests.get(f"{self.url}/owner/", headers=self.headers) as response:
            return response

    @log
    def delete_booking(self, id_: str) -> requests.Response:
        """
        DELETE /booking/ \n
        :param id_: booking id.
        :return: json data.
        """
        with requests.delete(f"{self.url}/", headers=self.headers, params={"id": id_}) as response:
            return response
