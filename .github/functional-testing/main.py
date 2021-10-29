import os
import sys

from ftlib import ftutil

if __name__ != '__main__':
    raise RuntimeError('This file cannot be loaded as a module!')

print(f'Launch parameters: {sys.argv}')

build_dir = None
build_config = None

# Parse command-line arguments
if len(sys.argv) == 2:
    build_dir = os.path.abspath(sys.argv[1])
elif len(sys.argv) == 3:
    if sys.argv[2].startswith('--config='):
        build_dir = os.path.abspath(sys.argv[1])
        build_config = sys.argv[2][len("--config="):]
    elif sys.argv[1].startswith('--config='):
        build_dir = os.path.abspath(sys.argv[2])
        build_config = sys.argv[1][len("--config="):]
    else:
        raise RuntimeError(f'Unrecognized launch parameters: {sys.argv}')
else:
    raise RuntimeError('Wrong number of launch parameters (expected 2 or 3)')

print(f'Passed build dir: "{build_dir}"')
if build_config is not None:
    print(f'Passed build config: "{build_config}"')

print()

print('Looking for executable candidates for testing...')
exe_candidates = ftutil.find_all_executable_candidates_for_testing(build_dir)
if build_config is not None:
    exe_candidates = [(root, file) for root, file in exe_candidates if build_config in root]
print(f'Done. Found candidates: {exe_candidates}.')
if len(exe_candidates) < 1:
    raise RuntimeError('No executables found')
if len(exe_candidates) > 4:
    raise RuntimeError('Too many found executable candidates')

print()

if not os.path.isfile('resources/tests_config.json'):
    print('The tests configuration file ("resources/tests_config.json") is not found; functional testing will be skipped.')
    sys.exit(0)

print('Loading the tests from "resources/tests_config.json"...')
tests = ftutil.load_tests_from_json('resources/tests_config.json')
print(f'Done. {len(tests)} tests are loaded.')

print()

sys.stdout.flush()

failed_tests_count = len(tests)

for exe_dir, exe_file in exe_candidates:
    print()

    exe_path = os.path.join(exe_dir, exe_file)

    print(f'*** Trying to test "{exe_path}"... ***')
    print()

    failed_tests_count = min(failed_tests_count, ftutil.run_all_tests(tests, executable_path=exe_path))

    print()
    print(f'Testing of "{exe_path}" is finished.')
    print(f'*** Done. Tests passed: {len(tests) - failed_tests_count}/{len(tests)}. ***')
    print()

    sys.stdout.flush()

    if failed_tests_count == 0:
        break

print()

sys.stdout.flush()

if failed_tests_count == 0:
    print('All tests passed.')
else:
    print(f'At least {failed_tests_count}/{len(tests)} tests failed.', file=sys.stderr)
    sys.exit(1)
