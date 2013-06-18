#include <iostream>
#include <string>
#include <boost/serialization/access.hpp> 
#include <boost/serialization/vector.hpp>    // replaces #include <vector>

class TestClass {
 public:
 TestClass() : a(0) {}
  void setA(int val) { a=val; }
  void add(float x);
  void show(const std::string &msg);
  bool operator==(const TestClass &rhs);

 private:
  std::vector<float> b;
  int a;

 private:
  friend class boost::serialization::access;
  template<class Archive>
    void serialize(Archive & ar, const unsigned int version) {
    ar & BOOST_SERIALIZATION_NVP(a);
    ar & BOOST_SERIALIZATION_NVP(b);
  }
};

// inline methods here to simplify things ... 
void TestClass::add(float x) { 
    b.push_back(x); 
}
void TestClass::show(const std::string &what) { 
    std::cout << what << ".a=" << a << std::endl;
    std::cout << what << "b.size()=" << b.size() << std::endl;;
    std::vector<float>::const_iterator itr=b.begin();
    while (itr != b.end()) {
        std::cout << "element:" << (*itr) << std::endl;
        itr++;
    }
}
