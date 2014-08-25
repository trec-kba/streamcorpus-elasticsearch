'''Run the elasticsearch index loader

.. This software is released under an MIT/X11 open source license.
   Copyright 2012-2014 Diffeo, Inc.

'''
from __future__ import absolute_import
import argparse
import logging

import elasticsearch
import streamcorpus
from streamcorpus_pipeline.stages import Configured
import yakonfig

from streamcorpus_elasticsearch.indexing import index_stream_item

logger = logging.getLogger(__name__)


class writer(Configured):
    '''stores StreamItems in an elasticsearch cluster
    '''
    config_name = 'elasticsearch_writer'
    default_config = {}
    #@staticmethod
    #def check_config(config, name):
    #    yakonfig.check_toplevel_config(kvlayer, name)

    def __init__(self, *args, **kwargs):
        super(writer, self).__init__(*args, **kwargs)

        es_config = yakonfig.get_global_config('elasticsearch')

        ## Setup elasticsearch client
        ## http://elasticsearch-py.readthedocs.org/en/master/api.html#elasticsearch
        self.es = elasticsearch.Elasticsearch(es_config['cluster'])

        self.index_name = self.config.get('index_name')
        if not self.index_name:
            raise Exception('elasticsearch_writer must have "index_name" specified')

    def __call__(self, t_path, name_info, i_str):
        for stream_item in streamcorpus.Chunk(t_path):
            index_stream_item(self.es, self.index_name, stream_item)
