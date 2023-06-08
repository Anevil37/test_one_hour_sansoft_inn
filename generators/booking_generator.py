import datetime
import uuid


class BookingGenerator:
    def __init__(self, space_id: str = None, datetime_from: str = None, datetime_to: str = None):
        self.date_now = (
            datetime.datetime.now(tz=datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
            + "Z"
        )

        if space_id is None:
            space_id = str(uuid.uuid4())
        if datetime_from is None:
            datetime_from = self.date_now
        if datetime_to is None:
            datetime_to = self.date_now.replace("2023", "2024")

        self.default_data = {
            "space_id": space_id,
            "datetime_from": datetime_from,
            "datetime_to": datetime_to,
        }
