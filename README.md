# readtidedata
scrapes a site and collect low tide data for a give number of locations

This program is able to read a web site and scrape the low tide data. The locations are specified in the tidecfg.py file in the form of a python list. If it is able to get the location specific tide data successfully it creates a file called low_tide_data.txt in the same folder as the program itself with a text formatted list of location name followed by the date, time and height of low tide between sunrise and sunset.

The attached requirement.txt specifies the modules needed to run this program. Create a folder and download all files from this repo.Create a virtual environment with the requirements.txt. Check to make sure that the file tidecfg.py has the list with valid locations. Then run python get_low_tide_data.py.
