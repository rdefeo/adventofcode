#include <cmath>
#include <cstdio>
#include <vector>
#include <iostream>
#include <sstream>
#include <algorithm>
#include <map>
#include <string>
#include <queue>
#include <deque>
#include <set>
#include <regex>
using namespace std;


int main() {
  vector<string> input;
  string line;
  while(getline(cin,line)) {
    input.push_back(line);
  }

  string output;
  for(int i = 0; i < 8; i++) {
    map<char,int> count;
    for(int j = 0; j < input.size(); j++) {
      count[input[j][i]]++;
    }
    pair<char,int> most(' ',9999);
    for(auto c : count) {
      //      cout << c.first << " : " << c.second << endl;
      if(c.second < most.second) {
	most = c;
      }
    }
    output.push_back(most.first);    
  }

  
  cout << output << endl;
  return 0;
}


