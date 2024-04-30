#!/usr/bin/env python3
"""this is a function that returns the
list of school having a specific topic"""


def schools_by_topic(mongo_collection, topic):
    """this function returns a list of dictionaries
    representing the schools with the specified topic"""
    filter = {"topics": {"$in": [topic]}}
    school_list = list(mongo_collection.find(filter))
    return school_list
