#!/usr/bin/env python3
import os
import shutil
import hashlib
import json
from datetime import datetime

BASE_DIR = os.path.expanduser("~/.svcs")

def init_repo(repo_name):
    repo_path = os.path.join(BASE_DIR, repo_name)
    if not os.path.exists(repo_path):
        os.makedirs(repo_path)
        os.makedirs(os.path.join(repo_path, "files"))
        os.makedirs(os.path.join(repo_path, "commits"))
        print(f"Repository '{repo_name}' initialized.")
    else:
        print(f"Repository '{repo_name}' already exists.")

def add_file(repo_name, file_path):
    repo_path = os.path.join(BASE_DIR, repo_name)
    if os.path.exists(repo_path):
        shutil.copy(file_path, os.path.join(repo_path, "files"))
        print(f"File '{file_path}' added to repository '{repo_name}'.")
    else:
        print(f"Repository '{repo_name}' does not exist.")

def commit(repo_name, message):
    repo_path = os.path.join(BASE_DIR, repo_name)
    if os.path.exists(repo_path):
        commit_id = hashlib.sha1(datetime.now().isoformat().encode()).hexdigest()
        commit_dir = os.path.join(repo_path, "commits", commit_id)
        os.makedirs(commit_dir)
        shutil.copytree(os.path.join(repo_path, "files"), os.path.join(commit_dir, "files"))
        commit_info = {
            "id": commit_id,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
        with open(os.path.join(commit_dir, "info.json"), "w") as f:
            json.dump(commit_info, f, indent=4)
        print(f"Commit '{commit_id}' created with message: '{message}'.")
    else:
        print(f"Repository '{repo_name}' does not exist.")

def log(repo_name):
    repo_path = os.path.join(BASE_DIR, repo_name)
    if os.path.exists(repo_path):
        commits = os.listdir(os.path.join(repo_path, "commits"))
        for commit_id in commits:
            with open(os.path.join(repo_path, "commits", commit_id, "info.json")) as f:
                commit_info = json.load(f)
                print(f"Commit ID: {commit_info['id']}")
                print(f"Message: {commit_info['message']}")
                print(f"Timestamp: {commit_info['timestamp']}")
                print("-" * 40)
    else:
        print(f"Repository '{repo_name}' does not exist.")

def status(repo_name):
    repo_path = os.path.join(BASE_DIR, repo_name)
    if os.path.exists(repo_path):
        files = os.listdir(os.path.join(repo_path, "files"))
        print(f"Files in repository '{repo_name}':")
        for file in files:
            print(f" - {file}")
    else:
        print(f"Repository '{repo_name}' does not exist.")

def menu():
    while True:
        print("\nSimple Version Control System (SVCS)")
        print("1. Initialize Repository")
        print("2. Add File to Repository")
        print("3. Commit Changes")
        print("4. View Commit Logs")
        print("5. Check Repository Status")
        print("6. Exit")
        choice = input("Select an option: ")

        if choice == '1':
            repo_name = input("Enter repository name: ")
            init_repo(repo_name)
        elif choice == '2':
            repo_name = input("Enter repository name: ")
            file_path = input("Enter file path to add: ")
            add_file(repo_name, file_path)
        elif choice == '3':
            repo_name = input("Enter repository name: ")
            message = input("Enter commit message: ")
            commit(repo_name, message)
        elif choice == '4':
            repo_name = input("Enter repository name: ")
            log(repo_name)
        elif choice == '5':
            repo_name = input("Enter repository name: ")
            status(repo_name)
        elif choice == '6':
            print("Exiting SVCS. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)
    menu()
