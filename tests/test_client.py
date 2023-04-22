from random import randint

import pytest

from generators.login_generator import LoginGenerator
from generators.user_generator import UserGenerator
from methods.client_api import ClientApi
from utils.utils import check_status_code


class TestSingIn:

    @pytest.fixture(autouse=True)
    def setup(self, config):
        self.config = config
        self.client_api = ClientApi(config=self.config)
        self.user = UserGenerator()
        self.login = LoginGenerator(config=self.config)

    # POST /sing-up/
    def test_sing_up(self):
        # Array
        test_data = self.user.default_data
        # Act
        response = self.client_api.post_sign_up(data=test_data)
        # Assert
        check_status_code(request=response, exp_code=200)
        assert response.json().get('token') is not None, f"Failed to get token! Actual body: {response.json()}"

    def test_sing_up_phone_already_exists(self):
        # Array
        data = self.user.default_data
        self.client_api.post_sign_up(data=data)
        # Act
        response = self.client_api.post_sign_up(data=data)
        # Assert
        check_status_code(request=response, exp_code=400)
        assert response.json().get('detail') == 'Phone already exists', f"Unexpected body: {response.json()}"

    def test_sing_up_validation_error(self):
        # Act
        response = self.client_api.post_sign_up(data={"test": "test"})
        # Assert
        check_status_code(request=response, exp_code=422)

    # POST /sing-in/
    def test_sing_in(self):
        # Act
        response = self.client_api.post_sign_in(data=self.login.default_data)
        # Assert
        check_status_code(request=response, exp_code=200)
        assert response.json().get('token') is not None, f"Failed to get token! Actual response: {response.json()}"

    def test_sing_in_incorrect_password(self):
        # Array
        self.login.default_data.update({"password": self.config['password'] + "test_sing_in_incorrect_password"})
        data = self.login.default_data
        # Act
        response = self.client_api.post_sign_in(data=data)
        # Assert
        check_status_code(request=response, exp_code=401)
        assert response.json().get('detail') == "Bad credentials", f"Unexpected response: {response.json()}"

    def test_sing_empty_password(self):
        # Array
        self.login.default_data.update({"password": ""})
        data = self.login.default_data
        # Act
        response = self.client_api.post_sign_in(data=data)
        # Assert
        check_status_code(request=response, exp_code=401)
        assert response.json().get('detail') == "Bad credentials", f"Unexpected response: {response.json()}"

    def test_sing_in_nonexistent_user(self):
        # Array
        self.login.default_data.update({"phone_number": self.config['phone'] + str(randint(0, 500))})
        data = self.login.default_data
        # Act
        response = self.client_api.post_sign_in(data=data)
        # Assert
        check_status_code(request=response, exp_code=404)
        assert response.json().get('detail') == "Phone is not registered", f"Unexpected response: {response.json()}"

    def test_sing_in_validation_error(self):
        # Act
        response = self.client_api.post_sign_in(data={})
        # Assert
        check_status_code(request=response, exp_code=422)
