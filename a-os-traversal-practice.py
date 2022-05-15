import os

# get current working directory
cwd = os.getcwd()
print(cwd)

# create a directory
directory = str(input("enter name of dir to create: "))
if os.path.exists(cwd + "/" + directory):
    print("folder 'my_dir' already exists")
else:
    os.mkdir(directory)

# list directory
list_dir = os.listdir()
print(list_dir)

# rename directory
directory_rename = str(input("enter name to rename dir to: "))
os.rename(cwd + "/" + directory, cwd + "/" + directory_rename)
print(list_dir)