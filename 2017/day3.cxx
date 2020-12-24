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

  int num;
  cin >> num;

  map<pair<int,int>,int> mem;

  //            U  L  D  R
  int dir[] = { 0, 1, 2, 3 };

  int x = 0;
  int y = 0;

  mem[{x,y}] = 1;
  x++;

  auto sum8 = [&](int x, int y) {
		return mem[{x-1,y+1}] + mem[{x,y+1}] + mem[{x+1,y+1}] +
		  mem[{x-1,y}] + 0 + mem[{x+1,y}] +
		  mem[{x-1,y-1}] + mem[{x,y-1}] + mem[{x+1,y-1}];
	      };
  
  int d = 0;
  for(int i = 2; i <= num; i++) {
    cout << x << ", " << y << endl;
    mem[{x,y}] = sum8(x,y);

    if(mem[{x,y}] > num) {
      cout << "first larger: " << mem[{x,y}] << endl;
      break;
    }
    if(d == 0) {
      if(mem[{x-1,y}] == 0) { x--; d = 1; continue; }
      else y++;
    }	
    if(d == 1) {
      if(mem[{x,y-1}] == 0) { y--; d = 2; continue; }
      else x--;
    }	
    if(d == 2) {
      if(mem[{x+1,y}] == 0) { x++; d = 3; continue; }
      else y--;
    }	
    if(d == 3) {
      if(mem[{x,y+1}] == 0) { y++; d = 0; continue; }
      else x++;
    }	
  }

  for(auto m : mem) {
    if(m.second == num) {
      cout << m.first.first << ", " << m.first.second << endl;
      cout << abs(m.first.first)+abs(m.first.second) << endl;
      break;
    }
  }
  return 0;
}


