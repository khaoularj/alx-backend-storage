#!/usr/bin/env python3
"""this script provides some stats about
Nginx logs stored in MongoDB"""
from pymongo import MongoClient
methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]


def log_stats(mongo_collection):
    """script provides some stats about
    Nginx logs stored in MongoDB"""
    total = mongo_collection.count_documents({})
    methods_counts = {}
    for method in methods:
        count = mongo_collection.count_documents({"method": method})
        methods_counts[method] = count

    status = mongo_collection.count_documents(
        {"method": "GET", "path": "/status"})
    return total, methods_counts, status


if __name__ == "__main__":
    nginx_collection = MongoClient('mongodb://127.0.0.1:27017').logs.nginx

    total, methods_counts, status = log_stats(nginx_collection)

    print(f"{total} logs")
    print("Methods:")
    for method, count in methods_counts.items():
        print(f"    method {method}: {count}")
    print(f"{status} status check")
