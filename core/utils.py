import uuid

from core.logger.logger import Logger
from core.modules.master_module import ResultStorage

logger_config = Logger()
utils_logger = logger_config.get_logger(config_name="default")


def wait_for_results(_keys: list | int, result_storage: ResultStorage, timeout_s: float | None = None):
    if not timeout_s:
        timeout_s = 600

    if not isinstance(_keys, list):
        _keys = [_keys]

    if all(k in result_storage.results.keys() for k in _keys):
        return True, [result_storage.results[k] for k in _keys]

    from datetime import datetime
    start_time = datetime.now()
    success = False
    result = None

    while (datetime.now() - start_time).seconds < timeout_s:
        _timeout_s = timeout_s - (datetime.now() - start_time).seconds
        with result_storage.new_item_condition:
            task_status = result_storage.new_item_condition.wait(timeout=_timeout_s)
            if task_status and all(k in result_storage.results.keys() for k in _keys):
                return True, [result_storage.results[k] for k in _keys]
            else:
                continue

    return success, result


def check_argument_types(args: dict, allowed_types: list[type]) -> [bool, str | None]:
    if not all(any(isinstance(a, t) for t in allowed_types) for a in list(args.values())):
        mistype_args = [arg_name for arg_name, arg_val in args.items()
                        if not any(isinstance(arg_val, t) for t in allowed_types)]
        msg = (f"All execute_mul_calculation arguments should be either int, float or list of those. "
               f"(Check: {[f"{a}={args[a]}" for a in mistype_args]})")
        utils_logger.critical(msg)
        return False, msg
    return True, None
