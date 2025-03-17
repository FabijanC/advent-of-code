#include <bits/stdc++.h>

using namespace std;

int main(int argc, char** argv) {
    FILE *f;
    f = fopen(argv[1], "r");
    vector<int> v;
    char c;
    while((c = fgetc(f)) != -1) {
        v.push_back(c - '0');
    }

    for (int step = 0; step < 100; ++step) {
        // IZVRSIO SE KOD U JAVI, NE MORAM DALJE
    }

    cout << endl;
}