from importlib import util as importlib_util


def import_module_from_path(module_name, file_path):
    spec = importlib_util.spec_from_file_location(module_name, file_path)
    module_obj = importlib_util.module_from_spec(spec)
    spec.loader.exec_module(module_obj)
    return module_obj


__all__ = ["import_module_from_path"]
