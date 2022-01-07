cmake_minimum_required(VERSION 3.17)
project(LinkedList CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED on)

enable_testing()

add_subdirectory(googletest)
add_subdirectory(test)
add_executable(LinkedList LinkedList.h main.cpp)
