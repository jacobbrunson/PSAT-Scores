#Jacob's PSAT Score Checker

Live version: http://scores.jacobbrunson.me

##What?
For every question on the PSAT, CollegeBoard has a corresponding web page that explains the question, and more importantly, tells you if you answered the question correctly.

This automatically logs into your CollegeBoard account, parses the (120+) pages for every question, and uses the information on them to calculate your score __before its available on CollegeBoard.__

##Why?
Many times, PSAT scores are available online, but schools don't receive online access codes for students to view them.

This service allows you to get your score without waiting for an access code from CollegeBoard.


##Installation

###Dependencies

+ Flask (http://flask.pocoo.org)
+ Beautiful Soup 4 (http://crummy.com/software/BeautifulSoup/)
+ Requests (http://python-requeÂsts.org)
+ PyYaml (http://pyyaml.org/)

###Usage

Run `python main.py` in the project directory

###Configuration

YAML is used for configuration. You may find these options in `config.yml`

+ `app.secret_key` Key used to encrypt session data. Not really important because no sensitive data is stored in the session
+ `app.debug` Should the app be run in debug mode?
+ `app.logging` Should the app log messages?


+ `server.host` Hostname that the server will run on
+ `server.port` Port that the server wil use


+ `collegeboard.login_url` URL of the CollegeBoard login page
+ `collegeboard.base_url` URL for all PSAT questions and answers


+ `messages.credentials` Error shown to user when their CollegeBoard login information is incorrect
+ `messages.unavilable` Error shown to user when this service will not work for them

+ `scoring.conversion_index` If you look at a PSAT raw score conversion table, this is the _maximum_ raw score in which every subject receives a 20. (For 2014, a score of -2 in each subject will get you a 20 in each subject)
+ `scoring.conversion` This is a transcription of the official PSAT raw score conversion table. The first item in the list should be [20, 20, 20], corresponding to the conversion_index above.
