# Git basics

#username: surfgreen
#pass: chaterbbooxx34
"""
# git is a version control system that manages files
# use a workflow that is similar to programmers
# the idea is infrastructure as code (how it is added to our system, what tests need to happen etc)
# think of git commits as making a snapshot (you add things generally dont remove things)
# think of it as swapping in and out files

Git is a distributed system. Each copy of the dependency is its own.  There is no master server

making repository example:
mkdir git-test
cd git-test

# initialized empty git repository
git init

#you should now see some files in the directory git-test
# tells us information about our repository

git status

#git makesa views into files called brances
# mergers merge the diffrent branches
# once we have files in our repository when we run git status we see more inforamtion about them

git status

git add hello.py
git add *.py

git status

#notice we have added the files and they are now staged and ready to be committed now
# (use "git rm --cached <file>..." to unstage)

# git has two steps adding and removing the files (staging the files)  then committing the files

git commit -m "commit that is added to commit and explains commit"

#note the first time you make a commit you get a warning because you dont have your email and name assocated

git config --global user.email "adamcgoss@protonmail.com"
git config --global user.name "Adam Goss"

# the above inforamtion is stored in the following file ~./gitconfig


# git status should now show a clean tree
get status

# Git has three  different views into the files:
1. Working directory
2. Staging
3. Repository (.git)

3 . to see what saved in the repository move to the .git folder and use the following command:
    # tree isn't installed by default on Debian derivatives so install it.
    # tree is a nice commandline tool that that produces a depth in‐dented listing of files

# tree is a easy way to see branches and the master

tree

1. to see the working directory go the the main folder which should
also contain our .git folder (repository)
    # git takes all the files and directorys from the repository and puts them into the working directory
    # if we have more than one branch we can make different branches the current views of the files

# this command shows us only the master branch because it is our only branch

git branch

# this command shows us only the master branch because it is our only branch

2. to work with the staging area files we use the following commands to add and remove files:

git add
git rm

# after adding a new .py file and making changes to one of the previously commited files

git status

    # we can now see our new file is untracked
    # the file we made changes to shows modified status

# the following command shows what changed in the file with a + before the line
    # the output also shows other things about the changes such as line etc
    # notice the new file has no differences

git diff

# you can also look at the diffrences of only a chosen file

git diff loop.py
git diff ./loop.py

# recap to add the files to staging area and commit we do the following:

git add *.py
git commit -m "text for second commit"

#this command shows us the history of commits, the comments added with -m, and who made the commits

git log


# Command recap:

mkdir git-test
cd git-test

git init

git status

git config --global user.emil "adamcgoss@protonmail.com"
git config --global user.name "Adam Goss"

git add <file or files>
git commit -m "commit that is added to commit"

cd ./git
tree

cd ..
git branch
git diff
git diff <filename>

git log

# adding and removing files

# We will use the above directory, repository that we made in the above example notes

# from the working repository we will make another folder called python_test

mkdir python_test
cd python_test

# make some new code files

git status

# we see nothing has been added to the commit and our working directory ./ is untracked

cd ..

# we now see that the new folder (directory) python_test/ is untracked
# we can add the entire directory by doing the following

git add python_test/


git status
    # the above get status shows us the new files we have added to the staging area
    # notice we are still working in the master branch

git commit -m "commit files from the folder python_test"

# show us our file structure

tree

# we will now remove files

git rm test3.py

# notice test3.py has been removed from the working directory!

ls -hal

# we can recursivly remove files from folders using -r

git rm -r python_test/

# notice the whole folder is removed from the working directory not just the files
# make commit

git commit -m "removed files"


"""
# Push and Pull

"""
To make a new repository on github log in and click the + sign in the upper right corner
name the repository add a README.txt file to have a file in the repository
set .gitignore to Python template this makes file management of file types easier
you can do this from the command line

# .gitignore - ignore certan files, good for keeping passwords and other data you dont want seen from being pushed
# Create a .gitignore file for your repository

touch .gitignore

# f you want to ignore a file that is already checked in, you must untrack the file before you add a rule to ignore it. 
# From your terminal, untrack the file.

git rm --cached FILENAME

# Configure Git to use the exclude file ~/.gitignore_global for all Git repositories.

git config --global core.excludesfile ~/.gitignore_global

# you can also exclude local file without creating a .gitignore file using rules you set up in your OS

#once you have created your repo on github copy the url to it once inside your computers local respitory
# run the following command to pull the github repo:

git clone https://github.com/surfgreen/pynet_a

# you have now pulled the folder pynet_a/ and all its files to your local working directory
cd pynet_a
ls -hal
tree

# we can now see the repo that we pulled.
# you are in the pulled repos working directory and will make and edit files here

git status

# make some files and add them to the repos staging area

git add *.py

# commit the files to the repo

git commit -m "first commit to pynet_a"

# Note the repository on our computer is not linked to the repository we made on github
# you can see the commit you made on your local computer using the git log command

# githup will not show the same as it has no knowlege of he computers commit as they are unlinked
# when we used the command git clone we made something called remote 
# remote established an automatic link between where we cloned from in our case github, to where we cloned it
    #origin specifies the remote (remote is the link between our local machine and the other repo we cloned from)
    #master specifies the branch

git push origin master

# master is your branch
git push origin <name_of_branch>


# the above command failed to push the data as the two repos aren't linked
# to link the repos  we need to finish setting up the line by do the following:

git remote -v

git push origin master

# this will push your master branch on our local machine to the master branch to the github repo
    # once this the branches are set up you can push using the following comand:
    # you will need your github credentials to do this

git push

# remember before you make changes you always want to pull the githubs repo
# other people are working on the project at the same time
# you don't want your push to not have the changes they have made
    #remember you need to specify the remote (in our case origin) and branch (master)
    # hahaha master doen't work anymore because its not PC  now you must use main

git pull origin master

git pull origin main # main in the branch

git pull

git status # to show us our changes

# show our changes
git log

# you can just remove untracked files

rm <untracked file in working directory>

# if the file is in the staging area but not commited and we want to remove it from staging:
# use the following command to remove it
    #(use "git restore --staged <file>..." to unstage)
    
git restore --staged test3a.py

# the old command to do this was:
    #git reset HEAD <file>
    # this command still works
    
git reset HEAD test3a.py

git status #will now show the untracked file


# getting rid of the changes made to a modified file
    # to discard changes to file that haven't been staged use the following command:
    # (use "git restore <file>..." to unstage)

git restore test2.py
    
    # the file has now been returned to what it was at the commit. All changes are reverted
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)


# you can make new files using the touch command.  just like when you make the .gitignore file
    # these are empty files
    
touch test3.py
touch test4.py
touch test5.py

# make changes to the tracked files for demo

# we can get rid of all the tracked changes by using the following command:
    # you can retreive the modifications later becasuse they were stashed

git stash

    #Saved working directory and index state WIP on main: 31c2e6b Update to readme
    #this is the output you get and where you can retrive the stashed changes need be

"""
# git branches

"""
#command to see the branchs

git branch

# commands to checkout a branch.
    # -b makes a branch named deval
    # the command makes a new branch named deval that is a copy of the branch main and switches you to that branch

git checkout -b deval main

# here is another way to create a new branch
    # the branch created is named feature1 and is the same as the other three branches
    # you are not switched to this new branch automaticly

git branch feature1

# to switch to a branch use the checkout command like this:

git checkout feature1
git checkout <branch name>

# after adding a file in one of the new branches we will use deval

git add test3a.py
git commit -m "committing to new branch that has new file"

# when we switch back to our main branch it is the same the commit to the different branch hasn't effected it

git log

# to get out of the git log use:

:q

# we can push the new branch to github by doing the following:

git push origin devel  # this was the old way
git push --set-upstream origin deval # this is the new way

# we can now see the new branch on github
# you now also have a pull request in github 
# this is how you could do a merge from the deval branch into the main branch 
# and see what the changes the diffrent branches have

# after merging the dveal branch into the main branch on our computer we wont see it

git checkout main

# we now need to do a pull of the main branch to see the changes

#old way
    git pull origin master
    git pull origin main
    
git pull

# you can now see the changes with git log

git log 

# note the main branch and the deval branch have a diffrences and 
# remember we made changes to the README.txt file in main
# you can see the diffrences by switching branches and running git log

git checkout dveal
git log

git checkout main
git log

# to make the deval once again match the main branch use the following command from inside the deval branch:

git rebase main
git log

# the two branchs are now the same

# make changes to the deval branch 

git status to see the changes

# we can merge the branch changes made to deval into the branch main from our computer
# use the following command:

git merge deval

# the git log will not show the changes

"""
#git rebase
"""
# The git rebase is used a lot when working with open source librarys
# many of the public projects have forks you can go to someone elses code and click fork
# that will make a copy of the code and put it in your directory.
# this is the same thing as a git clone but through the GUI and back links giving you the remote to the code

#often when you are working on forks the code you are working on can become out of date
# the main repos get a lot of updates to keep your forks up to date use the git rebase command
# to update your fork and use rebase do the following

#this command fetch all the changes that have been made and pulls them down
# remember origin is the name you are fetching from

git fetch origin

# switch to the branch thats out of date that you want to 

git checkout <branch you will rebase>

git rebase  origin/<name of branch>

# this now will update your branch and can be shown though the log

# these command will update your whole repository 
git fetch origin
git rebase 


git fetch really only downloads new data from a remote repository - 
but it doesn't integrate any of this new data into your working files. 
Fetch is great for getting a fresh view on all the things that happened in a remote repository. 
Due to it's "harmless" nature, you can rest assured: 
fetch will never manipulate, destroy, or screw up anything.

"""

# common git work flows

"""
Step 1
# pull repo you will be working on

git clone https://github.com/ktbyers/netmiko


# notice the clone branch is named develop you can see all the remote branches from the repo you cloned

git branch -r

Step 2
# make a production branch (master branch) and a develop branch)

git checkout -b develop

# always keep these two branches up to date by using rebase
# when you want to make a change to the repo make a new branch 
# make sure everything is up to date first
# this is done by making your new branch off the remote code with origin/develop

git checkout -b  test_feature origin/develop

# in this branch make all your changes, commit them, test, and eventualy push the branch to github
# from github merge in the changes from the branch you pushed to the develop branch

# after some time merge the develop branch into the master branch on github  
# best practice. This way the master isnt constantly changing

# remember to rebase the master and develop

# use the .gitignore file even if you have a private repository 
# you block files by adding them to the .gitignore

"""
# Netmiko simplifies the ssh connections

"""
Tries to set up ssh connections so you can use them for automation
Disables output  paging 

Netmiko doesn't understand the commands you are sending or validate them


from netmiko import ConnectHandler

net_connect = ConnectHandler(host='cisco1.lasthop.ip', username='rover', password= 'password', device_type='cisco-ios')

#by puttin in an invalid device type you can see the list of accepted device types

#device_type can specify your connection type by doing the following:
    #defualt is ssh
device_type = 'cisco_ios' # this is the same as 'cisco_ios_ssh'
device_type = 'cisco_ios_telnet'
device_type = 'cisco_ios_serial'
device_type = 'cisco_ios_ssh'

#shows us the device command prompt line
net_connect.find_prompt()

#session_log
    #use this to log your actions
    # session_log='file_we_log_to.log'


net_connect = ConnectHandler(host='cisco1.lasthop.ip',
                             username='rover',
                             password='password',
                             device_type='cisco-ios',
                             session_log='log_file.log',)

device_dict = {'host':'cisco1.lasthop.ip',
          'username':'rover',
          'password':'password',
          'device_type':'cisco-ios',
          'session_log'='log_file.log'
}

#send_command is the main way to send commands
output= net_connect.send_command("show ip brief")


#netmiko uses the device prompt to know when the command is done running
    #this can be controld by using expect string this takes regular exprestions and uses raw strings
#look for a trailing # sign
output = net_connect.send_command("show ip int brief", expect_string=r'#')

# if you have a charter that isn't found it will take a while and eventually timeout
    #search pattern never detected
output = net_connect.send_command("show ip int brief", expect_string=r'>')
"""


####################### Exercises ###########################

"""
#My solutions to the exercises can be found at:
#Class1 Reference Solutions
#https://github.com/ktbyers/pyplus_course/tree/master/class1/exercises?__s=4tlrjds8fu5yh73gu7u4

#GITHOMEWORK
1. Create a GitHub account (it's free for public repositories).

2. Create a new repository in GitHub for this class. Add a README file and a Python .gitignore file.

3. Clone the repository that you just created on GitHub into your home directory in the lab environment.

4. Configure your name and email address on the lab server:

$ git config --global user.name "John Doe"
$ git config --global user.email jdoe@domain.com


5. Add and commit three files into your repository in the lab environment. Use 'git status' to verify that all your changes have been committed and that you are working on the 'main' branch.  Push these changes up to GitHub.

6. Create a 'test' branch in your repository.
    a. Ensure that you are working on the 'test' branch.
    b. Add two directories to the 'test' branch. Each directory should contain at least one file. These files should be committed into the 'test' branch.
    c. Use 'git log' to look at your history of commits.
    d. Modify one of your previously committed files. Use 'git diff' to look at the pending changes in this file. Add and commit these changes.

7. Push the 'test' branch up to GitHub.

8. Create a Pull Request inside of GitHub (pull request that would merge the 'test' branch into the 'main' branch). Look at the 'files changed' in the pull request. Merge the pull request.

9. Back on your AWS server
    a. Switch back to the 'main' branch.
    b. Use a 'git pull' to retrieve all of the updates from GitHub on the main branch.
    c. Verify your 'main' branch now has all of the changes that you had previously made in the 'test' branch.

10. In the 'main' branch use 'git rm' to remove some file from the branch. Commit this change.

11. Edit one of your files. Once again use 'git diff' to look at the change pending in that file. Use 'git checkout -- <file>' to discard that pending change. Verify your 'git status' is now clean.

12. In GitHub, edit the README.md file and commit a change to the 'main' branch in GitHub. On the lab server also edit the README.md file and commit the change into the lab server. Use 'git pull' to pull the 'main' branch from GitHub into the lab server. At this point you should have a merge conflict. It should look something like this:

$ git pull origin main
From https://github.com/ktbyers/pyneta
 * branch            main     -> FETCH_HEAD
Auto-merging README.md
CONFLICT (content): Merge conflict in README.md
Automatic merge failed; fix conflicts and then commit the result.​


Edit the README.md file to correct the merge conflict. The README.md file should have something like the following inside of it:

​$ cat README.md
# pyneta
Test PyNet Repository

Some additional information on this repository.

<<<<<<< HEAD
Create a merge conflict.
=======
More changes to readme.
>>>>>>> 1690ce5a6ddb640198ccf3bca26f32a65d772b92


The ​'<<<<<', '=====', '>>>>>' indicate where the inconsistencies on the file are. Git is basically stating I have this first line(s) from one change and this second line(s) from another change and I don't know which one you want to keep. Which line do you want to keep (could be one of the lines, both of the lines, none of the lines).

Here is how I fixed the merge conflict in the above file:

$ cat README.md
-----------------
# pyneta
Test PyNet Repository

Some additional information on this repository.

Create a merge conflict.

More changes to readme.​
-----------------

# Then I need to add and commit the file
$ git add README.md
$ git commit -m "Fixing merge conflict"
[main e87901a] Fixing merge conflict



Netmiko

1. In the lab environment use Netmiko to connect to one of the Cisco NX-OS devices. You can find the IP addresses and username/passwords of the Cisco devices in the 'Lab Environment' email or alternatively in the ~/.netmiko.yml file. Simply print the router prompt back from this device to verify you are connecting to the device properly.

2. Add a second NX-OS device to your first exercise. Make sure you are using dictionaries to represent the two NX-OS devices. Additionally, use a for-loop to accomplish the Netmiko connection creation. Once again print the prompt back from the devices that you connected to.

3. For one of the Cisco IOS devices, use Netmiko and the send_command() method to retrieve 'show version'. Save this output to a file in the current working directory.

"""