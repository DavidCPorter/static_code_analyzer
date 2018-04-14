from github import Github
import sys
import time

import understand
from subprocess import call
import gitlab
import json
from git import Repo
from pathlib import Path
import pdb
from cmd import Cmd
from random import *


repo_objects = list()
commit_lists = {}


class MyPrompt(Cmd):
    def do_choose(self, args):
        arg0 = int(args)
        if arg0>len(repo_objects) or arg0<1:
            print("ERROR: not valid repo choice - Index out of range")
            return
        clone_repos(arg0)

    def do_search(self, args):
        #arg[0]=index of repo_objects
        #arg[1]=keyword
        args = args.split(" ")
        arg0 = int(args[0])

        if arg0>len(repo_objects) or arg0<0:
            print("ERROR: not valid repo choice - Index out of range")
            return
        if validate_cloned(repo_objects[arg0-1]):
            matched_commits = search_commits(repo_objects[arg0-1], args[1])
            key = randint(1, 1000)
            commit_lists[key] = matched_commits
            print("RESULT KEY = %s" %key )
            print(matched_commits)
            print("how would you like to analyze?")
            return
        else:
            print("repo not located, please redo step 1")
            return

    def do_analyze(self, args):
        count = 0
        #arg[0] = requested index
        #analyze matched commit logs
        args = args.split(" ")
        #get requested repo args[0]
        repo = repo_objects[int(args[0])-1]
        #get requested repo commits key args[1]
        commits = commit_lists[int(args[1])]
        if commits == None:
            print("no commits matched your search... try search step again")
            return
        for commit_pair in commits:
            count+=1
            pair = commits[commit_pair]
            #parent of matched commit
            before = pair[1]
            #matched commit
            after = pair[0]
            file_prefix = repo.name
            file_prefix = file_prefix+str(count)
            f = open('%s.sh' %file_prefix,'w' )
            f.write('cd projects\ncd %s\ngit checkout %s\nund create -languages java ../%sbefore.udb\nund add -lang java ./ ../%sbefore.udb\nund analyze ../%sbefore.udb\n' %(repo.name, before, file_prefix, file_prefix, file_prefix))
            f.close()
            create_udb(file_prefix)
            print("FIRST UDB CREATED")
            # time.sleep(3)

            f = open('%s.sh' %file_prefix,'w' )
            f.write('cd projects\n cd %s\ngit checkout %s\nund create -languages java ../%safter.udb\nund add -lang java ./ ../%safter.udb\nund analyze ../%safter.udb' %(repo.name, after, file_prefix, file_prefix, file_prefix))
            f.close()
            create_udb(file_prefix)
            print("SECOND UDB CREATED")
            # time.sleep(3)


    # def do_compare(self):


    def do_quit(self, args):
        """Quits the program."""
        print ("Quitting.")
        raise SystemExit


def create_udb(arg):
    with open('%s.sh' %arg, 'rb') as file:
        script = file.read()
    rc = call(script, shell=True)
    print("udb file created")
    pdb.set_trace()
    return

def validate_cloned(repo):
    checkdir = Path("./projects/%s" % repo.name)
    if checkdir.is_dir():
        return True
    else:
        return False

def get_repos():

    # Access Token
    mygithub = Github("d566ce209207556c3dcedb2eff139a63c5cd8a9e")

    the_query = {}
    count = 0
    #Get repos
    for repo in mygithub.get_user().get_repos():
        repo_objects.append(repo)
        count+=1
        print(str(count)+"->"+repo.name)


def clone_repos(index):
    #clone each repo to projects
    repo = repo_objects[index-1]
    checkdir = Path("./projects/%s" % repo.name)
    if validate_cloned(repo):
        print("%s already cloned" %repo.name)
        return
    else:
        print("cloning %s" %repo.name)
        Repo.clone_from(repo.html_url, "./projects/%s" % repo.name)
        print('done cloning %s' %repo.name)
        return

    #find issue-related commits

def search_commits(repo, keyword):
    commitMatchDict = {}
    for commit in repo.get_commits():
        message = commit.raw_data['commit']['message']
        if keyword in message:
            if commit.parents == None:
                continue
            #not 100% sure first index is what we want
            commitMatchDict[message] = (commit.sha, commit.parents[0].sha)

    return commitMatchDict






    #
    # for
    #
    # db = understand.open("./understand/%s.udb" % name)
    #
    # entities = db.ents()
    # import pdb
    # pdb.set_trace()

# print characteristics of unsorted entities
    # export PATH=$PATH:/Applications/Understand.app/scitools/bin/macosx/



if __name__ == '__main__':
    print("instructions: ")
    get_repos()
    prompt = MyPrompt()
    prompt.prompt = '> '
    prompt.cmdloop('Starting prompt...')
