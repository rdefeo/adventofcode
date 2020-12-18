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
  string line;
  regex m_rx("(\\w+) => (\\w+)");
  map<string,vector<string>> molmap;
  map<string,string> rmolmap;
  while(getline(cin,line)) {
    smatch m;
    if(regex_match(line,m,m_rx)) {
      molmap[m[1]].push_back(m[2]);
      rmolmap[m[2]] = m[1];
      //      cout << m[1] << " => " << m[2] << endl;
    }
  }

  string molecule("CRnCaCaCaSiRnBPTiMgArSiRnSiRnMgArSiRnCaFArTiTiBSiThFYCaFArCaCaSiThCaPBSiThSiThCaCaPTiRnPBSiThRnFArArCaCaSiThCaSiThSiRnMgArCaPTiBPRnFArSiThCaSiRnFArBCaSiRnCaPRnFArPMgYCaFArCaPTiTiTiBPBSiThCaPTiBPBSiRnFArBPBSiRnCaFArBPRnSiRnFArRnSiRnBFArCaFArCaCaCaSiThSiThCaCaPBPTiTiRnFArCaPTiBSiAlArPBCaCaCaCaCaSiRnMgArCaSiThFArThCaSiThCaSiRnCaFYCaSiRnFYFArFArCaSiRnFYFArCaSiRnBPMgArSiThPRnFArCaSiRnFArTiRnSiRnFYFArCaSiRnBFArCaSiRnTiMgArSiThCaSiThCaFArPRnFArSiRnFArTiTiTiTiBCaCaSiRnCaCaFYFArSiThCaPTiBPTiBCaSiThSiRnMgArCaF");

  //    string molecule("HOH");
  set<string> distinct;

  cout << molecule << endl;
  /*
  for(int i = 0; i < molecule.size(); i++) {
    string one(molecule.substr(i,1));
    string two(molecule.substr(i,2));

    //  cout << i << ": " << one << " " << two << endl;
    if(molmap.find(one) != molmap.end()) {
      for(auto m : molmap[one])
	distinct.insert(molecule.substr(0,i)+m+molecule.substr(i+1));
    }
    if(one == two) continue;
    if(molmap.find(two) != molmap.end()) {
      for(auto m : molmap[two])
	distinct.insert(molecule.substr(0,i)+m+molecule.substr(i+2));
    }
  }

  for(auto d : distinct) {
    cout << d << endl;
  }
  cout << "distinct: " << distinct.size() << endl;
  */

  auto count_str = [&](string s){
		     int c = 0;
		     for(int i = molecule.find(s); i != string::npos; i = molecule.find(s,i+1), c++) {}
		     return c;
		   };
  auto count_sym = [&](string s) {
		     return count_if(molecule.begin(),
				     molecule.end(),
				     [](char c){return c>='A' && c<='Z';});
		   };
  cout << count_sym(molecule) - count_str("Rn") - count_str("Ar") - 2*count_str("Y") -1;
    
    
  string e("e");
  queue<pair<string,int>> meds;
  meds.push({molecule,0});

  long long c = 0;
  while(!meds.empty()) {
    c++;
    pair<string,int> p = meds.front();
    meds.pop();

    if(c % 10000 == 0)
      cout << p.first << ", " << p.second << endl;
    
    string tmp = p.first;
    if(tmp == e) {
      cout << "steps: " << p.second << endl;
      break;
    }
    
    for(auto rm : rmolmap) {
      int pos = tmp.size()-1;
      while((pos = tmp.rfind(rm.first,pos)) != string::npos) {
	//	cout << endl << tmp << endl;
	//	cout << "found : " << rm.first << " at pos " << pos << endl;
	string new_tmp = tmp.substr(0,pos)+rm.second+tmp.substr(pos+rm.first.size());
	//	cout << new_tmp << endl;
	meds.push({new_tmp,p.second+1});
	//	pos += rm.first.size()+1;
	pos--;
      }
    }
  }

  return 0;
}


