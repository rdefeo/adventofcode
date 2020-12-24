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
  int chksum = 0;

  /*
  for(int y = 0; y < 16; y++) {
    int mn = 1000000;
    int mx = 0;
    for(int x = 0; x < 16; x++) {
      int num;
      cin >> num;
      mn = min(mn,num);
      mx = max(mx,num);
    }
    chksum += (mx-mn);
  }
  */

  for(int y = 0; y < 16; y++) {
    vector<int> vec(16);
    for(int x = 0; x < 16; x++) {
      cin >> vec[x];
    }
    sort(vec.begin(),vec.end(),greater<int>());

    for(int i = 0; i < vec.size()-1; i++) {
      for(int j = i+1; j < vec.size(); j++) {
	cout << "checking: " << vec[i] << ", " << vec[j] << endl;
	if(vec[i] % vec[j] == 0) {
	  chksum += (vec[i]/vec[j]);
	  break;
	}
      }
    }
  }
  
  cout << "chksum: " << chksum << endl;
  return 0;
}


