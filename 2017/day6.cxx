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
  vector<int> blocks;
  int mem;
  while(cin >> mem) {
    blocks.push_back(mem);
  }

  map<vector<int>,int> hist;
  int cycles = 0;
  for(auto b : blocks) cout << b; cout << endl;
  while(hist.find(blocks) == hist.end()) {
    hist[blocks] = cycles;
    int m = 0;
    for(int i = 0; i < blocks.size(); i++) {
      m = max(blocks[i],m);
    }
    int mi = 0;
    for(int i = 0; i < blocks.size(); i++) {
      if(blocks[i] == m) { mi = i; break; }
    }
    
    int d = blocks[mi]; // amount of memory to distribute
    blocks[mi] = 0;
    int i = (mi+1)%blocks.size();
    while(d--) {
      blocks[i++%blocks.size()]++;
    }
    for(auto b : blocks) cout << b << " "; cout << endl;    
    cycles++;
  }
  cout << "cycles: " << cycles-hist[blocks] << endl;
  return 0;
}


