import json

import httpx

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
    ) -> httpx.Response:
        """
        GET /space/ \n
        :return: json data.
        """
        params = {
            "id": id_,
            "available_from": available_from,
            "available_to": available_to,
            "city": city,
            "type": type_,
            "country": country,
            "limit": limit,
            "offset": offset,
        }
        params = {key: value for key, value in params.items() if value}

        resp = httpx.get(
            f"{self.url}/",
            headers=self.headers,
            params=params,
        )

        return resp

    @log
    def get_space_filter(self) -> httpx.Response:
        """
        GET /space/filter/ \n
        :return: json data.
        """
        return httpx.get(f"{self.url}/filter/", headers=self.headers)

    @log
    def create_space(self, data: json) -> httpx.Response:
        """
        POST /space/ \n
        :param data: data for create space.
        :return: json data.
        """
        return httpx.post(f"{self.url}/", headers=self.headers, json=data)

    @log
    def delete_space(self, id_: str) -> httpx.Response:
        """
        DELETE /space/ \n
        :param id_: space id.
        :return: json data.
        """
        return httpx.delete(f"{self.url}/", headers=self.headers, params={"id": id_})

    @log
    def get_space_owner(self, limit: int = None, offset: int = None) -> httpx.Response:
        """
        GET /space/owner \n
        :return: json data.
        """
        params = {"limit": limit, "offset": offset}
        params = {key: value for key, value in params.items() if value}

        return httpx.get(f"{self.url}/owner/", headers=self.headers, params=params)
