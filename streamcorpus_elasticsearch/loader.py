'''Run the elasticsearch index loader

.. This software is released under an MIT/X11 open source license.
   Copyright 2012-2014 Diffeo, Inc.

'''
from __future__ import absolute_import, division
import argparse
import logging

import elasticsearch

import dblogger
import kvlayer
import rejester
import yakonfig
import streamcorpus

from streamcorpus_elasticsearch.indexing import index_stream_item

logger = logging.getLogger(__name__)

config_name = 'elasticsearch'

def load_stream_items(kvl, es, index_name):
    '''Index stream_items in elasticsearch '''

    start_time = time.time()
    count = 0
    for sid, data in kvl.scan('stream_items'):
        count += 1
        if count % 100 == 0:
            elapsed = time.time() - start_time
            rate = count / elapsed
            logger.info('%d StreamItems loaded in %.3f seconds --> %.1f/sec', count, elapsed, rate)

        ## Decompress and deserialize data into stream_item
        errors, data = streamcorpus.decrypt_and_uncompress(data)
        stream_item = streamcorpus.deserialize(data)

        index_stream_item(es, index_name, stream_item)


if __name__ == '__main__':
    ## Setup configuration
    ## See <wiki>/projects/yakonfig
    parser = argparse.ArgumentParser(description='load streamitems into elasticsearch',
                                     conflict_handler='resolve')
    parser.add_argument('index_name', help-'name of the index to use in elasticsearch cluster (creates if new)')
    args = yakonfig.parse_args(parser, [yakonfig, rejester, kvlayer, dblogger])
    config = yakonfig.get_global_config()

    ## Setup elasticsearch client
    ## http://elasticsearch-py.readthedocs.org/en/master/api.html#elasticsearch
    es = elasticsearch.Elasticsearch(config['elasticsearch']['cluster'])

    ## Setup kvlayer client
    kvl = kvlayer.client()
    kvl.setup_namespace({'stream_items': 2})

    ## Load stream items
    load_stream_items(kvl, es, args.index_name)
