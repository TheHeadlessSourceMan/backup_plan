![Status: Stable](https://img.shields.io/badge/status-draft-yellow.svg?style=plastic)
![Python Version: 2.7](https://img.shields.io/badge/Python%20Version-3.8-blue.svg?style=plastic)
![Release Version: 1.0](https://img.shields.io/badge/Release%20Version-1.0-green.svg?style=plastic)
[![webpage:click here](https://img.shields.io/badge/webpage-click%20here-blue.svg?style=plastic)](https://TheHeadlessSourceMan.wordpress.com)
<!-- [![PyPI](https://img.shields.io/pypi/v/backup_plan.svg)]() -->

<!-- If you fork this repo, update the badges below to reflect your own GitHub username and project name -->
[![build](https://github.com/TheHeadlessSourceMan/backup_plan/actions/workflows/ci.yml/badge.svg)]()
[![flake8](https://github.com/TheHeadlessSourceMan/backup_plan/actions/workflows/ci.yml/badge.svg?event=push)]()
[![mypy](https://github.com/TheHeadlessSourceMan/backup_plan/actions/workflows/ci.yml/badge.svg?event=push)]()
[![pylint](https://github.com/TheHeadlessSourceMan/backup_plan/actions/workflows/ci.yml/badge.svg?event=push)]()
[![codecov](https://codecov.io/gh/TheHeadlessSourceMan/backup_plan/branch/main/graph/badge.svg)](https://codecov.io/gh/TheHeadlessSourceMan/backup_plan)

# backup_plan
This tool allows you to set up an individual backup plan for each directory.

The idea is we often have many different backup plans in play.  For instance, we've got a OneDrive where we keep work stuff, a Google drive where we store memes, a Proton drive for our super-secret diary, a website or home server we want to ftp changes over to, and a github project or two hiding over in the corner.  How do we juggle all that, so that everything stays backed-up?

 This project proposes that each directory has a ``.backup_plan`` file inside, which specifies where and how to back it up (can even have multiple).  Then you have a tool that flies around in the background and backs up everything for you.

## Current status
Rough draft stage

There is an sftp plugin and a keepass plugin for storing credentials to the various sites.

## Architecture
* This should be very easy to extend, as it leverages the python package manager to install plugins (via pip, or whatever) and automatically announce them to the backup plan.
* Example .backup_plan format
```json
[
  {
    "plugin": "sftp",
    "location": "ftp.example.com",
    "name": "./my_project",
    "username": "bob",
    "lastHash": ""
  }
]
```
