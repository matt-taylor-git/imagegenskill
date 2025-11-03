cmake_minimum_required(VERSION 3.16)
project(ImagenSkillTest VERSION 1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find Qt6
find_package(Qt6 REQUIRED COMPONENTS Core Gui Widgets)

# Auto-generate Qt resource file
set(CMAKE_AUTORCC ON)

# Add executable
add_executable(test_ui
    test_mainwindow.cpp
    main.cpp
    resources.qrc
)

# Link Qt libraries
target_link_libraries(test_ui
    Qt6::Core
    Qt6::Gui
    Qt6::Widgets
)

# Set output directory
set_target_properties(test_ui PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}
)
