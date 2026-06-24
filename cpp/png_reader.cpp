#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h"

namespace py = pybind11;

// function exposed to Python
py::array_t<unsigned char> read_png(const std::string& path) {
    int width, height, channels;

    unsigned char* data = stbi_load(path.c_str(), &width, &height, &channels, 0);
    if (!data) {
        throw std::runtime_error("Failed to load image: " + path);
    }

    // create numpy array (H x W x C)
    auto result = py::array_t<unsigned char>(
        { height, width, channels },
        data
    );

    // free stb memory after copy into numpy
    stbi_image_free(data);

    return result;
}

PYBIND11_MODULE(png_reader, m) {
    m.def("read_png", &read_png, "Read a PNG image into a numpy array");
}