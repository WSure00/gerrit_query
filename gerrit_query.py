# -*- coding: utf-8 -*-
# author:m18830190201@163.com

import requests
import sys
import re
import datetime

class GerritQuery(object):

    def __init__(self,username,password,url,owner=None,status=None,branch=None,project=None,mergedafter=None,mergedbefore=None):

        self.__header={
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive'
        }

        self.changes_list=[]
        self.origin_changes_n=0
        self.uniq_changes_n=0
        
        if username:
            self.__username=username.strip()

        if password:
            self.__password=password.strip()

        if url:
            self.url=url.strip()
            self.login_url=self.url+"/login/%2F"
            self.change_url=self.url+"/changes/?q="

        if owner:
            self.owner=owner.strip()
        else:
            self.owner=""
        if status:
            self.status=status.strip()
        else:
            self.status=""
        if branch:
            self.branch=branch.strip()
        else:
            self.branch=""
        if project:
            self.project=project.strip()
        else:
            self.project=""
        if mergedafter:
            self.mergedafter=mergedafter.strip()
        else:
            self.mergedafter=""
        if mergedbefore:
            self.mergedbefore=mergedbefore.strip()
        else:
            self.mergedbefore=""
    
    def __str__(self) -> str:
        pass

    def __set_cookie(self):
        data={'username':self.__username,'password':self.__password}
        session = requests.session()
        response = session.post(self.login_url,data)
        
        if response.status_code == 200:
            # print(self.change_url+" post ok")
            pass
        else :
            print(self.change_url+" login failed")
            print("login url: ",self.login_url)
            print("response: ",response.status_code)
            sys.exit(1)

        GerritAccount_Cookie = session.cookies.get_dict()["GerritAccount"]
        self.__header["Cookie"] = "GerritAccount=" + GerritAccount_Cookie
        return self.__header

    def __set_owner(self):
        if self.owner != "":
            self.change_url+="+owner:{}".format(self.owner)
        return self.change_url
   
    def __set_status(self):
        if self.status != "":
            self.change_url+="+status:{}".format(self.status)
        return self.change_url

    def __set_branch(self):
        if self.branch != "":
            self.change_url+="+branch:{}".format(self.branch)
        return self.change_url

    def __set_project(self):
        if self.project != "":
            self.change_url+="+project:{}".format(self.project)
        return self.change_url

    def __set_mergedafter(self):
        if self.mergedafter != "":
            self.change_url+="+mergedafter:{}".format(self.mergedafter)
        return self.change_url

    def __set_mergedbefore(self):
        if self.mergedbefore != "":
            self.change_url+="+mergedbefore:{}".format(self.next_day(self.mergedbefore))
        return self.change_url

    def __make_url(self):
        self.__set_status()
        self.__set_owner()
        self.__set_branch()
        self.__set_project()
        self.__set_mergedafter()
        self.__set_mergedbefore()
        return self.change_url

    def get_url(self,url,headers):
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            print(response,url)
            return response.status_code

    def check_url(self,url,headers):

        change_str="change_id"
        response=self.get_url(url,headers)
        if type(response) != int:
            if change_str in self.get_url(url,headers):
                return True
            else:
                return False
        else:
            return False

    def next_day(self,end):
        date=str(datetime.datetime.strptime(end,'%Y-%m-%d')+datetime.timedelta(days=1)).split(" ")[0]
        date=date.split("-")[0]+"-"+date.split("-")[1]+"-{}".format(int(date.split("-")[2]))
        return date

    def uniq_changes(self,changes_list):
        uniq_changes_list=list(set(changes_list))
        uniq_changes_list.sort(key=changes_list.index)
        return len(uniq_changes_list)

    def query_changes(self):

        self.__make_url()
        self.__set_cookie()

        headers=self.__header

        # skip changes and step=150
        i=0
        while True:
            skip_url=self.change_url+"&start={}".format(i*150)
            if self.check_url(skip_url,headers):
                i+=1
                response=self.get_url(skip_url,headers)
                # print(skip_url)
                pattern = re.compile(r'\"change_id\":\"[A-Za-z0-9]{35,64}\"')
                self.changes_list.extend(pattern.findall(response))
                self.origin_changes_n+=len(self.changes_list)
                self.uniq_changes_n+=self.uniq_changes(self.changes_list)
            else:
                break
        return {"changes_list":self.changes_list,"origin_nums":self.origin_changes_n,"deduplicate_nums":self.uniq_changes_n}
