import sys
import math

class Reaction:
    def __init__(self, product_name, product_amount, reactants_amount):
        self.product_name = product_name
        self.product_amount = product_amount
        self.reactants_amount = reactants_amount

reactions = {}
with open(sys.argv[1]) as f:
    for line in f.readlines():
        left, right = map(lambda x: x.strip(), line.split(" => "))
        product_amount, product_name = right.split(" ")
        reactants_amount = {}
        for reactant_info in left.split(", "):
            reactant_amount, reactant_name = reactant_info.split(" ")
            reactants_amount[reactant_name] = int(reactant_amount)
        reactions[product_name] = Reaction(product_name, int(product_amount), reactants_amount)


# needed = {"FUEL": 1}
# spare = {}
# while True:
#     if len(needed) == 1 and "ORE" in needed:
#         break
#     new_needed = {}
#     # new_spare = {}
#     for chemical in needed:
#         if chemical == "ORE":
#             new_needed["ORE"] = needed["ORE"]
#             continue
#         amount = max(0, needed[chemical] - spare.get(chemical, 0))
#         # new_spare[chemical] = max(0, spare.get(chemical, 0) - needed[chemical])
#         spare[chemical] = max(0, spare.get(chemical, 0) - needed[chemical])
#         reaction = reactions[chemical]
#         for reactant in reaction.reactants_amount:
#             reactant_amount = math.ceil(amount / reaction.product_amount) * reaction.reactants_amount[reactant]
#             if reactant not in new_needed:
#                 new_needed[reactant] = 0
#             new_needed[reactant] += reactant_amount

#         chemical_produced = math.ceil(amount / reaction.product_amount) * reaction.product_amount
#         # new_spare[chemical] += chemical_produced - amount
#         spare[chemical] += chemical_produced - amount

#     needed = new_needed
#     print("needed:", list(filter(lambda item: item[1] > 0, needed.items())))
#     print("spare:", list(filter(lambda item: item[1] > 0, spare.items())))
#     input()
    # spare = new_spare
# print(needed["ORE"])
needed = {chemical: 0 for chemical in reactions}
needed["FUEL"] = 1
needed["ORE"] = 0
spare = {chemical: 0 for chemical in reactions}
spare["ORE"] = 0
while True:
    for chemical in needed:
        if chemical != "ORE" and needed[chemical] > 0:
            break
    else:
        break
    
    for chemical in needed:
        if chemical == "ORE" or needed[chemical] == 0:
            continue
        amount = max(0, needed[chemical] - spare[chemical])
        spare[chemical] = max(0, spare[chemical] - needed[chemical])
        reaction = reactions[chemical]
        for reactant in reaction.reactants_amount:
            reactant_amount = math.ceil(amount / reaction.product_amount) * reaction.reactants_amount[reactant]
            needed[reactant] += reactant_amount

        chemical_produced = math.ceil(amount / reaction.product_amount) * reaction.product_amount
        spare[chemical] += chemical_produced - amount
        needed[chemical] = 0
        
    
    print("needed:", list(filter(lambda item: item[1] > 0, needed.items())))
    print("spare:", list(filter(lambda item: item[1] > 0, spare.items())))
    input()
print(needed["ORE"])
'''
def get_ore_needed_for(name, amount_needed):
    needed = 0
    reaction = reactions[name]
    reactants_needed = list(reaction.reactants_amount.keys())
    if len(reactants_needed) == 1 and reactants_needed[0] == "ORE":
        needed = math.ceil(amount_needed / reaction.product_amount) * reaction.reactants_amount["ORE"]#{"ORE": reactants_needed["ORE"] / reaction.product_amount}
    else:
        for reactant in reactants_needed:
            needed_curr = get_ore_needed_for(reactant, amount_needed)
            print(name, reactant, needed_curr)
            needed += needed_curr
            #needed += math.ceil(reaction.reactants_amount[reactant] * needed_curr / reaction.product_amount)
            # for other_reactant in needed_curr:
            #     if other_reactant not in needed:
            #         needed[other_reactant] = 0
            #     needed[other_reactant] += (needed_curr[other_reactant] / reaction.product_amount) * needed_curr[reactant]
    
    return needed

print(get_ore_needed_for("FUEL", 1))
'''
