def is_valid_str(param: any):
    if not param: return False
    if not isinstance(param, str): return False
    if param.isspace(): return False
    return True

def is_valid_str_or_null(param: any):
    if param is None: return True
    return is_valid_str(param)