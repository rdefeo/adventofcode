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


struct Ingredient {
  string name;
  int c;
  int d;
  int f;
  int t;
  int cal;
};

vector<Ingredient> I;

pair<long long,int> compute_score(int a, int b, int c, int d, int e) {
  //  cout << "scoring: " << a << ", " << b << ", " << c << ", " << d;
  long long s = 0;
  long long cap = I[0].c*a + I[1].c*b + I[2].c*c + I[3].c*d;
  long long dur = I[0].d*a + I[1].d*b + I[2].d*c + I[3].d*d;
  long long fla = I[0].f*a + I[1].f*b + I[2].f*c + I[3].f*d;
  long long tex = I[0].t*a + I[1].t*b + I[2].t*c + I[3].t*d;
  long long cal = I[0].cal*a + I[1].cal*b + I[2].cal*c +I[3].cal*d;
  //  cout << endl << "  : " << cap << " " << dur << " " << fla << " " << tex << endl;
  if(cap < 0) cap = 0;
  if(dur < 0) cap = 0;
  if(fla < 0) cap = 0;
  if(tex < 0) cap = 0;
  s = cap * dur * fla * tex;
  //  cout << " = " << s << endl;
  return {s,cal};
}

int main() {
  regex c_rx("(\\w+): capacity ([-]?\\d+), durability ([-]?\\d+), flavor ([-]?\\d+), texture ([-]?\\d+), calories ([-]?\\d+)");


  string line;
  while(getline(cin,line)) {
    smatch m;
    if(regex_match(line,m,c_rx)) {
      Ingredient i({m[1],stoi(m[2]),stoi(m[3]),stoi(m[4]),stoi(m[5]),stoi(m[6])});
      I.push_back(i);
    }
  }

  map<tuple<int,int,int,int>,pair<long long,int>> cookies;
  /*
  for(int a = 0; a < 100; a++) {
    for(int b = 0; b <= 100-a; b++) {
      if(a+b == 100)
	cookies[{a,b,0,0}] = compute_score(a,b,0,0,0);
    }
  }
  */
  
  for(int a = 0; a < 100; a++) {
    for(int b = 0; b <= 100-a; b++) {
      for(int c = 0; c <= 100-b; c++) {
	for(int d = 0; d <= 100-c; d++) {
	  if(a+b+c+d == 100) {
	    pair<long long,int> s = compute_score(a,b,c,d,0);
	    if(s.second == 500)
	      cookies[{a,b,c,d}] = s;
	  }
	}
      }
    }
  }
  
  long long ms = 0;
  for(auto c : cookies) {
    ms = max(ms,c.second.first);
  }
  cout << "max score: " << ms << endl << endl;;
  
  return 0;
}


