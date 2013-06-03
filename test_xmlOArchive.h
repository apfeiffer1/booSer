
#include <boost/serialization/vector.hpp>    // includes <vector>

class TestStruct {
public:
  TestStruct() : a(0) {}

  void add(float x);
  void show();
	
  bool operator==(const TestStruct &rhs);
  
  std::vector<float> b;
  int a;

  friend class boost::serialization::access;
  template<class Archive>
      void serialize(Archive & ar, const unsigned int version)
      {
          ar & BOOST_SERIALIZATION_NVP(a);
          ar & BOOST_SERIALIZATION_NVP(b);
      }
};

void TestStruct::add(float x) { 
    b.push_back(x); 
}

void TestStruct::show() { 
    std::cout << "a=" << a << std::endl;
	std::cout << "len(b)="<< b.size() << std::endl;

	std::vector<float>::iterator it = b.begin();
	while (it != b.end() ) {
		std::cout << "   " << *it << std::endl;
		it++;
	}

}

bool TestStruct::operator==(const TestStruct &rhs) {
	return ( (a==rhs.a) && (b==rhs.b) ); 
}
