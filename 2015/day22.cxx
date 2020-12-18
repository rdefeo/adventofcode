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

class Item {
public:
  Item(string n, int c, int d, int a, int h = 0) : name(n), cost(c), damage(d), armor(a), heal(h) {}
  string name;
  int cost;
  int damage;
  int armor;
  int heal;
};

vector<Item> weapons = { Item("Dagger", 8, 4, 0),
			 Item("Shortsword", 10, 5, 0),
			 Item("Warhammer", 25, 6, 0),
			 Item("Longsword", 40, 7, 0),
			 Item("Greataxe", 74, 8, 0) };

vector<Item> armors = { Item("Leather", 13, 0, 1),
			Item("Chainmail", 31, 0, 2),
			Item("Splintmail", 53, 0, 3),
			Item("Bandedmail", 75, 0, 4),
			Item("Platemail", 102, 0, 5) };

vector<Item> rings = { Item("Damage +1", 25, 1, 0),
		       Item("Damage +2", 50, 2, 0),
		       Item("Damage +3", 100, 3, 0),
		       Item("Defense +1", 20, 0, 1),
		       Item("Defense +2", 40, 0, 2),
		       Item("Defense +3", 80, 0, 3) };

vector<Item> spells = { Item("Magic Missile", 53, 4, 0),
			Item("Drain", 73, 4, 0, 2),
			Item("Magic Missile", 53, 4, 0),
			Item("Magic Missile", 53, 4, 0),
			

class Person {
public:
  Person(string n, int p, int d, int a) : name(n), hp(p), damage(d), armor(a) {}
  string name;
  int hp;
  int damage;
  int armor;
};

int main() {
  Person attacker("attacker",100,8,2);

  auto item_dam = [&](vector<Item> r) {
		    int d = 0;
		    for(auto rr : r)
		      d += rr.damage;
		    return d;
		  };
  auto item_arm = [&](vector<Item> r) {
		    int a = 0;
		    for(auto rr : r)
		      a += rr.armor;
		    return a;
		  };
  auto item_cos = [&](vector<Item> r) {
		    int g = 0;
		    for(auto rr : r)
		      g += rr.cost;
		    return g;
		  };

  auto item_nam = [&](vector<Item> r) {
		    for(auto rr : r)
		      cout << rr.name << ", ";
		  };

  auto fight = [&](Item w, vector<Item> a, vector<Item> r, Person att, int &gold) {
		 cout << "fight: " << w.name << ", ";
		 item_nam(a);
		 cout << ", ";
		 item_nam(r);
		 gold = w.cost + item_cos(a) + item_cos(r);
		 int hp = 100;
		 while(hp >= 0 || att.hp >= 0) {
		   int d = (w.damage + item_dam(r)) - att.armor;
		   if(d <= 0) d = 1;
		   att.hp -= d;
		   if(att.hp <= 0) break;
		   d = att.damage - (item_arm(a) + item_arm(r));
		   if(d <= 0) d = 1;
		   hp -= d;
		   if(hp <= 0) break;
		 }
		 if(hp > 0) {
		   cout << " - Won! " << gold << endl;
		   return true;
		 } else { cout << " - LOSE" << endl; }
		 return false;
	       };
  
  int min_gold = 1000000;
  int max_gold = 0;
  for(auto w : weapons) {
    for(int ai = 0; ai <= 1; ai++) {
      vector<bool> mya(armors.size(),false);
      fill(mya.end()-ai,mya.end(),true);
      do {
	vector<Item> a;
	for(int k = 0; k < mya.size(); k++)
	  if(mya[k])
	    a.push_back(armors[k]);
	for(int ri = 0; ri <= 2; ri++) {
	  vector<bool> myr(rings.size(),false);
	  fill(myr.end()-ri,myr.end(),true);
	  do {
	    vector<Item> r;
	    for(int m = 0; m < myr.size(); m++)
	      if(myr[m])
		r.push_back(rings[m]);
	    // fight with w, a, r[]
	    int gold;
	    bool win = fight(w,a,r,attacker,gold);
	    if(win) min_gold = min(gold,min_gold);
	    else max_gold = max(gold,max_gold);
	  } while(next_permutation(myr.begin(),myr.end()));
	}
      } while(next_permutation(mya.begin(),mya.end()));
    }
  }
  cout << "min gold: " << min_gold << endl;
  cout << "max gold: " << max_gold << endl;
  return 0;
}


