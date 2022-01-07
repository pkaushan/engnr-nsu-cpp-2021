add_executable(LinkedList_test
        LinkedList_tests.cpp
        )

target_link_libraries(LinkedList_test
        gtest
        gmock_main
        )

enable_testing()
add_test(NAME google_test COMMAND LinkedList_test)