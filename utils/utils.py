import pytest_check
from httpx import Response


def check_status_code(request: Response, exp_code: int):
    """
    Check status code for request. \n
    :param request: http(s) request
    :param exp_code: expected status code.
    """
    status_code = request.status_code
    pytest_check.is_true(
        status_code == exp_code,
        f"Unexpected status code!\n" f"Expected: {exp_code},\n" f"Actual: {status_code}",
    )
