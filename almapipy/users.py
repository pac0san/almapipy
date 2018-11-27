# -*- coding: utf-8 -*-

from .client import Client
from . import utils

#from json import loads

class SubClientUsers(Client):
    """
    Alma provides a set of Web services for handling user information,
    enabling you to quickly and easily manipulate user details.
    These Web services can be used by external systems
    such as student information systems (SIS) to retrieve or update user data.
    For more info: https://developers.exlibrisgroup.com/alma/apis/users
    """

    def __init__(self, cnxn_params={}):

        # Copy cnnection parameters and add info specific to API.
        self.cnxn_params = cnxn_params.copy()
        self.cnxn_params['api_uri'] = "/almaws/v1/users"
        self.cnxn_params['web_doc'] = "https://developers.exlibrisgroup.com/alma/apis/users"
        self.cnxn_params['wadl_url'] = "https://developers.exlibrisgroup.com/resources/wadl/0aa8d36f-53d6-48ff-8996-485b90b103e4.wadl"
        self.cnxn_params['api_uri_full'] = self.cnxn_params['base_uri']
        self.cnxn_params['api_uri_full'] += self.cnxn_params['api_uri']

        # Hook in subclients of api
        self.loans = SubClientUsersLoans(self.cnxn_params)
        self.requests = SubClientUsersRequests(self.cnxn_params)
        self.fees = SubClientUsersFees(self.cnxn_params)
        self.deposits = SubClientUsersDeposits(self.cnxn_params)

    def create(self, identifier, id_type, user_data, raw=False):
        """Create a single user if it does not exist yet in Alma

        Args:
            identifier (str): The identifier itself for the user.
                See: <https://developers.exlibrisgroup.com/alma/apis/xsd/rest_user.xsd#user_identifiers>
            id_type (str): The identifier type for the user
                Values: from the code-table: UserIdentifierTypes
                <https://api-XX.hosted.exlibrisgroup.com/almaws/v1/conf/code-tables/UserIdentifierTypes?apikey=XXXXXXXXXX>
                See: <https://developers.exlibrisgroup.com/alma/apis/xsd/rest_user.xsd#user_identifiers>
            user_data (dict): Data for user enrollment.
                Setting words for fields: [first_name, last_name,
                middle_name, email, user_group, ...].
                Format {'field': 'value', 'field2', 'value2'}.
                Values(user_group): code-table: UserGroups.
                <https://api-XX.hosted.exlibrisgroup.com/almaws/v1/conf/code-tables/UserGroups?apikey=XXXXXXXXXX>
                See <https://developers.exlibrisgroup.com/alma/apis/xsd/rest_user.xsd#user>
            raw (bool): If true, returns raw requests object.

        Returns: (?)
            The user (at Alma) if a new user is created.
            "{'total_record_count': 0}" if the 'identifier' was already set. 

        """

        headers = {'Authorization': 'apikey {}'.format(self.cnxn_params['api_key'])}
        
        data=user_data.copy()
        
        # Avoid sending 'primary_id' as 'id_type'
        args = {}
        query = {}
        if id_type != 'primary_id':
            args['id_type'] = id_type
            query['identifiers'] = identifier
# TODO: add 'user_identifier' stuff into 'user_data'
        else:
            query['primary_id'] = identifier
            data['primary_id'] = identifier

        args['q'] = self.__format_query__(query)
        
        url = self.cnxn_params['api_uri_full']

        # Search for a user with this 'user_identifier'
        response = self.Get(url, args=args, headers=headers, raw=raw)

        """
        print("\nDebug: users.py Create #1")
        print(headers)
        print(url)
        print(args)
        print(response)
        print("")
        """

# TODO: ¿what happens when no response? Parse 'requests.models.Response'
        if response['total_record_count'] == 0:
            # No user exists with this 'identifier': Let's create it.

            """
            # 'user_identifier' chunk
            aux_dict = {}
            aux_dict['value'] = identifier
            aux_dict['id_type'] = {} 
            aux_dict['id_type']['value'] = id_type
            aux_dict['status'] = 'ACTIVE'
            aux_dict['segment_type'] = 'External'
            data['user_identifier'] = [ aux_dict ]
            """
            """
            aux_dict = "{ 'user_identifier': [{ 'value': '" + identifier  + "', 'id_type': { 'value': '" + id_type + "' }, 'status': 'ACTIVE', 'segment_type': 'External' }] }"
            data = loads(aux_dict.replace("'", "\""))
            """

            args.pop('q', None)

            """
            print("\nDebug: users.py Create #2")
            print(headers)
            print(url)
            print(args)
            print(data)
            """

            # Send request
            response = self.Post(url, data=data, args=args, headers=headers, raw=raw)

            """
            print(response)
            print("")
            """

        else:
            # User already exist in Alma.
            response = {'total_record_count': 0}

        return response

    def read(self, user_id=None, query={}, limit=10, offset=0, all_records=False, q_params={}, raw=False):
        """Retrieve a user list or a single user.

        Args:
            user_id (str): A unique identifier for the user.
                Gets more detailed information.
            query (dict): Search query for filtering a user list. Optional.
                Searching for words from fields: [primary_id, first_name,
                last_name, middle_name, email, job_category, identifiers,
                general_info and ALL.].
                Only AND operator is supported for multiple filters.
                Format {'field': 'value', 'field2', 'value2'}.
                e.g. query = {'first_name': 'Sterling', 'last_name': 'Archer'}
            limit (int): Limits the number of results.
                Valid values are 0-100.
            offset (int): The row number to start with.
            all_records (bool): Return all rows returned by query.
                Otherwise returns number specified by limit.
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            List of user or a specific user's details.

        """

        args = q_params.copy()

        headers = {'Authorization': 'apikey {}'.format(self.cnxn_params['api_key'])}

        """
        print("\nDebug: users.py Read #1")
        print(query)
        print(args)
        print("")
        """

        url = self.cnxn_params['api_uri_full']
        if user_id:
            url += ("/" + str(user_id))
        else:
            # include paramets specific to user list
            if int(limit) > 100:
                limit = 100
            elif int(limit) < 1:
                limit = 1
            else:
                limit = int(limit)
            args['limit'] = limit
            args['offset'] = int(offset)

            # add search query if specified in desired format
            if query:
                args['q'] = self.__format_query__(query)

        response = self.Get(url, args=args, headers=headers, raw=raw)
        if user_id:
            return response

        """
        print("\nDebug: users.py Read #2")
        print(url)
        print(args)
        print(headers)
        print(response)
        print("")
        """

        # make multiple api calls until all records are retrieved
        if all_records:
            response = self.__read_all__(url=url, args=args, headers=headers, raw=raw,
                                         response=response, data_key='user')
        return response

    def update(self, primary_id, user_data, raw=False):
        """Update a single user if it does exist yet in Alma
           
        WARNING: This function is only for Alma Sorcerer's Apprentices.
                 Advanced users' data structure knowledge is required.

        Args:
            primary_id (str): The primary ididentifier of the user.
                See: <https://developers.exlibrisgroup.com/alma/apis/xsd/rest_user.xsd#user_identifiers>
            user_data (dict): Data for user enrollment.
                Setting words for fields: [first_name, last_name,
                middle_name, email, user_group, ...].
                Format {'field': 'value', 'field2', 'value2'}.
                Values(user_group): code-table: UserGroups.
                <https://api-XX.hosted.exlibrisgroup.com/almaws/v1/conf/code-tables/UserGroups?apikey=XXXXXXXXXX>
                See <https://developers.exlibrisgroup.com/alma/apis/xsd/rest_user.xsd#user>
            raw (bool): If true, returns raw requests object.

        Returns: (?)
            "{'total_record_count': 1}" if the user was updated successfully.
            "{'total_record_count': 0}" if there were any trouble. 

        """

        headers = {'Authorization': 'apikey {}'.format(self.cnxn_params['api_key'])}
        url = self.cnxn_params['api_uri_full'] + "/" + str(primary_id)

        # Search for a user with this 'primary_id'
        response = self.Get(url, args={}, headers=headers, raw=raw)

        """
        print("\nDebug: users.py Update #1")
        print(headers)
        print(url)
        print(user_data)
        print(response)
        """

# TODO: ¿what happens when no response? Parse 'requests.models.Response'
        if response['primary_id']:
            # Found an user with this 'primary_id': Let's update it.

            """
            print("\nDebug: users.py Update #3")
            print(user_data)
            """

            # Send request
            self.Put(url, data=user_data, headers=headers, raw=raw)
            response = {'total_record_count': 1}

            """
            print("\nDebug: users.py Update #4")
            print(headers)
            print(url)
            print(user_data)
            print(response)
            print(raw)
            print("")
            """

        else:
            # (a single) User not found in Alma.
            response = {'total_record_count': 0}

        return response

    def delete(self, identifier, id_type, raw=False):
        """Remove a single user if it does exist in Alma

        Args:
            identifier (str): The identifier itself for the user.
                See: <https://developers.exlibrisgroup.com/alma/apis/xsd/rest_user.xsd#user_identifiers>
            id_type (str): The identifier type for the user
                Values: from the code-table: UserIdentifierTypes
                <https://api-XX.hosted.exlibrisgroup.com/almaws/v1/conf/code-tables/UserIdentifierTypes?apikey=XXXXXXXXXX>
                See: <https://developers.exlibrisgroup.com/alma/apis/xsd/rest_user.xsd#user_identifiers>
            raw (bool): If true, returns raw requests object.

        Returns: (?)
            "{'total_record_count': 1}" if the user has been successfully removed.
            "{'total_record_count': 0}" if the 'identifier' was not present in Alma.

        """

        headers = {'Authorization': 'apikey {}'.format(self.cnxn_params['api_key'])}
        
        # Avoid sending 'primary_id' as 'id_type'
        args = {}
        query = {}
        if id_type != 'primary_id':
            args['id_type'] = id_type
            query['identifiers'] = identifier
# TODO: add 'user_identifier' stuff into 'user_data'
        else:
            query['primary_id'] = identifier

        args['q'] = self.__format_query__(query)
        
        url = self.cnxn_params['api_uri_full']

        # Search for a user with this 'user_identifier'
        response = self.Get(url, args=args, headers=headers, raw=raw)

        """
        print("\nDebug: users.py delete #1")
        print(headers)
        print(url)
        print(args)
        print(response)
        """

# TODO: ¿what happens when no response? Parse 'requests.models.Response'
        if response['total_record_count'] == 1:
            # A single user exists with this 'identifier': Let's remove it.
            args.clear()
            args['primary_id'] = query['primary_id']
            url += (str('/' + args['primary_id']))

            """
            print("\nDebug: users.py delete #2")
            print(headers)
            print(url)
            print(args)
            """

            # Send request
# SEE: "TODO: Eval exception 204" at the end of Delete 'function' in 'client.py'
#            response = self.Delete(url, args=args, headers=headers, raw=raw)
            self.Delete(url, args=args, headers=headers, raw=raw)
            response = {'total_record_count': 1}

            """
            print("\nDebug: users.py delete #3")
            print(response)
            print("")
            """

        else:
            # (a single) User not found in Alma.
            response = {'total_record_count': 0}

        return response


class SubClientUsersLoans(Client):
    """Handles the Loans endpoints of Users API"""

    def __init__(self, cnxn_params={}):
        self.cnxn_params = cnxn_params.copy()
        self.cnxn_params['api_uri'] += '/'
        self.cnxn_params['api_uri_full'] += '/'

    def read(self, user_id, loan_id=None, limit=10, offset=0,
            all_records=False, q_params={}, raw=False):
        """Retrieve a list of loans for a user.

        Args:
            user_id (str):      A unique identifier for the user.
            loan_id (str):      A unique identifier for the loan.
            limit (int): Limits the number of results.
                Valid values are 0-100.
            offset (int): The row number to start with.
            all_records (bool): Return all rows returned by query.
                Otherwise returns number specified by limit.
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            List of loans or a specific loan for a given user.

        """

        headers = {'Authorization': 'apikey {}'.format(self.cnxn_params['api_key'])}

        args = q_params.copy()

        url = self.cnxn_params['api_uri_full']
        url += (str(user_id) + "/loans")

        if loan_id:
            url += ('/' + str(loan_id))
        else:
            if int(limit) > 100:
                limit = 100
            elif int(limit) < 1:
                limit = 1
            else:
                limit = int(limit)
            args['limit'] = limit
            args['offset'] = int(offset)

        response = self.Get(url, args=args, headers=headers, raw=raw)
        if loan_id:
            return response

        # make multiple api calls until all records are retrieved
        if all_records:
            response = self.__Get_all__(url=url, args=args, headers=headers, raw=raw,
                                         response=response, data_key='item_loan')
        return response


class SubClientUsersRequests(Client):
    """Handles the Requests endpoints of Users API"""

    def __init__(self, cnxn_params={}):
        self.cnxn_params = cnxn_params.copy()
        self.cnxn_params['api_uri'] += '/'
        self.cnxn_params['api_uri_full'] += '/'

    def read(self, user_id, request_id=None, limit=10, offset=0,
            all_records=False, q_params={}, raw=False):
        """Retrieve a list of requests for a user.

        Args:
            user_id (str):      A unique identifier for the user.
            request_id (str):   A unique identifier for the request.
            limit (int): Limits the number of results.
                Valid values are 0-100.
            offset (int): The row number to start with.
            all_records (bool): Return all rows returned by query.
                Otherwise returns number specified by limit.
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            List of requests or a specific request for a given user.

        """
        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']

        url = self.cnxn_params['api_uri_full']
        url += (str(user_id) + "/requests")

        if request_id:
            url += ('/' + str(request_id))
        else:
            if int(limit) > 100:
                limit = 100
            elif int(limit) < 1:
                limit = 1
            else:
                limit = int(limit)
            args['limit'] = limit
            args['offset'] = int(offset)

        response = self.Get(url, args, raw=raw)
        if request_id:
            return response

        # make multiple api calls until all records are retrieved
        if all_records:
            response = self.__Get_all__(url=url, args=args, raw=raw,
                                         response=response, data_key='user_request')
        return response


class SubClientUsersFees(Client):
    """Handles the Fines and Fees endpoints of Users API"""

    def __init__(self, cnxn_params={}):
        self.cnxn_params = cnxn_params.copy()
        self.cnxn_params['api_uri'] += '/'
        self.cnxn_params['api_uri_full'] += '/'

    def read(self, user_id, fee_id=None, q_params={}, raw=False):
        """Retrieve a list of fines and fees for a user.

        Args:
            user_id (str):      A unique identifier for the user.
            fee_id (str):       A unique identifier for the fee.
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            List of fines/fees or a specific fine/fee for a given user.

        """
        url = self.cnxn_params['api_uri_full']
        url += (str(user_id))
        url += '/fees'
        if fee_id:
            url += ('/' + str(fee_id))

        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']

        return self.Get(url, args, raw=raw)


class SubClientUsersDeposits(Client):
    """Handles the Deposits endpoints of Users API"""

    def __init__(self, cnxn_params={}):
        self.cnxn_params = cnxn_params.copy()
        self.cnxn_params['api_uri'] += '/'
        self.cnxn_params['api_uri_full'] += '/'

    def read(self, user_id, deposit_id=None, limit=10, offset=0,
            all_records=False, q_params={}, raw=False):
        """Retrieve a list of deposits for a user.

        Args:
            user_id (str):      A unique identifier for the user.
            deposit_id (str): A unique identifier for the deposit.
            limit (int): Limits the number of results.
                Valid values are 0-100.
            offset (int): The row number to start with.
            all_records (bool): Return all rows returned by query.
                Otherwise returns number specified by limit.
            q_params (dict): Any additional query parameters.
            raw (bool): If true, returns raw requests object.

        Returns:
            List of deposits or a specific deposit for a given user.

        """
        args = q_params.copy()
        args['apikey'] = self.cnxn_params['api_key']

        url = self.cnxn_params['api_uri_full']
        url += (str(user_id) + "/deposits")

        if deposit_id:
            url += ('/' + str(deposit_id))
        else:
            if int(limit) > 100:
                limit = 100
            elif int(limit) < 1:
                limit = 1
            else:
                limit = int(limit)
            args['limit'] = limit
            args['offset'] = int(offset)

        response = self.Get(url, args, raw=raw)
        if deposit_id:
            return response

        # make multiple api calls until all records are retrieved
        if all_records:
            response = self.__Get_all__(url=url, args=args, raw=raw,
                                        response=response, data_key='user_deposit')
        return response
