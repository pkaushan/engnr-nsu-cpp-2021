from typing import Callable, List

from ftlib.executable_test import ExecutableTest


def any() -> Callable[[ExecutableTest, str, str], None]:
    def result(test: ExecutableTest, stdout: str, stderr: str):
        pass

    return result


def filtered_by(
    allowed_stdouts: List[str] = None,
    banned_stdouts: List[str] = None,
    allowed_stderrs: List[str] = None,
    banned_stderrs: List[str] = None,
    stdout_case_sensitive: bool = True,
    stderr_case_sensitive: bool = True
) -> Callable[[ExecutableTest, str, str], None]:
    allowed_stdouts       = [] if allowed_stdouts is None else list(allowed_stdouts)
    banned_stdouts        = [] if  banned_stdouts is None else list(banned_stdouts)
    allowed_stderrs       = [] if allowed_stderrs is None else list(allowed_stderrs)
    banned_stderrs        = [] if  banned_stderrs is None else list(banned_stderrs)
    stdout_case_sensitive = (stdout_case_sensitive == True)
    stderr_case_sensitive = (stderr_case_sensitive == True)

    def result(test: ExecutableTest, origin_stdout: str, origin_stderr: str):
        out_transformer: Callable[[str], str] = (lambda out: out) if stdout_case_sensitive else (lambda out: out.casefold())
        err_transformer: Callable[[str], str] = (lambda err: err) if stderr_case_sensitive else (lambda err: err.casefold())

        casefold_stdout = out_transformer(origin_stdout)
        casefold_stderr = err_transformer(origin_stderr)

        try:
            for banned_stdout in banned_stdouts:
                if casefold_stdout == out_transformer(banned_stdout):
                    raise ValueError(
                         'The content of stdout is one of the banned values.\n'
                        f'Stdout: <{origin_stdout}>'
                    )

            for allowed_stdout in allowed_stdouts:
                if casefold_stdout == out_transformer(allowed_stdout):
                    break
            else:
                if len(allowed_stdouts) > 0:
                    raise ValueError(
                         'The content of stdout is outside of the expected values list.\n'
                        f'Stdout: <{origin_stdout}>.\n'
                        f'Expected one of the followed: {allowed_stdouts}'
                    )
        finally:
            for banned_stderr in banned_stderrs:
                if casefold_stderr == err_transformer(banned_stderr):
                    raise ValueError(
                         'The content of stderr is one of the banned values.\n'
                        f'Stderr: <{origin_stderr}>'
                    )

            for allowed_stderr in allowed_stderrs:
                if casefold_stderr == err_transformer(allowed_stderr):
                    break
            else:
                if len(allowed_stderrs) > 0:
                    raise ValueError(
                         'The content of stderr is outside of the expected values list.\n'
                        f'Stderr: <{origin_stderr}>.\n'
                        f'Expected one of the followed: {allowed_stderrs}'
                    )

    return result
