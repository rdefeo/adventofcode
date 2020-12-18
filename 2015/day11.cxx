#include <cmath>
#include <cstdio>
#include <vector>
#include <iostream>
#include <sstream>
#include <algorithm>
#include <map>
#include <string>
using namespace std;


int main() {
  string password;

  getline(cin,password);

  auto inc_3 = [&](string p) {
		 for(int i = 0; i < p.size()-2; i++) {
		   if(p[i] == p[i+1]-1 && p[i+1] == p[i+2]-1) {
		     return true;
		   } 
		 }
		 return false;
	       };
  auto bad_letter = [&](string p){
			for(auto i : p) 
			  if(i == 'i' || i == 'o' || i == 'l') return true;
			return false;
		    };
  auto pair_overlap = [&](string p){
			int p1 = -1; int p2 = -1;
			for(int i = 0; i < p.size()-1; i++) {
			  if(p[i] == p[i+1]) {
			    if(p1 == -1) p1 = i;
			    else p2 = i;
			  }
			}
			if(p2-p1 >= 2) { cout << "pair pass" << endl; return true; }
			return false;
		      };

  auto pwd_increment = [&](string &p) {
			 auto it = p.rbegin();
			 while(it != p.rend()) {
			   if(*it == 'z') {
			     *it = 'a';
			     it++;
			   } else {
			     (*it)++;
			     break;
			   }
			 }
		       };
  

  while(!inc_3(password) || bad_letter(password) || !pair_overlap(password)) {
    cout << "finding new password : ";
    pwd_increment(password);
    cout << password << endl;
  }


  cout << password << endl;
  
  return 0;
}


