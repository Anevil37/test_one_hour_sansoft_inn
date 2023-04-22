import pytest

from methods.booking_api import BookingApi
from methods.space_api import SpaceApi
from generators.booking_generator import BookingGenerator
from generators.space_generator import SpaceGenerator
from utils.utils import check_status_code


class TestBooking:

    @pytest.fixture(autouse=True)
    def setup(self, config):
        self.config = config
        self.booking_api = BookingApi(config=self.config)
        self.space_api = SpaceApi(config=self.config)
        self.space = SpaceGenerator(config=self.config)
        self.space_id = self.space_api.post_space(data=self.space.default_data).json().get('id')

    def teardown(self):
        booking = self.booking_api.get_booking_owner()
        if booking.status_code == 200:
            if len(booking.json()) != 0:
                for book in booking.json():
                    self.booking_api.delete_booking(id_=book.get('id'))
            else:
                print('Nothing to delete for bookings.')
        space = self.space_api.get_space(city=self.space.default_data.get('city'))
        if space.status_code == 200:
            try:
                space_id = space.json()[0].get('id')
                self.space_api.delete_space(id_=space_id)
            except IndexError:
                print('Nothing to delete for spaces.')

    # POST /booking/
    def test_create_booking(self):
        # Array
        data = BookingGenerator(space_id=self.space_id).default_data
        # Act
        response = self.booking_api.post_booking(data=data)
        cost = response.json().get('cost')
        booking_id = response.json().get('id')
        # Assert
        check_status_code(request=response, exp_code=200)
        assert cost != 0, f"Unexpected cost for booking: {response.json()}!"
        assert booking_id is not None, f"Booking id not found: {booking_id}!"

    def test_create_booking_datetime_zero(self):
        # Array
        date_now = BookingGenerator().date_now
        data = BookingGenerator(
            space_id=self.space_id,
            datetime_from=date_now,
            datetime_to=date_now
        ).default_data
        # Act
        response = self.booking_api.post_booking(data=data)
        # Assert
        check_status_code(request=response, exp_code=400)
        assert response.json().get('detail') == 'Book time must be greater then 0', \
            f"Incorrect response: {response.json()}!"

    def test_create_booking_datetime_in_future_not_available_date(self):
        # Array
        date_now = BookingGenerator().date_now.replace("2023", "2050")
        data = BookingGenerator(
            space_id=self.space_id,
            datetime_to=date_now
        ).default_data
        # Act
        response = self.booking_api.post_booking(data=data)
        # Assert
        check_status_code(request=response, exp_code=400)
        assert response.json().get('detail') == 'Book date is out of space available dates', \
            f"Incorrect response: {response.json()}!"

    @pytest.mark.skip(reason='BUG')
    def test_create_booking_datetime_in_past_not_available_date(self):
        # Array
        date_now = BookingGenerator().date_now.replace("2023", "2010")
        data = BookingGenerator(
            space_id=self.space_id,
            datetime_to=date_now
        ).default_data
        # Act
        response = self.booking_api.post_booking(data=data)
        # Assert
        check_status_code(request=response, exp_code=400)
        assert response.json().get('detail') == 'Book date is out of space available dates', \
            f"Incorrect response: {response.json()}!"

    def test_create_booking_validation_error(self):
        # Act
        response = self.booking_api.post_booking(data={"test":"test"})
        # Assert
        check_status_code(request=response, exp_code=422)

    # GET /booking/owner/
    def test_get_booking_owner(self):
        # Array
        booking_id = self.booking_api.post_booking(
            data=BookingGenerator(space_id=self.space_id).default_data
        ).json().get('id')
        # Act
        response = self.booking_api.get_booking_owner()
        # Assert
        check_status_code(request=response, exp_code=200)
        booking_ids = []
        for booking in response.json():
            if booking.get('id'):
                booking_ids.append(booking.get('id'))
        assert booking_id in booking_ids, f"Booking for owner not found in {response.json()}!"

    def test_get_booking_owner_after_delete_space(self):
        # Array
        booking_id = self.booking_api.post_booking(
            data=BookingGenerator(space_id=self.space_id).default_data
        ).json().get('id')
        self.space_api.delete_space(id_=self.space_id)
        # Act
        response = self.booking_api.get_booking_owner()
        # Assert
        check_status_code(request=response, exp_code=200)
        booking_ids = []
        for booking in response.json():
            if booking.get('id'):
                booking_ids.append(booking.get('id'))
        assert booking_id not in booking_ids, f"Booking: {booking_id} found after delete for owner!"

    def test_get_booking_owner_after_delete_book(self):
        # Array
        booking_id = self.booking_api.post_booking(
            data=BookingGenerator(space_id=self.space_id).default_data
        ).json().get('id')
        self.booking_api.delete_booking(id_=booking_id)
        # Act
        response = self.booking_api.get_booking_owner()
        # Assert
        check_status_code(request=response, exp_code=200)
        booking_ids = []
        for booking in response.json():
            if booking.get('id'):
                booking_ids.append(booking.get('id'))
        assert booking_id not in booking_ids, f"Booking: {booking_id} found after delete for owner!"

    # GET /booking/tenant/
    def test_get_booking_tenant(self):
        # Array
        booking_id = self.booking_api.post_booking(
            data=BookingGenerator(space_id=self.space_id).default_data
        ).json().get('id')
        # Act
        response = self.booking_api.get_booking_tenant()
        # Assert
        check_status_code(request=response, exp_code=200)
        booking_ids = []
        for booking in response.json():
            if booking.get('id'):
                booking_ids.append(booking.get('id'))
        assert booking_id in booking_ids, f"Booking for tenant not found in {response.json()}!"

    def test_get_booking_tenant_after_delete_space(self):
        # Array
        booking_id = self.booking_api.post_booking(
            data=BookingGenerator(space_id=self.space_id).default_data
        ).json().get('id')
        self.space_api.delete_space(id_=self.space_id)
        # Act
        response = self.booking_api.get_booking_tenant()
        # Assert
        check_status_code(request=response, exp_code=200)
        booking_ids = []
        for booking in response.json():
            if booking.get('id'):
                booking_ids.append(booking.get('id'))
        assert booking_id not in booking_ids, f"Booking: {booking_id} found after delete for tenant!"

    def test_get_booking_tenant_after_delete_book(self):
        # Array
        booking_id = self.booking_api.post_booking(
            data=BookingGenerator(space_id=self.space_id).default_data
        ).json().get('id')
        self.booking_api.delete_booking(id_=booking_id)
        # Act
        response = self.booking_api.get_booking_tenant()
        # Assert
        check_status_code(request=response, exp_code=200)
        booking_ids = []
        for booking in response.json():
            if booking.get('id'):
                booking_ids.append(booking.get('id'))
        assert booking_id not in booking_ids, f"Booking: {booking_id} found after delete for tenant!"

    # DELETE /booking/
    def test_delete_booking(self):
        # Array
        booking_id = self.booking_api.post_booking(
            data=BookingGenerator(space_id=self.space_id).default_data
        ).json().get('id')
        # Act
        response = self.booking_api.delete_booking(id_=booking_id)
        # Assert
        check_status_code(request=response, exp_code=200)
        assert response.json().get('detail') == "Successfully deleted", f"Incorrect response: {response.json()}!"

    def test_delete_booking_already_deleted(self):
        # Array
        booking_id = self.booking_api.post_booking(
            data=BookingGenerator(space_id=self.space_id).default_data
        ).json().get('id')
        self.booking_api.delete_booking(id_=booking_id)
        # Act
        response = self.booking_api.delete_booking(id_=booking_id)
        # Assert
        check_status_code(request=response, exp_code=400)

    def test_delete_booking_id_not_found(self):
        # Array
        booking_id = self.space.default_data['id']
        self.booking_api.delete_booking(id_=booking_id)
        # Act
        response = self.booking_api.delete_booking(id_=booking_id)
        # Assert
        check_status_code(request=response, exp_code=400)
        assert response.json().get('detail') == "Wrong booking id", f"Incorrect response: {response.json()}!"
