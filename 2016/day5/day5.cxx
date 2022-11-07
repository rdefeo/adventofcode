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
#include "md5.h"
using namespace std;


int main() {
  string door_id("ffykfhsq");
  string pwd("........");

  int idx = 0;
  while(any_of(pwd.begin(),pwd.end(),[&](char c){return c == '.';})) {
    string hash_str(door_id + to_string(idx));
    string result = MD5(hash_str).hexdigest();
    if(result.substr(0,5) == "00000") {
      if(result[5] >= '0' && result[5] < '8' && pwd[result[5]-'0'] == '.') {
	pwd[result[5]-'0'] = result[6];
	cout << "pwd: " << pwd << endl;
      }
    }
    idx++;
    if(idx % 100000 == 0) cout << idx << endl;
  }
  cout << pwd << endl;
  return 0;
}


