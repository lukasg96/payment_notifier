# Introduction
This project consists of a script to notify people via e-mail, that they have to
pay some money. This information is read out a spreadsheet and sorted into
multiple e-mails.

## Indented use case
This script was wrote with membership fees in mind. It is not for professional
invoicing. So it might also be useful if you are responsible for the coffee
money in your office or something like that.

## Recommend guidelines
- Only use e-mail addresses of people, which agreed to get regular mail from
you.
- Don't send mail to often  (Don't spam people).
- Please use a system which is running continuously regardless (some server you
  have access to) or which does not
use al lot of energy (raspberry pi or similar). You don't need to run some
powerful system over night for this.

# Setup

## Installing Python
You need `python3` for this script, which is pre installed on modern linux
systems anyway. If you run a system without a `python3`-installation, here some
ways to install it.

### with conda (on windows)

1. Install [anaconda](https://docs.anaconda.com/anaconda/install/) (miniconda probably works too?).
2. `conda env create` reads the `environment.yml` file in this
    repository, creates a new env and installs all necessary packages
    into it.
3. Activate the new env: `conda activate z0-env`

### on linux

1. Installing python

```
sudo apt-get install python3
```

2. Install pip

```
sudo apt-get install python3-pip
```


## Installing python libraries

1. Install the necessary python libraries using pip

```
python3 -m pip install numpy
python3 -m pip install math
python3 -m pip install pandas
python3 -m pip install time
python3 -m pip install datetime
python3 -m pip install smtplib
python3 -m pip install email.message
python3 -m pip install getpass
```

## Clone the Repository

Clone the repository from github

```
git clone https://github.com/lukasg96/payment_notifier
```

# Configuration
Configurations  are specified in `config.txt`. __The configurations concerning the smtp server and the used e-mail account have to be specified before running.__ The the script will not run with the example settings shown there. The other settings can be changed as needed. The settings are explained in comments in `config.txt`.

You can open `config.txt` with for example:
```
vim config.txt
```

# Source data
The script reads its information from a spreadsheet specified in `config.txt` which shall be formatted like in in `Source.xlsx`. The example e-mail addresses in the spreadsheet are no real addresses. So they will result in a error. They therefore have to be changed. It is recommended to first use your own addresses to test your setup.

# Usage
If all configurations are done and the files are in place, the script can be run
from the new directory.

Navigate to the directory with:
```
cd payment_notifier
```
and then run the script.
```
python3 main.py
```
The script will then ask for the password to the e-mail you specified in
`config.txt`. It is intentionally not included in the configurations to avoid
storing it in plan text.

Since the script reads the source spreadsheet new every time it send mail, it
can be run continually, while the user is changing the spreadsheet over time.

# Contact
If you use my script and it makes your life a bit easier you could pay me a
coffee or a drink via:

PayPal: https://paypal.me/lgru96

Project Link: https://github.com/lukasg96/payment_notifier
