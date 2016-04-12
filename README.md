# Setup
Commands you should execute and filenames/folders are surrounded with backticks, e.g. `execute this`, `/home/brian/`

1. Clone this repository.
    - From the command prompt/terminal do `git clone https://github.com/briancecker/cmps115.git`
    - This will clone the repository into a directory called `cmps115`. You can rename this if you'd like.
2. Install python3.5 and pip for python3
    - varies by OS
3. Install virtualenv
    - `pip install virtualenv`
4. Somewhere on your computer (in the project directory is fine) do:
    - `virtualenv venv`
        - This will make a new directory/folder called `venv` which will contain a virtual python environment. 
        - Set up your IDE to use this virtual environment.
            - In Visual Studio: 
                - "To create a virtual environment, right-click the Python Environments item in Solution Explorer and select 'Add Virtual Environment...'."
                - Specify the location in which you created `venv` in the "Location of the virtual environment box"
                - See Virtual Environment section of 
                [https://github.com/Microsoft/PTVS/wiki/Python-Environments](https://github.com/Microsoft/PTVS/wiki/Python-Environments) if you have a problem
    - DO NOT COMMIT `venv`
5. Start using your virtualenv
    - On windows: from command prompt `venv\Scripts\activate`
    - On mac/linux: `source venv/bin/activate`
6. Run `pip install -r cmps115/requirements_dev.txt`
    - This will install all dependencies listed in the `requirements_dev.txt` file. This might take a while as the file grows larger.
    - Rerun this command everytime `requirements_dev.txt` changes
    - You should UPDATE `requirements_dev.txt` every time you add a python package to the project and commit that update.
7. Test it out!
    - cd to `cmps115/lazylecturebot`
    - `python manage.py runserver`
    - There might be some warnings, but if it ends with something like the following, then it's working.
   
        Django version 1.9.4, using settings 'lazy_lecture_bot.settings'
        Starting development server at http://127.0.0.1:8000/
        Quit the server with CONTROL-C.
    - If the previous step didn't have errors, then in your browser, navigate to http://127.0.0.1:8000/
        - It should say something other than an error
        - The django server is now running on localhost (127.0.0.1) on port 8000 of your computer. You can use 
        for pretty much all development purposes and to not waste time deploying to another server.
     

