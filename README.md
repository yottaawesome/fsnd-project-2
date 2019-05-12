# Full Stack Developer Nanodegree Project 2: Digital Bookshelf

## Introduction

This repository contains my solution for project 2 of the Full Stack Developer Nanodegree. The project mandates the creation of a catalog-type web app where users will be authenticated via a third-party login provider (such as Google), and will be able to create, read, update, and delete items. This app is to be built using Python and Flask using a SQLite backend.

As such, this project will take the shape of a digital bookshelf where users will be able to create categories of books as well as view, add, update and delete their books.

## :warning: Alert

The client's `package.json` uses `node-sass`, which uses a [vulnerable version](https://nvd.nist.gov/vuln/detail/CVE-2018-20834) of `node-tar`. The [issue](https://github.com/sass/node-sass/issues/2625) is being tracked. I'm currently awaiting for `node-sass` to issue a new version, and then I'll upgrade the dependencies. For now, you might see NPM complaining about this vulnerability.

## Status

_In development._

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

You'll need the following prerequisites.

* Python
* Pip
* `virtualenv`
* Node
* NPM
* A Google account and a configured Google Web Application
* A GitHub account and a configured GitHub Application.
* Git to clone this repository.

### Server

You'll need to set up a Google Developer Client application and a GitHub application in order to obtain the relevant client IDs and secrets, plus the secrets JSON file from Google. These details are used by the server and client to authenticate against GitHub and Google. The following files will need to be present at the root of `svr`. Note that all files starting with `secret.` are deliberately ignored in `.gitignore`.

* `secret.google_client_secrets.json:` the downloaded JSON file for your Google application from Google Developer Console.
* `secret.github_client_secrets.json:` JSON file containing the GitHub secrets. Consult `example.secret.github_client_secrets.json` for an example file.

Once you have done this, follow the below instructions.

* From Bash:
  * Move into the server dir: `cd src/svr`.
  * Create virtual environment: `env virtualenv`.
  * Activate virtual environment: `source env/bin/activate`.
  * Install Python dependencies: `pip install -r requirements.txt`.
  * Create the DB: `python create_db.py`.
  * Run development server: `python main.py` or `source run`.
  * Visit [localhost:5000](http://localhost:5000).

### SPA

* From Bash:
  * Move into the SPA dir: `cd src/spa`.
  * Install NPM dependencies: `npm install`.
  * Build the client using one of the following commands:
    * `npm run dev`: run a one-off development build.
    * `npm run prod`: run a one-off production build.
    * `npm run dev-watch`: run the development build and rebuild on file changes.
    * `npm run prod-watch`: run the production build and rebuild on file changes.

Further details will be added soon.
