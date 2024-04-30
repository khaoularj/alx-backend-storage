#!/usr/bin/env python3
"""this is a function that lists all documents in a collection"""


def list_all(mongo_collection):
    """function that returns a list of all
    documents in the collection or an empty list"""
    docs = mongo_collection.find()

    if not docs:
        return []
    return list(docs)
