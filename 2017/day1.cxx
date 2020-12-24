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
  string input;
  getline(cin,input);

  int sum = 0;
  for(int i = 0; i < input.size()-1; i++) {
    if(input[i] == input[i+1]) {
      sum += input[i]-'0';
    }
  }
  if(input[input.size()-1] == input[0])
    sum += input[0]-'0';

  cout << "sum: " << sum << endl;

  int dist = input.size()/2;
  sum = 0;
  for(int i = 0; i < input.size(); i++) {
    int ni = i + dist;
    //    cout << "ni: " << ni << " - " << i << endl;
    if(ni >= input.size()) ni %= input.size();
    if(input[i] == input[ni]) {
      sum += input[i]-'0';
    }
  }
  cout << "sum: " << sum << endl;
  
  return 0;
}


