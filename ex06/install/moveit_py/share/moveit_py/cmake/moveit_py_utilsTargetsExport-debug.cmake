#----------------------------------------------------------------
# Generated CMake target import file for configuration "Debug".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "moveit_py::moveit_py_utils" for configuration "Debug"
set_property(TARGET moveit_py::moveit_py_utils APPEND PROPERTY IMPORTED_CONFIGURATIONS DEBUG)
set_target_properties(moveit_py::moveit_py_utils PROPERTIES
  IMPORTED_LOCATION_DEBUG "${_IMPORT_PREFIX}/lib/libmoveit_py_utils.so."
  IMPORTED_SONAME_DEBUG "libmoveit_py_utils.so."
  )

list(APPEND _IMPORT_CHECK_TARGETS moveit_py::moveit_py_utils )
list(APPEND _IMPORT_CHECK_FILES_FOR_moveit_py::moveit_py_utils "${_IMPORT_PREFIX}/lib/libmoveit_py_utils.so." )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
