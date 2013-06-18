#include <fstream>
#include <boost/archive/xml_oarchive.hpp>
#include "TestClass.h"

int main() {
    // create class instance
    TestClass t1;
    
    // add some data:
    t1.setA(41);
    t1.add(42.); // add something to the vector
    
    // create and open a character archive for output
    std::string arFileName = "testClass.boostArchiveXML";
    std::ofstream ofs(arFileName.c_str());

    // save data to archive
    {
        boost::archive:: xml_oarchive oa(ofs);
        // write class instance to archive
        oa << BOOST_SERIALIZATION_NVP(t1);
        // archive and stream are closed when dtors are called
    }
    t1.show("t1"); // show content of class 
    std::cout << "Object stored to file" << std::endl;
    return 0;
}
