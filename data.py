import json
import re 

__package__ = None


def load(filename):
    try:
        with open(filename) as file:
            file_as_a_string = file.read()   
        file_as_a_string = sorted(json.loads(file_as_a_string), key=lambda projects: projects["project_id"])
        return file_as_a_string# Returns: list. All the project data from the read file, or None.
    except:
        return None         #Returns: None. Returns None if the file cannot load


def get_project_count(db):
    return len(db)         # Returns: number. The number of projects in the list.


def get_project(db, id):
    for projects in db:
        if  str(projects['project_id']) == str(id):
            return projects         #Returns: Dict. Returns a dictionary with the given ID specific data.
    return None             #Return: None. Returns None if there is no project with given ID


def search(db, sort_by='start_date', sort_order='desc', techniques=None, search=None, search_fields=None, category=None):
    if techniques != None:
        db = get_project_that_contains_all(techniques, db)

    if category != None:
        db = get_project_with_course(category, db)
    
    if search != None: 
        search = re.sub('[\W_]+', '', search).lower()
        db = check_if_string_matches(db, search, search_fields)
    if sort_by == 'project_id':
        return sorted(db, key=lambda projects: projects[sort_by])
    if sort_order == 'ace':
        return sorted(db, key=lambda projects: projects[sort_by])
    elif sort_order == 'desc':
        return sorted(db, key=lambda projects: projects[sort_by], reverse=True)
    
    else:
        return db
    # Returns: list. sorted or unsorted list that can be searched if parameters are sent in.


def check_if_string_matches(db, string_line, fields):
    list_of_projects_that_contains_string = []
    shorted_name = ""
    if fields == None:
        for projects in db:
            for key in projects:
                shorted_name = re.sub('[\W_]+', '', str(projects[key])).lower()
                list_of_projects_that_contains_string = add_project_to_list(list_of_projects_that_contains_string, string_line, shorted_name, projects)
    
    else:
        for field in fields:
            for projects in db:
                shorted_name = re.sub('[\W_]+', '', str(projects[field])).lower()
                list_of_projects_that_contains_string = add_project_to_list(list_of_projects_that_contains_string, string_line, shorted_name, projects)
    
    
    if len(list_of_projects_that_contains_string) > 0:
        return list_of_projects_that_contains_string
    else:
        return []
        # Returns: list. list of projects that contains "string_line" in one of the projects "fields" 
            

def true_if_id_in_projectlist(projects,list_of_projects_that_contains_string):
    true_or_false = True
    for i in range(len(list_of_projects_that_contains_string)):
        if projects['project_id'] == list_of_projects_that_contains_string[i]['project_id']:
            true_or_false = False
    return true_or_false # Returns: boolean. True if the project is not in list, False if project already in list.


def add_project_to_list(db, string_line, shorted_name, projects):
    if len(db) > 0:
        true_or_false = true_if_id_in_projectlist(projects, db)
        if re.search(string_line, shorted_name) and true_or_false == True: 
            db.append(projects)
    else:
        if re.search(string_line, shorted_name):
            db.append(projects)
    return db # Returns: list. a list with aditional project from "projects"
        
                
def get_techniques(db):
    list_of_techniques = []
    for projects in db:
        for techniques in projects['techniques_used']:
            if techniques not in list_of_techniques:
                list_of_techniques.append(techniques)
    return sorted(list_of_techniques) # Returns: list. a sorted list of all techniques used across all projects.

def get_course_id(db):
    list_of_course_id = []
    for project in db:
        if project['course_id'] not in list_of_course_id:
            list_of_course_id.append(project['course_id'])
    list_of_course_id = sorted(list_of_course_id)
    return list_of_course_id # Returns: list. list of all course id:s that excists in the database.
    
    
def get_project_that_contains(technique, db):
    list_of_projects = []
    project_id = 0
    project_name = ''
    for projects in db:
        project_id = projects['project_id']
        project_name = projects['project_name']
        for techniques in projects['techniques_used']:
            if techniques == technique:
                list_of_projects.append({"id" : project_id, "name" : project_name})         
        project_id = 0
        project_name = ''
        
    return list_of_projects # Returns: list. list of only the projects (only name and id) that contains all of the techniques of parameter "techniques" 


def get_project_that_contains_all(techniques, db):
    list_of_projects = []
    project_has_all = []

    for projects in db:
        for i in range(len(techniques)):
            for technique in projects['techniques_used']:
                if technique == techniques[i]:
                    project_has_all.append(1)
        
        if len(project_has_all) == len(techniques): 
            list_of_projects.append(projects)        
        project_has_all = []

    return list_of_projects # Returns: list. list of only the projects that contains all of the techniques of parameter "techniques" 

def get_project_with_course(category, db):
    list_of_projects = []
    for project in db:
        if project['course_id'] == category:
            list_of_projects.append(project)
    return list_of_projects


def get_technique_stats(db):
    technique_dictionary ={} 
    all_techniques = get_techniques(db)
    for i in range(len(all_techniques)):
        technique_dictionary.update({all_techniques[i] : get_project_that_contains(all_techniques[i], db)})
    return technique_dictionary         # Returns: dict. Technique stats (see above).


def get_latest(db):
    sorted_list = sorted(db, key=lambda projects: projects['end_date'], reverse=True)
    return sorted_list[0]#a dict of latest project
#this is a comment