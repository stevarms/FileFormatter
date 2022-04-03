# FileFormatter
A simple python application that is intended to rename files in a specific format and split archives into 2GB parts

**This code is a work in progress**

# How it works

The application has several fields for user input which are used in the naming.  The user can drag and drop files they want renamed into the window.  The files will all be named according to the selected type and any 7z, zip, or rar files will all be extracted and rezipped with 7zip to ensure they are under 2GB limit.  The package includes a version of 7zip however, its limited to 7zip and zip files.  The application will use the installed version of 7zip if its found at the path defined in the application under "z_install"

E.G.

# Getting Started
1. [install python 3](https://www.python.org/downloads/)
2. update pip `py -m pip install --upgrade pip`
3. install the requirements with pip `py -m pip install -r .\requirements.txt`
4. optionally install 7zip and specify the install path in the script.  Its set to `z_install = r"C:\Program Files\7-Zip\7z.exe` by default
7. run FileFormatter.py `py path_to_location/fileformatter.py' from the command line

# Known issues
UI is pretty ugly

# Planned Features
none yet
