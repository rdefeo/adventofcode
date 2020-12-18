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
  string line;
  regex s_rx("Sue (\\d+): (\\w+): (\\d+), (\\w+): (\\d+), (\\w+): (\\d+)");
  map<int,map<string,int>> sues;
  while(getline(cin,line)) {
    smatch m;
    if(regex_match(line,m,s_rx)) {
      sues[stoi(m[1])][m[2]] = stoi(m[3]);
      sues[stoi(m[1])][m[4]] = stoi(m[5]);
      sues[stoi(m[1])][m[6]] = stoi(m[7]);
    }
  }

  map<string,int> clues;
  clues["children"] = 3;
  clues["samoyeds"] = 2;
  clues["akitas"] = 0;
  clues["vizslas"] = 0;
  clues["cars"] = 2;
  clues["perfumes"] = 1;

  map<string,int> clues_gt;
  clues_gt["cats"] = 7;
  clues_gt["trees"] = 3;
  
  map<string,int> clues_lt;
  clues_lt["pomeranians"] = 3;
  clues_lt["goldfish"] = 5;
  
  for(auto s : sues) {
    bool found = true;
    for(auto c : clues) {
      if(s.second.find(c.first) != s.second.end() &&
	 s.second[c.first] != c.second)
      found = false;
    }
    for(auto c : clues_gt) {
      if(s.second.find(c.first) != s.second.end() &&
	 s.second[c.first] <= c.second)
      found = false;
    }
    for(auto c : clues_lt) {
      if(s.second.find(c.first) != s.second.end() &&
	 s.second[c.first] >= c.second)
      found = false;
    }

    if(found)
      cout << "sue: " << s.first << endl;
  }
  
  return 0;
}


