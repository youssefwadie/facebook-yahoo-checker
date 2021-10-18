# Facebook Yahoo Checker 
A very simple and small Python script for generating and filtering dead yahoo accounts that are associated with valid facebook accounts.
# Requirements
To get started, you need Python 3 and pip working on your system.

On *MS Windows* install [Python](https://www.python.org/downloads/windows) **and make sure that Python is added to the PATH environment variable.**
### Note
Microsoft Visual C++ 2014 or higher is **required**. You can get it with [Microsoft C++ build tools](https://visualstudio.microsoft.com/vs/features/cplusplus/)

---
On *Ubuntu*, *Mint*, or *Debian*; use `apt-get`
```bash
$ sudo apt-get install python3 python3-pip
```
---
On *Arch Linux* or *Manjaro*; use `pacman`
```bash
$ sudo pacman -S python python-pip
```

## Browser
You can use any *chromium-based* web broswer by changing `BINARY_PATH`  and `DRIVER_PATH` variables in the script according to your installation path for the *browser* and the [*webdriver*](https://chromedriver.chromium.org/), by default the script uses *chromium* but you can change it to any chromium-based browser.
# Installation:
```
git clone https://github.com/youssefwadie/facebook-yahoo-checker.git
cd facebook-yahoo-checker
pip install -r requirements.txt
```

# Usage
```
python main.py -t <NUMBER OF ACCOUNTS TO GENERATE AND TEST> -i <FILE>
```
# Notes
* You don't have to use both -t and -i options at the same time, one is enough.
* If you are using UNIX-like operating system you can insert the following line at the beginning of main.py file
	```
	#!/bin/env python
	```
	Make the file excutable
	```
	chmod +x main.py
	```
	#### Now you can run the script with *./main.py*
