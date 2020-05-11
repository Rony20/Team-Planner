from ldap3 import Server, Connection, NTLM, SUBTREE, core

from ..core.config import AD_URL, AD_DOMAIN, OU, SUPERUSER_USERNAME, SUPERUSER_PASSWORD

class ADConnector():
    """Class for Active Directory connection and communication."""
    def __init__(self):
        """Initialize AD server. Initialize connection to AD as None."""
        self.server = Server(AD_URL)
        self.connection = None

    def create_ad_connection(self, ad_username, ad_password) -> None:
        """
        Initialize connection to AD using username and password
        of perticular employee.

        :param ad_username: AD username of employee.
        :type ad_username: str
        :param ad_password: AD password of employee.
        :type ad_password: str
        """
        self.connection = Connection(self.server, user=f"{AD_DOMAIN}\\{ad_username}", password=ad_password, authentication=NTLM)

    def search_employee_id(self, ad_username) -> int:
        """
        Search for employee_id of employee based on username.

        :param ad_username: AD username of employee.
        :type ad_username: str
        :return: id of employee based on username. Raises exception if employee's id
        is not stored in case of super user account.
        :rtype: int
        """

        filter = f"(sAMAccountName={ad_username})"
        employee_id = None
        try:
            self.connection.search(f"OU={OU},DC={AD_DOMAIN},DC=LOCAL", search_filter=filter, search_scope=SUBTREE, attributes=['employeeID'])
            employee_id = self.connection.response[0]['attributes']['employeeID']
        except core.exceptions.LDAPException as error:
            print(error)

        if type(employee_id) != str:
            raise Exception("User is not employee !")
        return int(employee_id)

    def check_ad_authentication(self, ad_username, ad_password) -> dict:
        """
        Check employee is authenticated or not by checking username
        and password pair in AD.

        :param ad_username: username of employee.
        :type ad_username: str
        :param ad_password: password of employee.
        :type ad_password: str
        :return: if employee is authenticated then return employee id
        and validate field as true.
        If not authenticated then return validate field as false.
        :rtype: dictionary object having is_validate and employee_id field. 
        """

        self.create_ad_connection(ad_username, ad_password)
        ad_object = {
            "employee_id": None,
            "is_validate": False
        }
        try:
            ad_connection = self.connection.bind()
            if ad_connection:
                employee_id = self.search_employee_id(ad_username)
                ad_object["employee_id"] = employee_id
                ad_object["is_validate"] = True
            self.connection.unbind()
        except core.exceptions.LDAPBindError as error:
            print(error)
        except Exception as error:
            print(error)

        return ad_object

    def check_user_status(self, username, user_id) -> dict:
        """
        Checks for the username in AD using super user account
        if user is finded then it compares employee id from ad
        and user_id param.

        :param username: username of employee extracted from token.
        :type username: str
        :param user_id: user_id of employee extracted from token.
        :type: user_id: int
        :return: if user is not finded by in AD by username and id check 
        then return dictionary object having 'is_user' field as false.
        If user is founded the return dictionary of having 'is_user' field as 
        true. Then chekcs if user is active or not. According to that 'active'
        field is sated.
        rtype: dictionary  object having field 'is_user' and 'active'(based on condition)
        """

        try:
            self.connection = Connection(self.server, read_only=True, user=f"{AD_DOMAIN}\\{SUPERUSER_USERNAME}", 
            password=SUPERUSER_PASSWORD, auto_bind=True)

            self.connection.search(f"OU=CDS,DC={AD_DOMAIN},DC=LOCAL", f"(sAMAccountName={username})", 
            search_scope=SUBTREE, attributes=['userAccountControl', 'employeeID'])
            
            if self.connection.entries == []:
                return {"is_user": False}
            else:
                for entry in self.connection.entries:
                    status = entry.userAccountControl.values[0]
                    employee_id = int(entry.employeeID.values[0])
                
                if status == 512 and user_id == employee_id:
                    return {"is_user": True, "active": True}
                else:
                    return {"is_user": True, "active": False}

        except core.exceptions.LDAPBindError as error:
            print(error)
        except core.exceptions.LDAPInvalidFilterError as error:
            print(error)
        except core.exceptions.LDAPException as error:
            print(error)