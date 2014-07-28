streamcorpus-elasticsearch
==========================

Use Cases
---------

 1. Ingest and index streamcorpus Chunk files from S3.  The chunk
 files might be part of a public data set, e.g. the [TREC KBA
 StreamCorpora](http://s3.amazonaws.com/aws-publicdatasets/trec/kba/index.html)
 or loaded by a private application of
 [streamcorpus-pipeline](http://streamcorpus.org)

 1. Enable easy discovery of *which* web domains contain particular
 keywords and language content.  For example, show me the web domains
 that contain the most documents written in the Chinese language and
 containing the word "Hétóng," which means "deal."  This will enable
 us to manually select which domains to prioritize in crawling more
 data.

 1. Enable easy browsing of documents matching keyword and language
 constraints.  For example, let me read each document that mentions
 "Hétóng" and let me see which web domains contain the most documents
 matching the query.


v1.0 Requirements
-----------------

  1. Is operated and configured with salt, so that all of your private
  config info gets stored in your own private git repo holding all the
  salt states.  

  1. Documented best practices for forking the repo and customizing,
  and pulling updates from the public upstream repo.

  1. Creates an ElasticSearch cluster using EC2 APIs

  1. Configure it for ingesting StreamItems and indexing appropriate
  fields (see Use Cases below).

  1. Configure ElasticSearch User Interface to enable filtering on
  StreamItem metadata (details in Use Case below)

  1. Display a list of results with excerpted snippets showing the
  query terms.

  1. Display facets of metadata indexed with the documents to support
  the two use cases below.

  1. View a document's clean_visible text inside of HTML ``PRE`` tags,
  so that the whitespace between words is visible.

  1. public pypi package (pushed by a buildbot that diffeo operates)

  1. py.test unit tests with >80% coverage as measured by `coverage`

  1. View a document's clean_html in an iframe


Strawman Design
---------------

This is a rough cut at a possible design.  Nothing in this is sacred;
it should all be challenged and re-evaluated during implementation.

 1. salt config pieces for configuring elasticsearch to consume
    StreamItems starting from a bare ubuntu cloud image
 1. python module that provides a streamcorpus-pipeline writer
    stage for pushing into elasticsearch with all the metadata
    fields constructed.
 1. tests can spin up a new instance and run a small selection of
    specific chunk files from the [TREC KBA 2014 Serif-only
    corpus](http://s3.amazonaws.com/aws-publicdatasets/trec/kba/index.html)
    corpus through it, and then run a battery of tests against it.
    This corpus contains all of the metadata described below, so tests
    can cover the full list of indexed field types.
    

StreamCorpus Metadata to Index
------------------------------

Fields needed for base requirements:

 * full-text search on clean_visible
 * facetted search on si.body.language.name
 * nested facetted queries on DNS domains, e.g. [boggle.doggy.com, doggy.com, com]
 * fielded exact match queries on stream_id, doc_id, abs_url


Other fields to index for future phases:

 * range queries on epoch_ticks
 * nested facetted queries on datetime buckets from zulu_timestamp prefixes: YEAR, YEAR-MONTH, YEAR-MONTH-DAY, YEAR-MONTH-DAY-HOUR
 * nested facetted search on tagger_id-->entity_type-->mention tokens (from boNAME and boNOM)
 * range queries on len(clean_visible)




Future Phases:
--------------

  1. Can this effectively utilize spot instances for "elastic" scaling
  when query load bursts?

