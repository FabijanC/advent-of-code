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

mini = 0
maxi = 1000000000000
limit = 1000000000000
while mini < maxi:
    fuel_amount = (mini + maxi) // 2 + 1
    needed = {chemical: 0 for chemical in reactions}
    needed["FUEL"] = fuel_amount
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
        
    needed_ore = needed["ORE"]
    if needed_ore <= limit:
        mini = fuel_amount
    else:
        maxi = fuel_amount - 1
print(maxi)
