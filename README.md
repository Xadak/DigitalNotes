# Digital Notes

## Introduction

My submission for the 2022 Information systems semester project

## Installation

1. Install [docker](https://www.docker.com/).
2. (Linux) Install docker-compose.
3. Clone [this repository](https://github.com/Xadak/Information-Systems-Semester-Project.git).
4. Open up a terminal of your choice and cd to the directory where you cloned the repository.
5. Execute the following commands in your terminal to start the server:
'sudo docker build -t webservice ./webservice'  
'sudo docker-compose up --build'
6. Connect to the server on port 5000 (eg. localhost:5000 on the host machine)

## Usage

First You'll need an account. Navigate to the register page and enter your details. You'll be automatically signed in. 

If you already have an account, just log in with your credentials.
Once you've successfully signed in, on the homepage you'll be able to see all your saved notes, edit them or delete them, as well as create a new one. 

You can sort your notes based on the last modified date using the arrow.

You can also filter your notes by title or tag(s).

To create a new note, click on the **New &#10133;** button.

You have to choose a title for your note, and optionally some comma separated tags. Once you've written your note, click on **save**. You should see your new note on the list. Click on it to view its contents and again to hide them.

You can delete your account at any time by clicking on **delete account**. __Warning!__ : when you delete your account, all your notes are lost!

### Administrator functions

An administrator account has extra capabilities. You have to be an administrator to register a new administrator account. In webservice/data/initial_admins.json you can add/change the initial administrator accounts when the server starts. You need to restart the server for the changes to take effect.

As an administrator you can delete a non-administrator user. Just fill in their username or their email and click **Delete**.
