''''delete all StreamItems in an elasticsearch index

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

logger = logging.getLogger(__name__)


if __name__ == '__main__':
    ## Setup configuration
    ## See <wiki>/projects/yakonfig
    parser = argparse.ArgumentParser(description=__doc__,
                                     conflict_handler='resolve')
    parser.add_argument('index_name', help='name of index to completely delete, use "_all" to destroy everything in the cluster')
    args = yakonfig.parse_args(parser, [yakonfig, rejester, kvlayer, dblogger])
    config = yakonfig.get_global_config()

    ## Setup elasticsearch client
    ## http://elasticsearch-py.readthedocs.org/en/master/api.html#elasticsearch
    es = elasticsearch.Elasticsearch(config['elasticsearch']['cluster'])


    ## TODO:  extend this to do more things than just delete?
    es.delete_by_query(index=args.index_name, q='*')
