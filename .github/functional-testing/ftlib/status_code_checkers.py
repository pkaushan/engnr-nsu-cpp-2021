from typing import Callable, List

from ftlib.executable_test import ExecutableTest


def custom_checker(
    predicate: Callable[[ExecutableTest, int], bool],
    error_description_factory: Callable[[ExecutableTest, int], str]
) -> Callable[[ExecutableTest, int], None]:
    def result(test: ExecutableTest, sc: int):
        if predicate(test, sc) is not True:
            raise ValueError(error_description_factory(test, sc))

    return result


def any() -> Callable[[ExecutableTest, int], None]:
    def result(test: ExecutableTest, sc: int):
        pass

    return result


def only0() -> Callable[[ExecutableTest, int], None]:
    def result(test: ExecutableTest, sc: int):
        if sc != 0:
            raise ValueError(f'The status code is {sc}, but only 0 is expected')

    return result


def non0() -> Callable[[ExecutableTest, int], None]:
    def result(test: ExecutableTest, sc: int):
        if sc == 0:
            raise ValueError(f'The status code is {sc}, but only non-zero status codes are expected')

    return result


def filtered_by(allowed_codes: List[int] = None, banned_codes: List[int] = None) -> Callable[[ExecutableTest, int], None]:
    allowed_codes = [] if allowed_codes is None else list(allowed_codes)
    banned_codes  = [] if banned_codes  is None else list(banned_codes)

    def result(test: ExecutableTest, sc: int):
        if sc in banned_codes:
            raise ValueError(f'The status code (={sc}) is one of the banned values: {banned_codes}')

        if (len(allowed_codes) > 0) and (sc not in allowed_codes):
            raise ValueError(f'The status code (={sc}) is outside of the expected values: {allowed_codes}')

    return result
