#!/bin/python3

import functools, logging, re

from inspect import getargspec

from typing import Union

from .loggers import CustomLogger, get_default_logger 

def _get_logging_level(logger, level):
    '''Get logging level method object based on what is passed in'''
    callback = logger.info
    if level == logging.DEBUG:
        callback = logger.debug
    elif level == logging.INFO:
        callback = logger.info
    elif level == logging.WARN:
        callback = logger.warn
    elif level == logging.ERROR:
        callback = logger.error
    else:
        callback = logger.info
    return callback

def _trim_whitespace_if_required(trim, string):
    return re.sub("\s\s+", " ", string) if trim else string

def log(description=None, trim=True, level=logging.INFO, _func=None, *, my_logger: Union[CustomLogger, logging.Logger] = None):
    '''
    Decorator to log function calls and their parameters
    https://ankitbko.github.io/blog/2021/04/logging-in-python/
    '''
    def decorator_log(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if my_logger is None:
                logger = get_default_logger()
            else:
                if isinstance(my_logger, CustomLogger):
                    logger = my_logger.get_logger(func.__name__)
                else:
                    logger = my_logger

            args_dict = dict(zip(getargspec(func).args, [re.sub(r'[\']', '', repr(a)) for a in args]))
            
            if trim:
                for k, v in args_dict.items():
                    if type(v) == str:
                        args_dict[k] = re.sub("\s\s+", " ", v)
                for k, v in kwargs.items():
                    if type(v) == str:
                        kwargs[k] = re.sub("\s\s+", " ", v)
            
            args_repr = []
            for key, value in args_dict.items():
                value = re.sub("\s\s+", " ", value) if trim else value
                data = f"{key}={value}"
                args_repr.append(data)
            
            kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]

            signature = ", ".join(args_repr + kwargs_repr)

            extra_logs = ""
            try:
                extra_logs = ""
                if "extra_logs" in kwargs.keys():
                    extra_logs = kwargs.items()["extra_logs"] + " - "
                elif "extra_logs" in args_dict.keys():
                    extra_logs = args_dict["extra_logs"] + " - "
            except:
                pass
            callback = _get_logging_level(logger, level)
            callback(f"{extra_logs}{description}: {func.__name__}({signature})")
            try:
                result = func(*args, **kwargs)
                callback(f"{extra_logs}{description}: {func.__name__}({signature}) completed successfully!")
                return result
            except Exception as e:
                logger.exception(f"Exception raised in '{func.__name__}': {str(e)}")
                raise e
        return wrapper

    if _func is None:
        return decorator_log
    else:
        return decorator_log(_func)

def exit_on_none(function):
    '''Wrapper to exit script with err code 1 if function returns None'''
    def wrapper(*args, **kwargs):
        data = function(*args, **kwargs)
        if data == None:
            exit(1)
        return data
    return wrapper


if __name__ == "__main__":
    @log(description="POSTing to data catalog")
    def foo(x, test):
        return

    foo("ad",test="asd")
