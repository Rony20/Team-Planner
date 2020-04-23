from ..db.mongodb_utils import DatabaseConnector, Collections

db_connector = DatabaseConnector()

def get_dropdowns():
    
    list_of_skills = list()
    list_of_pm = list()

    skills = db_connector.collection(Collections.COC).find({"coc_code": 11}, {"_id":0, "coc_desc":0, "coc_code":0})
    for skill in skills:
        list_of_skills.append(skill)

    pms = db_connector.collection(Collections.COC).find({"coc_code": 12}, {"_id":0, "coc_desc":0, "coc_code":0}) 
    for pm in pms:
        list_of_pm.append(pm)

    dropdowns = {
        "Skills": list_of_skills,
        "PM": list_of_pm
    }

    return dropdowns

def get_pm_list():

    list_of_pm = list()

    pms = db_connector.collection(Collections.COC).find({"coc_code": 12}, {"_id":0, "coc_desc":0, "coc_code":0})
    for pm in pms:
        list_of_pm.append(pm)

    return list_of_pm