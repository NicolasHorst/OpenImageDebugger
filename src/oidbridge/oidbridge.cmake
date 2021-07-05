cmake_minimum_required(VERSION 3.10.0)

add_library(${PROJECT_NAME} SHARED
            ../oid_bridge.cpp
            ../../debuggerinterface/python_native_interface.cpp
            ../../ipc/message_exchange.cpp
            ../../ipc/raw_data_decode.cpp
            ../../system/process/process.cpp
            $<$<BOOL:${UNIX}>:../../system/process/process_unix.cpp>
            $<$<BOOL:${WIN32}>:../../system/process/process_win32.cpp>)

target_compile_options(${PROJECT_NAME}
                       PUBLIC "$<$<PLATFORM_ID:UNIX>:-Wl,--exclude-libs,ALL>")

target_include_directories(${PROJECT_NAME}
                           PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/../..)

target_include_directories(${PROJECT_NAME} SYSTEM
                           PRIVATE ${PYTHON_INCLUDE_DIR})

target_link_libraries(${PROJECT_NAME} PRIVATE
                      Qt5::Core
                      Qt5::Network
                      Threads::Threads
                      ${PYTHON_LIBRARY})

install(TARGETS ${PROJECT_NAME} DESTINATION OpenImageDebugger)

# Need to unset these vars to trigger find_package with a different required version
unset(PYTHON_INCLUDE_DIR CACHE)
unset(PYTHON_LIBRARY CACHE)

# TODO: deal with macos installation
include(${CMAKE_CURRENT_SOURCE_DIR}/../../../resources/deployscripts.cmake)
