#include <bits/stdc++.h>
using namespace std;

typedef pair<int,int> pii;
// typedef pair<int, Config> pic;

struct Config {
    pii pos;
    set<char> collected_keys;
    int gScore;
    int fScore;
    Config(pii &pos, set<char> &collected_keys, int gScore, int fScore) :
        pos(pos), collected_keys(collected_keys), gScore(gScore), fScore(fScore) {}

    // bool operator<(const Config& other) {
    //     return pos == other.pos && collected_keys == other.collected_keys;
    // }
};

struct pic {
    int score;
    Config config;
    pic(const int& _score, const Config& _config) :
        score(_score), config(_config) {}
};

struct gScore_comparator {
    bool operator()(Config& config1, Config& config2) const {
        return config1.gScore < config2.gScore;
    }
};

int heuristic(const set<char> &keys) {
    return 0;
}

char OPEN = '.';
char START = '@';
char WALL = '#';
int INF = 1e9;

int HEIGHT;
int WIDTH;
int TOTAL_KEYS;
int TOTAL_DOORS;

pii DELTAS[] = {make_pair(-1,0), make_pair(1,0), make_pair(0,-1), make_pair(0,1)};

int main(int argc, char** argv) {
    map<char, pii> keys;
    set<char> doors;
    vector<vector<char> > area;

    pii start;

    // parse
    HEIGHT = area.size();
    WIDTH = area[0].size();
    TOTAL_KEYS = keys.size();
    TOTAL_DOORS = doors.size();
    area[start.first][start.second] = OPEN;

    set<char> start_collected_keys;
    Config start_config(start, start_collected_keys, 0,);
    unordered_map<Config, int> gScore;
    gScore[start_config] = 0;

    unordered_map<Config, int> fScore;
    fScore[start_config] = heuristic(start_config);

    set<pic, pic_comparator> openSet;
    openSet.insert(pic(fScore[start_config], start_config));

    while (!openSet.empty()) {
        const pic &optimal = *openSet.rbegin();
        openSet.erase(openSet.end());
        const Config &current = optimal.config;
        const int &current_fScore = optimal.score;
        
        if (current.collected_keys.size() == TOTAL_KEYS) {
            cout << current_fScore << endl;
            break;
        }

        for (const pii &delta: DELTAS) {
            const int& neighbor_i = current.pos.first + delta.first;
            if (neighbor_i < 0 || neighbor_i >= HEIGHT) {
                continue;
            }

            const int& neighbor_j = current.pos.second + delta.second;
            if (neighbor_j < 0 || neighbor_j >= WIDTH) {
                continue;
            }

            const char &kind = area[neighbor_i][neighbor_j];
            if (kind == WALL || doors.count(kind) && 0 == current.collected_keys.count(tolower(kind))) {
                continue;
            }

            pii neighbor_pos(neighbor_i, neighbor_j);
            set<char> neighbor_collected_keys;
            Config neighbor(neighbor_pos, neighbor_collected_keys);
            if (islower(kind)) {
                neighbor.collected_keys.insert(kind);
            }

            const int tentative_gScore = gScore[current] + 1;
            if (gScore.count(current) == 0 || tentative_gScore < gScore[current]) {
                gScore[neighbor] = tentative_gScore;
                fScore[neighbor] = gScore[neighbor] + heuristic(neighbor);
                pic neighbor_pair(fScore[neighbor], neighbor);
                if (!openSet.count(neighbor_pair)) {
                    openSet.insert(neighbor_pair);
                }
            }
        }
    }
}
