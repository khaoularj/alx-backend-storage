#!/usr/bin/env python3
"""this is a function that inserts a new
document in a collection based on kwargs"""


def insert_school(mongo_collection, **kwargs):
    """this function return the ObjectId of the newly inserted document"""
    return mongo_collection.insert_one(kwargs).inserted_id
