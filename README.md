# Full Stack Developer Nanodegree Project 2: Digital Bookshelf

## Introduction

This repository contains my solution for project 2 of the Full Stack Developer Nanodegree. The project mandates the creation of a catalog-type web app where users will be authenticated via a third-party login provider (such as Google), and will be able to create, read, update, and delete items. This app is to be built using Python and Flask using a SQLite backend.

As such, this project will take the shape of a digital bookshelf where users will be able to create categories of books as well as view, add, update and delete their books.

## Status

_Complete._

## Project structure

The application is split in two parts: the server-side and the client-side.

### Server-side

The server-side is built as a Python Flask back end. The source code is located in the `src/svr` directory, and the main package is `svr`. Three subpackages are underneath `svr`.

* **app:** Contains the core logic of the Flask web application.
* **db:** Contains the database abstraction components.
* **tests:** Contains the unit tests.

### Client-side

The client-side is a single-page application (SPA) built in Inferno that acts as the default client for the Python server. The source code is located in `src/spa`. The client is highly componentized, as would be expected in React-type SPAs.

## Setting up

You'll need the following prerequisites to minimally run this project. Instructions for setting these up for Udacity's Vagrant VM are below. If you're using your own UNIX-like environment, consult your environment's package manager on how to best fulfill these prerequisites.

* Python 3
* Pip 3
* `virtualenv`
* A Google account and a configured Google Web Application
* Git to clone this repository
* Node and NPM, for building and developing the SPA client. This was optional previously as these files were included for the Udacity assessor's convenience, but have since been removed after passing this assessment.
* A relatively modern web browser.

The following prerequisites are optional:

* A GitHub account and a configured GitHub Application, for enabling GitHub authentication.

You'll need to set up a Google Developer Client application and optionally a GitHub application in order to enable the application to authenticate against third-party providers. For the application to function, you must at least configure a Google Web Application client and supply the relevant JSON secrets file. The application checks for the following files via the `svr/cfg/secret.cfg.json` file in order to do this.

* `secret.google_client_secrets.json:` the downloaded JSON file for your Google application from Google Developer Console. This must be provided.
* `secret.github_client_secrets.json:` JSON file containing the GitHub application secrets. Consult `example.secret.github_client_secrets.json` for an example file. If this file is not found, the application disables GitHub authentication.

Note that all files starting with `secret.` are deliberately ignored in `.gitignore`.

### Setting up Google authentication

1. Visit [Google Developer Console](https://console.developers.google.com/).
2. Create a new project and give it an appropriate name, e.g. My Bookshelf.
3. From the Project Dashboard, click _Credentials_ > _OAuthConsent screen_.
4. Choose an appropriate _Application name_ (e.g. My Bookshelf) and _Support email_, then click save.
5. From the Credentials tab, click _Create credentials_ and choose _OAuth client ID_.
6. In the next screen, click _Web application_ and then _Create_.
7. Give your credentials an appropriate _Name_ (e.g. Bookshelf Client) and add http://localhost:5000 to the _Authorised JavaScript origins_. Do not add http://127.0.0.1:5000 -- Google will seemingly accept this but fail when using it.
8. Save your changes and then click _Download JSON_. Name the downloaded file `secret.google_client_secrets.json` and place it in a folder of your choosing.
9. Modify `svr/cfg/secret.cfg.json` to include the path to the downloaded file. Ensure the file and folder are accessible.

### (Optional) Setting up GitHub authentication

1. Log into GitHub.
2. From the top-right-hand-side, click _Settings_.
3. Click _Developer settings_.
4. From the _OAuth Apps_ tab, click _New OAuth App_.
5. Set the fields:
    * _Application name_ to something appropriate (e.g. bookshelf).
    * _Homepage URL_ to http://localhost:5000/github.
    * _Authorization callback URL_ to http://localhost:5000/githubcallback.
6. Click save. Make note of the _Client ID_ and _Client Secret_ of your newly created GitHub application.
7. In `src/svr`, rename `example.secret.github_client_secrets.json` to `secret.github_client_secrets.json`.
8. Open `secret.github_client_secrets.json` and add your _Client ID_ and _Client Secret_ from step 6 to the appropriate fields in the JSON body.
9. Place `secret.github_client_secrets.json` in a folder of your choosing which can be read.
10. Modify `svr/cfg/secret.cfg.json` to include the path to the file. Ensure the file and folder are accessible.

Once you have have setup Google or Google and GitHub authentication, follow the below instructions as they pertain to your environment.

### Using Udacity's Vagrant VM

The Udacity VM does not have `virtualenv`, so this will need to be installed. Follow the instructions below.

1. [Install VirtualBox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1) for your platform. Udacity suggests using VirtualBox 5.1, but students report newer versions work as well.
2. [Install Vagrant](https://www.vagrantup.com/downloads.html) appropriately for your platform.
3. [Fork and clone locally](https://github.com/udacity/fullstack-nanodegree-vm) the Udacity VM on GitHub.
4. From Bash:
    1. `cd` into the `vagrant` directory in the Udacity repository you cloned in the previous step.
    2. Run `vagrant up`. This will set up the VM, but it may take quite a while to do so. Consider a :coffee: or twelve.
    3. Run `vagrant ssh` to SSH into the VM once it's set up.
    4. Install virtualenv: `sudo apt install virtualenv`.
    5. Clone this repository **into a non-shared directory** on your Vagrant VM. Shared VirtualBox/Vagrant directories [cause problems with NPM](https://github.com/npm/npm/issues/992) if you intend to build and develop the SPA client.
    6. Build the SPA client:
        1. Install Node and NPM:
            1. Run `curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash -`.
            2. Run `sudo apt-get install -y nodejs`.
        2. `cd` into `src/spa` in this repository.
        3. Install NPM dependencies: `npm install`.
        4. Run `npm run dev` (development build) or `npm run prod` (prod build). Consult `package.json` for the full list of build commands.
    7. Set up the server:
        1. `cd` into `src/svr` in this repository.
        2. Create a Python 3 virtual environment: `virtualenv -p python3 env`.
        3. Activate the Python virtual environment: `source env/bin/activate`.
        4. Install Python dependencies: `pip install -r requirements.txt`.
        5. In `svr/cfg`, rename `example.secret.cfg.json` to `secret.cfg.json`.
        6. Enter the path to the GitHub secrets file, the path to the Google secrets file, and the connection string the application will use.
        7. Create the DB: `python create_db.py`.
        8. Run development server: `python main.py` or `source run`.
        9. Visit [localhost:5000](http://localhost:5000).

### Using your own UNIX-like environment

From the shell of your choice, do the following:

1. Install virtualenv.
2. Clone this repository.
3. Build the SPA client:
    1. Install Node and NPM.
    2. `cd` into `src/spa` in this repository.
    3. Install NPM dependencies: `npm install`.
    4. Run `npm run dev` (development build) or `npm run prod` (prod build). Consult `package.json` for the full list of build commands.
4. Set up the server:
    1. `cd` into `src/svr` in this repository.
    2. Create a Python 3 virtual environment: `virtualenv -p python3 env`.
    3. Activate the Python virtual environment: `source env/bin/activate`.
    4. Install Python dependencies: `pip install -r requirements.txt`.
    5. Create the DB: `python create_db.py`.
    6. Run development server: `python main.py` or `source run`.
    7. Visit [localhost:5000](http://localhost:5000).
