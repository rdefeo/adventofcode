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

  int limit = 34000000;
  int i = 800000;
  int inc = limit / 3400;

  auto get_sum = [&](int i){
		   int sum = 0;
		   int d = (int)sqrt((double)i)+1;
		   for(int j = 1; j <= d; j++) {
		     if(i % j == 0) {
		       sum += j;
		       sum += i/j;
		     }
		   }
		   return sum*10;
		 };
  
  i = 1;
  while(get_sum(i) < limit)
    i++;
  cout << "house: " << i << endl;
  
  auto get_sum2 = [&](int i){
		    int sum = 0;
		    int d = (int)sqrt((double)i)+1;
		    for(int j = 1; j <= d; j++) {
		      if(i % j == 0) {
			if(j <= 50)
			  sum += i/j;
			if(i/j <= 50)
			  sum += j;
		      }
		    }
		    return sum*11;
		  };

  i = 1;
  while(get_sum2(i) <= limit)
    i++;
  cout << "house: " << i << endl;
  return 0;
}


