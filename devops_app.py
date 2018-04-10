from github import Github
import sys

import understand

import gitlab
import json
from git import Repo
from pathlib import Path


##gotta figure out how to get from github to gitlab... but gotta move on, let's just work with gitlab for now


# private token or personal token authentication


def main():

    # Access Token
    mygithub = Github("d566ce209207556c3dcedb2eff139a63c5cd8a9e")

    repo_names = list()
    repo_urls = list()
    count = 0

    #Get repos
    for repo in mygithub.get_user().get_repos():
        repo_names.append(repo.name)
        repo_urls.append(repo.html_url)

    for name in repo_names:
        checkdir = Path("./projects/%s" % name)
        if checkdir.is_dir():
            count+=1
            continue
        else:
            Repo.clone_from(repo_urls[count], "./projects/%s" % name)
            count+=1


    #get issue commits
    # dif issue commits
    # cat



#     db = understand.open("./understandDB/simple.udb")
#
#     entities = db.ents()
#
# # print characteristics of unsorted entities
#     for ent in entities:
#         print(ent.name())
#         print("Longname: " + ent.longname())
#         print("Parameters: ", ent.parameters())
#         print("Kind: ", ent.kind())
#         print("Metric: ", ent.metrics())
#         print("Parent: ", ent.parent())
#         print("Type: ", ent.type())
#         print("Name: ", ent.name())
#         print("---")


if __name__ == '__main__':
   main()
