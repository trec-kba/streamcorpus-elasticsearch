'''indexing configuration for loading a
:class:`~streamcorpus.StreamItem` into elasticsearch

.. This software is released under an MIT/X11 open source license.
   Copyright 2012-2014 Diffeo, Inc.

'''
import datetime

def stream_item_to_json(stream_item):
    '''Create a JSON object from a :class:`~streamcorpus.StreamItem`

    The fields created in this JSON object will be indexed by
    elasticsearch, so this is essentially the index configuration.    
    '''
    ## TODO: figure out how to cause elasticsearch to treat these
    ## fields as ``typed`` in some way.  For example, the abs_url
    ## really should become a clickable link URL, does it need to be
    ## renamed for elasticsearch to figure that out?  Or can we load a
    ## schema?  

    ## Can the `timestamp` field be identified here as the thing to
    ## use for building time series?

    ## Can we turn on fancier indexing for the primary body text,
    ## which is `clean_visible`?
    doc = {
        'timestamp' : datetime.datetime.utcfromtimestamp(stream_item.stream_time.epoch_ticks),
        'abs_url' : stream_item.abs_url,
        'clean_visible' : stream_item.body.clean_visible,
        'language' : stream_item.body.language.name,
        'stream_id' : stream_item.stream_id,
        'doc_id' : stream_item.doc_id,
        'source' : stream_item.source or 'UNKNOWN',        
    }
    return doc

def index_stream_item(es, index_name, stream_item):
    '''Index an individual :class:`~streamcorpus.StreamItem`
    
    Uses :attr:`~streamcorpus.StreamItem.stream_id` as `id`
    '''

    ## Call elasticsearch index function on remote server
    res = es.index(
        index=index_name,
        doc_type='stream_items',
        id=stream_item.stream_id,
        body=stream_item_to_json(stream_item),
        )


def index_stream_items(es, index_name, stream_items, batch_size=100):
    '''Index multiple :class:`~streamcorpus.StreamItem` instances

    Treats `stream_items` as a possibly very large generator and
    indexes in batches of `batch_size`
    '''
    return NotImplemented
    ## TODO: implement this using the bulk ingest API
    ## http://elasticsearch-py.readthedocs.org/en/master/api.html#elasticsearch.Elasticsearch.bulk
