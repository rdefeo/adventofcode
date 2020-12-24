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
  int num_valid = 0;
  string pwd;

  

  while(getline(cin,pwd)) {
    set<string> words;
    string word;
    bool valid = true;
    bool part1 = false;
    
    auto valid_word = [&](string word){
			if(part1) return words.count(word) > 0;
			else {
			  // get all anagrams of 'word' and check words
			  sort(word.begin(),word.end());
			  do {
			    if(words.count(word) > 0) return false;
			  } while(next_permutation(word.begin(),word.end()));
			}
			return true;
		      };
    

    for(int i = 0; i < pwd.size(); i++) {
      if(pwd[i] != ' ')
	word.push_back(pwd[i]);
      else {
	if(!valid_word(word)) { valid = false; break; }
	else { words.insert(word); word = ""; }
      }	
    }
    if(!valid_word(word)) valid = false;
    if(valid) num_valid++;
  }

  cout << "num valid: " << num_valid << endl;
  
  return 0;
}


