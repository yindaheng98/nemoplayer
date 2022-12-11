#include <pybind11/pybind11.h>
#include "./common.h"

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

int add(int i, int j) { return i + j; }

namespace py = pybind11;

class PyPlayer {
 private:
  Player player;

 public:
  PyPlayer(const VpxVideoInfo *info, vpx_img_fmt_t img_fmt, int scale) {
    vpx_codec_err_t error = init(&player, info, img_fmt, scale);
    if (error != VPX_CODEC_OK) throw error;
  }
  vpx_codec_err_t Decode(const uint8_t *data, unsigned int data_sz) {
    return decode(&player, data, data_sz, NULL, 0);
  }
  vpx_codec_err_t GetFrame(unsigned char *buffer) {
    return get_frame(&player, buffer);
  }
  vpx_codec_err_t SetSRFrame(unsigned char *img_buf, int scale) {
    return set_sr_frame(&player, img_buf, scale);
  }
  ~PyPlayer() {
    vpx_codec_err_t error = destory(&player);
    if (error != VPX_CODEC_OK) throw error;
  };
};

PYBIND11_MODULE(nemoplayer, m) {
  m.doc() = R"pbdoc(
        Pybind11 example plugin
        -----------------------

        .. currentmodule:: nemoplayer

        .. autosummary::
           :toctree: _generate

           add
           subtract
    )pbdoc";

  m.def("add", &add, R"pbdoc(
        Add two numbers

        Some other explanation about the add function.
    )pbdoc");

  m.def(
      "subtract", [](int i, int j) { return i - j; }, R"pbdoc(
        Subtract two numbers

        Some other explanation about the subtract function.
    )pbdoc");
  py::class_<PyPlayer>(m, "PyPlayer")
      .def(py::init<const VpxVideoInfo *, vpx_img_fmt_t, int>())
      .def("Decode", &PyPlayer::Decode)
      .def("GetFrame", &PyPlayer::GetFrame)
      .def("SetSRFrame", &PyPlayer::SetSRFrame);

#ifdef VERSION_INFO
  m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
  m.attr("__version__") = "dev";
#endif
}
