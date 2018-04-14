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
import re
import lxml.etree as etree
#file prefix_dict allows user to access udb files for comparison. key = commit_message and value is tuple of udb file paths. This will store all the udb file paths for each search analysis so that they can compare them with our algorithm.
file_prefix_dict = {}
repo_objects = list()
#commit_list contains commit sets for each query of repo
#user required to use repo number and random key to access commit_list data
#user can store many query results for different repos in this dictionary for each session
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
            #commit_list contains commit sets for each query of repo
            commit_lists[key] = matched_commits
            print("RESULT KEY = %s" %key )
            print(matched_commits)
            print("Step 3: Now you can analyze your commit changes\nType: analyze <repo_number> <RESULT KEY>\nthis will produce analyzed udb files)
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
            file_prefix_dict[commit_pair] = ('./projects/%sbefore.udb'%file_prefix, './projects/%safter.udb'%file_prefix)

            f = open('%s.sh' %file_prefix,'w' )
            f.write('cd projects\ncd %s\ngit checkout %s\nund create -languages java ../%sbefore.udb\nund add -lang java ./ ../%sbefore.udb\nund analyze ../%sbefore.udb\n' %(repo.name, before, file_prefix, file_prefix, file_prefix))
            f.close()
            create_udb(file_prefix)
            #need to remove .sh file

            print("FIRST UDB CREATED")

            f = open('%s.sh' %file_prefix,'w' )
            f.write('cd projects\n cd %s\ngit checkout %s\nund create -languages java ../%safter.udb\nund add -lang java ./ ../%safter.udb\nund analyze ../%safter.udb' %(repo.name, after, file_prefix, file_prefix, file_prefix))
            f.close()
            create_udb(file_prefix)

            print("SECOND UDB CREATED")
            print(file_prefix_dict)
            print("\nStep 4: Next step is to view the parameter changes on all functions and methods.\n TYPE: compare <index of dictionary item (commit) to compare>\n ")
            # if count == 1:
            #     break


    def do_compare(self, index):
        file_paths = list(file_prefix_dict.values())
        udb_before = file_paths[int(index)-1][0]
        udb_after = file_paths[int(index)-1][1]
        compare_udbs(udb_before, udb_after)
        print("your comparison xml file (parameterChange.xml) is now available in your current directory\n\nYou may restart the process from step 1 if you want more analyses")

    def do_quit(self, args):
        """Quits the program."""
        print ("Quitting.")
        raise SystemExit

#algo here:
def sortKeyFunc(ent):
    return str.lower(ent.longname())

def compare_udbs(udb_before, udb_after):
    # Open Database
    dbBefore = understand.open(udb_before)
    dbAfter = understand.open(udb_after)

    root = etree.Element("root")
    doc = etree.SubElement(root, "doc")



    entsBefore = dbBefore.ents("function,method,procedure")
    #entsBefore = dbBefore.ents()
    entsAfter = dbAfter.ents("function,method,procedure")
    #entsAfter = dbAfter.ents()


    for funcB in sorted(entsBefore,key = sortKeyFunc):
      for funcA in sorted(entsAfter,key = sortKeyFunc):
        if funcB.name() == funcA.name():
          method = etree.SubElement(doc,"method", name = funcB.name())
          #print("Haha, these two equal!")
          for paramA in funcA.ents("Define","Parameter"):
            for paramB in funcB.ents("Define","Parameter"):

               if paramA == paramB and paramA.type() != paramB.type():

                  change = etree.SubElement(method,"change")
                  parameter = etree.SubElement(change, "parameter", oldtype = paramB.type(), newtype = paramA.type()).text = str(paramB)

    tree = etree.ElementTree(root)
    tree.write("parameterChange.xml")

    dbBefore.close()
    dbAfter.close()


def create_udb(arg):
    with open('%s.sh' %arg, 'rb') as file:
        script = file.read()
    rc = call(script, shell=True)
    print("udb file created")
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
        print("Instruction:\nType: choose <repo_number>\nthis will clone the repo locally or tell you it's already cloned")


def clone_repos(index):
    #clone each repo to projects
    repo = repo_objects[index-1]
    checkdir = Path("./projects/%s" % repo.name)
    if validate_cloned(repo):
        print("%s already cloned" %repo.name)
        print('Step2: search the commit metadata\nType: search <repo_number> <inLine keyword>')
        return
    else:
        print("cloning %s" %repo.name)
        Repo.clone_from(repo.html_url, "./projects/%s" % repo.name)
        print('done cloning %s' %repo.name)
        print('Step2: search the commit metadata\nType: search <repo_number> <inLine keyword>')
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
    print("instructions:\nYou will be prompted through a series of steps\nStep1: choose repository to analyze\nStep2: search repositories commit metadata using keyword search to retrieve a list of commits and their parent commits that match the keyword search\nStep3: analyze the commits entity data using Understand API\nStep4: compare the entity data to learn what method and function parameter changes occured in the repo based on your metadata search at\n\nAt any point in the process you can redo any of the previous steps if you'd like by simply running those commands again")
    get_repos()
    prompt = MyPrompt()
    prompt.prompt = '> '
    prompt.cmdloop('Starting prompt...')
