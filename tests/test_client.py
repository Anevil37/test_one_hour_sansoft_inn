from random import randint

import pytest

from generators.login_generator import LoginGenerator
from generators.user_generator import UserGenerator
from methods.client_api import ClientApi
from utils.utils import check_status_code


class TestClient:
    @pytest.fixture(autouse=True)
    def setup(self, config):
        self.config = config
        self.client_api = ClientApi(config=self.config)
        self.user = UserGenerator()
        self.login = LoginGenerator(config=self.config)

    # POST /sing-up/
    def test_sing_up(self):
        test_data: dict = self.user.default_data
        response = self.client_api.sign_up(data=test_data)
        check_status_code(request=response, exp_code=200)

        assert (
            response.json().get("token") is not None
        ), f"Failed to get token! Actual body: {response.json()}"

    def test_sing_up_phone_already_exists(self):
        data = self.user.default_data
        self.client_api.sign_up(data=data)

        response = self.client_api.sign_up(data=data)
        check_status_code(request=response, exp_code=400)

        assert (
            response.json().get("detail") == "Phone already exists"
        ), f"Unexpected body: {response.json()}"

    def test_sing_up_validation_error(self):
        response = self.client_api.sign_up(data={"test": "test"})
        check_status_code(request=response, exp_code=422)

    # POST /sing-in/
    def test_sing_in(self):
        response = self.client_api.sign_in(data=self.login.default_data)
        check_status_code(request=response, exp_code=200)

        assert (
            response.json().get("token") is not None
        ), f"Failed to get token! Actual response: {response.json()}"

    def test_sing_in_incorrect_password(self):
        self.login.default_data.update(
            {"password": self.config["password"] + "test_sing_in_incorrect_password"}
        )

        data = self.login.default_data
        response = self.client_api.sign_in(data=data)
        check_status_code(request=response, exp_code=401)

        assert (
            response.json().get("detail") == "Bad credentials"
        ), f"Unexpected response: {response.json()}"

    def test_sing_empty_password(self):
        self.login.default_data.update({"password": ""})

        data = self.login.default_data
        response = self.client_api.sign_in(data=data)

        assert (
            response.json().get("detail") == "Bad credentials"
        ), f"Unexpected response: {response.json()}"

    def test_sing_in_nonexistent_user(self):
        self.login.default_data.update(
            {"phone_number": self.config["phone"] + str(randint(0, 500))}
        )
        data = self.login.default_data

        response = self.client_api.sign_in(data=data)
        check_status_code(request=response, exp_code=404)

        assert (
            response.json().get("detail") == "Phone is not registered"
        ), f"Unexpected response: {response.json()}"

    def test_sing_in_validation_error(self):
        response = self.client_api.sign_in(data={})
        check_status_code(request=response, exp_code=422)
