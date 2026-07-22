"""
"""

from __future__ import annotations

import os
import sys
import types
from importlib import import_module
from pathlib import Path
from warnings import warn
from user_conf import user_script_paths


def run_python_file(filename: str, args: list[str], package=None):
    """Run a python file as if it were the main program on the command line.

    .. versionchanged:: 7.7
       Set and restore ``PYWIKIBOT_TEST_...`` environment variables.

    :param filename: The path to the file to execute, it need not be a
        .py file.
    :param args: is the argument list to present as sys.argv, as strings.
    :param package: The package of the script. Used for checks.
    :type package: Optional[module]
    """
    # Create a module to serve as __main__
    old_main_mod = sys.modules['__main__']
    main_mod = types.ModuleType('__main__')
    sys.modules['__main__'] = main_mod
    main_mod.__file__ = filename
    main_mod.__builtins__ = sys.modules['builtins']
    if package:
        main_mod.__package__ = package.__name__

    # Set sys.argv and the first path element properly.
    old_argv = sys.argv

    # set environment values
    sys.argv = [filename] + args
    sys.path.insert(0, os.path.dirname(filename))

    try:
        with open(filename, 'rb') as f:
            source = f.read()
        exec(compile(source, filename, 'exec', dont_inherit=True),
             main_mod.__dict__)
    finally:
        # Restore the old __main__
        sys.modules['__main__'] = old_main_mod

        # Restore the old argv and path
        sys.argv = old_argv
        sys.path.pop(0)


def handle_args(
    _,
    *args: str,
) -> tuple[str, list[str], list[str], list[str]]:
    """Handle args and get filename.

    .. versionchanged:: 7.7
       Catch ``PYWIKIBOT_TEST_...`` environment variables.

    :return: filename, script args, local pwb args, environment variables
    """
    fname = None
    for index, arg in enumerate(args, start=1):
        if arg in ('-version', '--version'):
            fname = 'version.py'
        elif arg in ('pwb', 'pwb.py', 'wrapper', 'wrapper.py'):
            pass
        else:
            fname = arg
            if not fname.endswith('.py'):
                fname += '.py'
        if fname:
            break
    else:
        index = 0

    return fname, list(args[index:])


def find_filename(filename):
    """Search for the filename in the given script paths.

    .. versionchanged:: 7.0
       Search users_scripts_paths in config.base_dir
    .. versionchanged:: 9.0
       Add config.base_dir to search path
    """
    path_list = []  # paths to find misspellings

    def test_paths(paths, root: Path):
        """Search for filename in given paths within 'root' base directory."""
        for file_package in paths:
            # package = file_package.split('.') # replaces I:/MD_TOOLS/mdwiki.toolforge.org/ by I:/MD_TOOLS/mdwiki/toolforge/org/
            path = [file_package] + [filename]
            testpath = root.joinpath(*path)
            if testpath.exists():
                return str(testpath)
            path_list.append(str(testpath.resolve()))
        return None

    # base_dir = config.base_dir
    base_dir = Path(__file__).parent

    found = test_paths(user_script_paths, Path(base_dir))

    if found is None:
        print(f"{filename} not found in any path in user_script_paths: ")
        for x in path_list:
            file_path = x.replace("\\", "/")
            print(f"\t {file_path}")
    return found


def execute():
    """Parse arguments, extract filename and run the script.

    .. versionadded:: 7.0
       renamed from :func:`main`
    """
    filename, script_args = handle_args(*sys.argv)

    if not filename:
        warn("No filename given")
        return False

    file_package = None

    if not os.path.exists(filename):
        filename = find_filename(filename)
        if filename is None:
            return True

    # When both pwb.py and the filename to run are within the current
    # working directory:
    # a) set __package__ as if called using python -m scripts.blah.foo
    # b) set __file__ to be relative, so it can be relative in backtraces,
    #    and __file__ *appears* to be an unstable path to load data from.
    # This is a rough (and quick!) emulation of 'package name' detection.
    # a much more detailed implementation is in coverage's find_module.
    # https://bitbucket.org/ned/coveragepy/src/default/coverage/execfile.py
    cwd = Path.cwd()
    syspath = Path(sys.argv[0])
    absolute_path = syspath.parent
    file_path = Path(filename)

    if absolute_path == cwd and cwd in file_path.parents:
        relative_filename = file_path.relative_to(absolute_path)
        # remove the filename, and use '.' instead of path separator.
        file_package = str(relative_filename.parent).replace(os.sep, '.')
        filename = os.path.join(os.curdir, str(relative_filename))

    module = None

    if file_package:
        try:
            module = sys.modules[file_package]
        except KeyError:
            try:
                module = import_module(file_package)
            except ImportError as e:
                warn(f'Parent module {file_package} not found: {e}',
                     ImportWarning)

    run_python_file(filename, script_args, module)

    return True


if __name__ == '__main__':
    execute()
