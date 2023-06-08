class LoginGenerator:
    def __init__(self, config):
        self.config = config
        self.default_data = {
            "phone_number": self.config["phone"],
            "password": self.config["password"],
        }
