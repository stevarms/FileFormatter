# FileFormatter
A simple python application that is intended to rename files in a specific format and split archives into 2GB parts

**This code is a work in progress**
**theres probably a lot of use cases i didnt try, let me know if you find bugs**

# How it works

The application has several fields for user input which are used in the naming.  The user can drag and drop files they want renamed into the window.  The files will all be named according to the selected type and any 7z, zip, or rar files will all be extracted and rezipped with 7zip to ensure they are under 2GB limit.  The package includes a version of 7zip however, its limited to 7zip and zip files.  The application will use the installed version of 7zip if its found at the path defined in the application under "z_install".  If there are multiple files that would be named the same, the application will append a number to the filename to differentiate them.
<details>
  <summary>sample input</summary>
  
  ![image](https://user-images.githubusercontent.com/1356742/161444495-0bcb73e9-95bb-4535-b9e3-00b648b51d96.png)
</details>
<details>
  <summary>sample output</summary>
  
  ![image](https://user-images.githubusercontent.com/1356742/161444135-2182a6ae-fd0f-4556-896d-bde9602118cb.png)
</details>

# Important Notes
* it only supports zip and 7z (also rar if you install 7zip yourself)
* it extracts files to the same directory they came from so you'll need enough space
* it should work on mac and even linux but i've never tested it

# Getting Started
1. [install python 3](https://www.python.org/downloads/)
2. download [FileFormatter.zip](https://github.com/stevarms/FileFormatter/releases) and extract it
3. run "setup.bat" it will automaticaly update pip and install the requirements.
4. optionally install [7zip](https://www.7-zip.org/) for .rar support
    * if you dont use the default install path or you use mac you need to update the z_install property in FileFormatter.py.  
    * Its set to `z_install = r"C:\Program Files\7-Zip\7z.exe` by default
5. run "run.bat" to launch Fileformatter

# Detailed Manual Install Guide (only use if the install scripts wont work for you ie linux & mac users)
1. [install python 3.11](https://www.python.org/downloads/)
    * download and run the installer dont worry about any options it asks we dont really need them
    * <details>
        <summary>click here to see what the download button looks like</summary>

        ![image](https://user-images.githubusercontent.com/1356742/166838670-36a7ba18-c188-4d50-8741-b9b2f5086e00.png)
      </details>
2. download the FileFormatter code from github
    * click the green "code" button and download zip.
    * extract that zip to some location on your computer (probably your downloads folder)
    * <details>
        <summary>click here to see what the download button looks like</summary>

        ![image](https://user-images.githubusercontent.com/1356742/166839837-42a4e1e2-47f7-43b5-b2bc-72dc1c5e0394.png)
      </details>
3. open a command prompt (search "cmd" in windows or "term" in mac/linux)
4. update pip. copy paste the following command into the command prompt `py -m pip install --upgrade pip`
5. navigate in the command prompt to the location you extracted the zip to
    * command prompt usually opens to your user directory so this command should do it `cd Downloads\FileFormatter-master`
6. install the requirements with pip `py -m pip install -r .\requirements.txt`
7. [Install 7zip](https://www.7-zip.org/)
    * you probably want the 64 bit version, just run the installer and click next to everything we dont require any special settings.
    * this step is optional but if you dont do it you wont be able to use .rar files with the program
    * if you dont install 7zip to the default path you need to edit the FileFormatter.py file and change the z_install variable in FileFormatter.py
    * <details>
        <summary>click here to see what the download button looks like</summary>

        ![image](https://user-images.githubusercontent.com/1356742/166840812-1295c70a-189e-45e8-b8b9-52de01b70c6c.png)
      </details>
8. run FileFormatter by pasting `py FileFormatter.py` into your command prompt
    * you have to leave the command prompt open while its running
    * if you close the command prompt and want to run the application again you'll need to do the "cd" command from step 6 followed by step 9.
  
# Known issues
* UI is pretty ugly

# Planned Features
none yet
