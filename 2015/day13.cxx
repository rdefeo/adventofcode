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
  regex hu_rx("^(\\w+) would (lose|gain) (\\d+) happiness units by sitting next to (\\w+)\\.$");

  set<string> all_names;
  map<pair<string,string>,int> happiness;
  string line;
  while(getline(cin,line)) {
    smatch fields;
    if(regex_match(line,fields,hu_rx)) {
      //      cout << fields[1] << " " << fields[2] << " " << fields[3] << " " << fields[4] << endl;
      all_names.insert(fields[1]);
      int units = stoi(fields[3]);
      happiness[{fields[1],fields[4]}] = (fields[2] == "gain" ? units : -units);
      happiness[{fields[1],fields[4]}] = (fields[2] == "gain" ? units : -units);
    }
  }
  vector<string> names;
  for(auto a : all_names)
    names.push_back(a);
  sort(names.begin(),names.end());

  cout << "Part 1:" << endl;
  int max_h = 0;
  int p = 0;
  do {
    int h = 0;
    for(int i = 0; i < names.size()-1; i++) {
      h += happiness[{names[i],names[i+1]}];
      h += happiness[{names[i+1],names[i]}];
    }
    h += happiness[{names[names.size()-1],names[0]}];
    h += happiness[{names[0],names[names.size()-1]}];
    max_h = max(h,max_h);
    p++;
  } while(next_permutation(names.begin(),names.end()));

  cout << "perms: " << p << endl;
  cout << "max happiness: " << max_h << endl;
  
  for(auto n : names) {
    happiness[{"Roberto",n}] = 0;
    happiness[{n,"Roberto"}] = 0;
  }
  names.push_back("Roberto");
  sort(names.begin(),names.end());
  
  cout << endl << "Part 2:" << endl;
  max_h = 0;
  p = 0;
  do {
    int h = 0;
    for(int i = 0; i < names.size()-1; i++) {
      h += happiness[{names[i],names[i+1]}];
      h += happiness[{names[i+1],names[i]}];
    }
    h += happiness[{names[names.size()-1],names[0]}];
    h += happiness[{names[0],names[names.size()-1]}];
    max_h = max(h,max_h);
    p++;
  } while(next_permutation(names.begin(),names.end()));

  cout << "perms: " << p << endl;
  cout << "max happiness: " << max_h << endl;
  
  return 0;
}


