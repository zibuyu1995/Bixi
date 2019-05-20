import importlib
import os
import sys
from contextlib import contextmanager, suppress


def symbol_by_name(name, imp=None):
    imp = importlib.import_module if imp is None else imp
    if ':' in name:
        module_name, _, attr = name.rpartition(':')
    else:
        module_name, _, attr = name.rpartition('.')
    try:
        module = imp(module_name)
    except ValueError as exc:
        raise ValueError(
            f'Cannot import {name!r}: {exc}',
        ).with_traceback(sys.exc_info()[2])
    return getattr(module, attr) if attr else module


def import_from_cwd(module: str, *, imp=None, package=None):
    """
    Import module, temporarily including modules in the current directory.
    Modules located in the current directory has
    precedence over modules located in `sys.path`.
    """

    if imp is None:
        imp = importlib.import_module
    with cwd_in_path():
        return imp(module, package=package)


@contextmanager
def cwd_in_path():
    """Context adding the current working directory to sys.path."""
    cwd = os.getcwd()
    if cwd in sys.path:
        yield
    else:
        sys.path.insert(0, cwd)
        try:
            yield cwd
        finally:
            with suppress(ValueError):
                sys.path.remove(cwd)
