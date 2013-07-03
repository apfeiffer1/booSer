
#include <sstream>
#include <fstream>
#include <iostream>

#include <boost/iostreams/filtering_streambuf.hpp>
#include <boost/iostreams/copy.hpp>
#include <boost/iostreams/filter/gzip.hpp>

// include headers that implement a binary archive:
#include <boost/archive/binary_oarchive.hpp>
#include <boost/archive/binary_iarchive.hpp>

#include "test_gzipArchive.h"

namespace bar = boost::archive;
namespace bio = boost::iostreams;

template<typename T> 
void save( std::ostringstream &outBuf, const T &obj) {
  bio::filtering_streambuf<bio::output> f;
  f.push(bio::gzip_compressor());
  f.push(outBuf);
  bar::binary_oarchive oa(f);
  oa << obj;   
  return;
} // gzip_compressor flushes when f goes out of scope

int main() {

    // for the compressed archive for output
    std::string arFileName = "gzip_boostArchive.gz";

    // create class instance
    TestStruct2 t2;
    
    // add some data:
    t2.a = 42;
    t2.add(42.);
    t2.add(43.);
    t2.add(44.);
    
    // save data to buffer
    std::ostringstream outBuf;
    save(outBuf, t2);
    t2.show();

    std::cout << "size of buffer: " << outBuf.str().size() << std::endl;
    std::ofstream out(arFileName.c_str(), std::ios::out|std::ios::binary);
    out << outBuf.str();
    out.close();

    std::cout << "Object stored to file" << std::endl;

    return 0;
}

