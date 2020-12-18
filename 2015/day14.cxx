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

struct Deer {
  string name;
  int v;
  int t;
  int r;
  bool flying;
  int dist;
  int t_remaining;
  int points;
};

int main() {
  regex r_rx("(\\w+) can fly (\\d+) km/s for (\\d+) seconds, but then must rest for (\\d+) seconds.");

  vector<Deer> deer;
  string line;
  while(getline(cin,line)) {
    smatch m;
    if(regex_match(line,m,r_rx)) {
      Deer d({m[1],stoi(m[2]),stoi(m[3]),stoi(m[4]),true,0,stoi(m[3]),0});
      deer.push_back(d);
    }
  }

  int time = 2503;
  /*
  // Part 1
  for(auto d : deer) {
    int dist = 0;
    int t = 0;
    while(t < time) {
      if(t + d.t < time) {
	dist += d.v*d.t;
	t += d.t;
      } else {
	dist += d.v*(time-t);
	break;
      }
      t += d.r;
    }
    cout << d.name << " " << dist << endl;
  }
  */

  int t = 0;
  while(t < time) {
    for(auto &d : deer) {
      if(d.flying) {
	d.dist += d.v;
      }
      d.t_remaining--; // whether flying or resting
      if(d.t_remaining == 0) {
	d.flying = !d.flying;
	if(d.flying)
	  d.t_remaining = d.t;
	else
	  d.t_remaining = d.r;
      }
    }
    int md = 0;
    for(auto d : deer) 
      md = max(d.dist,md);
    for(auto &d : deer)
      if(d.dist == md)
	d.points++;
    t++;
  }

  for(auto d : deer)
    cout << d.name << " " << d.points << endl;
  return 0;
}


