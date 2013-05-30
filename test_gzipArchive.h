
#include <boost/serialization/vector.hpp>    // includes <vector>

class TestStruct2 {
public:
  TestStruct2() : a(0) {}

  void add(float x);
  void show();
	
  bool operator==(const TestStruct2 &rhs);
  
  std::vector<float> b;
  int a;

  friend class boost::serialization::access;
  template<class Archive>
      void serialize(Archive & ar, const unsigned int version)
      {
          ar & a;
          ar & b;
      }
};

void TestStruct2::add(float x) { 
    b.push_back(x); 
}
void TestStruct2::show() { 
    std::cout << "a=" << a << std::endl;
	std::cout << "len(b)="<< b.size() << std::endl;

	std::vector<float>::iterator it = b.begin();
	while (it != b.end() ) {
		std::cout << "   " << *it << std::endl;
		it++;
	}

}

bool TestStruct2::operator==(const TestStruct2 &rhs) {
	return ( (a==rhs.a) && (b==rhs.b) ); 
}
