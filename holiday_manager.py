import json
import requests
import os
import calendar
import time
import random

import datetime as dt

from bs4 import BeautifulSoup
from dataclasses import dataclass

clear_term = 'cls||clear'

## May add an exit note that makes a suggestion based on the weather
## May add an exit ASCII Logo if time allows

# -------------------------------------------
# Modify the holiday class to 
# 1. Only accept Datetime objects for date.
# 2. You may need to add additional functions
# 3. You may drop the init if you are using @dataclasses
# --------------------------------------------

@dataclass
class Holiday:
    """ Holiday Class """
    name: str
    date: str
    category: str
    
    def __str__ (self):
        str_output = f'{name} | {category} | {date}'
        return str_output
          
class WeatherReport:
    """ This class stores the weather information """
    
    def __init__(self):
        self.__locale = 'Castries, St Lucia'
        self.__country = 'Wish I Were There'
        self.__current_weather = 'Raining Cats and Dogs'
        self.__country = self.get_locale()
        #self.__current_weather = self.check_weather('current')
        # Uncomment above line when program is ready
        
    # def __post_init__(self):
    #     self.__locale, self.__country = self.get_locale()
    #     self.__current_weather = self.check_weather('weather')
    #     print('Here')
        
    def return_data(self):
        return self.__locale, self.__current_weather
    
    def get_date_from_timestamp(self, timestamp):
        converted = dt.datetime.strftime(
            dt.datetime.fromtimestamp(timestamp),'%Y-%m-%d'
        )
        return converted

    
    def check_weather(self, request_type):
        #self.__current_weather = self.get_weather(request_type)
        try:
            self.__current_weather = self.get_weather(request_type)
        except:
            self.__current_weather = 'Current Weather Unavailable - A Heat Ticket has been Submitted.'
        return self.__current_weather
    
    
    def get_weather(self, request_type): #, locale, locale_country, request_type):
        end_point = {'current': "weather", 'daily': "forecast/daily"}
        weather_url = "https://community-open-weather-map.p.rapidapi.com/" 
        weather_url += end_point[request_type]

        if self.__country != 'US':
            local_units = 'metric'
            temp_unit = '°C'
        else:
            local_units = 'imperial'
            temp_unit = '°F'

        querystring = {"q": self.__locale, "units": local_units}

        # Uncomment when ready for publish
        # headers = {
        #     "X-RapidAPI-Host": "community-open-weather-map.p.rapidapi.com",
        #     "X-RapidAPI-Key": 
        # }

        response = requests.request(
            "GET", weather_url, headers=headers, params=querystring
        ).json()

        print('API Called')

        parsed_response = self.parse_weather_response(response, temp_unit, request_type)
        return parsed_response
        
        
    def get_locale(self):
        try:
            ip_path = 'http://ipinfo.io/json'
            data = requests.get(ip_path).json()
            return f'{data["city"]}, {data["region"]}', data['country']
        except:
            print('Your location has been estimated and may be inaccurate.')
            return 'Castries, St Lucia', "Wish I Were There"
        
    
    def parse_weather_response(self, response, temp_unit, request_type):
        if request_type == 'current':
            current_weather = {
                'Temperature': str(response['main']['temp']) + temp_unit,
                'Feels Like': str(response['main']['feels_like']) + temp_unit,
                'Humidity': "{:}%".format(response['main']['humidity']),
                'Wind': response['wind']['speed']
            }

            current_weather_string = " | ".join(
                key + ": " + str(current_weather[key]) for key in current_weather.keys()
            )
            return current_weather_string
        else:
            daily_weather = response['list']
            daily_data = {}
            for day in daily_weather:
                date = self.get_date_from_timestamp(day['dt'])
                high = str(day['temp']['max']) + temp_unit
                fore = day['weather'][0]['main']
                clouds = "{:}%".format(day['clouds'])
                daily_data[date] = {'High': high, 'Forecast': fore, 'Cloud Cover': clouds}
            return daily_data
    
    
# -------------------------------------------
# The HolidayList class acts as a wrapper and container
# For the list of holidays
# Each method has pseudo-code instructions
# --------------------------------------------
class HolidayList:
    def __init__(self, errors):
        #self.__innerHolidays = []
        self.__errors = errors
        self.__inner_holidays = {}
        self.__pre_loaded_path = 'pre_loaded_holidays.json'
        self.__pre_loaded_holidays = self.read_json()
        
    def add_holiday(self, holiday_object):
        # Make sure holidayObj is an Holiday Object by checking the type
        # Use innerHolidays.append(holidayObj) to add holiday
        # print to the user that you added a holiday
        if not isinstance(holiday_object, Holiday):
            print(self.__errors[0])
            return
        holidate = holiday_object.date
        if holidate in self.__inner_holidays:
            self.__inner_holidays[holidate].append(holiday_object)
            print("Added holiday to existing date.")
        else:
            self.__inner_holidays[holidate] = [holiday_object]
            print("Added holiday to a new date.")

    def findHoliday(HolidayName, Date):
        # Find Holiday in innerHolidays
        # Return Holiday
        pass

    def removeHoliday(HolidayName, Date):
        # Find Holiday in innerHolidays by searching the name and date combination.
        # remove the Holiday from innerHolidays
        # inform user you deleted the holiday
        pass
    
    def convert_new_holidays(self, provided_holidays):
        for new_holiday in provided_holidays:
            if 'category' not in new_holiday:
                category = 'Custom Holiday'
            else:
                category = new_holiday['category']
                
            holiday_object = Holiday(
                new_holiday['name'], 
                new_holiday['date'], 
                category
            )
            
            self.add_holiday(holiday_object)
        
    def read_json(self):
        """ 
        This function check for existing files and loads base
        holidays if there are no existing files.
        """
        try:
            if 'managed_holidays.json' in os.listdir():
                print('Loading Managed Holidays...'.center(78, " "),"\n")
                file = open('managed_holidays.json')
                managed_holidays = json.load(file)
                return manged_holidays
            else:
                print('New Environment Detected'.center(78, " "),"\n")
                print('Gathering Preloaded Holidays'.center(78, " "),"\n")
                
        except:
            print('New Environment Detected'.center(78, " "),'\n')
            print('Gathering Preloaded Holidays'.center(78, " "),"\n")
        
        file = open(self.__pre_loaded_path)
        provided_holidays = json.load(file)['holidays']     
        self.convert_new_holidays(provided_holidays)

    def save_to_json(filelocation):
        # Write out json file to selected file.
        pass
    
    def standard_date(self, date, year):
        actual_date = dt.datetime.strftime(dt.datetime.strptime(f'{date}, {year}', '%b %d, %Y'),'%Y-%m-%d')
        return actual_date
    
    def scrape_manager(self):
        """ This function is responsible for controlling the holiday scrape. """
        current_year = dt.datetime.today().year
        target_range = [_ for _ in range(current_year - 2, current_year + 3)]

        all_scraped = {}
        for year in target_range:
            scraped_holidays = scrape_holidays(year)
            all_scraped[year] = scraped_holidays
            print(f'{year}: {len(scraped_holidays)}')

        combined = {"holidays": []}
        for year in all_scraped:
            for holiday in all_scraped[year]:
                combined['holidays'].append(all_scraped[year][holiday])

        
    def scrape_holidays(self, target_year):
        """ This function holds the API call and prepares the data for use. """
        scrape_path = f'https://www.timeanddate.com/holidays/us/{target_year}'#'?hol=43122559'
        raw_scrape = requests.get(scrape_path).text
        soup = BeautifulSoup(raw_scrape)
        holidays = strain_soup(soup, target_year)
        return holidays      
        
        
    def strain_soup(self, soup, target_year):
        tables = soup.find_all('table', {'class': 'table'})
        body = tables[0].find_all('tr')
        holiday_dict = {}

        # This for loop cleans the scrape, and places it in a temporary dictionary
        for row in body:
            details = row.get_text("|").split("|")[:4]
            try:
                cleaned_date = standard_date(details[0].strip(), target_year)

                name = details[2].strip()
                if '(substitute)' in name:
                    continue

                category = details[3].strip()
                # I am removing this category because events exist on multiple days
                if 'COVID-19 Lockdown' in category:
                    continue

                holiday_inner_dict = {
                    "name": name, 
                    'date': cleaned_date, 
                    "category": [category]
                }
                if name in holiday_dict:
                    holiday_dict[name]['category'].append(category)
                    cats = list(set(holiday_dict[name]['category']))
                    holiday_dict[name]['category'] = cats
                else:
                    holiday_dict[name] = holiday_inner_dict
            except:
                continue
        return holiday_dict    
        
        
    # def scrapeHolidays():
    #     # Scrape Holidays from https://www.timeanddate.com/holidays/us/ 
    #     # Remember, 2 previous years, current year, and 2  years into the future. You can scrape multiple years by adding year to the timeanddate URL. For example https://www.timeanddate.com/holidays/us/2022
    #     # Check to see if name and date of holiday is in innerHolidays array
    #     # Add non-duplicates to innerHolidays
    #     # Handle any exceptions.     
    #     pass

    def num_holidays(self):
        """ This function returns the total number of holidays """
        return len(self.__inner_holidays)
    
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
    

    

    # def getWeather(weekNum):
    #     # Convert weekNum to range between two weeks (something between 1-52)
    #     # Use Try / Except to catch problems
    #     # Query API for weather in that week range
    #     # Format weather information and return weather string.
    #     pass
    


    def viewCurrentWeek():
        # Use the Datetime Module to look up current week and year
        # Use your filter_holidays_by_week function to get the list of holidays 
        # for the current week/year
        # Use your displayHolidaysInWeek function to display the holidays in the week
        # Ask user if they want to get the weather
        # If yes, use your getWeather function and display results
        pass


############## GENERAL FUNCTIONS ##############
##-------------------------------------------## 

#.............    GET FUNCTIONS  .............#

def get_datetime():
    return(dt.datetime.now())        
        
def get_templates():
    templates = requests.get(
        'https://raw.githubusercontent.com/jedc4xer/holiday_manager/main/manager_template.txt'
    ).text.split(",")
    return templates        

def get_errors():
    errors = requests.get(
        'https://raw.githubusercontent.com/jedc4xer/holiday_manager/main/user_communication.txt'
    ).text.split(",")
    return errors      
    
def get_month_number(text_month):
    # There is a better way to do this, but I'm doing it this way.
    month_dict ={
        'January': 1,
        'February': 2, 
        'March': 3,
        'April': 4,
        'May': 5,
        'June': 6,
        'July': 7,
        'August': 8,
        'September': 9,
        'October': 10,
        'November': 11,
        'December': 12
    }
    return month_dict[text_month]    
    
def get_week_nums(year, month):
    end_of_month = calendar.monthrange(year, month)[1]
    starting_week = dt.datetime(year, month, 1).isocalendar()[1]
    ending_week = dt.datetime(year, month, end_of_month).isocalendar()[1]
    
    # This tries to build a list that will be empty if starting week > ending week
    res = list(range(starting_week, ending_week + 1))
    if not res:
        week_num = 52 if starting_week != 53 else 53
        res = list(range(starting_week, week_num + 1)) + list(range(1, ending_week + 1))
    return res    
    
    
#.............   MENU FUNCTIONS  .............#    
      
def display_menu_template(active_menu, arg_list):
    clean_screen()
    current_weather = arg_list[0]
    current_day_info = arg_list[1]
    locale_info = arg_list[2]
    holiday_cnt = arg_list[3]
    print(
        templates[1].format(
        current_menu = active_menu, 
        current_weather = current_weather,
        day_info = current_day_info, 
        locale = locale_info,
        holiday_cnt = holiday_cnt
        )
    )

    
def holiday_view_builder():
    print('  Leave blank for current week.')
    which_year = input("  Which year would you like to view? >> ")
    
    if which_year.strip() != "":
        year_passed = check_input(which_year, 'year', [1950, 2050]) 
        if not year_passed:
            return False
        which_year = int(which_year)
        month_passed = False
        week_passed = False
        while not month_passed:
            print('\n  To search by week number, input the week number.')
            print('  Otherwise, input the name of a month.')
            which_month = input("  Which month of the year? (i.e. Jan, august) >> ")
            if which_month.isnumeric():
                if int(which_month) in range(1,54):
                    try:
                        week_choice = match_week_to_date(which_month, which_year)
                        week_choice = list(map(lambda x: convert_dt(x), [week_choice[0], week_choice[1]]))
                        month_passed = True
                        return week_choice
                    except:
                        print('That week does not seem to be an option. Please try again.')
                else:
                    print(' That week is not an option. Please try again.')
            else:
                which_month = check_month(which_month)
                if which_month:
                    month_passed = True
                    month_num = get_month_number(which_month)
                    week_nums = get_week_nums(which_year, month_num)
                    translate = True if week_nums[0] > week_nums[1] else False
                    week_dict = {}
                    print('\n   #: Date Range','\n   ``````````````')
                    for i, week in enumerate(week_nums):
                        if (i == 0 and translate):
                            dates = match_week_to_date(week, which_year - 1)
                        else:
                            dates = match_week_to_date(week, which_year)
                        week_dict[str(week)] = list(map(lambda x: convert_dt(x), [dates[0], dates[1]]))
                        
                        dates = " to ".join(str(_.month) + "-" + str(_.day) for _ in dates)
                        print(f'{str(week).rjust(4)}: {dates}')
                    example = random.choice([_ for _ in week_dict.keys()])
                    week_choice = input(f'\n  Choose a week: (i.e. "{example}") >> ')
                    if (week_choice.isnumeric() and week_choice in week_dict.keys()):
                        return week_dict[week_choice]
                    else:
                        if '"' in week_choice:
                            print('  Hmmm... Try leaving out the " " marks. That was just an example. ')
                            delay(2)
                        else:
                            print("  Hmmm... That just doesn't compute.\n  Starting Infinite Loop...")
                            delay(2)
                            print("  Wheeew, done. That was exhausting. Good thing you got a fancy processor.")
                            delay(2)
        # Once the month has passed get the month number and determine which weeks are in the month
        # for every week in the month print a menu_string consisting of the week_num, date_range
        # ask the user to pick their chosen week
        # The weeknumber will be used to determine which holidays to display, so holidays will be matched to a week number    
    
def convert_dt(date_time_object):
    return dt.datetime.strftime(date_time_object, '%G-%m-%d')

def match_week_to_date(week_num, year):
    date_string = f'{year}-V{int(week_num)}-1'
    start_date = dt.datetime.strptime(date_string, "%G-V%V-%w").date()
    end_date = start_date + dt.timedelta(days=6.9)
    return start_date, end_date

def delay(duration):
    time.sleep(duration)
    
def clean_screen():
    os.system(clear_term)
    
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

#.............  CHECK FUNCTIONS  .............#

def check_input(input_string, requirements, limits):
    if requirements == 'number':
        if (input_string.isnumeric() and int(input_string) in range(1, limits + 1)):
            return True
    elif requirements == 'year':
        if (input_string.isnumeric() and int(input_string) in range(limits[0], limits[1])):
            return True
    print(f'  {input_string} is not a valid {requirements}. Please try again.')
    delay(1.5)
    return False

def check_month(month_input):
    allowed_months = [
        'Jan', 'January', 'Feb', 'February', 'Mar', 'March', 'Apr', 
        'April', 'May', 'May', 'Jun', 'June', 'Jul', 'July', 'Aug', 
        'August', 'Sept', 'September', 'Oct', 'October', 'Nov', 'November', 
        'Dec', 'December'
    ]
    month_converter = [
        'January', 'February', 'March', 'April', 'May', 
        'June', 'July', 'August', 'September', 'October', 
        'November', 'December'
    ]
    if month_input.capitalize() not in allowed_months:
        print('  That month is not recognized. Please try again. ')
        return False
    else:
        month_input = month_input.capitalize()
        if month_input in month_converter:
            matched = month_input
        else:
            matched = allowed_months[allowed_months.index(month_input) + 1]       
    return matched
    

    
def main():
    #locale_info, country = get_locale()
    errors = get_errors()
    current_day_info = modify_current_date_time()
    CurrentWeather = WeatherReport()
    locale_info, current_weather = CurrentWeather.return_data()
    BoontaEve = HolidayList(errors)
    holiday_cnt = BoontaEve.num_holidays()
    delay(2)
    main_args = [current_weather, current_day_info, locale_info, holiday_cnt]
    outer_passed = False
    while not outer_passed:
        passed = False
        while not passed:
            display_menu_template('Main Menu', main_args)
            print(templates[3])
            main_menu_choice = input('  Please Choose an Option >> ')
            passed = check_input(main_menu_choice, 'number', 5)
        main_menu_choice = int(main_menu_choice)
        if main_menu_choice == 1:
            pass
        elif main_menu_choice == 2:
            pass
        elif main_menu_choice == 3:
            pass
        elif main_menu_choice == 4:
            passed = False
            while not passed:
                display_menu_template('Holiday Viewer', main_args)
                passed = holiday_view_builder()
                    
                
        elif main_menu_choice == 5:
            return
        
    
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
    main()
    
    # Closing Sequence
    #display_menu_template('Closing',['','',''])
    clean_screen()
    print(templates[2])
    print("\n" * 2)
    print('Closing the Manager'.center(78," "))
    delay(1.5)
    clean_screen()
    print("\n" * 2)
    print('Goodbye!!'.center(78," "))
    print('May the fourth be with you.'.center(78," "))
    print("\n" * 3);


    
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






    


        
# This saves the scrape to file
# combined_json = json.dumps(combined)

# with open('scraped_holidays.json', 'w') as file:
#     file.write(combined_json)
#     file.close()












