#!/usr/bin/env bash

# Makes the bash script to print out every command before it is executed except echo
trap '[[ $BASH_COMMAND != echo* ]] && echo $BASH_COMMAND' DEBUG

cd '.github/functional-testing'         || exit $?

python3 --version                       || exit $?

echo
echo '===================== Functional testing of debug ======================'
python3 main.py "../../$LAB_INDEX/build/debug"   || exit $?
echo
echo 'debug: ok.'
echo '========================================================================'

echo
echo

echo '===================== Functional testing of release ===================='
python3 main.py "../../$LAB_INDEX/build/release" || exit $?
echo
echo 'release: ok.'
echo '========================================================================'

echo
echo

echo 'Passed.'