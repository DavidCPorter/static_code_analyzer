from github import Github
import sys

import understand

import gitlab

##gotta figure out how to get from github to gitlab... but gotta move on, let's just work with gitlab for now


# private token or personal token authentication


def main():

    #Gitlab REPOs
    # for arg in args:
    #     if arg != 'tomahawk':
    #         sys.stderr.write('arg needs to be "tomahawk"')
    #
    # mygitlab = gitlab.Gitlab('http://0.0.0.0:80', private_token='QvsMuiYs9SziromWuX-g')
    #
    # projects = mygitlab.projects.list()
    # print (args)


    # Access Token
    mygithub = Github("d566ce209207556c3dcedb2eff139a63c5cd8a9e")

    # Then play with your Github objects:
    for repo in g.get_user().get_repos():
        print(repo.url)

    #get issue commits
    # dif issue commits
    # cat



    db = understand.open("./understandDB/simple.udb")

    entities = db.ents()

# print characteristics of unsorted entities
    for ent in entities:
        print(ent.name())
        print("Longname: " + ent.longname())
        print("Parameters: ", ent.parameters())
        print("Kind: ", ent.kind())
        print("Metric: ", ent.metrics())
        print("Parent: ", ent.parent())
        print("Type: ", ent.type())
        print("Name: ", ent.name())
        print("---")


if __name__ == '__main__':
   main()
