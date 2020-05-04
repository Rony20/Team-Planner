from enum import Enum

from ..db.mongodb_utils import DatabaseConnector, Collections

db_connector = DatabaseConnector()


class CocType(str, Enum):
    """Enumerations for COC."""

    skills = "skill"
    PM = "Project Manager/Technical Lead"
    PMO = "PMO / Project Management Officer"


def add_coc(list_of_data, data_type) -> None:
    """
    add_coc method takes list of data as argument and adds it in the COC database.
    This argument can contain any type of list such as skills, PMs, PMOs.

    :param list_of_data: list describing the data whose COC is to be made.
    :type list_of_data: list
    """

    last_index = 0
    data_in_db = []
    coc_desc = CocType[data_type]

    cursor = db_connector.collection(
        Collections.COC).find({"coc_desc": coc_desc}, {"_id": 0, "coc_desc": 0, "coc_code": 0, "code": 0})
    for coc_obj in cursor:
        data_in_db.append(coc_obj["value"])

    untracked_data = list(set(list_of_data)-set(data_in_db))
    if len(untracked_data) != 0:
        cursor_for_index = db_connector.collection(Collections.COC).find({"coc_desc": coc_desc}, {
            "_id": 0, "coc_desc": 0, "coc_code": 0, "value": 0}).sort([('code', -1)]).limit(1)
        for x in cursor_for_index:
            last_index = x["code"]
        coc_data = []
        for index, data in enumerate(untracked_data):
            data_object = {
                "coc_code": 11,
                "coc_desc": coc_desc,
                "code":  index + last_index + 1,
                "value": data
            }
            coc_data.append(data_object)
        db_connector.collection(Collections.COC).insert_many(coc_data)


def map_skill_with_coc(employee_skills) -> list:
    """
    map_skill_with_coc is a mapper function for list of skills to its coc code

    :param employee_skills: employee skills coming from hrms
    :type employee_skills: list of string
    :return: list of integers representing skills of employee
    :rtype: list
    """
    employee_skills_coc = []
    cursor = {}
    for skill in employee_skills:
        cursor = db_connector.collection(
            Collections.COC).find_one({"coc_code": 11, "value": skill}, {"_id": 0, "coc_desc": 0, "coc_code": 0})
        if cursor is not None:
            employee_skills_coc.append(cursor["code"])
    return employee_skills_coc
