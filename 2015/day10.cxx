#include <cmath>
#include <cstdio>
#include <vector>
#include <iostream>
#include <sstream>
#include <algorithm>
#include <map>
#include <string>
using namespace std;


int main() {
  string line;
  getline(cin,line);
  string out("");
  
  for(int num = 0; num < 50; num++) {
    out = "";
    int n = 1;
    for(int i = 0; i < line.size(); i+=n) {
      char c = line[i];
      n = 1;
      while(i+n < line.size() && c == line[i+n]) {
	n++;
      }
      out.push_back('0'+n);
      out.push_back(c);
    }
    line = out;
  }
  cout << line << endl;
  cout << line.size() << endl;
  
  return 0;
}


