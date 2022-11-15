# -*- coding: utf-8 -*-
# author:m18830190201@163.com

import getpass

from gerrit_query import GerritQuery

# necessary parameters: url,username,password

# input your target gerrit server url
url="https://gerrit.example.cn"

# add your username and password to login target gerrit server
username=input("please input your username: ")
password=getpass.getpass('password: ')


# optional parameters: status,owner,branch,project,mergedafter,mergedbefore
status=""
owner=""
branch=""
project=""

# input merged time eg:2022-1-1
mergedafter=""
mergedbefore=""


test=GerritQuery(url=url,username=username,password=password,status=status,owner=owner,branch=branch,project=project,mergedafter=mergedafter,mergedbefore=mergedbefore)

# output result of querying, return a dictionary includes "changes_list","origin_nums","deduplicate_nums"
print(test.query_changes())

# the total changes list after querying
print(test.query_changes()["changes_list"])

# the number of all changes
print(test.query_changes()["origin_nums"])

# the number of not duplicated changes
print(test.query_changes()["deduplicate_nums"])