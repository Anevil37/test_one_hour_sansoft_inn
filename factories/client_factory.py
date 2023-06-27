import uuid

from phone_gen import PhoneNumber


class ClientFactory:
    def __init__(self):
        self.phone_number = PhoneNumber("RS").get_number(full=False)
        self.guid = str(uuid.uuid4())[:6]
        self.default_data = {
            "first_name": f"Autotest_first_name_{self.guid}",
            "last_name": f"Autotest_last_name_{self.guid}",
            "phone_number": f"{self.phone_number}",
            "email": f"Autotest_email_{self.guid}@gmail.com",
            "password": f"Aboba322228",
        }
