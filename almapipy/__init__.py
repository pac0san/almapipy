# -*- coding: utf-8 -*-

"""
Python requests wrapper for the Ex Libris Alma API
"""


from .client import Client
from .bibs import SubClientBibs
from .analytics import SubClientAnalytics
from .courses import SubClientCourses
from .users import SubClientUsers
from .acquisitions import SubClientAcquistions
from .conf import SubClientConfiguration
from .partners import SubClientPartners
from .electronic import SubClientElectronic
from .task_lists import SubClientTaskList
from . import utils


__author__ = "Steve Pelkey"
__author_email__ = "spelkey@ucdavis.edu"
__project_name__ = "almapipy"
__project_description__ = "Python requests wrapper for the Ex Libris Alma API"
__project_url__ = "https://github.com/UCDavisLibrary/almapipy"
__license__ = "MIT License"
__version__ = "0.1.2.dev0"
__status__ = "Development"


class AlmaCnxn(Client):
    """"Interface with Alma APIs.

    Various Apis are namespaced beneath this object according to documentation
    at https://developers.exlibrisgroup.com/alma/apis.

    E.g.
    > alma = AlmaCnxn(your_api_key)
    > alma.bibs.catalog.get_record(bib_id) # returns bibliographic records

    Args:
        api_key (str): Your Api Key
        Location (str): Geographic location of library.
        data_format (str): Format of returned data. json or xml.
            If xml is selected, data will be returned as python xml ElementTree.
    """

    def __init__(self, apikey, location='America', data_format='json'):

        super(AlmaCnxn, self).__init__()

        # determine base uri based on location
        locations = {'America': 'https://api-na.hosted.exlibrisgroup.com',
                     'Europe': 'https://api-eu.hosted.exlibrisgroup.com',
                     'Asia Pacific': 'https://api-ap.hosted.exlibrisgroup.com',
                     'Canada': 'https://api-ca.hosted.exlibrisgroup.com',
                     'China': 'https://api-cn.hosted.exlibrisgroup.com'}
        if location != 'America':
            if location not in locations.keys():
                message = "Valid location arguments are "
                message += ", ".join(locations.keys())
                raise utils.ArgError(message=message)
        self.cnxn_params['location'] = location
        self.cnxn_params['base_uri'] = locations[location]

        # handle preferred format
        if data_format not in ['json', 'xml']:
            message = "Format argument must be either 'json' or 'xml'"
            raise utils.ArgError(message)
        self.cnxn_params['format'] = data_format
        ns = {'header': 'http://com/exlibris/urm/general/xmlbeans'}
        self.cnxn_params['xml_ns'] = ns

        # TODO: validate api key. return list of accessible endpoints
        # call __validate_key__
        self.cnxn_params['api_key'] = apikey

        # Set 'User-Agent' for REST queries
        self.cnxn_params['User-Agent'] = '{}/{}'.format(__name__,__version__)

        # Hook in the various Alma APIs based on what API key can access
        self.bibs = SubClientBibs(self.cnxn_params)
        self.analytics = SubClientAnalytics(self.cnxn_params)
        self.courses = SubClientCourses(self.cnxn_params)
        self.users = SubClientUsers(self.cnxn_params)
        self.acq = SubClientAcquistions(self.cnxn_params)
        self.conf = SubClientConfiguration(self.cnxn_params)
        self.partners = SubClientPartners(self.cnxn_params)
        self.electronic = SubClientElectronic(self.cnxn_params)
        self.task_lists = SubClientTaskList(self.cnxn_params)

    def __validate_key__(self, apikey):
        # loop through each api and access the /test endpoint.
        # return list of accessible apis.
        pass
