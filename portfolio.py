#!/usr/bin/env python3
from flask import Flask, render_template, url_for, request, abort, send_file
import data 
from werkzeug.exceptions import HTTPException
import API

app = Flask("portfolio")

db = data.load("data.json")


@app.route("/")
def index():
    db = data.load("data.json")
    latest_project= data.get_latest(db)
    return render_template("index.html", latest_project=latest_project)



@app.route("/list") 
def list():
    db = data.load("data.json")
    list_of_all_categorys = data.get_course_id(db)
    return render_template("list.html", projects_to_render=db, category_list=list_of_all_categorys)


@app.route("/project/<project_id>")
def project(project_id):
    db = data.load("data.json")
    project = data.get_project(db , project_id)
    if project != None:
        return render_template("project.html", project_to_render=project)
    abort(404)

@app.route("/list-search")
def search_in_list():
    db = data.load("data.json")
    searchterm = request.args.get("searchterm")
    sort_by = request.args.get("sort_by")
    sort_order = request.args.get("sort_order")
    checked_category = request.args.get("checked_categorys")
    search_fields = request.args.getlist("search_fields")
    list_of_all_categorys = data.get_course_id(db)
    if checked_category == 'all':
        checked_category = None
    if not search_fields:
        search_fields = None
    if sort_by == None:
        sort_by = 'project_name'
    matches = data.search(db, search=searchterm, search_fields=search_fields, sort_by=sort_by, sort_order=sort_order, category=checked_category)
    if matches:
        return render_template("list.html", projects_to_render=matches, category_list=list_of_all_categorys)
    else:
        return render_template("list.html", projects_to_render=matches, category_list=list_of_all_categorys)
    

@app.route("/techniques-search")
def search_in_tech():
    db = data.load("data.json")
    list_of_checked_techniques = request.args.getlist("checked_techniques")
    list_of_all_techniques = data.get_techniques(db)
    matches = data.search(db, sort_by='project_id', techniques=list_of_checked_techniques)
    if matches:
        return render_template("techniques.html", projects_to_render=matches, technique_list=list_of_all_techniques)
    else:
        return render_template("techniques.html", projects_to_render=matches, technique_list=list_of_all_techniques)
    

@app.route("/techniques")
def techniques():
    db = data.load("data.json")
    list_of_all_techniques = data.get_techniques(db)
    return render_template("techniques.html", projects_to_render=db, technique_list=list_of_all_techniques)

@app.route("/about_me")
def about_me():
    return render_template("about_me.html")

@app.errorhandler(Exception)
def handle_exeption(error):
    if isinstance(error, HTTPException):
        render_template("404.html", error=error)
    return render_template("404.html", error=error)

    



@app.route('/mutant/regelbok')
def render_pdf():
    pdf_path = 'mua_regelbok.pdf'
    return send_file(pdf_path, as_attachment=False)

db_mutant = API.load("mutant.json")


@app.route("/mutant")
def mutant():
    db_mutant = API.load("mutant.json")
    return render_template("mutant.html", list_of_players=db_mutant)



@app.route("/player/<name>")
def player(name):
    db_mutant = API.load("mutant.json")
    player = API.get_player(db_mutant , name)
    if player != None:
        return render_template("player.html", player=player)
    else:
        return render_template("mutant.html")

@app.route("/new_player")
def new_player():
    db_mutant = API.load("mutant.json")
    if request.args.get("name") != "" and API.check_if_name_alredy_exists(request.args.get("name"), db_mutant) == True:
        API.create_player(request.args.get("name"), db_mutant)

    if request.args.get("rm_name") != "":
        API.remove_player(request.args.get("rm_name"), db_mutant)

    db_mutant = API.load("mutant.json")
    return render_template("mutant.html", list_of_players=db_mutant)



# $$$$$$$\                                        $$\   
# $$  __$$\                                     $$$$ |  
# $$ |  $$ | $$$$$$\   $$$$$$\   $$$$$$\        \_$$ |  
# $$$$$$$  | \____$$\ $$  __$$\ $$  __$$\         $$ |  
# $$  ____/  $$$$$$$ |$$ /  $$ |$$$$$$$$ |        $$ |  
# $$ |      $$  __$$ |$$ |  $$ |$$   ____|        $$ |  
# $$ |      \$$$$$$$ |\$$$$$$$ |\$$$$$$$\       $$$$$$\ 
# \__|       \_______| \____$$ | \_______|      \______|
#                     $$\   $$ |                        
#                     \$$$$$$  |                        
#                      \______/                         

@app.route("/updated_page1/<name>")
def updated_page1(name):
    db_mutant = API.load("mutant.json")
    player = API.get_player(db_mutant , name)
    for stat in player['stats']:
        if request.args.get(stat) != player['stats'][stat]:
            player['stats'][stat] = request.args.get(stat)

    if request.args.get("player") != player['player']:
        player['player'] = request.args.get("player")
        
    if request.args.get("gm") != player['gm']:
        player['gm'] = request.args.get("gm")
        
    if request.args.get('pcname') != player['name']:
        player['name'] = request.args.get('pcname')

    if request.args.get("klass") != player['info']['Klass']:
        player['info']['Klass'] = request.args.get("klass")

    if request.args.get("tidigare_yrke") != player['info']['Tidigare yrke']:
        player['info']['Tidigare yrke'] = request.args.get("tidigare_yrke")

    if request.args.get("hemort") != player['info']['Hemort']:
        player['info']['Hemort'] = request.args.get("hemort")

    if request.args.get("age") != player['info']['Ålder']:
        player['info']['Ålder'] = request.args.get("age")  

    if request.args.get("sex") != player['info']['Kön']:
        player['info']['Kön'] = request.args.get("sex")

    if request.args.get("length") != player['info']['Längd']:
        player['info']['Längd'] = request.args.get("length") 

    if request.args.get("weight") != player['info']['Vikt']:
        player['info']['Vikt'] = request.args.get("weight") 

    if request.args.get('appearance_up') != player['Utseende_uppe']:
        player['Utseende_uppe'] = request.args.get('appearance_up')

    if request.args.get('appearance') != player['Utseende']:
        player['Utseende'] = request.args.get('appearance')

    if request.args.get("trauma") != player['misc']['traumatröskel'][0]:
        player['misc']['traumatröskel'][0] = request.args.get("trauma")
    
    if request.args.get("stab") != player['misc']['stab']:
        player['misc']['stab'] = request.args.get("stab")
    
    if request.args.get("initiativ") != player['misc']['initiativbonus']:
        player['misc']['initiativbonus'] = request.args.get("initiativ")
    
    if request.args.get("skade") != player['misc']['skadebonus']:
        player['misc']['skadebonus'] = request.args.get("skade")

    if request.args.get("bär") != player['misc']['bärförmåga']:
        player['misc']['bärförmåga'] = request.args.get("bär")
    
    if request.args.get("reaktion") != player['misc']['reaktionsvärde']:
        player['misc']['reaktionsvärde'] = request.args.get("reaktion")
    
    if request.args.get("rykte") != player['misc']['Rykte']:
        player['misc']['Rykte'] = request.args.get("rykte")
    
    if request.args.get("status") != player['misc']['status']:
        player['misc']['status'] = request.args.get("status")
    
    if request.args.get("strid") != player['misc']['förfly_strid']:
        player['misc']['förfly_strid'] = request.args.get("strid")
    
    if request.args.get("springa") != player['misc']['förfly_springa']:
        player['misc']['förfly_springa'] = request.args.get("springa")
    
    if request.args.get("sprint") != player['misc']['förfly_sprint']:
        player['misc']['förfly_sprint'] = request.args.get("sprint")
    
    if request.args.get("kp_max") != player['misc']['max_kroppspoäng']:
        player['misc']['max_kroppspoäng'] = request.args.get("kp_max")
    
    if request.args.get("kp") != player['misc']['kroppspoäng']:
        player['misc']['kroppspoäng'] = request.args.get("kp")
    
    if request.args.get('new_nat_skill') != "" and request.args.get('new_nat_skill') != None:
        API.add_skill(player, request.args.get('new_nat_skill'), 'natural_skills')
    if request.args.get('new_tra_skill') != "" and request.args.get('new_tra_skill') != None:
        API.add_skill(player, request.args.get('new_tra_skill'), 'trained_skills')
    skill_to_change = {}
    for skills in player['natural_skills']:
        skill_to_change[request.args.get('n_change_' + skills +'_name')] = request.args.get('n_change_' + skills)
    API.edit_skill( player, 'natural_skills', skill_to_change)
    skill_to_change = {}
    for skills in player['trained_skills']:
        skill_to_change[request.args.get('t_change_' + skills +'_name')] = request.args.get('t_change_' + skills)
    API.edit_skill( player, 'trained_skills', skill_to_change)
    
    if request.args.get('new_ability') != "" and request.args.get('new_ability') != None:
        API.add_ability(player, request.args.get('new_ability'))
    abilities_to_change = {}
    for ability in player['abilities']:
        abilities_to_change[request.args.get('a_change_' + ability +'_name')] = [request.args.get('a_change_' + ability + "_lyte"), request.args.get("a_change_" + ability + "_discription")]
    API.edit_ability( player, abilities_to_change)


    player['resonans'] = API.calculate_resonans(request.args.getlist('resonans'))

    API.update('mutant.json', db_mutant)
    return render_template("player.html", player=player)




# $$$$$$$\                                       $$$$$$\  
# $$  __$$\                                     $$  __$$\ 
# $$ |  $$ | $$$$$$\   $$$$$$\   $$$$$$\        \__/  $$ |
# $$$$$$$  | \____$$\ $$  __$$\ $$  __$$\        $$$$$$  |
# $$  ____/  $$$$$$$ |$$ /  $$ |$$$$$$$$ |      $$  ____/ 
# $$ |      $$  __$$ |$$ |  $$ |$$   ____|      $$ |      
# $$ |      \$$$$$$$ |\$$$$$$$ |\$$$$$$$\       $$$$$$$$\ 
# \__|       \_______| \____$$ | \_______|      \________|
#                     $$\   $$ |                          
#                     \$$$$$$  |                          
#                      \______/                           

@app.route("/updated_page2/<name>")
def updated_page2(name):
    db_mutant = API.load("mutant.json")
    player = API.get_player(db_mutant , name)
    for stat in player['armor']:
        if request.args.get("armor_change_" + stat + "_name") != player['armor'][stat][0]:
            player['armor'][stat][0] = request.args.get("armor_change_" + stat + "_name")
        if request.args.get("armor_change_" + stat + "_beg") != player['armor'][stat][1]:
            player['armor'][stat][1] = request.args.get("armor_change_" + stat + "_beg")
        if request.args.get("armor_change_" + stat + "_beg") != player['armor'][stat][2]:
            player['armor'][stat][2] = request.args.get("armor_change_" + stat + "_abs")

    if request.args.get('new_stridf') != "" and request.args.get('new_stridf') != None:
        API.add_skill(player, request.args.get('new_stridf'), 'stridsfärdigheter')
    skill_to_change = {}
    for skills in player['stridsfärdigheter']:
        skill_to_change[request.args.get('stridf_change_' + skills + '_name')] = request.args.get('stridf_change_' + skills + '_value')
    API.edit_skill( player, 'stridsfärdigheter', skill_to_change)

    if request.args.get("p2_max_kp") != player['misc']['max_kroppspoäng']:
        player['misc']['max_kroppspoäng'] = request.args.get("p2_max_kp")
    if request.args.get("p2_kp") != player['misc']['kroppspoäng']:
        player['misc']['kroppspoäng'] = request.args.get("p2_kp")
    if request.args.get("trauma_1") != player['misc']['traumatröskel'][0]:
        player['misc']['traumatröskel'][0] = request.args.get("trauma_1")
    if request.args.get("trauma_2") != player['misc']['traumatröskel'][1]:
        player['misc']['traumatröskel'][0] = request.args.get("trauma_2")
    if request.args.get("trauma_3") != player['misc']['traumatröskel'][2]:
        player['misc']['traumatröskel'][0] = request.args.get("trauma_3")
        
    if request.args.get("intiv") != player['misc']['initiativbonus']:
        player['misc']['initiativbonus'] = request.args.get("intiv")
    if request.args.get("förfly_strid") != player['misc']['förfly_strid']:
        player['misc']['förfly_strid'] = request.args.get("förfly_strid")
    if request.args.get("förfly_springa") != player['misc']['förfly_springa']:
        player['misc']['förfly_springa'] = request.args.get("förfly_springa")
    if request.args.get("förfly_sprint") != player['misc']['förfly_sprint']:
        player['misc']['förfly_sprint'] = request.args.get("förfly_sprint")
    if request.args.get("skadebonus") != player['misc']['skadebonus']:
        player['misc']['skadebonus'] = request.args.get("skadebonus")

    if request.args.get("bärförmåga") != player['misc']['bärförmåga']:
        player['misc']['bärförmåga'] = request.args.get("bärförmåga")
    if request.args.get("bärvikt") != player['misc']['bärvikt']:
        player['misc']['bärvikt'] = request.args.get("bärvikt")
    if request.args.get("bär_minus") != player['misc']['bär_minus']:
        player['misc']['bär_minus'] = request.args.get("bär_minus")

    if request.args.get("rust_beg") != player['misc']['rust_beg']:
        player['misc']['rust_beg'] = request.args.get("rust_beg")
    if request.args.get("iaktagelse_minus") != player['misc']['iaktagelse_minus']:
        player['misc']['iaktagelse_minus'] = request.args.get("iaktagelse_minus")
    if request.args.get("stab") != player['misc']['stab']:
        player['misc']['stab'] = request.args.get("stab")

    if request.args.get("figur_huvud") != player['figur']['huvud']:
        player['figur']['huvud'] = request.args.get("figur_huvud")
    if request.args.get("figur_kropp") != player['figur']['kropp']:
        player['figur']['kropp'] = request.args.get("figur_kropp")
    if request.args.get("figur_h_arm") != player['figur']['h_arm']:
        player['figur']['h_arm'] = request.args.get("figur_h_arm")
    if request.args.get("figur_v_arm") != player['figur']['v_arm']:
        player['figur']['v_arm'] = request.args.get("figur_v_arm")
    if request.args.get("figur_h_ben") != player['figur']['h_ben']:
        player['figur']['h_ben'] = request.args.get("figur_h_ben")
    if request.args.get("figur_v_ben") != player['figur']['v_ben']:
        player['figur']['v_ben'] = request.args.get("figur_v_ben")


    if request.args.get('new_ammo') != "" and request.args.get('new_ammo') != None:
        API.add_ammo(player, request.args.get('new_ammo'))
    ammo_to_change = {}
    for ammo in player['ammo']:
        ammo_to_change[request.args.get('ammo_type_' + ammo)] = {"mod": request.args.get( 'ammo_mod_' + ammo), "antal": request.args.get( 'ammo_amount_' + ammo), "skada": request.args.get( 'ammo_dmg_' + ammo), "skjutna":[request.args.get( 'ammo_shot_' + ammo + '_1'),request.args.get( 'ammo_shot_' + ammo + '_2')]} 
    API.edit_ammo(player, ammo_to_change)  

    added_thing = 0
    if request.args.get('new_thing') != "" and request.args.get('new_thing') != None:
        added_thing = -1
        API.add_equipment(player, request.args.get('new_thing'))
    thing_to_change = []
    for thing in range(len(player['equipment']) + added_thing):
        thing_to_change.append([request.args.get( 'thing_change_' + str(thing) + '_name'), request.args.get( 'thing_change_' + str(thing))])
    API.edit_equipment(player, thing_to_change)

    added_weapons = 0
    if request.args.get('new_weapon') != "" and request.args.get('new_weapon') != None:
        added_weapons = -1
        API.add_weapon(player, request.args.get('new_weapon'))
    weapon_to_change = []
    for thing in range(len(player['weapons']) + added_weapons):
        weapon_to_change.append({"vapen":request.args.get( 'weapon_change_' + str(thing) + '_name'), "fattning":request.args.get( 'weapon_change_' + str(thing) + '_fattning'), "initiativ":request.args.get( 'weapon_change_' + str(thing) + '_initiativ'), "magasin":request.args.get( 'weapon_change_' + str(thing) + '_magasin'), "pen":request.args.get( 'weapon_change_' + str(thing) + '_pen'), "pål":request.args.get( 'weapon_change_' + str(thing) + '_pål'), "max_pål":request.args.get( 'weapon_change_' + str(thing) + '_max_pål'), "räckv":request.args.get( 'weapon_change_' + str(thing) + '_räckv'), "skada":request.args.get( 'weapon_change_' + str(thing) + '_skada'), "tålighet":request.args.get( 'weapon_change_' + str(thing) + '_tålighet')})
    API.edit_weapon(player, weapon_to_change)

    API.update('mutant.json', db_mutant)
    return render_template("player.html", player=player)




# $$$$$$$\                                       $$$$$$\  
# $$  __$$\                                     $$ ___$$\ 
# $$ |  $$ | $$$$$$\   $$$$$$\   $$$$$$\        \_/   $$ |
# $$$$$$$  | \____$$\ $$  __$$\ $$  __$$\         $$$$$ / 
# $$  ____/  $$$$$$$ |$$ /  $$ |$$$$$$$$ |        \___$$\ 
# $$ |      $$  __$$ |$$ |  $$ |$$   ____|      $$\   $$ |
# $$ |      \$$$$$$$ |\$$$$$$$ |\$$$$$$$\       \$$$$$$  |
# \__|       \_______| \____$$ | \_______|       \______/ 
#                     $$\   $$ |                          
#                     \$$$$$$  |                          
#                      \______/                           

@app.route("/updated_page3/<name>")
def updated_page3(name):
    db_mutant = API.load("mutant.json")
    player = API.get_player(db_mutant , name)
    if request.args.get("pocket_money") != player['stash'][0]['pocket_money']:
        player['stash'][0]['pocket_money'] = request.args.get("pocket_money")
    if request.args.get("bank_money1") != player['stash'][0]['bank_money1']:
        player['stash'][0]['bank_money1'] = request.args.get("bank_money1")
    if request.args.get("bank_money2") != player['stash'][0]['bank_money2']:
        player['stash'][0]['bank_money2'] = request.args.get("bank_money2")

    added_items = 0
    if request.args.get('new_stash_item') != "" and request.args.get('new_stash_item') != None:
        added_items = -1
        API.add_stash_item(player, request.args.get('new_stash_item'))
    stash_to_change = []
    for thing in range(len(player['stash'][1]) + added_items):
        stash_to_change.append({"name":request.args.get( 'name_' + str(thing)),"antal": request.args.get( 'antal_' + str(thing)), "vikt": request.args.get( 'vikt_' + str(thing)), "värde": request.args.get( 'värde_' + str(thing)), "info":request.args.get( 'info_' + str(thing))})
    API.edit_stash(player, stash_to_change)


    API.update('mutant.json', db_mutant)
    return render_template("player.html", player=player)

@app.route("/info")
def info():
    return render_template("info.html")

if __name__ == "__main__":
    app.run()
