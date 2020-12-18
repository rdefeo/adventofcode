#include <cmath>
#include <cstdio>
#include <vector>
#include <iostream>
#include <sstream>
#include <algorithm>
#include <map>
#include <set>
#include <string>
#include <curses.h>
using namespace std;

int dirX[] = { -1, 0, 1, -1, 1, -1, 0, 1 };
int dirY[] = { -1, -1, -1, 0, 0, 1, 1, 1 };
int width = 0;

bool in_map(int x, int y) {
  return (x >= 0 && x < width && y >= 0 && y < width);
}

typedef unsigned long ulong;
void set_bit(ulong &num, int bit, int x) {
  num ^= (-x ^ num) & (1UL << bit);
}
bool get_bit(ulong num, int bit) {
  return (num >> bit) & 1UL;
}

ulong convert(const vector<string> &state) {
  ulong s = 0;
  for(int y = 0; y < width; y++) {
    for(int x = 0; x < width; x++) {
      set_bit(s,y*width+x,(state[y][x]=='#'?1:0));
    }
  }
  return s;
}

vector<string> step(vector<string> &state) {
  
  vector<string> nstate(state.size());

  // set corners
  state[0][0] = '#';
  state[0][width-1] = '#';
  state[width-1][0] = '#';
  state[width-1][width-1] = '#';
  
  for(int y = 0; y < state.size(); y++) {
    for(int x = 0; x < state[y].size(); x++) {
      if(state[y][x] == '#') {
	int lit = 0;
	for(int i = 0; i < 8; i++) {
	  int nx = x+dirX[i];
	  int ny = y+dirY[i];
	  if(in_map(nx,ny) && state[ny][nx] == '#')
	    lit++;
	}
	if(lit == 2 || lit == 3) nstate[y].push_back('#');
	else nstate[y].push_back('.');
      }
      if(state[y][x] == '.') {
	int lit = 0;
	for(int i = 0; i < 8; i++) {
	  int nx = x+dirX[i];
	  int ny = y+dirY[i];
	  if(in_map(nx,ny) && state[ny][nx] == '#')
	    lit++;
	}
	if(lit == 3) nstate[y].push_back('#');
	else nstate[y].push_back('.');
      }
    }
  }
  // set corners
  nstate[0][0] = '#';
  nstate[0][width-1] = '#';
  nstate[width-1][0] = '#';
  nstate[width-1][width-1] = '#';
  return nstate;
}

int main() {
  vector<string> lights;
  
  string line;
  while(getline(cin,line)) {
    lights.push_back(line);
  }
  width = lights[0].size();
  cout << "width = " << width << endl;

  auto print = [&](vector<string> v){ for(auto s : v) cout << s << endl; };
  print(lights);

  vector<string> tmp(lights);
  int i = 0;
  while(i < 100) {
    tmp = step(tmp);
    //    cout << endl << "step " << 4-i << endl;
    //    print(tmp);
    i++;
  }

  
  // count lights
  int count = 0;
  for(auto y : tmp)
    for(auto x : y)
      if(x == '#')
	count++;
  cout << "lit: " << count << endl;
    
  return 0;
}


