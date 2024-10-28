cmake_minimum_required(VERSION 3.10)

# Project properties
set(PROJECT_ORG gepetto)
set(PROJECT_NAME toolbox-parallel-robots)
set(PROJECT_DESCRIPTION
    "Set of tools to work with robots with bilateral constraints")
set(PROJECT_URL "https://github.com/${PROJECT_ORG}/${PROJECT_NAME}")

# Project options * Since the project is Python only for now, we remove the
# option of building the python interface option(BUILD_PYTHON_INTERFACE "Build
# the Python unit tests and helpers" ON)
set(BUILD_PYTHON_INTERFACE ON)
# option(INSTALL_PYTHON_INTERFACE_ONLY "Install *ONLY* the Python interface"
# OFF) option(BUILD_TESTING "Build unit tests" OFF)
set(BUILD_TESTING ON)

# Project configuration
set(CUSTOM_HEADER_DIR ${PROJECT_NAME})
set(PROJECT_COMPATIBILITY_VERSION AnyNewerVersion)

# Check if the submodule cmake have been initialized
set(JRL_CMAKE_MODULES "${CMAKE_CURRENT_LIST_DIR}/cmake")
if(EXISTS "${JRL_CMAKE_MODULES}/base.cmake")
  message(STATUS "JRL cmakemodules found in 'cmake/' git submodule")
else()
  find_package(jrl-cmakemodules QUIET CONFIG)
  if(jrl-cmakemodules_FOUND)
    get_property(
      JRL_CMAKE_MODULES
      TARGET jrl-cmakemodules::jrl-cmakemodules
      PROPERTY INTERFACE_INCLUDE_DIRECTORIES)
    message(STATUS "JRL cmakemodules found on system at ${JRL_CMAKE_MODULES}")
  elseif(${CMAKE_VERSION} VERSION_LESS "3.14.0")
    message(
      FATAL_ERROR
        "\nCan't find jrl-cmakemodules. Please either:\n"
        "  - use git submodule: 'git submodule update --init'\n"
        "  - or install https://github.com/jrl-umi3218/jrl-cmakemodules\n"
        "  - or upgrade your CMake version to >= 3.14 to allow automatic fetching\n"
    )
  else()
    message(STATUS "JRL cmakemodules not found. Let's fetch it.")
    include(FetchContent)
    FetchContent_Declare(
      "jrl-cmakemodules"
      GIT_REPOSITORY "https://github.com/jrl-umi3218/jrl-cmakemodules.git")
    FetchContent_MakeAvailable("jrl-cmakemodules")
    FetchContent_GetProperties("jrl-cmakemodules" SOURCE_DIR JRL_CMAKE_MODULES)
  endif()
endif()

# JRL-cmakemodule setup
include("${JRL_CMAKE_MODULES}/base.cmake")

# Print initial message
message(STATUS "${PROJECT_DESCRIPTION}, version ${PROJECT_VERSION}")
message(STATUS "Copyright (C) 2023-2024 LAAS-CNRS")
message(STATUS "All rights reserved.")
# message(STATUS "Released under the BSD 3-Clause License.")

# Project definition
compute_project_args(PROJECT_ARGS LANGUAGES CXX)
project(${PROJECT_NAME} ${PROJECT_ARGS})

if(BUILD_PYTHON_INTERFACE)
  include("${JRL_CMAKE_MODULES}/python.cmake")
  add_project_dependency(pinocchio REQUIRED)
  string(REGEX REPLACE "-" "_" PY_NAME ${PROJECT_NAME})

  set(${PROJECT_NAME}_PYTHON_FILES
      __init__.py
      actuation_data.py
      actuation_model.py
      actuation.py
      closures.py
      constraints.py
      forward_kinematics.py
      freeze_joints.py
      inverse_kinematics.py
      inverse_dynamics.py
      jacobian.py
      mounting.py
      projections.py)
  foreach(python ${${PROJECT_NAME}_PYTHON_FILES})
    python_install_on_site(${PY_NAME} ${python})
  endforeach(python ${${PROJECT_NAME}_PYTHON_FILES})

  set(${PROJECT_NAME}_SLIDERS_PYTHON_FILES slider_generation.py tk_robot_sliders.py
                                           tk_sliders_manager.py util_frames.py)
  foreach(python ${${PROJECT_NAME}_SLIDERS_PYTHON_FILES})
    python_install_on_site(${PY_NAME} sliders/${python})
  endforeach(python ${${PROJECT_NAME}_SLIDERS_PYTHON_FILES})

endif(BUILD_PYTHON_INTERFACE)

install(FILES package.xml DESTINATION share/${PROJECT_NAME})
