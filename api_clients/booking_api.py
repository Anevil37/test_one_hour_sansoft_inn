import json

import httpx

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
    def create_booking(self, data: json) -> httpx.Response:
        """
        POST /booking/ \n
        :param data: data for create booking.
        :return: json data.
        """
        return httpx.post(f"{self.url}/", headers=self.headers, json=data)

    @log
    def get_booking_tenant(self) -> httpx.Response:
        """
        GET /booking/tenant/ \n
        :return: json data.
        """
        return httpx.get(f"{self.url}/tenant/", headers=self.headers)

    @log
    def get_bookings_for_owner(self) -> httpx.Response:
        """
        GET /booking/owner/ \n
        :return: json data.
        """
        return httpx.get(f"{self.url}/owner/", headers=self.headers)

    @log
    def delete_booking(self, id_: str) -> httpx.Response:
        """
        DELETE /booking/ \n
        :param id_: booking id.
        :return: json data.
        """
        return httpx.delete(f"{self.url}/", headers=self.headers, params={"id": id_})
