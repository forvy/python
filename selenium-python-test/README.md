# Selenium-Python-Example

This repository contains the base setup of a UI testing project,
using Python, Selenium Webdriver, and Page Object Model pattern.

A simple search in DuckDuckGo to check that results are displayed is used as an example

# Requirements

* Python 3.7.X
* pip and setup tools
* [venv](<https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/>) (recommended)

# Installation

1. Download or clone the repository 
2. Open a terminal
3. Go to the project root directory "/selenium-python-test/".
4. Create a virtual environment: `py -m venv venv`
5. Activate the virtual environment executing the following script: `.\venv\Scripts\activate`
6. Execute the following command to download the necessary libraries:  `pip install -r requirements.txt`

# Test Execution

1. Open a terminal
2. From the project root directory run: `pytest -v --html=results/report.html`

# Configuration

By default, tests will be executed in Chrome (normal mode). Preferences can be changed in "/data/config.yaml" file

# Results

To check the report, open the '/results/report.html' file once the execution has finished.
   
