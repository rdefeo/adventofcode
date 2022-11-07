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

//             N  E  S  W
int dir[] =  { 0, 1, 2, 3 };

void make_step(int &x, int &y, int &d, char nd, int dist) {
  if(d == 0) {
    x += (nd == 'R' ? dist : -dist);
    d = (nd == 'R' ? 1 : 3);
  }
  else if(d == 1) {
    y += (nd == 'R' ? dist : -dist);
    d = (nd == 'R' ? 2 : 0);
  }
  else if(d == 2) {
    x += (nd == 'R' ? -dist : dist);
    d = (nd == 'R' ? 3 : 1);
  }
  else if(d == 3) {
    y += (nd == 'R' ? -dist : dist);
    d = (nd == 'R' ? 0 : 2);
  }
}

int intersect(pair<int,int> a1, pair<int,int> a2, pair<int,int> b1, pair<int,int> b2) {
  // a |, b -
  if(a1.first == a2.first && b1.second == b2.second &&
     max(a1.second,a2.second) > b1.second && min(a1.second,a2.second) < b1.second &&
     max(b1.first,b2.first) > a1.first && min(b1.first,b2.first) < a1.first)
    return a1.first+b1.second;
  // a -, b |
  if(a1.second == a2.second && b1.first == b2.first &&
     max(a1.first,a2.first) > b1.first && min(a1.first,a2.first) < b1.first &&
     max(b1.second,b2.second) > a1.second && min(b1.second,b2.second) < a1.second)
    return a1.second+b1.first;;
  return 0;
}

int main() {
  regex srx("([RL]\\d+)");

  string inp;
  getline(cin,inp);
  regex_iterator<string::iterator> rit(inp.begin(),inp.end(),srx);
  regex_iterator<string::iterator> rend;

  vector<pair<int,int>> points;
  int x = 0;
  int y = 0;
  int d = 0; // start N
  points.push_back({x,y});
  while(rit != rend) {
    make_step(x,y,d,rit->str()[0],stoi(rit->str().substr(1)));
    points.push_back({x,y});
    // if back, back-1 intersect with any prev
    if(points.size() > 2) {
      auto a = points.rbegin();
      auto b = points.rbegin()+1;
      for(auto it = points.begin(); it <  points.end()-2; it++) {
	int dist;
	if(dist = intersect(*a,*b,*it,*(it+1))) {
	  cout << "first repeat: " << dist << endl;
	}
      }
    }
    
    cout << x << ", " << y << endl;
    rit++;
  }
  cout << x+y << endl;

  for(auto it = points.begin()+1; it < points.end()-1; it++) {
    for(auto jt = points.begin(); jt < it; jt++) {
      
    }
  }
  return 0;
}


