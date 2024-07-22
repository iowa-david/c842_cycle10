SQL injection is a common problem when dealing with user inputs into a system. I have worked on many web front-end projects where they are mostly internally facing and verifying the inputs to ensure there is no SQL injection and other issues that have yet to be a part of the project. I wanted to put together a tool to check a host and see what can be done about that with a Python script that ideally would be embedded in a CI/CD pipeline.

# scripting_check.py
This script takes a given URL and runs an analysis to determine whether potential SQL and cross-site scripting exist in forms and pages within a website.

## Installation
The program requires two additional Python libraries, requests for running web requests, and a beautiful soup for web scraping.
If you do not have them installed, you can install them by the following command: 
Pip install requests beautifulsoup4

## Description
The script takes a website that the user provides and then crawls through the forms that can be found. The forms that are found are checked for cross-script scripting (XSS) and SQL injection using the 1==1 injection pattern.

## Three main points:
- Python allows for relatively easy validation of common scripting exploits.
- Verifying that there are no easily exploited SQL injections should be included in test runs within an application development team’s pipeline. The easier it is, the more likely the testing will be run.
- Web scraping is easily accomplished with beautiful soup. Multiple different types of SQL injection can be run. Finding those that are run with 1 == 1 are some of the easiest to detect.
  
## Room for improvement:
- Create an API on top of the script so the program can be efficiently run within a CI/CD pipeline and versioned and updated so changes are not required in the build pipeline.
Allow for credentials to be included for logging into sites that require authentication so that more of the website can be explored for exploits.
- add fully featured logging and alerting to alert when exploits are found and share the information with those who are subscribed to the alerts

References and libraries:
* https://beautiful-soup-4.readthedocs.io/en/latest/
* https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/07-Input_Validation_Testing/05-Testing_for_SQL_Injection
