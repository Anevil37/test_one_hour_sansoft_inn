import pytest
import configparser

import requests


def pytest_addoption(parser):
    parser.addoption("--env", action='store', default='TEST', help='Chose environment: default TEST')


@pytest.fixture(scope="session", autouse=True)
def config(request):
    print("\n")
    print("Creating session.\n")

    env = request.config.getoption("--env")
    configuration = configparser.RawConfigParser()
    configuration.read(".\\config.ini")

    test_config = {
        'url': configuration.get(env, 'url'),
        'phone': configuration.get(env, 'phone'),
        'password': configuration.get(env, 'password')
    }

    token = requests.post(
        url=f"{test_config['url']}/client/sign-in",
        headers={
            'Content-Type': 'application/json',
            'Connection': 'keep-alive',
            'Accept': 'application/json'
        },
        json={
            "phone_number": test_config['phone'],
            "password": test_config['password']
        }
    ).json().get('token')

    if token is not None:
        test_config.update({"token": token})
    else:
        raise Exception("Unable to get token!")

    print("Session successfully created.\n")
    return test_config
