
cmake_minimum_required (VERSION 2.6)

project (BooSerExamples CXX)

include_directories ( "/opt/local/include/", ${BooSerExamples_SOURCE_DIR} ) 

FIND_PACKAGE( Boost 1.46 COMPONENTS serialization iostreams REQUIRED )
INCLUDE_DIRECTORIES( ${Boost_INCLUDE_DIR} )

ENABLE_TESTING()

macro (setup exeName testString)
	add_executable(${exeName} ${exeName}.cxx)
	TARGET_LINK_LIBRARIES(${exeName} ${Boost_LIBRARIES} )

	add_test (${exeName} ${exeName} )
	set_tests_properties (${exeName} PROPERTIES PASS_REGULAR_EXPRESSION ${testString} )
endmacro (setup)


setup(test_embedded    "tNew-after.a=42")
setup(test_gzipArchive "result is 0")
setup(test_xmlOArchive "XML written to file")
setup(storeText        "Object stored to file")
setup(loadText         "Object loaded from file")
setup(storeXML         "Object stored to file")
setup(loadXML          "Object loaded from file")
setup(storeGzip        "Object stored to file")
setup(loadGzip         "Object loaded from file")
setup(storePba         "Object stored to file")
setup(loadPba          "Object loaded from file")

