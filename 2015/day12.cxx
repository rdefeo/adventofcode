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

int part1(string line) {
  // Part 1
  regex num_rx("([-]?\\d+){1,}");

  regex_iterator<string::iterator> rit(line.begin(),line.end(),num_rx);
  regex_iterator<string::iterator> rend;
  
  int sum = 0;
  while(rit != rend) {
    //    cout << rit->str() << endl;
    sum += stoi(rit->str());
    rit++;
  }
  return sum;
}

int main() {

  string line;
  getline(cin,line);
  
  cout << "sum: " << part1(line) << endl;


  // Part 2

  // find all objects with no sub-objects, but with "red"
  // find all objects with no sub-objects

  regex obj_red_rx("\\{[^\\{}]*:\"red\"[^\\{}]*\\}");
  regex obj_rx("\\{([^\\{}]*)\\}");

  cout << "line size: " << line.size() << endl;

  bool ready = false;
  while(!ready) {
    ready = true;
    while(regex_match(line,obj_red_rx)) {
      cout << "match!" << endl;
      ready = false;
      line = regex_replace(line,obj_red_rx,"\"r\""); // remove all obj that contain red
    }
    line = regex_replace(line,obj_rx,"[$1]");
  }
  cout << "line size: " << line.size() << endl;
  cout << "sum: " << part1(line) << endl;
  
  return 0;
}


