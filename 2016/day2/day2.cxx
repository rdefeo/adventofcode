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

int keys[] = { 1, 2, 3, 4, 5, 6, 7, 8, 9 };

int get_key(int &x, int &y) {
  //  cout << x << ", " << y;
  if(x < 0) x = 0;
  if(x > 2) x = 2;
  if(y < 0) y = 0;
  if(y > 2) y = 2;
  int k =keys[y*3+x];
  //  cout << " : " << x << ", " << y << " = " << k << endl;
  return k;
}

//       1
//     2 3 4
//   5 6 7 8 9    1
//     A B C
//       D

char keys2[] = { '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D' };

map<char,int> dir = { { 'U', 0 },
		      { 'R', 1 },
		      { 'D', 2 },
		      { 'L', 3 } };

map<char,vector<char>> k2dir = { { '1', { '1', '1', '3', '1' } },
				 { '2', { '2', '3', '6', '2' } },
				 { '3', { '1', '4', '7', '2' } },
				 { '4', { '4', '4', '8', '3' } },
				 { '5', { '5', '6', '5', '5' } },
				 { '6', { '2', '7', 'A', '5' } },
				 { '7', { '3', '8', 'B', '6' } },
				 { '8', { '4', '9', 'C', '7' } },
				 { '9', { '9', '9', '9', '8' } },
				 { 'A', { '6', 'B', 'A', 'A' } },
				 { 'B', { '7', 'C', 'D', 'A' } },
				 { 'C', { '8', 'C', 'C', 'B' } },
				 { 'D', { 'B', 'D', 'D', 'D' } } };

char get_key2(int &x, int &y) {
  
  
}

int main() {
  char c = '5';
  string line;
  vector<char> code;
  while(getline(cin,line)) {
    char nk;
    for(auto l : line) {
      nk = k2dir[c][dir[l]];
      c = nk;
    }
    code.push_back(c);
  }
  for(auto x : code)
    cout << x;
  cout << endl;
  
  /*
    // Part 1
  int x = 0;
  int y = 0;
  int k = get_key(x,y);
  vector<int> code;

  char c;
  string line;
  while(getline(cin,line)) {
    int nk;
    for(auto c : line) {
      //      cout << c << endl;
      if(c == 'U') y--;
      if(c == 'R') x++;
      if(c == 'L') x--;
      if(c == 'D') y++;
      //      nk = get_key(x,y);
      nk = get_ke2(x,y);
    }
    code.push_back(nk);
  }
  for(auto c : code) {
    cout << c;
  }
  */
  

  return 0;
}


