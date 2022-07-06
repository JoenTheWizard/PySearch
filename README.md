# PySearch / PyDork

This was a small project I made ages ago with Python to try and test some functionalities with Google's search API using the 'googlesearch' module. It provides a terminal and a GUI version of the project.

The original intent of the project was to use a wordlist of dork queries and enumerate each resulting URL from Google's search engine. Each query returns the top 10 results. Sending too many requests will result in a HTTP request timeout, there's no multithreading (as sending many requests at the same time would result in a quicker time out) but values such as the Top-level domain (TLD) and the 'Pause' or request delay can be changed. 

Tkinter module is obviously required for the GUI and 'google' module is required for fetching the requests.
