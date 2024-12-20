import random
import uuid

from api_clients.space_api import SpaceApi


class SpaceFactory:
    def __init__(self, config):
        self.config = config
        self.guid = str(uuid.uuid4())
        self.rnd_number = random.randint(0, 89)
        self.space_api = SpaceApi(config=self.config)
        self.types = self.space_api.get_space_filter().json().get("types")
        self.default_data = {
            "name": f"Autotest_space_{self.guid[:6]}",
            "type": random.choice(self.types),
            "city": f"Autotest_city_{self.guid[:6]}",
            "country": f"Autotest_count_{self.guid[:6]}",
            "address": f"Autotest_address_{self.guid[:6]}",
            "area": self.rnd_number + 1,
            "price": self.rnd_number + 2,
            "available_from": "2020-01-01T01:01:01.001Z",
            "available_to": "2030-01-01T01:01:01.001Z",
            "short_description": f"Autotest_short_desc_{self.guid[:6]}",
            "detailed_description": f"Autotest_detail_desc_{self.guid[:6]}",
            "image_urls": [
                "https://www.neptunus.co.uk/wp-content/uploads/2018/08/demontabel-bouwen-Flexolution-2-flex2shop-mclaren-showroom-hatfield-8-820x546.jpg"
            ],
            "id": self.guid,
            "lat": str(self.rnd_number),
            "lng": str(self.rnd_number),
        }
