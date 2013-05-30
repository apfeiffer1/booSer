booSer
======

A project mainly to learn and test some aspects of boost serialization.

Contains in the python/ subdir a script (makeSerial.py) to convert C++
header files into boost-serializable header files. This is done using
the python bindings in libclang (with a small add-on, so you'll have
to use my fork of clang for a while).

