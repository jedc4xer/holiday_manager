import datetime as dt
import json
from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass
import os
from time import sleep

clear_term = 'cls||clear'


# -------------------------------------------
# Modify the holiday class to 
# 1. Only accept Datetime objects for date.
# 2. You may need to add additional functions
# 3. You may drop the init if you are using @dataclasses
# --------------------------------------------
class Holiday:
      
    def __init__(self,name, date):
        #Your Code Here      
        pass
    
    def __str__ (self):
        # String output
        # Holiday output when printed.
        pass
          
            
# -------------------------------------------
# The HolidayList class acts as a wrapper and container
# For the list of holidays
# Each method has pseudo-code instructions
# --------------------------------------------
class HolidayList:
    def __init__(self, locale, country):
        self.innerHolidays = []
        self.locale = locale
        self.country = country
        print(self.locale)
   
    def addHoliday(holidayObj):
        # Make sure holidayObj is an Holiday Object by checking the type
        # Use innerHolidays.append(holidayObj) to add holiday
        # print to the user that you added a holiday
        pass

    def findHoliday(HolidayName, Date):
        # Find Holiday in innerHolidays
        # Return Holiday
        pass

    def removeHoliday(HolidayName, Date):
        # Find Holiday in innerHolidays by searching the name and date combination.
        # remove the Holiday from innerHolidays
        # inform user you deleted the holiday
        pass

    def read_json(filelocation):
        # Read in things from json file location
        # Use addHoliday function to add holidays to inner list.
        pass

    def save_to_json(filelocation):
        # Write out json file to selected file.
        pass
        
    def scrapeHolidays():
        # Scrape Holidays from https://www.timeanddate.com/holidays/us/ 
        # Remember, 2 previous years, current year, and 2  years into the future. You can scrape multiple years by adding year to the timeanddate URL. For example https://www.timeanddate.com/holidays/us/2022
        # Check to see if name and date of holiday is in innerHolidays array
        # Add non-duplicates to innerHolidays
        # Handle any exceptions.     
        pass

    def numHolidays():
        # Return the total number of holidays in innerHolidays
        pass
    
    def filter_holidays_by_week(year, week_number):
        # Use a Lambda function to filter by week number and save this as holidays, use the filter on innerHolidays
        # Week number is part of the the Datetime object
        # Cast filter results as list
        # return your holidays
        pass

    def displayHolidaysInWeek(holidayList):
        # Use your filter_holidays_by_week to get list of holidays within a week as a parameter
        # Output formated holidays in the week. 
        # * Remember to use the holiday __str__ method.
        pass
    
#     def get_date_from_timestamp(self, timestamp):
#         converted = dt.datetime.strftime(
#             dt.datetime.fromtimestamp(timestamp),'%Y-%m-%d'
#         )
#         return converted
    
#     def parse_weather_response(self, response, temp_unit, request_type):
#         if request_type == 'current':
#             current_weather = {
#                 'Current Temperature': response['main']['temp'],
#                 'Feels Like': response['main']['feels_like'],
#                 'Humidity': response['main']['humidity'],
#                 'Wind': response['wind']['speed']
#             }

#             current_weather_string = " | ".join(
#                 key + ": " + str(current_weather[key]) + temp_unit for key in current_weather.keys()
#             )
#             return current_weather_string
#         else:
#             daily_weather = response['list']
#             daily_data = {}
#             for day in daily_weather:
#                 date = self.get_date_from_timestamp(day['dt'])
#                 high = str(day['temp']['max']) + temp_unit
#                 fore = day['weather'][0]['main']
#                 clouds = "{:}%".format(day['clouds'])
#                 daily_data[date] = {'High': high, 'Forecast': fore, 'Cloud Cover': clouds}
#             return daily_data
    

    # def getWeather(weekNum):
    #     # Convert weekNum to range between two weeks (something between 1-52)
    #     # Use Try / Except to catch problems
    #     # Query API for weather in that week range
    #     # Format weather information and return weather string.
    #     pass
    
#     def get_weather(self, locale, locale_country, request_type):
#         end_point = {'current': "weather", 'daily': "forecast/daily"}
#         weather_url = "https://community-open-weather-map.p.rapidapi.com/" 
#         weather_url += end_point[request_type]

#         if locale_country != 'US':
#             local_units = 'metric'
#             temp_unit = '°C'
#         else:
#             local_units = 'imperial'
#             temp_unit = '°F'

#         querystring = {"q": locale, "units": local_units}

#         headers = {
#             "X-RapidAPI-Host": "community-open-weather-map.p.rapidapi.com",
#             "X-RapidAPI-Key": "5e816765c8msh3e05c78f8f5fad5p1b2217jsn7b6b195a96ba"
#         }

#         response = requests.request(
#             "GET", weather_url, headers=headers, params=querystring
#         ).json()
        
#         print('API Called')

#         parsed_response = self.parse_weather_response(response, temp_unit, request_type)
#         return parsed_response
    
#     def check_weather(self):
#         try:
#             current_weather = self.get_weather(locale, locale_country, 'daily')
#         except:
#             current_weather = 'Current Weather Unavailable - A Heat Ticket has been Submitted.'
#         print(current_weather)

    def viewCurrentWeek():
        # Use the Datetime Module to look up current week and year
        # Use your filter_holidays_by_week function to get the list of holidays 
        # for the current week/year
        # Use your displayHolidaysInWeek function to display the holidays in the week
        # Ask user if they want to get the weather
        # If yes, use your getWeather function and display results
        pass

def get_datetime():
    return(dt.datetime.now())        

def clean_screen():
    os.system(clear_term)
    
def delay(duration):
    sleep(duration)
        
def get_templates():
    templates = requests.get(
        'https://raw.githubusercontent.com/jedc4xer/holiday_manager/main/manager_template.txt'
    ).text.split(",")
    return templates        
    
def display_menu_template(active_menu, current_day_info, locale_info):
    clean_screen()
    print(
        templates[1].format(
        current_menu = active_menu, 
        day_info = current_day_info, 
        locale = locale_info)
    )


def get_locale():
    try:
        ip_path = 'http://ipinfo.io/json'
        data = requests.get(ip_path).json()
        return f'{data["city"]}, {data["region"]}', data['country']
    except:
        print('Your location has been estimated and may be inaccurate.')
        return 'Castries, St Lucia', "Wish I Were There"


    
def modify_current_date_time():
    current_dt = get_datetime()
    current_date = dt.datetime.strftime(current_dt,'%A, %B %d, %Y')
    current_time = dt.datetime.strftime(current_dt,'%H:%M:%S')
    if current_time < '06:00':
        time_of_day = 'Early Morning'
    elif (current_time >= '06:00' and current_time < '10:00'):
        time_of_day = 'Morning'
    elif (current_time >= '10:00' and current_time < '12:00'):
        time_of_day = 'Late Morning'
    elif (current_time >= '12:00' and current_time < '15:00'):
        time_of_day = 'Afternoon'
    elif (current_time >= '15:00' and current_time < '18:00'):
        time_of_day = 'Late Afternoon'
    elif (current_time >= '18:00' and current_time < '21:00'):
        time_of_day = 'Early Evening'    
    elif current_time >= '21:00':
        time_of_day = 'Evening'
    else:
        time_of_day = '[error] - Somehow we have ended up on Naboo!'
        
    day_info = f'{current_date} | {time_of_day}'
    return day_info


def main():
    locale_info, country = get_locale()
    current_day_info = modify_current_date_time()
    delay(2)
    display_menu_template('Main Menu', current_day_info, locale_info)
    BoontaEve = HolidayList(locale_info, country)
    # Large Pseudo Code steps
    # -------------------------------------
    # 1. Initialize HolidayList Object
    # 2. Load JSON file via HolidayList read_json function
    # 3. Scrape additional holidays using your HolidayList scrapeHolidays function.
    # 3. Create while loop for user to keep adding or working with the Calender
    # 4. Display User Menu (Print the menu)
    # 5. Take user input for their action based on Menu and check the user input for errors
    # 6. Run appropriate method from the HolidayList object depending on what the user input is
    # 7. Ask the User if they would like to Continue, if not, end the while loop, ending the program.  If they do wish to continue, keep the program going. 

clean_screen()
templates = get_templates()
print(templates[0])


if __name__ == "__main__":
    main();


    
# Additional Hints:
# ---------------------------------------------
# You may need additional helper functions both in and out of the classes, add functions as you need to.
#
# No one function should be more then 50 lines of code, if you need more then 50 lines of code
# excluding comments, break the function into multiple functions.
#
# You can store your raw menu text, and other blocks of texts as raw text files 
# and use placeholder values with the format option.
# Example:
# In the file test.txt is "My name is {fname}, I'm {age}"
# Then you later can read the file into a string "filetxt"
# and substitute the placeholders 
# for example: filetxt.format(fname = "John", age = 36)
# This will make your code far more readable, by seperating text from code.









