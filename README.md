booSer
======

A project mainly to learn and test some aspects of boost serialization.

Contains in the python/ subdir a script (makeSerial.py) to convert C++
header files into boost-serializable header files. This is done using
the python bindings in libclang (with a small add-on, so you'll have
to use my fork of clang for a while).

Added EOS portable binary archives (which are drop-in compatible with 
the ones from boost, and are heavily using other parts from boost) from: 

	<http://epa.codeplex.com>

Simply reading on OS-X 10.8.4 a gzipArchive written on a 32bit platform 
(Ubuntu 12.04) causes a segfault:

	32> storeGzip
	cp 32/gzip_boostArchive.gz osx/.
	osx> loadGzip   <-- crash
	
Doing the same with the portable binary archive works OK.

