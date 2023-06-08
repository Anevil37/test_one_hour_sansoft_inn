from datetime import datetime

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s | [%(levelname)s] | %(message)s",  # формат логов
            "datefmt": "%Y-%m-%d %H:%M:%S",  # формат даты
        },
        "detail": {
            "format": "%(asctime)-15s %(levelname)-5s %(filename)s "
            "+%(lineno)d %(funcName)s [%(threadName)s]: %(message)s",  # формат логов
            "datefmt": "%Y-%m-%d %H:%M:%S",  # формат даты
        },
    },
    "handlers": {
        "console": {  # параметры вывода логов в консоль
            "class": "logging.StreamHandler",
            "formatter": "default",  # используемый форматтер
            "stream": "ext://sys.stdout",  # указываем, что нужно выводить в консоль
        },
        # "file": {  # параметры записи логов в файл
        #     "filename": f"logs/log_{datetime.now().strftime('%d-%m-%Y_%H-%M')}.log",  # название файла
        #     "mode": "a",  # a-дозаписывать, w-перезаписывать, w работает только если maxBytes=0
        #     "maxBytes": 500000,  # максимальный размер файла
        #     "backupCount": 10,  # количество дополнительных файлов, если первый файл достигнет максимального размера
        #     "formatter": "default",  # используемый форматтер
        #     "encoding": "utf-8",  # кодировка файла
        #     "class": "logging.handlers.RotatingFileHandler"  # указываем, что нужно записывать в файл
        # }
    },
    "loggers": {
        "root": {
            "handlers": ["console"],  # "file",
            "level": "INFO",  # уровень логирования. Доступные уровни: DEBUG, INFO, WARNING, ERROR, CRITICAL
            "propagate": True,
        }
    },
}
