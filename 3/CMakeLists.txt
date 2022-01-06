cmake_minimum_required(VERSION 3.17)
project(LinkedList)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED on)

add_subdirectory(src/main)
add_subdirectory(src/LinkedList)
enable_testing()

add_subdirectory(googletest)
add_subdirectory(test)

if (MSVC)
    target_compile_options(main
            PRIVATE /W4
            # PRIVATE /WX
            )
else()
    target_compile_options(main
            PRIVATE -Wall
            PRIVATE -pedantic
            )
endif()