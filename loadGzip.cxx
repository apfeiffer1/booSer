
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
void load( std::istringstream &inBuf, T &obj) {
  bio::filtering_streambuf<bio::input> f;
  f.push(bio::gzip_decompressor());
  f.push(inBuf);
  bar::binary_iarchive ia(f);
  ia >> obj;
  return;
} // gzip_compressor flushes when f goes out of scope

int main() {

    // for the compressed archive for output
    std::string arFileName = "gzip_boostArchive.gz";
 
    std::stringstream buf;
    std::ifstream inFile(arFileName.c_str(), std::ios::in|std::ios::binary);
    buf << inFile.rdbuf();
    inFile.close();

    // ... restore the class instance to its orginal state
    TestStruct2 t2New;
    std::istringstream iss( buf.str() ); 
    t2New.show();
    load(iss, t2New);
    t2New.show();

    std::cout << "Object loaded from file" << std::endl;

    return 0;
}

