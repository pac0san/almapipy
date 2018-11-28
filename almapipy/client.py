# -*- coding: utf-8 -*-

"""
Common Client for interacting with Alma API
"""

import json
import xml.etree.ElementTree as ET

import requests

from . import utils


class Client(object):
    """
    Reads responses from Alma API and handles response.
    """

    def __init__(self, cnxn_params={}):
        # instantiate dictionary for storing alma api connection parameters
        self.cnxn_params = cnxn_params

#    def post(self, url, data, args, object_type, raw=False):
    def Post(self, url, data, args, headers, raw=False):
        """
        Uses requests library to make Exlibris API Post call.
        Returns data of type specified during init of base class.

        Args:
            url (str): Exlibris API endpoint url.
            data (dict): Data to be posted.
            args (dict): Query string parameters for API call.
            headers (dict): API Key Auth in Headers.
#            object_type (str): Type of object to be posted (see alma docs)
            raw (bool): If true, returns raw response.

        Returns:
            JSON-esque, xml, or raw response.
        """

        data_aux = data.copy()
        args_aux = args.copy()

        # Preserve Auth and add 'User-Agent' and 'content-type' in headers
        headers_aux = headers.copy()
        headers_aux['User-Agent'] = self.cnxn_params['User-Agent']

        # Determine format of data to be posted according to order of importance:
        # 1) Local declaration, 2) dtype of data parameter, 3) global setting.
        if 'format' not in args_aux.keys():
            if type(data_aux) == ET or type(data_aux) == ET.Element:
                content_type = 'xml'
            elif type(data_aux) == dict:
                content_type = 'json'
            else:
                content_type = self.cnxn_params['format']
            args_aux['format'] = self.cnxn_params['format']
        else:
            content_type = args_aux['format']

        # Determine 'content-type' and set 'data_aux' format in consecuence
        if content_type == 'json':
            headers_aux['content-type'] = 'application/json'
            if type(data_aux) != str:
                data_aux = json.dumps(data_aux)
        elif content_type == 'xml':
            headers_aux['content-type'] = 'application/xml'
            if type(data_aux) == ET or type(data_aux) == ET.Element:
                data_aux = ET.tostring(data_aux, encoding='unicode')
            elif type(data_aux) != str:
                message = "XML payload must be either string or ElementTree."
                raise utils.ArgError(message)
        else:
            message = "Post content type must be either 'json' or 'xml'"
            raise utils.ArgError(message)

        # Send request
        response = requests.post(url, data=data_aux, params=args_aux, headers=headers_aux)
        if raw:
            return response

        # Parse content
        content = self.__parse_response__(response)

        return content

    def Get(self, url, args, headers, raw=False):
        """
        Uses requests library to make Exlibris API Get call.
        Returns data of type specified during init of base class.

        Args:
            url (str): Exlibris API endpoint url.
            args (dict): Query string parameters for API call.
            headers (dict): API Key Auth in Headers.
            raw (bool): If true, returns raw response.

        Returns:
            JSON-esque, xml, or raw response.
        """
        
        args_aux = args.copy()
        headers_aux = headers.copy()
        
        # handle data format. Allow for overriding of global setting.
        data_format = self.cnxn_params['format']
        if 'format' not in args_aux.keys():
            args_aux['format'] = data_format

        # Preserve Auth and add 'User-Agent' in headers
        headers_aux['User-Agent'] = self.cnxn_params['User-Agent']

        # Send request.
        response = requests.get(url, params=args_aux, headers=headers_aux)

        if raw:
            return response

        # Parse content
        content = self.__parse_response__(response)

        return content

    def Put(self, url, data, headers, raw=False):
        """
        Uses requests library to make Exlibris API Put call.
        Returns data of type specified during init of base class.

        Args:
            url (str): Exlibris API endpoint url.
            data (dict): Data to be puted.
            headers (dict): API Key Auth in Headers.
#            object_type (str): Type of object to be puted (see alma docs)
            raw (bool): If true, returns raw response.

        Returns:
            JSON-esque, xml, or raw response.
        """

        data_aux = data.copy()

        # Preserve Auth and add 'User-Agent' in headers
        headers_aux = headers.copy()
        headers_aux['User-Agent'] = self.cnxn_params['User-Agent']
        
        # Determine format of data to be puted according to order of importance:
        # 1) Local declaration, 2) dtype of data parameter, 3) global setting.
        if type(data_aux) == ET or type(data_aux) == ET.Element:
            content_type = 'xml'
        elif type(data_aux) == dict:
            content_type = 'json'
        else:
            content_type = self.cnxn_params['format']

        # Determine 'content-type' and set 'data_aux' format in consecuence
        if content_type == 'json':
            headers_aux['content-type'] = 'application/json'
            if type(data_aux) != str:
                data_aux = json.dumps(data_aux)
        elif content_type == 'xml':
            headers_aux['content-type'] = 'application/xml'
            if type(data_aux) == ET or type(data_aux) == ET.Element:
                data_aux = ET.tostring(data_aux, encoding='unicode')
            elif type(data_aux) != str:
                message = "XML payload must be either string or ElementTree."
                raise utils.ArgError(message)
        else:
            message = "Put content type must be either 'json' or 'xml'"
            raise utils.ArgError(message)

        # Send request
        response = requests.put(url, data=data_aux, headers=headers_aux)

        if raw:
            return response

        # Parse content
        content = self.__parse_response__(response)

        return content

    def Delete(self, url, args, headers, raw=False):
        """
        Uses requests library to make Exlibris API Delete call.
        Returns data of type specified during init of base class.

        Args:
            url (str): Exlibris API endpoint url.
            args (dict): Query string parameters for API call.
            headers (dict): API Key Auth in Headers.
            raw (bool): If true, returns raw response.

        Returns:
            JSON-esque, xml, or raw response.
        """

        args_aux = args.copy()

        # Preserve Auth and add 'User-Agent' in headers
        headers_aux = headers.copy()
        headers_aux['User-Agent'] = self.cnxn_params['User-Agent']

        # Determine format of data to be posted
        if 'format' not in args_aux.keys():
            args_aux['format'] = self.cnxn_params['format']

        # Determine 'content-type'
        if args_aux['format'] == 'json':
            headers_aux['content-type'] = 'application/json'
        elif args_aux['format'] == 'xml':
            headers_aux['content-type'] = 'application/xml'
        else:
            message = "Post content type must be either 'json' or 'xml'"
            raise utils.ArgError(message)

        # Send request
        response = requests.delete(url, params=args_aux, headers=headers_aux)

        if raw:
            return response

#TODO: Eval exception 204
        """
        # Parse content
        content = self.__parse_response__(response)

        return content
        """
        return response

    def __format_query__(self, query):
        """Converts dictionary of brief search query to a formated string.
        https://developers.exlibrisgroup.com/blog/How-we-re-building-APIs-at-Ex-Libris#BriefSearch

        Args:
            query: dictionary of brief search query.
                Format - {'field': 'value', 'field2', 'value2'}.
        Returns:
            String of query.
        """
        q_str = ""
        i = 0
        if type(query) != 'dict':
            message = "Brief search query must be a dictionary."
        for field, filter_value in query.items():
            field = str(field)
            filter_value = str(filter_value)
            if i > 0:
                q_str += " AND "
            q_str += (field + "~")
            q_str += filter_value.replace(" ", "_")
            i += 1

        return q_str

    def __Get_all__(self, url, args, headers, raw, response, data_key, max_limit=100):
        """Makes multiple API calls until all records for a query are retrieved.
            Called by the 'all_records' parameter.

        Args:
            url (str): Exlibris API endpoint url.
            args (dict): Query string parameters for API call.
            headers (dict): API Key Auth in Headers.
            raw (bool): If true, returns raw response.
            response (xml, raw, or json): First API call.
            data_key (str): Dictionary key for accessing data.
            max_limit (int): Max number of records allowed to be retrieved in a single call.
                Overrides limit parameter. Reduces the number of API calls needed to retrieve data.

        Returns:
            response with remainder of data appended.
            """
        # raw will return a list of responses
        if raw:
            responses = [response]
            response = response.json()

        args['offset'] = args['limit']
        limit = args['limit']

        # get total record count of query
        if type(response) == dict:
            total_records = int(response['total_record_count'])
        elif type(response) == ET.Element:
            total_records = int(response.attrib['total_record_count'])
        else:
            total_records = limit

        # set new retrieval limit
        records_retrieved = limit
        args['limit'] = max_limit
        limit = max_limit

        # Preserve Auth and add 'User-Agent' in headers
        headers_aux = headers.copy()
        headers_aux['User-Agent'] = self.cnxn_params['User-Agent']

        while True:
            if total_records <= records_retrieved:
                break

            # make call and increment counter variables
            new_response = self.get(url, args=args, headers=headers_aux, raw=raw)
            records_retrieved += limit
            args['offset'] += limit

            # append new records to initial response
            if type(new_response) == dict:
                response[data_key] += new_response[data_key]
            elif type(new_response) == ET.Element:
                for row in list(new_response):
                    response.append(row)
            elif raw:
                responses.append(new_response)

        if raw:
            response = responses

        return response

    def __parse_response__(self, response):
        """Parses alma response depending on content type.

        Args:
            response: requests object from Alma.

        Returns:
            Content of response in format specified in header.
        """
        status = response.status_code
        url = response.url
        try:
            response_type = response.headers['content-type']
            if ";" in response_type:
                response_type, charset = response_type.split(";")
        except:
            message = 'Error ' + str(status) + response.text
            raise utils.AlmaError(message, status, url)

        # decode response if xml.
        if response_type == 'application/xml':
            xml_ns = self.cnxn_params['xml_ns']  # xml namespace
            content = ET.fromstring(response.text)

            # Received response from ex libris, but error retrieving data.
            if str(status)[0] in ['4', '5']:
                try:
                    first_error = content.find("header:errorList", xml_ns)[0]
                    message = first_error.find("header:errorCode", xml_ns).text
                    message += " - "
                    message += first_error.find("header:errorMessage", xml_ns).text
                    message += " See Alma documentation for more information."
                except:
                    message = 'Error ' + str(status) + " - " + str(content)
                raise utils.AlmaError(message, status, url)

        # decode response if json.
        elif response_type == 'application/json':
            content = response.json()

            # Received response from ex libris, but error retrieving data.
            if str(status)[0] in ['4', '5']:
                try:
                    if 'web_service_result' in content.keys():
                        first_error = content['web_service_result']['errorList']['error'][0]
                    else:
                        first_error = content['errorList']['error'][0]
                    message = first_error['errorCode']
                    message += " - "
                    message += first_error['errorMessage']
                    if 'trackingID' in first_error.keys():
                        message += "TrackingID: " + message['trackingID']
                    message += " See Alma documentation for more information."
                except:
                    message = 'Error ' + str(status) + " - " + str(content)
                raise utils.AlmaError(message, status, url)

        else:
            content = response

            if str(status)[0] in ['4', '5']:
                message = str(status) + " - "
                message += str(content.text)
                raise utils.AlmaError(message, status, url)
        return content
