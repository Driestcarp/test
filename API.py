import json
import re


def load(filename):
    with open(filename) as f:
        db = json.loads(f.read())
    return db

def update(filename, db):
    with open(filename, "w") as f:
        json.dump(db, f, ensure_ascii=False, indent=4)



def add_skill(player, skill_name, what_kina_skill ):
    player[what_kina_skill][skill_name] = "0"

def edit_skill(player, what_kinda_skill, dict_of_skills):
    pop_at = []
    for skill in player[what_kinda_skill]:
        for edited_skill in dict_of_skills:
            try:
                if skill == edited_skill and int(dict_of_skills[edited_skill]) < 0:
                    pop_at.append(skill)
            except:
                pass
            if skill == edited_skill and player[what_kinda_skill][skill] != dict_of_skills[edited_skill]:
                player[what_kinda_skill][skill] = dict_of_skills[edited_skill]
    for i in pop_at:
        player[what_kinda_skill].pop(i)


def add_ability(player, skill_name):
    player["abilities"][skill_name] = ["",""]

def edit_ability(player, dict_of_abilities):
    pop_at = []
    for ability in player['abilities']:
        for edited_ability in dict_of_abilities:
            try:
                if ability == edited_ability and (dict_of_abilities[edited_ability][1] == "del" or dict_of_abilities[edited_ability][1] == "-1"):
                    pop_at.append(ability)
            except:
                pass
            if ability == edited_ability:
                if player['abilities'][ability][1] != dict_of_abilities[edited_ability][1]:
                    player['abilities'][ability][1] = dict_of_abilities[edited_ability][1]
                if player['abilities'][ability][0] != dict_of_abilities[edited_ability][0]:
                    player['abilities'][ability][0] = dict_of_abilities[edited_ability][0]
    for i in pop_at:
        player['abilities'].pop(i)

def add_equipment(player, thing_name):
    player['equipment'].append([thing_name, "0"])

def edit_equipment( player, thing_to_change):
    remove = []
    for item in range(len(player['equipment'])):
        for thing in range(len(thing_to_change)):
            try:
                if item == thing and int(thing_to_change[thing][1]) < 0:
                    remove.append(thing)
            except:
                pass
            if item == thing:
                if player['equipment'][item][1] != thing_to_change[thing][1]:
                    player['equipment'][item][1] = thing_to_change[thing][1]
                if player['equipment'][item][0] != thing_to_change[thing][0]:
                    player['equipment'][item][0] = thing_to_change[thing][0]

    number_of_removes = 0
    for i in remove:
        player['equipment'].pop(i - number_of_removes)
        number_of_removes += 1

def add_ammo(player, new_ammo):
    player['ammo'][new_ammo] = {"mod": "", "antal": "","skada": "","skjutna": ["", ""]}

def edit_ammo(player, ammo_to_change):
    pop_at = []
    for a_type in player['ammo']:
        for e_ammo in ammo_to_change:
            try:
                if a_type == e_ammo and (int(ammo_to_change[e_ammo]['antal']) < 0):
                    pop_at.append(a_type)
            except:
                pass
            if a_type == e_ammo:
                if player['ammo'][a_type]['mod'] != ammo_to_change[e_ammo]['mod']:
                    player['ammo'][a_type]['mod'] = ammo_to_change[e_ammo]['mod']
                if player['ammo'][a_type]['antal'] != ammo_to_change[e_ammo]['antal']:
                    player['ammo'][a_type]['antal'] = ammo_to_change[e_ammo]['antal']
                if player['ammo'][a_type]['skada'] != ammo_to_change[e_ammo]['skada']:
                    player['ammo'][a_type]['skada'] = ammo_to_change[e_ammo]['skada']
                if player['ammo'][a_type]['skjutna'][0] != ammo_to_change[e_ammo]['skjutna'][0]:
                    player['ammo'][a_type]['skjutna'][0] = ammo_to_change[e_ammo]['skjutna'][0]
                if player['ammo'][a_type]['skjutna'][1] != ammo_to_change[e_ammo]['skjutna'][1]:
                    player['ammo'][a_type]['skjutna'][1] = ammo_to_change[e_ammo]['skjutna'][1]
    for i in pop_at:
        player['ammo'].pop(i)

def add_weapon(player, weapon_to_add):
    player['weapons'].append({
        "vapen": weapon_to_add, 
        "fattning": "",
        "initiativ": "",
        "magasin": "",
        "pen": "",
        "pål": "",
        "max_pål": "",
        "räckv": "",
        "skada": "",
        "tålighet": "",
        "vikt": ""
    })
def edit_weapon(player, weapon_to_change):
    pop_at = []
    for weapon in range(len(player['weapons'])):
        for e_weapon in range(len(weapon_to_change)):
            try:
                if weapon == e_weapon and ((int(weapon_to_change[e_weapon]['fattning']) < 0) or (int(weapon_to_change[e_weapon]['pål']) < 0) or (int(weapon_to_change[e_weapon]['tålighet']) < 0)):
                    pop_at.append(weapon)
            except:
                pass
            if weapon == e_weapon:
                if player['weapons'][weapon]['vapen'] != weapon_to_change[e_weapon]['vapen']:
                    player['weapons'][weapon]['vapen'] = weapon_to_change[e_weapon]['vapen']
                if player['weapons'][weapon]['fattning'] != weapon_to_change[e_weapon]['fattning']:
                    player['weapons'][weapon]['fattning'] = weapon_to_change[e_weapon]['fattning']
                if player['weapons'][weapon]['initiativ'] != weapon_to_change[e_weapon]['initiativ']:
                    player['weapons'][weapon]['initiativ'] = weapon_to_change[e_weapon]['initiativ']
                if player['weapons'][weapon]['magasin'] != weapon_to_change[e_weapon]['magasin']:
                    player['weapons'][weapon]['magasin'] = weapon_to_change[e_weapon]['magasin']
                if player['weapons'][weapon]['pen'] != weapon_to_change[e_weapon]['pen']:
                    player['weapons'][weapon]['pen'] = weapon_to_change[e_weapon]['pen']
                if player['weapons'][weapon]['pål'] != weapon_to_change[e_weapon]['pål']:
                    player['weapons'][weapon]['pål'] = weapon_to_change[e_weapon]['pål']
                if player['weapons'][weapon]['max_pål'] != weapon_to_change[e_weapon]['max_pål']:
                    player['weapons'][weapon]['max_pål'] = weapon_to_change[e_weapon]['max_pål']
                if player['weapons'][weapon]['räckv'] != weapon_to_change[e_weapon]['räckv']:
                    player['weapons'][weapon]['räckv'] = weapon_to_change[e_weapon]['räckv']
                if player['weapons'][weapon]['skada'] != weapon_to_change[e_weapon]['skada']:
                    player['weapons'][weapon]['skada'] = weapon_to_change[e_weapon]['skada']
                if player['weapons'][weapon]['tålighet'] != weapon_to_change[e_weapon]['tålighet']:
                    player['weapons'][weapon]['tålighet'] = weapon_to_change[e_weapon]['tålighet']
    for i in pop_at:
        player['weapons'].pop(i)

def add_stash_item(player, new_item):
    player['stash'][1].append({
                    "name": new_item,
                    "antal": "",
                    "vikt": "",
                    "värde": "",
                    "info": ""
                })
    
def edit_stash(player, things_to_edit):
    remove = []
    for item in range(len(player['stash'][1])):
        for thing in range(len(things_to_edit)):
            try:
                if item == thing and int(things_to_edit[thing]['antal']) < 0:
                    remove.append(thing)
            except:
                pass
            
            if item == thing:
                if player['stash'][1][thing]['name'] != things_to_edit[thing]['name']:
                    player['stash'][1][thing]['name'] = things_to_edit[thing]['name']
                if player['stash'][1][thing]['antal'] != things_to_edit[thing]['antal']:
                    player['stash'][1][thing]['antal'] = things_to_edit[thing]['antal']
                if player['stash'][1][thing]['vikt'] != things_to_edit[thing]['vikt']:
                    player['stash'][1][thing]['vikt'] = things_to_edit[thing]['vikt']
                if player['stash'][1][thing]['värde'] != things_to_edit[thing]['värde']:
                    player['stash'][1][thing]['värde'] = things_to_edit[thing]['värde']
                if player['stash'][1][thing]['info'] != things_to_edit[thing]['info']:
                    player['stash'][1][thing]['info'] = things_to_edit[thing]['info']


    number_of_removes = 0
    for i in remove:
        player['stash'][1].pop(i - number_of_removes)
        number_of_removes += 1

def get_player(db, name):
    for player in db:
        if player['name'] == name:
            return player
    return None

def create_player(name, db):
    new_player = load('empty_char.json')
    new_player['name'] = name
    db.append(new_player)
    update("mutant.json", db)

def check_if_name_alredy_exists(name, db):
    for player in db:
        if player['name'] == name:
            return False
    return True

def remove_player(name, db):
    player_to_remove = -1
    for player in range(len(db)):
        if db[player]['name'] == name:
            player_to_remove = player
    if player_to_remove > 0:
        db.pop(player_to_remove)
        update("mutant.json", db)

def calculate_resonans(list_of_num):
    numb_of_res = 0
    for i in list_of_num:
        numb_of_res += int(i)
    return numb_of_res
                
    
def main():
    db = load("mutant.json")
    print(db[0]["natural_skills"])
    add_skill(get_player(db, 'Lars Göran'), 'aaa', 'natural_skills',)
    print(db[0]["natural_skills"])
    dict_of_skills = {
        "cum": "22",
        "aaa": "-1"
    }
    edit_skill(db, get_player(db, 'Lars Göran'), 'natural_skills', dict_of_skills )
    print(db[0]["natural_skills"])
    #update("new_mutant.json", db)

