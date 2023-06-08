""" Логирование."""
import functools
import inspect
import logging
import logging.config
import os

from requests import Response
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from utils.logger.log_config import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger()


def log(func: any, is_class_method: bool = True):
    """
    Декоратор для записи работы методов в log. \n
    :param func: функция, для которой производится логирование.
    :param is_class_method: параметр, который указывает, что используется метод класса.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """Метод выполняющий запись информации в log."""

        if is_class_method:
            args_repr = [repr(a) for a in args[1:]]
        else:
            args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        logger.info(f"method '{func.__name__}' called with args [{signature}]")
        test_name = os.environ.get("PYTEST_CURRENT_TEST")
        if test_name is not None:
            test_name = test_name.split(":")[-1].split(" ")[0]

        try:
            result = func(*args, **kwargs)
            if isinstance(result, Response):
                if result.status_code == 400:
                    logger.error(
                        f"{result.status_code} {result.reason} \n"
                        f"test_name: {test_name}\n"
                        f"method_name: {func.__name__}\n"
                        f"request_method: {result.request.method}\n"
                        f"request_url: {result.request.url}\n"
                        f"request_body: {result.request.body}\n"
                        f"response_text: {result.text}\n"
                    )
                    return result

                elif result.status_code in [401, 403]:
                    logger.warning(
                        f"{result.status_code} {result.reason} \n"
                        f"test_name: {test_name}\n"
                        f"method_name: {func.__name__}\n"
                        f"request_method: {result.request.method}\n"
                        f"request_url: {result.request.url}\n"
                        f"request_body: {result.request.body}\n"
                        f"response_text: {result.text}\n"
                    )
                    return result

                elif result.status_code in range(500, 600):
                    logger.critical(
                        f"{result.status_code} {result.reason} \n"
                        f"test_name: {test_name}\n"
                        f"method_name: {func.__name__}\n"
                        f"request_method: {result.request.method}\n"
                        f"request_url: {result.request.url}\n"
                        f"request_body: {result.request.body}\n"
                        f"response_text: {result.text}\n"
                    )
                    return result

                if logging.getLevelName(logger.getEffectiveLevel()) == "INFO":
                    logger.info(
                        f"\n"
                        f"test_name: {test_name}\n"
                        f"method_name: {func.__name__}\n"
                        f"request_method: {result.request.method}\n"
                        f"request_url: {result.request.url}\n"
                        f"request_body: {result.request.body}\n"
                        f"response_status_code: {result.status_code}\n"
                        f"response_text: {result.text}\n"
                    )

                elif logging.getLevelName(logger.getEffectiveLevel()) == "DEBUG":
                    logger.debug(
                        f"\n"
                        f"test_name: {test_name}\n"
                        f"method_name: {func.__name__}\n"
                        f"request_method: {result.request.method}\n"
                        f"request_url: {result.request.url}\n"
                        f"request_body: {result.request.body}\n"
                        f"response_status_code: {result.status_code}\n"
                        f"response_content: {result.content}\n"
                        f"response_text: {result.text}\n"
                        f"request_headers: {result.headers}\n"
                        f"docstring: {func.__doc__}\n"
                        f"encoding: {result.encoding}\n"
                        f"cookies: {result.cookies}\n"
                        f"elapsed: {result.elapsed}\n"
                    )

            return result

        except NoSuchElementException:
            trace = inspect.trace()
            if logging.getLevelName(logger.getEffectiveLevel()) == "DEBUG":
                logger.exception(
                    f"No Such Element Exception\n"
                    f"test_name: {test_name}\n"
                    f"method_name: {func.__name__}\n"
                )
            else:
                logger.error(
                    f"No Such Element Exception\n"
                    f"test_name: {test_name}\n"
                    f"method_name: {func.__name__}\n"
                    f"File {trace[1][1]}, line {trace[1][2]}, in {trace[1][3]}\n  >> {''.join(trace[1][4]).strip()}\n"
                )

        except TimeoutException:
            trace = inspect.trace()
            if logging.getLevelName(logger.getEffectiveLevel()) == "DEBUG":
                logger.exception(
                    f"Timeout Exception\n"
                    f"test_name: {test_name}\n"
                    f"method_name: {func.__name__}\n"
                )
            else:
                logger.error(
                    f"Timeout Exception\n"
                    f"test_name: {test_name}\n"
                    f"method_name: {func.__name__}\n"
                    f"File {trace[1][1]}, line {trace[1][2]}, in {trace[1][3]}\n  >> {''.join(trace[1][4]).strip()}\n"
                )

        except Exception as e:
            trace = inspect.trace()
            if logging.getLevelName(logger.getEffectiveLevel()) == "DEBUG":
                logger.exception(
                    f"{type(e).__name__, e.args}\n"
                    f"test_name: {test_name}\n"
                    f"method_name: {func.__name__}\n"
                )
            else:
                logger.error(
                    f"{type(e).__name__} Exception\n"
                    f"test_name: {test_name}\n"
                    f"method_name: {func.__name__}\n"
                    f"File {trace[1][1]}, line {trace[1][2]}, in {trace[1][3]}\n  >> {''.join(trace[1][4]).strip()}\n"
                )

    return wrapper
