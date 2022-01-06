cmake_minimum_required(VERSION 3.17)
project(LinkedList)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED on)

add_executable(${PROJECT_NAME} main.cpp LinkedList.h)



enable_testing()


add_subdirectory(googletest)
add_subdirectory(test)

