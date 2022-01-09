import os
import subprocess
from typing import Callable, List, Optional


class ExecutableTestFailedError(RuntimeError):
    pass


class ExecutableTest:
    def __init__(
        self,
        name: str,
        executable_path: str,
        executable_args: List[str] = [],
        working_dir: str = None,
        stdin: str = None,
        # (self, status_code) -> None
        exe_expected_status_codes_tester: 'Callable[[ExecutableTest, int], None]' = None,
        # (self, stdout, stderr) -> None
        exe_ostreams_expected_content_tester: 'Callable[[ExecutableTest, str, str], None]' = None,
        # (self) -> None
        fs_expected_state_tester: 'Callable[[ExecutableTest], None]' = None,
        # (self) -> None
        setup_routine: 'Callable[[ExecutableTest], None]' = None,
        # (self) -> None
        teardown_routine: 'Callable[[ExecutableTest], None]' = None
    ):
        self.__name: str = str() if name is None else name
        self.__setup_routine: Callable[[self], None] = setup_routine
        self.__teardown_routine: Callable[[self], None] = teardown_routine
        self.__executable_path: str = executable_path
        self.__executable_args: List[str] = executable_args
        self.__working_dir: str = working_dir
        self.__stdin: str = stdin
        self.__exe_expected_status_codes_tester: Callable[[self, int], None] = exe_expected_status_codes_tester
        self.__exe_ostreams_expected_content_tester: Callable[[self, str, str], None] = exe_ostreams_expected_content_tester
        self.__fs_expected_state_tester: Callable[[self], None] = fs_expected_state_tester


    # Returns exception occurred during execution of the teardown routine.
    # Exceptions occurred in any other stage of testing will be re-thrown.
    def test_and_throw_errors(self) -> Optional[Exception]:
        if self.__setup_routine is not None:
            self.__setup_routine(self)

        run_exe_exception = self.__test_executable_safe()
        teardown_exception = self.__teardown_safe()

        if run_exe_exception is not None:
            raise ExecutableTestFailedError from run_exe_exception

        return teardown_exception


    def get_name(self) -> str:
        return self.__name

    name = property(fget=get_name)


    def set_executable_path(self, new_path: str):
        self.__executable_path = new_path

    def get_executable_path(self) -> str:
        return self.__executable_path

    executable_path = property(fget=get_executable_path, fset=set_executable_path)


    def set_working_dir(self, wd: str):
        self.__working_dir = wd

    def get_working_dir(self) -> str:
        return self.__working_dir if ( (self.__working_dir is not None) and (len(self.__working_dir) > 0) ) else os.getcwd()

    working_dir = property(fget=get_working_dir, fset=set_working_dir)


    def get_exe_full_command(self) -> str:
        args_str = ' '.join(f'"{w}"' for w in self.__executable_args)
        return f'"{self.__executable_path}" {args_str}'


    def __teardown_safe(self) -> Optional[Exception]:
        try:
            if self.__teardown_routine is not None:
                self.__teardown_routine(self)
        except Exception as err:
            return err

        return None


    def __test_executable_safe(self) -> Optional[Exception]:
        try:
            self.__test_executable_unsafe()
        except Exception as err:
            return err


    def __test_executable_unsafe(self):
        completed_process = self.__run_executable_unsafe()

        try:
            try:
                if self.__exe_expected_status_codes_tester is not None:
                    self.__exe_expected_status_codes_tester(self, completed_process.returncode)
            finally:
                if self.__exe_ostreams_expected_content_tester is not None:
                    self.__exe_ostreams_expected_content_tester(self, completed_process.stdout, completed_process.stderr)
        finally:
            if self.__fs_expected_state_tester is not None:
                self.__fs_expected_state_tester(self)


    def __run_executable_unsafe(self) -> subprocess.CompletedProcess:
        args = [self.__executable_path] if self.__executable_args is None else [self.__executable_path] + self.__executable_args
        stdin, input = (subprocess.DEVNULL, None) if self.__stdin is None else (None, self.__stdin)
        capture_output = False if self.__exe_ostreams_expected_content_tester is None else True
        text = True
        cwd = self.__working_dir

        return subprocess.run(
            args=args,
            stdin=stdin,
            input=input,
            capture_output=capture_output,
            text=text,
            cwd=cwd
        )
