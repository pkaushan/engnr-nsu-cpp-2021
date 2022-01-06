add_executable(main
        main.cpp
        )
target_include_directories(main
        PRIVATE "../LinkedList"
        )
target_link_libraries(main
        list
        )