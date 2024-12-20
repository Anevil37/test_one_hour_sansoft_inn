import pytest

from api_clients.space_api import SpaceApi
from factories.space_factory import SpaceFactory
from utils.utils import check_status_code


class TestSpace:
    @pytest.fixture(autouse=True)
    def setup(self, config):
        self.config = config
        self.space_api = SpaceApi(config=self.config)
        self.space = SpaceFactory(config=self.config)

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
        data: dict = self.space.default_data
        response = self.space_api.create_space(data=data)
        check_status_code(request=response, exp_code=200)

        assert (
            response.json().get("name") == data["name"]
        ), f"Unexpected response name: {response.json()}"

    def test_create_space_validation_error(self):
        response = self.space_api.create_space(data={"test": "test"})
        check_status_code(request=response, exp_code=422)

    # GET /space/
    @pytest.mark.parametrize(
        "param", ["", "id", "available_from", "available_to", "city", "type", "country"]
    )
    def test_get_space(self, param):
        resp_value = self.space_api.create_space(data=self.space.default_data).json().get(param)

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

        check_status_code(request=response, exp_code=200)
        assert len(response.json()) != 0, f"Space not found. Actual response: {response.json()}"

    def test_get_spaces_with_all_params(self):
        space_data = self.space_api.create_space(data=self.space.default_data).json()
        response = self.space_api.get_space(
            id_=space_data.get("id"),
            available_from=space_data.get("available_from"),
            available_to=space_data.get("available_to"),
            city=space_data.get("city"),
            type_=space_data.get("type"),
            country=space_data.get("country"),
        )

        check_status_code(request=response, exp_code=200)
        assert len(response.json()) != 0, f"Space not found. Actual response: {response.json()}"

    def test_get_spaces_with_incorrect_param_value(self):
        space_city = self.space_api.create_space(data=self.space.default_data).json().get("city")
        response = self.space_api.get_space(city=space_city + self.space.guid)

        check_status_code(request=response, exp_code=200)
        assert len(response.json()) == 0, f"Len response is incorrect: {response.json()}!"

    # DELETE /space/
    def test_delete_space(self):
        space_id = self.space_api.create_space(data=self.space.default_data).json().get("id")
        del_response = self.space_api.delete_space(id_=space_id)
        get_response = self.space_api.get_space(id_=space_id)

        check_status_code(request=del_response, exp_code=200)
        assert (
            del_response.json().get("detail") == "Successfully deleted"
        ), f"Incorrect response: {del_response.json()}!"
        assert (
            len(get_response.json()) == 0
        ), f"Len GET response is incorrect: {get_response.json()}!"

    def test_delete_space_already_deleted(self):
        space_id = self.space_api.create_space(data=self.space.default_data).json().get("id")
        self.space_api.delete_space(id_=space_id)
        del_response = self.space_api.delete_space(id_=space_id)

        check_status_code(request=del_response, exp_code=400)

    def test_delete_space_id_not_found(self):
        del_response = self.space_api.delete_space(id_=self.space.default_data.get("id"))

        check_status_code(request=del_response, exp_code=400)

    # GET /space/owner/
    def test_get_spaces_owner(self):
        self.space_api.create_space(data=self.space.default_data).json()
        response = self.space_api.get_space_owner()

        check_status_code(request=response, exp_code=200)
        assert len(response.json()) != 0, f"Space not found. Actual response: {response.json()}"

    # GET /space/filter/
    def test_get_spaces_filter(self):
        space_data = self.space.default_data
        self.space_api.create_space(data=space_data).json()
        response = self.space_api.get_space_filter()

        check_status_code(request=response, exp_code=200)

        kok = response.json().get("cities")

        assert space_data["city"] in response.json().get("cities")
        assert space_data["type"] in response.json().get(
            "types"
        ), f"City: {space_data['city']} and type: {space_data['type']} not found in filter: {response.json()}!"
