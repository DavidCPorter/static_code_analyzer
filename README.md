HW2 SUMMARY:

The purpose of this homework for us was to build a program that would analyze metrics and parameter changes (insights) of the code based on the metadata in the commits. So you can essentially correlate development process insights to various topics in your program. So, we intended to build a program that:  
1- ensures you have a copy of your repos locally  
2- keyword searches a selected repo for commit metadata matches  
3- analyze each matched commit's patch file to deduce parameter changes and metrics across the repo for the metadata matched  
4- group the insights together to form a summary of metatdata insights on a repo. (one xml of all the commits matching the critera)  

***PROBLEM SUMMARY***  
However we came across a problem using the understand api via the command line with the "und" tool. It complained about an APIlicense error. However, we were unable to resolve this issue because the advice was to close the db files, but we never opened any before we got this error. This error was during a loop through these steps for each commit pair:
1) und create database
2) und add dir to Database
3) und analyze db

We completed these commands each time through a loop of commit states in a repo. The error was thrown the second time through. We assumed there was a problem with the multiple requests to understand, but we've tried to modify the code by 1) trying to learn if there was a step to close the db after the 3 prior steps, 2) only doing one loop then asking the user for analysis of another set; basically implementing a manual loop. However this still resulted in APILicense error. We figured this may be a problem with macOS, but ultimately decided to move on.  

*********************

All that being said, we still were happy with what we are able to produce, knowing without that error we'd have a great program. You can still gain insights on just a single patch file, but this fell short of fulfilling the purpose of the full repo metadata analysis we were shooting for. In order to avoid the api error you should follow the example sequence below.  

Now for the basic instructions:

Please be sure to :
1) have python3 activated
2) pip install Github  
3) install any other dependencies you are prompted for if not installed already  
4) clone our repo repo  
5) type: python3 devops_app.py  
6) the command prompt will take you through a series of instructions you need to follow, but this is what you need to know:    

a) you start by viewing a list of repos in a stock account we made on github. If you want to use your own repo you can swap the access token in the file.  
b) you select a repo by typing:  
-> choose <repo#>  
c) the program will clone the #repo from the list or tell you it's already cloned  
d) then you will search the commit metadata for the repo  
-> search <repo#> <keyword>  
** this may take a while depending on how many commits are in the repo_objects**  
**this will return a dictionary of commit messages along with their patch (commit pairs) to analyze**  
e) there will be a RESULT KEY associated with the metadata search results, you use that key in the next command with the position in the commit message patch (COMMIT_DICT) you want to analyze:  
-> analyze <repo#> <RESULT KEY> <position in COMMIT_DICT>  
**note, we really just wanted to analyze all of them, but that's were we ran into the API license problem**  
f) The program will create analyzed udb files for you and the next step is to compare them and output the results. You can comapre using two different methods: Parameters or Metrics.  
-> compare -parameters    OR    -> compare -metrics    

This will produce the xml output containing the patch file insights for a given commit that met the metadata search critera.    

Once again, the goal was to have a lot of these xmls and to combine them to learn more about the correlation of repo metadata to development insights across all commits.    

Example Sequence:  
-> choose 5  
-> search 5 fix  
-> analyze 5 <RESULT_KEY> 2  
-> compare -metrics  
or
-> compare -parameters
