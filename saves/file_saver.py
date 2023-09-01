import json

red_player = {
    'num_Medics': 0,
    'num_Observers': 2,
    'num_Supply_carts': 4,
    'num_Cannons': 0,
    'num_Musketeers': 0,
    'num_Pikemen': 0,
    'num_Shields': 0,
    'num_Knights': 0,
    'num_Commanders': 1
}


# with open("test.txt", "w") as test_file:
#     json.dump(red_player, test_file)

 


with open("test.txt", "r") as test_file:
    red_player = json.load(test_file)

print(red_player)