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

regex rx("([a-z\\-]+)(\\d+)\\[(\\w+)\\]$");

int check_room(string room) {
  auto get_count = [&](string room, char c){
		     int count = 0;
		     for(auto r : room)
		       if(r == c) count++;
		     return count;
		   };

  int sector = 0;
  smatch m;
  if(regex_match(room,m,rx)) {
    string room(m[1]);
    sector = stoi(m[2]);
    string chk(m[3]);

    map<char,int> counts;
    for(auto r : room) {
      if(r != '-')
	counts[r]++;
    }
    vector<pair<char,int>> sorted;
    for(auto c : counts) {
      sorted.push_back(c);
    }
    sort(sorted.begin(),sorted.end(),[&](pair<char,int> &l,pair<char,int> &r){
				       if(l.second > r.second) return true;
				       else if(l.second == r.second) return l.first < r.first;
				       return false;});
    for(int i = 0; i < chk.size(); i++) {
      if(chk[i] != sorted[i].first) return 0;
    }
  } else {
    cout << "failed match!" << endl;
  }
  return sector;
}

string rotate(string room) {
  smatch m;
  if(regex_match(room,m,rx)) {
    string room(m[1]);
    int sector = stoi(m[2]);
    string chk(m[3]);

    for(auto &r : room) {
      if(r == '-') { r = ' '; continue; }
      r += sector % 26;
      if(r > 'z') r -= 26;
    }
    cout << sector << " : ";
    return room;
  }
  return "";
}

int main() {
  string room;
  int sid_sum = 0;
  while(getline(cin,room)) {
    sid_sum += check_room(room);

    cout << rotate(room) << endl;
  }
  cout << "sector id sum: " << sid_sum << endl;
  return 0;
}


