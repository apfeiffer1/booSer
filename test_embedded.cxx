
#include "test_embedded_serialize.icc"

int main() {
    // create and open a character archive for output
    std::string arFileName = "test1.boostArchive";
    std::ofstream ofs(arFileName.c_str());

    // create class instance
    TestStruct1 t1;
    
    // add some data:
    t1.a = 42;
    t1.add(42.);
    
    // save data to archive
    {
        boost::archive::text_oarchive oa(ofs);
        // write class instance to archive
        oa << t1;
        // archive and stream closed when destructors are called
    }
    t1.show("t1");

    // ... some time later restore the class instance to its orginal state
    TestStruct1 tNew;
    tNew.show("tNew-before");
    {
        // create and open an archive for input
        std::ifstream ifs(arFileName.c_str());
        boost::archive::text_iarchive ia(ifs);
        // read class state from archive
        ia >> tNew;;
        // archive and stream closed when destructors are called
    }
	tNew.show("tNew-after");
    return 0;
}

