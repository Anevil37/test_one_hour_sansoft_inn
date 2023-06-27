# TODO Rewrite factories, like
# import factory.fuzzy
# class ProfileFactory(BaseFactory):
#     class Meta:
#         model = Profile
#
#     id = factory.LazyFunction(uuid4)
#
#     given_name = factory.Faker("first_name")
#     last_name = factory.Faker("last_name")
#
#     email = factory.Faker("email")
#     account_email = factory.LazyAttribute(
#         lambda o: f"treehive_dummy_email-{o.given_name}-{o.last_name}-{datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')}-{random_chars(4)}@treehive.nl".lower()
#     )
#
#     known_as = factory.Faker("first_name")
#     date_of_birth = factory.fuzzy.FuzzyDate(datetime.date(2018, 1, 1))
#
#     gender = factory.fuzzy.FuzzyInteger(0, 1)
#     language = factory.fuzzy.FuzzyInteger(0, 4)
#
#     address_line_1 = factory.Faker("street_address")
#     city = factory.Faker("city")
#     region = factory.Faker("state")
#     zip_code = factory.Faker("zipcode")
#     country = factory.fuzzy.FuzzyInteger(0, 192)
#
#     nationalities = []
#
#     title = factory.fuzzy.FuzzyInteger(0, 5)
#     telephone = factory.Faker("phone_number")
