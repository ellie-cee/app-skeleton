#!/usr/bin/env python

import os
import fnmatch
import pathlib
import sys

#This function goes through all of the files and subdirectories in the file path specified by the user
#and appends all filepaths to a list. The function then returns this list
def walk_files(src_filepath = "."):
    filepath_list = []
    for root, dirs, files in os.walk(src_filepath):
        for file in files:
            
            if root == '.':
                root_path = os.getcwd() + "/"
            else:
                root_path = root
            
            if (root_path != src_filepath) and (root != '.'):
                filepath = root_path + "/" + file
            else:
                filepath = root_path + file
            if filepath not in filepath_list:
                filepath_list.append(filepath)       
    return filepath_list

def deCnr(path):
    return str(path).replace("cnr","srd").replace("CnR","SrD").replace("Cnr","SrD")

def refactor_css_json(file:pathlib.PosixPath):
    print(f"refactoring {'/'.join(file.parts)}")
    input = file.read_text()
    input = input.replace("cnr","srd")
    output = open(file,"w")
    output.write(input)
    
def refactor_js(file:pathlib.PosixPath):
    print(f"refactoring {'/'.join(file.parts)}")
    input = file.read_text()
    input = input.replace("cnr","srd").replace("CnR","SrD").replace("Cnr","SrD")
    output = open(file,"w")
    output.write(input)
    
paths = walk_files("./home/")
renameDirs = []
renameFiles = []
for path in paths:
    
    
    if ".git" in path:
        continue
    if "output" in path:
        continue
    file = pathlib.Path(path)
    
    if "cnr" in file.parent.name or "impl" in file.parent.name:    
        if file.parent not in renameDirs:
            renameDirs.append(file.parent)
    if "cnr" in file.name.lower():
        renameFiles.append(file)

    print(str(file))
    match file.suffix:
        case ".py":
            refactor_css_json(file)
        case ".js":
            refactor_js(file)
        case ".css":
            refactor_css_json(file)
            
dir:pathlib.PosixPath
    
