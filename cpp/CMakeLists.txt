cmake_minimum_required(VERSION 3.10)
project(png_reader)

set(CMAKE_CXX_STANDARD 17)

find_package(pybind11 REQUIRED)

pybind11_add_module(png_reader png_reader.cpp)