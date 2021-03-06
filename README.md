# SGDAllianceData

## Setup (Required)

- Install Node if you don't have it installed already
- Currently using node v10.12.0 for development  
- Make sure you're running the scripts in a virtual environment
- Makefile has all the commands you need to run the scripts to produce the data files.

- To install required packages run the this command:
- $ is no part of the command(s), just visual cue since terminal looks like that.

## Node Version Management installation (optional)

- If you do not have nvm installed, please follow the following to setup node environment on your machine. This is for Mac OS.
- NVM allows you to work with different versions of node in case you have different project with varying node versions.

### NVM with Homebrew

```
$ brew update
$ brew install nvm
$ mkdir ~/.nvm
$ vim ~/.bash_profile
```

#### bash_profile nvm setup
- Add the following lines to your bash_profile

```
$ export NVM_DIR=~/.nvm
$ source $(brew --prefix nvm)/nvm.sh
```

- Go back to your terminal after adding above lines to your bash_profile
- Run the following commands to activate reload bash_profile  since you just made a change to it. 

```
$ source ~/.bash_profile
```

#### installing node with nvm

- You can install any node version you want
- Check the [list of node releases](https://nodejs.org/en/download/releases/)
- For this project we used node 10.12.0, so go ahead and install that with nvm. See below.

```
$ nvm install 10.12.0
```

- To see list of node version available in your machine run the following

```
$ nvm ls
```

- To pick specific node version to use for your project run the following.

```
$ nvm use 10.12.0
```

- To set default node version in case you don't wanna be picking node version each time you're working on node related tasks. Do this outside your virtual environment

```
$ nvm alias default 10.12.0
```

## Run everything in single command

```
$ Make build
```
- No need to run commands below if you run this as it includes all the commands

## Running Commands one by one

``` 
$ Make setup
```

## File dependencies (Required if running Makefile commands one by one)

- Some of the scripts depend on pather_search_results.txt and disease_association.txt files to produce output json files
- Run the following to build the depencies before running the scripts

```
$ Make build-disease
$ Make build-panther
```

## Disease Association file

```
$ Make run-disease
```

## Phenotype File

```
$ Make run-phenotype 
```

## Expression File

```
$ Make run-expression 
```

## Basic Gene Information File

```
$ Make run-bgi
```

## File structure

- This is where the modules that get necessary data are

```
|-- src
|   |-- basic_gene_information
|   |   |-- basic_gene_information.py
|   |-- data_assets
|   |   |-- disease_association.txt
|   |   |-- panther_search_results.txt
|   |-- data_dump
|   |   |-- json data files are deposited here
|   |-- data_helpers
|   |   |-- data_helpers.py
|   |-- disease
|   |   |-- disease.py 
|   |-- expression
|   |   |-- expression.py
|   |-- phenotype
|   |   |-- phenotype.py  
|   |-- models
|   |   |-- models.py    
```
