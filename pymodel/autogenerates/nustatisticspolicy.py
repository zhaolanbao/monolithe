# -*- coding: utf-8 -*-


from restnuage import NURESTObject


class NUStatisticsPolicy(NURESTObject):
    """ Represents a StatisticsPolicy object """

    def __init__(self):
        """ Initializing object """

        super(NUStatisticsPolicy, self).__init__()

        # Read/Write Attributes
        
        self.data_collection_frequency = None
        self.description = None
        self.name = None
        
        self.expose_attribute(local_name=u"data_collection_frequency", remote_name=u"dataCollectionFrequency", attribute_type=str)
        self.expose_attribute(local_name=u"description", remote_name=u"description", attribute_type=str)
        self.expose_attribute(local_name=u"name", remote_name=u"name", attribute_type=str)

        # Fetchers
        

    @classmethod
    def get_remote_name(cls):
        """ Remote name that will be used to generates URI """

        return u"statisticspolicy"

    # REST methods
    