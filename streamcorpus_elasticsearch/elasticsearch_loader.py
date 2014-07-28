'''Run the elasticsearch index loader

.. This software is released under an MIT/X11 open source license.
   Copyright 2012-2014 Diffeo, Inc.

'''
from __future__ import absolute_import
import argparse

import logging
import dblogger
import kvlayer
import rejester
import yakonfig
import elasticsearch
import streamcorpus
import datetime

logger = logging.getLogger(__name__)

config_name = 'elasticsearch'

def index_stream_item(es, sid, data):
    ''' Index an individual stream_item '''

    ## Demcompress and deserialize data into stream_item
    errors, data = streamcorpus.decrypt_and_uncompress(data)
    stream_item = streamcorpus.deserialize(data)

    ## Create the document that will be indexed
    ## Individual fields to index were selected by jrf
    doc = {
        'timestamp' : datetime.datetime.utcfromtimestamp(stream_item.stream_time.epoch_ticks),
        'abs_url' : stream_item.abs_url,
        'clean_visible' : stream_item.body.clean_visible,
        'language' : stream_item.body.language.name,
        'stream_id' : stream_item.stream_id,
        'doc_id' : stream_item.doc_id,
    }

    ## Call elasticsearch index function on remote server
    res = es.index(index="stream-item-index",
                   doc_type='stream_items',
                   id=stream_item.stream_id,
                   body=doc)


def load_stream_items(kvl, es):
    '''Index stream_items in elasticsearch '''

    for count, (sid, data) in enumerate(kvl.scan('stream_items')):
        ## logging defaults don't seem to be working as I expected
        ## so will incorrectly make this 'critical'
        logger.critical('%d', count)
        index_stream_item(es, sid, data)


if __name__ == '__main__':
    ## Setup configuration
    ## See <wiki>/projects/yakonfig
    parser = argparse.ArgumentParser(description='load streamitems into elasticsearch',
                                     conflict_handler='resolve')
    args = yakonfig.parse_args(parser, [yakonfig, rejester, kvlayer, dblogger])
    config = yakonfig.get_global_config()

    ## Setup elasticsearch client
    ## http://elasticsearch-py.readthedocs.org/en/master/api.html#elasticsearch
    es = elasticsearch.Elasticsearch(config['elasticsearch']['cluster'])

    ## Setup kvlayer client
    kvl = kvlayer.client()
    kvl.setup_namespace({'stream_items': 2})

    ## Load stream items
    load_stream_items(kvl, es)
