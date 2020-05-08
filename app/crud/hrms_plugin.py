import json
from collections import namedtuple

from ..utils.hrms_plugin import get_auth_token, get_graphql_response, USERS_LIST, SKILL_LIST, TECHONOLOGY_LIST
from ..db.mongodb_utils import DatabaseConnector, Collections
from ..crud.employees import create_employee, edit_employee
from .coc import add_coc, map_skill_with_coc
from ..models.employees import UpdateEmployee, Employee
from ..utils.logger import Logger

db_connector = DatabaseConnector()
logger = Logger()


def insert_employee_into_database(employee) -> None:
    """
    insert_employee_into_database is mapper method. It will
    convert employee argument into database acceptable
    employee format and stores employee in database.

    :param employee: employee
    :type employee: employee
    """
    employee_skills = employee["skill"]
    employee_skills.append(employee["primaryTechnology"])
    employee_skills.append(employee["secondaryTechnology"])
    skills_set = map_skill_with_coc(employee_skills)
    skills_set = list(set(skills_set))

    employee_object = {
        "employee_id": int(employee["empCode"]),
        "employee_name": employee["name"],
        "designation": employee["designation"],
        "skills": skills_set,
        "past_projects": [],
        "current_projects": [],
        "availability": [],
        "is_allocated": True
    }

    employee_object = Employee(**employee_object)
    create_employee(employee_object)


def compare_user_data(user_in_hrms, user_in_db) -> str:
    """
    compare_user_data method takes two objects and compares them. First argument repressnts 
    Employee according to HRMS data and second represents Employee according to DB data. This
    method returns the name of the field where data mismatch is found.

    :param user_in_hrms: Employee according to HRMS data.
    :type user_in_hrms: dict
    :param user_in_db: Employee according to DB data.
    :type user_in_db: dict
    :return: the name of the field where data mismatch is found.
    :rtype: str
    """
    user_hrms_skills = user_in_hrms["skill"]
    if user_in_hrms["primaryTechnology"]:
        user_hrms_skills.append(user_in_hrms["primaryTechnology"])
    if user_in_hrms["secondaryTechnology"]:
        user_hrms_skills.append(user_in_hrms["secondaryTechnology"])

    user_hrms_skills_in_coc = list(set(map_skill_with_coc(user_hrms_skills)))

    if user_in_db["designation"] != user_in_hrms["designation"]:
        return "designation"
    else:
        untracked_skills = list(
            set(user_in_db["skills"])-set(user_hrms_skills_in_coc))
        if untracked_skills != 0:
            return "skills"
    return "unchanged"


def check_employee_in_database(users_list_in_hrms) -> None:
    """
    check_employee_in_database method takes a particular employee
    from HRMS and compare it with DB data,
    if no document is found then the employee is created in DB.
    It document is found then its fields are compared for updation.

    :param users_list_in_hrms: Employee object as of HRMS
    :type users_list_in_hrms: dict
    """
    for user in users_list_in_hrms:
        cursor = db_connector.collection(Collections.EMPLOYEES).find_one(
            {"employee_id": int(user["empCode"])},
            {"_id": 0, "current_projects": 0, "past_projects": 0,
             "availability": 0, "is_allocated": 0}
        )
        if cursor is None:
            insert_employee_into_database(user)
        else:
            change_required = compare_user_data(user, cursor)
            if change_required == "designation":
                update_designation_obj = UpdateEmployee(
                    **{'designation': user['designation']})
                edit_employee(int(user["empCode"]), update_designation_obj)
            elif change_required == "skills":
                update_skill_obj = UpdateEmployee(
                    **{'skills': list(set(map_skill_with_coc(user["skill"])))})
                edit_employee(int(user["empCode"]), update_skill_obj)


def sync_hrms_with_database():
    """
    sync_hrms_with_database method sync four kind of data from HRMS.
    skills in company, PMs in company, PMO in company and employees in company.
    """
    hrms_token = get_auth_token()

    skill_response = get_graphql_response(SKILL_LIST, hrms_token)
    skills_list = skill_response["data"]["allSkill"]

    technology_list = get_graphql_response(TECHONOLOGY_LIST, hrms_token)
    skills_list = skills_list + technology_list["data"]["allTechnology"]
    add_coc(skills_list, "skills")

    users_response = get_graphql_response(USERS_LIST, hrms_token)
    users_list = users_response["data"]["employeeSkillDetails"]["EmployeeSkillsList"]

    logger.info("HRMS data successfully fetched.")

    pm_list = []
    pmo_list = []

    for employee in users_list:
        if ("Technical Lead" or "Project Manager") in employee["designation"]:
            pm_list.append(employee["empCode"])
        elif "PMO" in employee["designation"]:
            pmo_list.append(employee["empCode"])
    add_coc(pm_list, "PM")
    add_coc(pmo_list, "PMO")
    check_employee_in_database(users_list)

    logger.info("HRMS sync successfully done.")
