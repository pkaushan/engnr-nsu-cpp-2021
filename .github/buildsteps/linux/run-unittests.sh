#!/usr/bin/env bash

# Makes the bash script to print out every command before it is executed except echo
trap '[[ $BASH_COMMAND != echo* ]] && echo $BASH_COMMAND' DEBUG

cd "$LAB_INDEX"     || exit $?

cd 'build'          || exit $?

ctest --version

echo
echo '======================== Unit testing of debug ========================='
cd 'debug'          || exit $?
ctest               || exit $?
cd '..'             || exit $?

echo
echo 'debug: ok.'
echo '========================================================================'

echo
echo

echo '======================== Unit testing of release ======================='
cd 'release'        || exit $?
ctest               || exit $?
cd '..'             || exit $?

echo
echo 'release: ok.'
echo '========================================================================'

echo
echo

echo 'Passed.'