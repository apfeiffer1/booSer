
#include <sstream>
#include <fstream>
#include <iostream>

#include <boost/iostreams/filtering_streambuf.hpp>
#include <boost/iostreams/copy.hpp>
#include <boost/iostreams/filter/gzip.hpp>

// include headers that implement an xml archive
#include <boost/archive/xml_oarchive.hpp>

#include <boost/serialization/vector.hpp>

#include "test_xmlOArchive.h"

namespace bar = boost::archive;
namespace bio = boost::iostreams;

// template<typename T> 
void saveAsXML(TestStruct & obj, std::string fileName ) {
  std::ofstream ofs(fileName.c_str());
  assert( ofs.good() );
  bar::xml_oarchive oa(ofs);
  oa << BOOST_SERIALIZATION_NVP(obj);
  return;
} // stream closes when it goes out of scope


int main() {

    // for the compressed archive for output
    std::string arFileName = "test2_boostArchive.gz";

    // create class instance
    TestStruct t2;
    
    // add some data:
    t2.a = 42;
    t2.add(42.);
    t2.add(43.);
    t2.add(44.);
    
    saveAsXML(t2, "outFile.xml");
    std::cout << "XML written to file (outFile.xml)" << std::endl;

    return 0;
}

