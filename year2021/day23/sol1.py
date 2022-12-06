from collections import defaultdict as dd

HALLWAY = 0
ROOM_A = 1
ROOM_B = 2
ROOM_C = 3
ROOM_D = 4
ROOMS = [ROOM_A, ROOM_B, ROOM_C, ROOM_D]

NEAR = 0
FAR = 1
ROOM_PARTS = [NEAR, FAR]
ROOM_SIZE = len(ROOM_PARTS)

HALLWAY_SIZE = 11
EMPTY_HALLWAY = (None,) * HALLWAY_SIZE
CORRECT_CONFIG = (
    EMPTY_HALLWAY,
    ("A", "A"),
    ("B", "B"),
    ("C", "C"),
    ("D", "D"),
)

ROOM_INDEX2ROOM_NAME = {
    ROOM_A: "A", ROOM_B: "B", ROOM_C: "C", ROOM_D: "D"
}

ROOM_NAME2ROOM_INDEX = { value: key for key, value in ROOM_INDEX2ROOM_NAME.items()}

PRICE = { "A": 1, "B": 10, "C": 100, "D": 1000 }
ROOM2HALLWAY = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8
}
POPULATABLE_HALLWAY_INDICES = 0, 1, 3, 5, 7, 9, 10

class BlockedError(Exception):
    pass

def get_modifiable_copy(config):
    return {
        "hallway": list(config[HALLWAY]),
        "A": list(config[ROOM_A]),
        "B": list(config[ROOM_B]),
        "C": list(config[ROOM_C]),
        "D": list(config[ROOM_D]),
    }

def get_unmodifiable_copy(modifiable_config):
    return (
        tuple(modifiable_config["hallway"]),
        tuple(modifiable_config["A"]),
        tuple(modifiable_config["B"]),
        tuple(modifiable_config["C"]),
        tuple(modifiable_config["D"]),
    )

def is_valid(config):
    cnt = dd(int)
    for amphipod in config[HALLWAY]:
        cnt[amphipod] += 1
    for room_index in ROOMS:
        for room_part in ROOM_PARTS:
            amphipod = config[room_index][room_part]
            cnt[amphipod] += 1
    return cnt["A"] == cnt["B"] == cnt["C"] == cnt["D"] == ROOM_SIZE

def get_distance(modifiable_config, hallway_index, room_index, room_part):
    room_name = ROOM_INDEX2ROOM_NAME[room_index]
    room_hallway_index = ROOM2HALLWAY[room_name]
    smaller_index = min(room_hallway_index, hallway_index)
    bigger_index = max(room_hallway_index, hallway_index)

    for i in range(smaller_index + 1, bigger_index): # don't include limits; collision check is performed in the beginning of each rek
        if modifiable_config["hallway"][i]:
            raise BlockedError

    dist_within_hallway = bigger_index - smaller_index
    return dist_within_hallway + room_part + 1

def populate_room(config, current_hallway_index):
    config_copy = get_modifiable_copy(config)
    amphipod = config_copy["hallway"][current_hallway_index]
    if amphipod is None:
        raise BlockedError

    far_part = config_copy[amphipod][FAR]
    if far_part:
        if far_part == amphipod:
            desired_room_part = NEAR
        else:
            raise BlockedError
    else:
        desired_room_part = FAR
    
    if config_copy[amphipod][NEAR]:
        raise BlockedError

    config_copy["hallway"][current_hallway_index] = None
    config_copy[amphipod][desired_room_part] = amphipod
    desired_room_index = ROOM_NAME2ROOM_INDEX[amphipod]
    dist = get_distance(config_copy, current_hallway_index, desired_room_index, desired_room_part)
    return dist, get_unmodifiable_copy(config_copy)

def populate_hallway(config, current_room_index, current_room_part, desired_hallway_index):
    amphipod = config[current_room_index][current_room_part]
    if amphipod is None:
        raise BlockedError
    
    if current_room_part == FAR and config[current_room_index][NEAR] is not None:
        raise BlockedError

    config_copy = get_modifiable_copy(config)
    current_room_name = ROOM_INDEX2ROOM_NAME[current_room_index]
    config_copy[current_room_name][current_room_part] = None
    config_copy["hallway"][desired_hallway_index] = amphipod
    dist = get_distance(config_copy, desired_hallway_index, current_room_index, current_room_part)
    return dist, get_unmodifiable_copy(config_copy)

INF = int(1e18)
memo = dd(lambda: INF)
sol = INF
def rek(config, cost):
    global sol
    if cost >= sol:
        return

    if not is_valid(config):
        return

    if cost >= memo[config]:
        return
    memo[config] = cost

    if config == CORRECT_CONFIG:
        print("Found correct", cost)
        sol = min(cost, sol)
        return

    for correct_hallway_index in POPULATABLE_HALLWAY_INDICES:
        if config[HALLWAY][correct_hallway_index] is None:
            continue
        # moving from hallway to room
        amphipod = config[HALLWAY][correct_hallway_index]
        try:
            distance, config_copy = populate_room(config, correct_hallway_index)
            rek(config_copy, cost + distance * PRICE[amphipod])
        except BlockedError:
            pass

    for correct_hallway_index in POPULATABLE_HALLWAY_INDICES:
        if config[HALLWAY][correct_hallway_index]:
            continue

        for room_index in ROOMS:
            for room_part in ROOM_PARTS:
                amphipod = config[room_index][room_part]
                if not amphipod:
                    continue
                try:
                    distance, config_copy = populate_hallway(config, room_index, room_part, correct_hallway_index)
                    rek(config_copy, cost + distance * PRICE[amphipod])
                except BlockedError:
                    pass

initial_config = []
initial_config.append(EMPTY_HALLWAY)
for _ in ROOMS:
    initial_config.append(tuple(input()))
initial_config = tuple(initial_config)

rek(initial_config, 0)
print(memo[CORRECT_CONFIG])
