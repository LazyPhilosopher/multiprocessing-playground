from core.modules.master_module import ResultStorage


def wait_for_result(_key, timeout_s: float, result_storage: ResultStorage):
    if _key in result_storage.results.keys():
        return True, result_storage.results[_key]

    from datetime import datetime
    start_time = datetime.now()
    success = False
    result = None

    while (datetime.now() - start_time).seconds < timeout_s:
        _timeout_s = timeout_s - (datetime.now() - start_time).seconds
        with result_storage.new_item_condition:
            task_status = result_storage.new_item_condition.wait(timeout=_timeout_s)
            if task_status and _key in result_storage.results.keys():
                success = True
                result = result_storage.results[_key]
                break
            else:
                continue

    return success, result
