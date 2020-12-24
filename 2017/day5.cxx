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
  vector<int> inst;
  int n;
  while(cin >> n) {
    inst.push_back(n);
  }

  int steps = 0;
  int pc = 0;
  while(pc >= 0 && pc < inst.size()) {
    int old_pc = pc;
    int off = inst[pc];
    pc += off;
    inst[old_pc] += (off >= 3 ? -1 : 1);
    steps++;
  }

  cout << "steps: " << steps << endl;
  
  return 0;
}


