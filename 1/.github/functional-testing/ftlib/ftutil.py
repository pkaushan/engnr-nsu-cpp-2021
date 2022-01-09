import json
import os
import platform
import sys
import traceback
from typing import List, Tuple

from ftlib import status_code_checkers, stdostreams_content_checkers
from ftlib.executable_test import ExecutableTest


# list of pair (dir, file name)
def find_all_executable_candidates_for_testing(rootdir: str) -> List[Tuple[str, str]]:
    is_windows = platform.system().lower().startswith('windows')
    exe_candidates = []

    for root, dirs, files in os.walk(rootdir):
        newDirs = [item for item in dirs if (item != 'CMakeFiles') and (not 'test' in item.lower())]
        dirs.clear()
        dirs += newDirs

        for file in files:
            filelower = file.lower()
            if 'make' in filelower:
                continue
            if 'test' in filelower:
                continue

            fullpath = os.path.join(root, file)

            if is_windows and not file.endswith('.exe'):
                continue
            if not (os.path.isfile(fullpath)):
                continue
            if not (os.access(fullpath, os.X_OK)):
                continue

            exe_candidates.append((root, file))

    return exe_candidates


def load_tests_from_json(config_path: str) -> List[ExecutableTest]:
    config_json = None
    with open(config_path, 'r') as config_file:
        config_json = json.load(config_file)

    tests_list_json = config_json.get('tests')
    if (tests_list_json is None) or (len(tests_list_json) < 1):
        return list[ExecutableTest]()

    result: List[ExecutableTest] = []

    for index, test_json in enumerate(tests_list_json, start=1):
        name: str                      = test_json.get('name')
        params: List[str]              = test_json.get('params')
        stdin: str                     = test_json.get('stdin')
        status_code_allowed: List[int] = None
        status_code_banned: List[int]  = None
        stdout_allowed: List[str]      = None
        stdout_banned: List[str]       = None
        stdout_case_sensitive: bool    = True
        stderr_allowed: List[str]      = None
        stderr_banned: List[str]       = None
        stderr_case_sensitive: bool    = True

        status_code_json  = test_json.get('status_code')
        if status_code_json is not None:
            status_code_allowed = status_code_json.get('allowed')
            status_code_banned = status_code_json.get('banned')

        stdout_json = test_json.get('stdout')
        if stdout_json is not None:
            stdout_allowed = stdout_json.get('allowed')
            stdout_banned = stdout_json.get('banned')
            stdout_case_sensitive = False if stdout_json.get('case_sensitive') is False else stdout_case_sensitive

        stderr_json = test_json.get('stderr')
        if stderr_json is not None:
            stderr_allowed = stderr_json.get('allowed')
            stderr_banned = stderr_json.get('banned')
            stderr_case_sensitive = False if stderr_json.get('case_sensitive') is False else stderr_case_sensitive

        if (name is None) or (len(name) < 1):
            name = f'Test #{index}'
        if params is None:
            params = []
        if status_code_allowed is None:
            status_code_allowed = []
        if status_code_banned is None:
            status_code_banned = []
        if stdout_allowed is None:
            stdout_allowed = []
        if stdout_banned is None:
            stdout_banned = []
        if stderr_allowed is None:
            stderr_allowed = []
        if stderr_banned is None:
            stderr_banned = []

        exe_expected_status_codes_tester = None
        if (len(status_code_allowed) > 0) or (len(status_code_banned) > 0):
            exe_expected_status_codes_tester=status_code_checkers.filtered_by(
                allowed_codes=status_code_allowed,
                banned_codes=status_code_banned
            )

        exe_ostreams_expected_content_tester = None
        if ((len(stdout_allowed) > 0  ) or
            (len(stdout_banned)  > 0  ) or
            (len(stderr_allowed) > 0  ) or
            (len(stderr_banned)  > 0  ) or
            (not stdout_case_sensitive) or
            (not stderr_case_sensitive) ):
             exe_ostreams_expected_content_tester=stdostreams_content_checkers.filtered_by(
                allowed_stdouts=stdout_allowed,
                banned_stdouts=stdout_banned,
                allowed_stderrs=stderr_allowed,
                banned_stderrs=stderr_banned,
                stdout_case_sensitive=stdout_case_sensitive,
                stderr_case_sensitive=stderr_case_sensitive
            )

        result.append(ExecutableTest(
            name=name,
            executable_path=None,
            working_dir=None,
            executable_args=params,
            stdin=stdin,
            exe_expected_status_codes_tester=exe_expected_status_codes_tester,
            exe_ostreams_expected_content_tester=exe_ostreams_expected_content_tester
        ))

    return result


# Returns number of failed tests
def run_all_tests(tests: List[ExecutableTest], executable_path: str, working_dir: str = None) -> int:
    result: int = 0

    for test in tests:
        print(f'Running the test "{test.name}"...')
        sys.stdout.flush()

        test.executable_path = executable_path
        test.working_dir = working_dir

        try:
            test.test_and_throw_errors()
        except Exception:
            result += 1
            print(f'The test "{test.name}" failed.\n'
                  f'Command line: {test.get_exe_full_command()}.\n'
                  f'Working dir: "{test.get_working_dir()}".\n'
                  f'Caused by:', file=sys.stderr)

            exc_info: str = traceback.format_exc()
            last_newline = exc_info.rfind('\n')
            if last_newline > 0:
                exc_info = '    |' + exc_info[:last_newline].replace('\n', '\n    |') + exc_info[last_newline:]

            print(exc_info, file=sys.stderr)

            sys.stderr.flush()
        else:
            print('Succeeded.')

        print()
        sys.stdout.flush()

    return result
