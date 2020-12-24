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

typedef pair<string, int> tower;

int main()
{
  map<string, string> tparents;
  vector<string> towers;

  regex s_rx("(\\w+)+");
  string line;
  while (getline(cin, line))
  {
    regex_iterator<string::iterator> s(line.begin(), line.end(), s_rx);
    regex_iterator<string::iterator> send;
    string root;
    int value;
    while (s != send)
    {
      cout << line << " : " << s->str() << endl;
      if (root.empty())
      {
        root = s->str();
        towers.push_back(root);
        s++;
        value = stoi(s->str());
        s++;
      }
      else
      {
        tparents[s->str()] = root;
        s++;
      }
    }
  }
  for (auto t : towers)
  {
    if (tparents.find(t) == tparents.end())
    {
      cout << "root: " << t << endl;
      break;
    }
  }
  return 0;
}
