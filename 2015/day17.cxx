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
using namespace std;


int main() {
  vector<int> containers;
  int c;
  while(cin >> c) {
    containers.push_back(c);
  }

  int comb = 0;
  int num = containers.size();
  map<int,int> nc;
  for(int r = 1; r < num; r++) {
    vector<bool> v(num);
    fill(v.end()-r,v.end(),true);

    do {
      int sum = 0;
      for(int i = 0; i < num; i++) {
	if(v[i])
	  sum += containers[i];
      }
      if(sum == 150) {
	comb++;
	nc[r]++;
      }
    } while(next_permutation(v.begin(),v.end()));
  }
  cout << "comb: " << comb << endl;
  cout << "nc: " << nc.begin()->second << endl;

  return 0;
}


