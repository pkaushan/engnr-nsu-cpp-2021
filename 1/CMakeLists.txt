cmake_minimum_required(VERSION 3.17)
project(lab_1)

set(CMAKE_CXX_STANDARD 14)
add_executable(hasher
        main.cpp
        Hashfunc.h
        Hashfunc.cpp
        )
if (MSVC)
    target_compile_options(hasher
            PRIVATE /W4
            PRIVATE /WX
            )
else()
    target_compile_options(hasher
            PRIVATE -Wall
            PRIVATE -pedantic
            PRIVATE -Werror
            )
endif()