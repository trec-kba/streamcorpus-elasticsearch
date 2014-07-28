'''Run the elasticsearch index loader under :mod:`rejester`.

.. This software is released under an MIT/X11 open source license.
   Copyright 2012-2014 Diffeo, Inc.

'''
from __future__ import absolute_import
import argparse
import itertools

import dblogger
import kvlayer
import rejester
import yakonfig
import elasticsearch

import logging

from diffeo_search_tools import elasticsearch_loader

logger = logging.getLogger(__name__)

def rejester_run(work_unit):
    '''Rejester entry point to run the elasticsearch load.

    This uses the work unit key as the input filename string for the
    reader specified in the work unit.  If the work unit data
    includes the key ``output`` then that value is passed as the matching
    output filename string.

    :param work_unit: work unit to run
    :type work_unit: :class:`rejester.WorkUnit`

    '''
    if 'config' not in work_unit.spec:
        raise rejester.exceptions.ProgrammerError(
            'could not run without global config')

    with yakonfig.defaulted_config([rejester, kvlayer, dblogger],
                                   config=work_unit.spec['config']):

        ## Setup elasticsearch client
        ## http://elasticsearch-py.readthedocs.org/en/master/api.html#elasticsearch
        es = elasticsearch.Elasticsearch(work_unit.spec['config']['elasticsearch']['cluster'])

        ## Setup kvlayer client
        kvl = kvlayer.client()
        kvl.setup_namespace({'stream_items': 2})

        ## Get data associate with work_unit
        key, data = kvl.get('stream_items', work_unit.key).next()

        ## Index an individual stream_item
        elasticsearch_loader.index_stream_item(es, kvl, data)


def rejester_terminate(work_unit):
    '''Rejester entry point on very unusual termination.

    This function is only called when the rejester worker is killed
    with a signal.  Does nothing.

    '''
    pass

# def _uuid_2_to_sid(pair):
#     '''Convert a pair of UUIDs to a stream ID'''
#     epoch_ticks_uuid, doc_id_uuid = pair
#     return '{}-{}'.format(epoch_ticks_uuid.int, doc_id_uuid.hex)

def _sid_iter(kvl, sources):
    '''Get an iterator over stream IDs. '''

    if sources is None:
        kvl.setup_namespace({'stream_items': 2})
        si_iter = kvl.scan_keys('stream_items')
    else:
        kvl.setup_namespace({'stream_items_with_source': 2})
        # Scan stream_items_with_source, but drop (now) the ones
        # that aren't in a valid source, then just return keys
        siws_iter = kvl.scan('stream_items_with_source')
        source_iter = itertools.ifilter(lambda p: p[1] in sources,
                                        siws_iter)
        si_iter = itertools.imap(lambda p: p[0], source_iter)
    # return itertools.imap(_uuid_2_to_sid, si_iter)
    return si_iter

def make_rejester_jobs(task_master, kvl, sources, work_spec_name):
    '''Create :mod:`rejester` jobs for inbound stream items.

    Each job runs :func:`rejester_run` in this module to run the
    elasticsearch index over a set of stream items.

    :param kvl: kvlayer client
    :type kvl: :class:`kvlayer._abstract_storage.AbstractStorage`
    :param list sources: source name strings to consider, or
      :const:`None` for all
    :param str work_spec_name: name of the rejester work spec

    '''
    work_spec = {
        'name': work_spec_name,
        'desc': 'elasticsearch loader',
        'min_gb': 1,
        'config': yakonfig.get_global_config(),
        'module': 'diffeo_search_tools.rejester_runner',
        'run_function': 'rejester_run',
        'terminate_function': 'rejester_terminate',
    }
    si_iter = _sid_iter(kvl, sources)
    # No value needed in following dict
    work_units = { key: 0 for key in si_iter }
    # work_units = { 'item': si_iter.next() }
    task_master.update_bundle(work_spec, work_units)

def main():
    parser = argparse.ArgumentParser(
        description='create rejester jobs to load elasticsearch',
        conflict_handler='resolve')
    parser.add_argument('--source', action='append',
                        help='source strings to consider')
    parser.add_argument('--work-spec-name', '-W', metavar='NAME',
                        default='elasticsearch',
                        help='name of rejester work spec')
    args = yakonfig.parse_args(parser, [yakonfig, rejester, kvlayer, dblogger])

    task_master = rejester.TaskMaster(yakonfig.get_global_config('rejester'))
    kvl = kvlayer.client()
    make_rejester_jobs(task_master, kvl, args.source,  args.work_spec_name)

if __name__ == '__main__':
    main()
