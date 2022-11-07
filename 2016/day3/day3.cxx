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
  int a1, b1, c1;
  int a2, b2, c2;
  int a3, b3, c3;
  int good = 0;
  while(cin >> a1 >> b1 >> c1 >> a2 >> b2 >> c2 >> a3 >> b3 >> c3) {
    if(a1 + a2 > a3 && a1 + a3 > a2 && a2 + a3 > a1)
      good++;
    if(b1 + b2 > b3 && b1 + b3 > b2 && b2 + b3 > b1)
      good++;
    if(c1 + c2 > c3 && c1 + c3 > c2 && c2 + c3 > c1)
      good++;
  }
  cout << good << endl;
  return 0;
}


