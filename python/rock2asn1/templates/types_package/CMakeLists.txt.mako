# Generated from ${context._with_template.uri} for ${lib_name}.

# CMakeLists.txt has to be located in the project folder and cmake has to be
# executed from 'project/build' with 'cmake ../'.
cmake_minimum_required(VERSION 2.6)

include($ENV{ESROCOS_CMAKE})

project(${lib_name})

add_subdirectory(asn)
