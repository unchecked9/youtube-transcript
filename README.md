# youtube-transcript

## Installation

### Google project set up

Google has very good steps to follow regarding a project set up as well as setting up credentials. Make sure you set up OAuth2.0 credentials to work with this application. Once you have the OAuth2.0 credentials set up you will have to wait for Google's approval before it will work. However you can still get ahead of the game and add in the client_secrets.json file from the credentials you set up in Google developers console.
https://developers.google.com/youtube/registering_an_application

### Python project set up

Now that you have the google part set up you just gotta set up the python project so that you can run the code.
https://www.python.org/downloads/release/python-378/ 
Here you will find the version of Python that is required to run this project. Download from either the mac or windows installers provided and then we will move on to getting a virtual environment set up.

### Virtual Env set up

Here we will use a module called pipenv. So what you will want to do is go to folder where this README is at and then open up a powershell there. What you will do next is run the command 
```
$ pip install pipenv
```
This will install this module and then now we will use it by running this command next 
```
$ virtualenv .
```
This command will actually set up the environment for us to use. Now that it is set up you will run this to activate the virtualenv
```
$ .\Scripts\activate
```
Now you are in the virtual environment and set up to finish up the installation.

### Modules installation

Now that you are inside your activated installation we will download all the required modules for the project to run
```
$ pip install scrapy google-api-python-client google-auth google-auth-oauthlib google-auth-httplib2
```
Once this finishes you are all set up to run the project.

## Running the project

### Running the channel/playlist transcript retriever

You will need to navigate back into the folder this README is inside of in powershell and make sure you are in the activated environment. See above on how to activate the environment. Now you will have to move into the folder transcriptscraper using this command.
```
$ cd transcriptscraper
```
Now that you are in the correct space you are able to use the project. Now you will have to input the channel or playlist url that you wish to download from, and you will also have to input the name of the output file. Here are two examples of using the application.

Channel:
```
$ scrapy crawl channel -a url=URL -o OUTPUT_FILE.csv
```
where you will replace URL with the channels url and OUTPUT_FILE with whatever you want to name the csv file that gets output with all the transcripts.

Playlist:
```
$ scrapy crawl playlist -a url=URL -o OUTPUT_FILE.csv
```
where you will replace URL with the playlists url and OUTPUT_FILE with whatever you want to name the csv file that gets output with all the transcripts.

Keep in mind some URL's will have special characters that will require you to surround them with quotes '' when you run the program.

EX:
```
$ scrapy crawl playlist -a url='URL with special characters' -o OUTPUT_FILE.csv
```


## Alternate Installation

### Anaconda Installation

If you are having trouble with the installation you can try using this method of installing scrapy 
https://docs.scrapy.org/en/latest/intro/install.html#windows

## Requesting more Quota

https://support.google.com/youtube/contact/yt_api_form Request more Quota here.
