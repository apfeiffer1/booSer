
#include <iostream>
#include <vector>

class Test1 {

 public:
  Test1();
  ~Test1();

 public: 
  void foo ();

 private:
  void helper();

};

class TestStruct1 {
public:
  TestStruct1() : a(0) {}

  void add(float x);
  void show(const std::string &);
  
  struct EmbStruct1 {
    float b;
  };

  typedef std::vector<EmbStruct1> EmbVect;

  EmbVect embedded;
  int a;

};

void TestStruct1::add(float x) { 
    EmbStruct1 tmp;
    tmp.b = x;
    embedded.push_back(tmp); 
}
void TestStruct1::show(const std::string &what) { 
    std::cout << what << ".a=" << a << std::endl;
    std::cout << what << ".embedded.size()=" << embedded.size() << std::endl;;
    EmbVect::const_iterator itr=embedded.begin();
    while (itr != embedded.end()) {
        std::cout << "element:" << (*itr).b << std::endl;
        itr++;
    }
}
