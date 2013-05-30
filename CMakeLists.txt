
cmake_minimum_required (VERSION 2.6)

project (PyClang)

include_directories ( "/opt/local/include/" ) 

FIND_PACKAGE( Boost 1.53 COMPONENTS serialization iostreams REQUIRED )
INCLUDE_DIRECTORIES( ${Boost_INCLUDE_DIR} )

add_executable(test_embedded test_embedded.cxx)
TARGET_LINK_LIBRARIES( test_embedded ${Boost_LIBRARIES} )

add_executable(test_gzipArchive test_gzipArchive.cxx)
TARGET_LINK_LIBRARIES( test_gzipArchive ${Boost_LIBRARIES} )

ENABLE_TESTING()

# test_embedded
add_test (test_embedded test_embedded)
set_tests_properties (test_embedded PROPERTIES PASS_REGULAR_EXPRESSION "tNew-before.a=0")
set_tests_properties (test_embedded PROPERTIES PASS_REGULAR_EXPRESSION "tNew-after.a=42")

# test_gzipArchive
add_test (test_gzipArchive test_gzipArchive)
set_tests_properties (test_gzipArchive PROPERTIES PASS_REGULAR_EXPRESSION "result is 0")
