#include <fstream>
#include <eos/portable_iarchive.hpp>
#include "TestClass.h"

int main() {  
    // ... some time later restore to its orginal state from file
    TestClass tNew;
    tNew.show("tNew-before"); // “empty” object

    std::string arFileName = "testClass.portBinArchive";
    {
        // create and open an archive for input
        std::ifstream ifs(arFileName.c_str());
        eos::portable_iarchive ia(ifs);
        // read class state from archive
        ia >> tNew;
        // archive and stream closed when dtors are called
    }

    tNew.show("tNew-after"); // restored to content from file

    std::cout << "Object loaded from file" << std::endl;

    return 0;
}

