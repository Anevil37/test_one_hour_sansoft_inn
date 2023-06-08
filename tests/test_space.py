import pytest

from generators.space_generator import SpaceGenerator
from methods.space_api import SpaceApi
from utils.utils import check_status_code


class TestSpace:
    @pytest.fixture(autouse=True)
    def setup(self, config):
        self.config = config
        self.space_api = SpaceApi(config=self.config)
        self.space = SpaceGenerator(config=self.config)

    def teardown(self):
        space = self.space_api.get_space(city=self.space.default_data.get("city"))
        if space.status_code == 200:
            try:
                space_id = space.json()[0].get("id")
                self.space_api.delete_space(id_=space_id)
            except IndexError:
                print("Nothing to delete.")

    # POST /space/create/
    def test_create_space(self):
        # Array
        data = self.space.default_data
        # Act
        response = self.space_api.post_space(data=data)
        # Assert
        check_status_code(request=response, exp_code=200)
        assert (
            response.json().get("name") == data["name"]
        ), f"Unexpected response name: {response.json()}"

    def test_create_space_validation_error(self):
        # Act
        response = self.space_api.post_space(data={"test": "test"})
        # Assert
        check_status_code(request=response, exp_code=422)

    # GET /space/
    @pytest.mark.parametrize(
        "param", ["", "id", "available_from", "available_to", "city", "type", "country"]
    )
    def test_get_space(self, param):
        # Array
        resp_value = self.space_api.post_space(data=self.space.default_data).json().get(param)
        # Act
        if param == "":
            response = self.space_api.get_space()
        elif param == "id":
            response = self.space_api.get_space(id_=resp_value)
        elif param == "available_from":
            response = self.space_api.get_space(available_from=resp_value)
        elif param == "available_to":
            response = self.space_api.get_space(available_to=resp_value)
        elif param == "city":
            response = self.space_api.get_space(city=resp_value)
        elif param == "type":
            response = self.space_api.get_space(type_=resp_value)
        elif param == "country":
            response = self.space_api.get_space(country=resp_value)
        else:
            raise Exception(f"Unexpected param: {param}!")
        # Assert
        check_status_code(request=response, exp_code=200)
        assert len(response.json()) != 0, f"Space not found. Actual response: {response.json()}"

    def test_get_spaces_with_all_params(self):
        # Array
        space_data = self.space_api.post_space(data=self.space.default_data).json()
        # Act
        response = self.space_api.get_space(
            id_=space_data.get("id"),
            available_from=space_data.get("available_from"),
            available_to=space_data.get("available_to"),
            city=space_data.get("city"),
            type_=space_data.get("type"),
            country=space_data.get("country"),
        )
        # Assert
        check_status_code(request=response, exp_code=200)
        assert len(response.json()) != 0, f"Space not found. Actual response: {response.json()}"

    def test_get_spaces_with_incorrect_param_value(self):
        # Array
        space_city = self.space_api.post_space(data=self.space.default_data).json().get("city")
        # Act
        response = self.space_api.get_space(city=space_city + self.space.guid)
        # Assert
        check_status_code(request=response, exp_code=200)
        assert len(response.json()) == 0, f"Len response is incorrect: {response.json()}!"

    # DELETE /space/
    def test_delete_space(self):
        # Array
        space_id = self.space_api.post_space(data=self.space.default_data).json().get("id")
        # Act
        del_response = self.space_api.delete_space(id_=space_id)
        get_response = self.space_api.get_space(id_=space_id)
        # Assert
        check_status_code(request=del_response, exp_code=200)
        assert (
            del_response.json().get("detail") == "Successfully deleted"
        ), f"Incorrect response: {del_response.json()}!"
        assert (
            len(get_response.json()) == 0
        ), f"Len GET response is incorrect: {get_response.json()}!"

    def test_delete_space_already_deleted(self):
        # Array
        space_id = self.space_api.post_space(data=self.space.default_data).json().get("id")
        self.space_api.delete_space(id_=space_id)
        # Act
        del_response = self.space_api.delete_space(id_=space_id)
        # Assert
        check_status_code(request=del_response, exp_code=400)

    def test_delete_space_id_not_found(self):
        # Act
        del_response = self.space_api.delete_space(id_=self.space.default_data.get("id"))
        # Assert
        check_status_code(request=del_response, exp_code=400)

    # GET /space/owner/
    def test_get_spaces_owner(self):
        # Array
        self.space_api.post_space(data=self.space.default_data).json()
        # Act
        response = self.space_api.get_space_owner()
        # Assert
        check_status_code(request=response, exp_code=200)
        assert len(response.json()) != 0, f"Space not found. Actual response: {response.json()}"

    # GET /space/filter/
    def test_get_spaces_filter(self):
        # Array
        space_data = self.space.default_data
        self.space_api.post_space(data=space_data).json()
        # Act
        response = self.space_api.get_space_filter()
        # Assert
        check_status_code(request=response, exp_code=200)
        assert space_data["city"] in response.json().get("cities") and space_data[
            "type"
        ] in response.json().get(
            "types"
        ), f"City: {space_data['city']} and type: {space_data['type']} not found in filter: {response.json()}!"
