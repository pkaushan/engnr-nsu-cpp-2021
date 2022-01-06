add_executable(LinkedList_test
        LinkedList_tests.cpp
        )
target_include_directories(LinkedList_test
        PRIVATE "../src/LinkedList"
        )
target_link_libraries(LinkedList_test
        LinkedList
        gtest
        gmock_main
        )

enable_testing()
add_test(NAME google_test COMMAND LinkedList_test)