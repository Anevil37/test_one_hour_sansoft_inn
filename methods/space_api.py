import json

import requests

from utils.logger.log import log


class SpaceApi:
    def __init__(self, config):
        self.config = config
        self.headers = {
            "Authorization": f"Bearer {self.config['token']}",
            "Content-Type": "application/json",
            "Connection": "keep-alive",
            "Accept": "application/json",
        }

        self.url = self.config["url"] + "/space"

    @log
    def get_space(
        self,
        id_: str = None,
        available_from: str = None,
        available_to: str = None,
        city: str = None,
        type_: str = None,
        country: str = None,
        limit: int = None,
        offset: int = None,
    ) -> requests.Response:
        """
        GET /space/ \n
        :return: json data.
        """
        with requests.get(
            f"{self.url}/",
            headers=self.headers,
            params={
                "id": id_,
                "available_from": available_from,
                "available_to": available_to,
                "city": city,
                "type": type_,
                "country": country,
                "limit": limit,
                "offset": offset,
            },
        ) as response:
            return response

    @log
    def get_space_filter(self) -> requests.Response:
        """
        GET /space/filter/ \n
        :return: json data.
        """
        with requests.get(f"{self.url}/filter/", headers=self.headers) as response:
            return response

    @log
    def create_space(self, data: json) -> requests.Response:
        """
        POST /space/ \n
        :param data: data for create space.
        :return: json data.
        """
        with requests.post(f"{self.url}/", headers=self.headers, json=data) as response:
            return response

    @log
    def delete_space(self, id_: str) -> requests.Response:
        """
        DELETE /space/ \n
        :param id_: space id.
        :return: json data.
        """
        with requests.delete(f"{self.url}/", headers=self.headers, params={"id": id_}) as response:
            return response

    @log
    def get_space_owner(self, limit: int = None, offset: int = None) -> requests.Response:
        """
        GET /space/owner \n
        :return: json data.
        """
        with requests.get(
            f"{self.url}/owner/", headers=self.headers, params={"limit": limit, "offset": offset}
        ) as response:
            return response
