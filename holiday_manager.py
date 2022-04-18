import os
import json
import time
import random
import string
import calendar
import requests

import datetime as dt

from bs4 import BeautifulSoup
from dataclasses import dataclass

clear_term = "cls||clear"

## May add an exit note that makes a suggestion based on the weather
## May add an exit ASCII Logo if time allows
## Did not notice that the holiday class is required to only accept DateTime objects


@dataclass
class Holiday:
    """ Holiday Class """

    name: str
    date: str
    category: str

    def __str__(self):
        categories = ", ".join(self.category)
        str_output = f"  {self.name} | {categories}"
        return str_output


class WeatherReport:
    """ This class stores the weather information """

    def __init__(self):
        self.__locale = "Castries, St Lucia"
        self.__country = "Wish I Were There"
        self.__current_weather = "Raining Cats and Dogs"
        self.__daily_weather = {"Sunny": "Sunny Somewhere Sometime"}
        if 1 == 0:
            self.get_locale()
            self.__current_weather = self.check_weather("current")
            print("  Weather Loaded")
            self.__daily_weather = self.check_weather("daily")

    def return_data(self):
        return self.__locale, self.__current_weather, self.__daily_weather

    def get_date_from_timestamp(self, timestamp):
        converted = dt.datetime.strftime(
            dt.datetime.fromtimestamp(timestamp), "%Y-%m-%d"
        )
        return converted

    def check_weather(self, request_type):
        # self.__current_weather = self.get_weather(request_type)
        try:
            weather = self.get_weather(request_type)
        except:
            weather = "Current Weather Unavailable - A Heat Ticket has been Submitted."
        return weather

    def get_weather(self, request_type):  # , locale, locale_country, request_type):
        end_point = {"current": "weather", "daily": "forecast/daily"}
        weather_url = "https://community-open-weather-map.p.rapidapi.com/"
        weather_url += end_point[request_type]

        if self.__country != "US":
            local_units = "metric"
            temp_unit = "°C"
        else:
            local_units = "imperial"
            temp_unit = "°F"

        querystring = {"q": self.__locale, "units": local_units}

        headers = {
            "X-RapidAPI-Host": "community-open-weather-map.p.rapidapi.com",
            "X-RapidAPI-Key": ,
        }
        response = requests.request(
            "GET", weather_url, headers=headers, params=querystring
        ).json()
        print("  Checking the Weather..." if request_type == "current" else "")
        parsed_response = self.parse_weather_response(response, temp_unit, request_type)
        return parsed_response

    def get_locale(self):
        try:
            ip_path = "http://ipinfo.io/json"
            data = requests.get(ip_path).json()
            self.__locale = f'{data["city"]}, {data["region"]}'
            self.__country = data["country"]
        except Exception as E:
            print("  ", E)
            print("  Your location has been estimated and may be inaccurate.")
            self.__locale = "Castries, St Lucia"
            self.__country = "Wish I Were There"
            delay(2)

    def parse_weather_response(self, response, temp_unit, request_type):
        if request_type == "current":
            current_weather = {
                "Temperature": str(response["main"]["temp"]) + temp_unit,
                "Feels Like": str(response["main"]["feels_like"]) + temp_unit,
                "Humidity": "{:}%".format(response["main"]["humidity"]),
                "Wind": response["wind"]["speed"],
            }

            current_weather_string = " | ".join(
                key + ": " + str(current_weather[key]) for key in current_weather.keys()
            )
            return current_weather_string
        else:
            daily_weather = response["list"]
            daily_data = {}
            for day in daily_weather:
                date = self.get_date_from_timestamp(day["dt"])
                high = str(day["temp"]["max"]) + temp_unit
                fore = day["weather"][0]["main"]
                clouds = "{:}%".format(day["clouds"])
                daily_data[date] = {
                    "High": high,
                    "Forecast": fore,
                    "Cloud Cover": clouds,
                }
            return daily_data


class HolidayList:
    """ This class manages the holidays. """

    def __init__(self, errors, forecast):
        # self.__innerHolidays = []
        self.__errors = errors
        self.__inner_holidays = {}
        self.__unsaved_holidays = 0
        self.__holiday_source = "unknown"
        self.__pre_loaded_holidays = self.read_json()
        self.__forecast = forecast
        self.__forecast_dates = [_ for _ in self.__forecast.keys()]

    def preview_holidays(self):
        print(self.__inner_holidays)

    def return_save_status(self):
        return self.__unsaved_holidays

    def standard_date(self, date, year):
        actual_date = dt.datetime.strftime(
            dt.datetime.strptime(f"{date}, {year}", "%b %d, %Y"), "%Y-%m-%d"
        )
        return actual_date

    def match_week_to_date(self, week_number, year):
        date_string = f"{year}-V{int(week_number)}-1"
        start_date = dt.datetime.strptime(date_string, "%G-V%V-%w").date()
        end_date = start_date + dt.timedelta(days=6.9)
        return start_date, end_date

    def check_for_current_week(self, date_list):
        if any((item in date_list for item in self.__forecast_dates)):
            q = "  Would you like to include available weather? (y/n) >> "
            if input(q).lower() in ["y", "yes", "yeah", "yea", "ye"]:
                return True
        return False

    def num_holidays(self):
        """ This function returns the total number of holidays """
        holiday_names = []
        for date in self.__inner_holidays:
            for holiday in self.__inner_holidays[date]:
                holiday_names.append(holiday.name)

        total_holidays = len(holiday_names)
        unique_holidays = len(set(holiday_names))
        return total_holidays, unique_holidays

    def get_weather(self, date):
        """ This function combines the weather with the data. 
        Assignment suggestions said to allow this function to query the 
        weather, but to limit the number of API calls, I am getting
        the weather when the application starts, and then passing it into the
        class during initialization. 
        """
        # "wod" is short for "weather_on_date"
        wod = self.__forecast[date]
        weather_string = (
            f"> High: {wod['High']} | {wod['Forecast']} | Clouds: {wod['Cloud Cover']}"
        )
        return weather_string

    def get_month_number(self, text_month):
        # There is a better way to do this, but I'm doing it this way.
        month_dict = {
            "January": 1, "February": 2, "March": 3, "April": 4, "May": 5,
            "June": 6, "July": 7, "August": 8, "September": 9, "October": 10,
            "November": 11, "December": 12,
        }
        return month_dict[text_month]

    def convert_dt(self, date_time, date_type):
        if date_type == "string":
            return dt.datetime.strftime(date_time, "%Y-%m-%d")
        else:
            return dt.datetime.strptime(date_time, "%Y-%m-%d").date()

    def scrape_holidays(self, target_year):
        """ This function holds the API call and prepares the data for use. """
        scrape_path = f"https://www.timeanddate.com/holidays/us/{target_year}"
        raw_scrape = requests.get(scrape_path).text
        soup = BeautifulSoup(raw_scrape, "html.parser")
        holidays = self.strain_soup(soup, target_year)
        return holidays

    def convert_new_holidays(self, provided_holidays):
        for new_holiday in provided_holidays:
            if "category" not in new_holiday:
                category = ["Custom Holiday"]
                holiday_object = Holiday(
                    new_holiday["name"], new_holiday["date"], category
                )
            else:
                category = new_holiday["category"]
                holiday_object = Holiday(
                    new_holiday["name"], new_holiday["date"], new_holiday["category"]
                )

            self.add_holiday(holiday_object)
            if self.__holiday_source == "managed":
                self.__unsaved_holidays += 1

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
            # print("Added holiday to existing date.")
        else:
            self.__inner_holidays[holidate] = [holiday_object]
            # print("Added holiday to a new date.")

    def input_holiday(self):
        passed = False
        while not passed:
            print("\n  * Add a Holiday * ")
            holiday = input("  Holiday: >> ")
            holiday = "".join(_ for _ in holiday if _ in string.ascii_letters + "-'_ ")
            if len(holiday) > 2:
                print('  "YYYY-mm-dd"')
                holidate = input("     Date: >> ")
                try:
                    holidate = dt.datetime.strptime(holidate, "%Y-%m-%d").date()
                    pretty_date = dt.datetime.strftime(holidate, "%B %d, %Y")
                    add_date = dt.datetime.strftime(holidate, "%Y-%m-%d")
                    passed = True
                except Exception as E:
                    print(E)
                    print(self.__errors[5])
                    delay(4)
            if passed:
                print(f"  {holiday} on {pretty_date}")
                passed = input("  Would you like to add this to the database? (y/n)>> ")
                if passed.lower() in ["y", "yes", "yeah", "ye", "yep"]:
                    new_holiday = [{"name": holiday, "date": add_date}]
                    self.convert_new_holidays(new_holiday)
                    passed = True
                    print(f"{holiday} added successfully".center(78, " "))

    def seek_holiday(self, user_input):
        match_found = False
        possible_matches = {}
        cntr = 0
        for date in self.__inner_holidays:
            for item in self.__inner_holidays[date]:
                if user_input in item.name.lower():
                    cntr += 1
                    match_date = item.date
                    match_name = item.name
                    possible_matches[str(cntr)] = [match_date, match_name]
                    print(f"  {str(cntr).rjust(2)}: {item.date} > {item.name}")
        if len(possible_matches) == 0:
            print("  There were no matches found.\n")
            return "failed"
        print("\n  If you want to delete one of these, enter the number.")
        print("  A failed match will return you to the main menu.")
        choice = input("  Enter your choice: >> ")
        if choice in possible_matches:
            print(
                f"  Removing {possible_matches[choice][1]} on {possible_matches[choice][0]}"
            )
            if input("  Proceed? (y/n) >> ").lower() in ["y", "yes", "yeah"]:
                match_found = True
        if match_found:
            return possible_matches[choice]
        return "passed"

    def remove_holiday(self):
        passed = False
        while not passed:
            print('  Enter either a date ( "YYYY-mm-dd") or a holiday.')
            user_input = input("  Find: >> ").lower()
            try:
                date_input = dt.datetime.strptime(user_input, "%Y-%m-%d").date()
                user_input = dt.datetime.strftime(date_input, "%Y-%m-%d")
            except:
                passed = False

            result = self.seek_holiday(user_input)
            if result == "passed":
                passed = True
            elif result == "failed":
                passed = False
            else:
                for item in self.__inner_holidays[result[0]]:
                    if item.name == result[1]:
                        try:
                            self.__inner_holidays[result[0]].remove(item)
                            print("  Item Successfully Removed")
                            self.__unsaved_holidays += 1
                            passed = True
                            delay(2)
                            break
                        except:
                            print("  Item Removal Failed")

    def read_json(self):
        """ 
        This function check for existing files and loads base
        holidays if there are no existing files.
        """
        try:
            if "managed_holidays.json" in os.listdir():
                print("Welcome Back!!".center(78, " "))
                print("Loading Managed Holidays...".center(78, " "), "\n")
                file = open("managed_holidays.json")
                managed_holidays = json.load(file)["holidays"]
                self.convert_new_holidays(managed_holidays)
                self.__holiday_source = "managed"
                delay(3)
            else:
                print("New Environment Detected".center(78, " "), "\n")
                print("Gathering Preloaded Holidays".center(78, " "), "\n")
                file = open("pre_loaded_holidays.json")
                managed_holidays = json.load(file)["holidays"]
                self.convert_new_holidays(managed_holidays)
                self.__holiday_source = "unmanaged"
        except:
            print("System Environment Inconsistency".center(78, " "), "\n")
            print("Gathering Preloaded Holidays".center(78, " "), "\n")
            delay(2)
            file = open("pre_loaded_holidays.json")
            provided_holidays = json.load(file)["holidays"]
            self.convert_new_holidays(provided_holidays)
            self.__holiday_source = "unmanaged"

    def save_holidays(self):
        combined = {"holidays": []}
        for year in self.__inner_holidays:
            for holiday in self.__inner_holidays[year]:
                holiday_to_save = {
                    "name": holiday.name,
                    "date": holiday.date,
                    "category": holiday.category,
                }
                combined["holidays"].append(holiday_to_save)
        print("  Storing data... please wait...".center(78, " "), "\n")
        try:
            combined_json = json.dumps(combined)
            with open("managed_holidays.json", "w") as file:
                file.write(combined_json)
                file.close()
            self.__unsaved_holidays = 0
        except:
            print("  Hmmm.... maybe I need a stepladder. I could not reach the shelf!.")

    def scrape_manager(self):
        """ This function is responsible for controlling the holiday scrape. """
        current_year = dt.datetime.today().year
        target_range = [_ for _ in range(current_year - 2, current_year + 3)]

        all_scraped = {}
        for year in target_range:
            scraped_holidays = self.scrape_holidays(year)
            all_scraped[year] = scraped_holidays
            print(f"  {year}: {len(scraped_holidays)}")
            delay(2)

        combined = {"holidays": []}
        for year in all_scraped:
            for holiday in all_scraped[year]:
                combined["holidays"].append(all_scraped[year][holiday])
        print("Merging Scraped Holidays...This may take a moment.".center(78, " "))
        self.convert_new_holidays(combined["holidays"])

    def strain_soup(self, soup, target_year):
        tables = soup.find_all("table", {"class": "table"})
        body = tables[0].find_all("tr")
        holiday_dict = {}

        # This for loop cleans the scrape, and places it in a temporary dictionary.
        # It then adds the temporary dict to a primary dict.
        for row in body:
            details = row.get_text("|").split("|")[:4]
            try:
                cleaned_date = self.standard_date(details[0].strip(), target_year)
                name = details[2].strip()
                if "(substitute)" in name:
                    continue

                category = details[3].strip()
                # I am removing this category because events exist on multiple days
                if "COVID-19 Lockdown" in category:
                    continue

                holiday_inner_dict = {
                    "name": name,
                    "date": cleaned_date,
                    "category": [category],
                }
                if name in holiday_dict:
                    holiday_dict[name]["category"].append(category)
                    cats = list(set(holiday_dict[name]["category"]))
                    holiday_dict[name]["category"] = cats
                else:
                    holiday_dict[name] = holiday_inner_dict
            except:
                continue
        return holiday_dict

    def filter_holidays_by_week(self, date_range):
        """ 
        While this function is expected to match by week number, I am matching on date.
        The reason for my decision, is that I have already matched a week number to a 
        date range through user input, and I have the data stored in a dictionary that 
        is keyed by date. Using a lambda to match on week number 'could' return inaccurate
        or incomplete results in week 1 of some years. For example, If I enter Week 1 because
        I want to know about New Years Day or a holiday in week 1, it might only match with 
        dates several days into the new year.
        
        I'm using a loop and lambda filter here because I spent way too much time trying to 
        figure out how to set the filter up to gather from my dict of a list of dicts.
        I know this is an inefficient use of a lambda filter, but I am not going to rewrite
        my data structure this late in the game.
        """

        starting_date = dt.datetime.strptime(date_range[0], "%Y-%m-%d")
        ending_date = dt.datetime.strptime(date_range[1], "%Y-%m-%d")

        date_list = [
            self.convert_dt(starting_date + dt.timedelta(days=i), "string")
            for i in range((ending_date - starting_date).days + 1)
        ]

        days = []
        for day in date_list:
            filtered_by_range = filter(
                lambda key: day in key, self.__inner_holidays.items()
            )
            days += list(filtered_by_range)
        return days, date_list

    def display_week_holidays(self, date_list):
        holiday_subset, dates = self.filter_holidays_by_week(date_list)
        weather_string = ""
        current = self.check_for_current_week(date_list)
        print("")
        for date in dates:
            if current:
                if date in [_ for _ in self.__forecast.keys()]:
                    weather_string = self.get_weather(date)
                else:
                    weather_string = "> Forecast is not available for this day."
            weekday = dt.datetime.strftime(self.convert_dt(date, "object"), "%A")
            print(f"  {weekday}, {date} {weather_string}")
            cntr = 0
            for celeb in holiday_subset:
                if celeb[0] == date:
                    cntr += 1
                    for holiday in celeb[1]:
                        print(holiday)
            print(" " if cntr != 0 else "  * No Holidays * \n")

        if input(" Press Enter to Continue: >> "):
            pass

    def get_week_nums(self, year, month):
        """ This function converts year/month -> list of week numbers. """
        end_of_month = calendar.monthrange(year, month)[1]
        starting_week = dt.datetime(year, month, 1).isocalendar()[1]
        ending_week = dt.datetime(year, month, end_of_month).isocalendar()[1]

        # This tries to build a list that will be empty if starting week > ending week
        res = list(range(starting_week, ending_week + 1))
        if not res:
            week_num = 52 if starting_week != 53 else 53
            res = list(range(starting_week, week_num + 1)) + list(
                range(1, ending_week + 1)
            )
        return res

    def check_month(self, month_input):
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
            print("  That month is not recognized. Please try again. ")
            return False
        else:
            month_input = month_input.capitalize()
            if month_input in month_converter:
                matched = month_input
            else:
                matched = allowed_months[allowed_months.index(month_input) + 1]
        return matched

    def drill_down_to_week(self, which_month, which_year):
        month_passed = True
        month_num = self.get_month_number(which_month)
        week_nums = self.get_week_nums(which_year, month_num)
        translate = True if week_nums[0] > week_nums[1] else False
        week_dict = {}
        print("\n   #: Date Range", "\n   ``````````````")
        for i, week in enumerate(week_nums):
            if i == 0 and translate:
                dates = self.match_week_to_date(week, which_year - 1)
            else:
                dates = self.match_week_to_date(week, which_year)

            week_dict[str(week)] = list(
                map(lambda x: self.convert_dt(x, "string"), [dates[0], dates[1]])
            )

            dates = " to ".join(str(_.month) + "-" + str(_.day) for _ in dates)
            print(f"{str(week).rjust(4)}: {dates}")
        example = random.choice([_ for _ in week_dict.keys()])
        week_choice = input(f'\n  Choose a week: (i.e. "{example}") >> ')
        if week_choice.isnumeric() and week_choice in week_dict.keys():
            return week_dict[week_choice]
        else:
            if '"' in week_choice:
                print(self.__errors[1])
                delay(2)
            else:
                print(self.__errors[2])
                delay(2)
                print(self.__errors[3])
                delay(2)

    def holiday_view_builder(self):
        """ This heavy function gathers user input and displays the requested view. """
        print('  Leave blank for current week. "exit" to close')
        which_year = input("  Which year would you like to view?  (i.e. 2020) >> ")
        if which_year.lower() == "exit":
            return True

        if which_year.strip() == "":
            today = dt.datetime.today().date()
            year, week_num = today.year, dt.datetime.strftime(today, "%W")
            week_choice = self.match_week_to_date(week_num, year)
            return list(
                map(
                    lambda x: self.convert_dt(x, "string"),
                    [week_choice[0], week_choice[1]],
                )
            )
        else:
            year_passed = check_input(which_year, "year", [2020, 2025])
            if not year_passed:
                print(errors)
                return False
            which_year = int(which_year)
            month_passed = False
            week_passed = False
            while not month_passed:
                print("\n  To search by week number, input the week number.")
                print("  Otherwise, input the name of a month.")
                which_month = input("  Which month of the year? (i.e. Jan, august) >> ")
                if which_month.isnumeric():
                    if int(which_month) in range(1, 54):
                        try:
                            # "which_month" in this case is actually the week number
                            # because the user bypassed the standard options.
                            week_choice = self.match_week_to_date(
                                which_month, which_year
                            )
                            week_choice = list(
                                map(
                                    lambda x: self.convert_dt(x, "string"),
                                    [week_choice[0], week_choice[1]],
                                )
                            )
                            month_passed = True
                            return week_choice
                        except Exception as E:
                            print(E)
                            print(
                                "That week does not seem to be an option. Please try again."
                            )
                    else:
                        print(" That week is not an option. Please try again.")
                else:
                    which_month = self.check_month(which_month)
                    if which_month:
                        return self.drill_down_to_week(which_month, which_year)
        # Fall-through returns None to Main Menu


########## END OF CLASS DECLARATIONS ##########
###############################################

##-------STARTING GENERAL FUNCTIONS----------##
# ............    GET FUNCTIONS  .............#


def get_datetime():
    return dt.datetime.now()


def get_templates():
    templates = requests.get(
        "https://raw.githubusercontent.com/jedc4xer/holiday_manager/main/manager_template.txt"
    ).text.split(",")
    return templates


def get_errors():
    errors = requests.get(
        "https://raw.githubusercontent.com/jedc4xer/holiday_manager/main/user_communication.txt"
    ).text.split(",")
    return errors


# .............   MENU FUNCTIONS  .............#


def prettify_current_menu(menu):
    return f"  HOLIDAY MANAGER > {menu}  ".center(75, "`")


def prettify_holiday_count(count, unique, save_status):
    if save_status > 0:
        unsaved = f"| Unsaved: {save_status}"
    else:
        unsaved = ""
    return f" {count} <- Count | Unique -> {unique} {unsaved}".center(75, "-")


def save_menu(BoontaEve):
    if input("  Do you want to save? (yes) >> ").lower() in ["y", "yes", "yeah", "yea"]:
        try:
            BoontaEve.save_holidays()
            print("  Save Succeeded")
        except Exception as E:
            print(E)
            print("  Save Failed")
    else:
        print("  Canceled without saving... Returning to main menu.")
    delay(2)


def display_menu_template(active_menu, arg_list):
    clean_screen()
    current_weather = arg_list[0]
    current_day_info = arg_list[1]
    locale_info = arg_list[2]
    holiday_cnt = arg_list[3]
    menu_identifier = prettify_current_menu(active_menu)
    print(
        templates[1].format(
            flow_location=menu_identifier,
            current_menu=active_menu,
            current_weather=current_weather,
            day_info=current_day_info,
            locale=locale_info,
            holiday_cnt=holiday_cnt,
        )
    )


# ............. GENERAL FUNCTIONS .............#


def delay(duration):
    time.sleep(duration)


def clean_screen():
    os.system(clear_term)


def modify_current_date_time():
    current_dt = get_datetime()
    current_date = dt.datetime.strftime(current_dt, "%A, %B %d, %Y")
    current_time = dt.datetime.strftime(current_dt, "%H:%M:%S")
    if current_time < "06:00":
        time_of_day = "Early Morning"
    elif current_time >= "06:00" and current_time < "10:00":
        time_of_day = "Morning"
    elif current_time >= "10:00" and current_time < "12:00":
        time_of_day = "Late Morning"
    elif current_time >= "12:00" and current_time < "15:00":
        time_of_day = "Afternoon"
    elif current_time >= "15:00" and current_time < "18:00":
        time_of_day = "Late Afternoon"
    elif current_time >= "18:00" and current_time < "21:00":
        time_of_day = "Early Evening"
    elif current_time >= "21:00":
        time_of_day = "Evening"
    else:
        time_of_day = "[error] - Somehow we have ended up on Naboo!"

    day_info = f"{current_date} | {time_of_day}"
    return day_info


# .............  CHECK FUNCTIONS  .............#


def check_input(input_string, requirements, limits):
    if requirements == "number":
        if input_string.isnumeric() and int(input_string) in range(1, limits + 1):
            return True
    elif requirements == "year":
        if input_string.isnumeric() and int(input_string) in range(
            limits[0], limits[1]
        ):
            return True
    print(f"  {input_string} is not a valid {requirements}. Please try again.")
    delay(1.5)
    return False


def check_exit():
    if BoontaEve.return_save_status() > 0:
        print("  There are unsaved changes.")
    exit = input("  Are you sure you want to exit? (yes/no) >> ").lower()
    if exit in ["y", "yes", "yeah", "yep", "ye", "uh huh"]:
        return True
    return False


# .............   ***  MAIN  ***  ............#


def main():
    # locale_info, country = get_locale()
    errors = get_errors()
    current_day_info = modify_current_date_time()
    CurrentWeather = WeatherReport()
    locale_info, current_weather, forecast = CurrentWeather.return_data()
    BoontaEve = HolidayList(errors, forecast)
    holiday_cnt, unique = BoontaEve.num_holidays()
    save_status = BoontaEve.return_save_status()
    delay(1)
    count_disp = prettify_holiday_count(holiday_cnt, unique, save_status)
    main_args = [current_weather, current_day_info, locale_info, count_disp]
    if holiday_cnt < 100:
        display_menu_template("Starting", main_args)
        BoontaEve.scrape_manager()

        holiday_cnt, unique = BoontaEve.num_holidays()
        save_status = BoontaEve.return_save_status()
        count_disp = prettify_holiday_count(holiday_cnt, unique, save_status)
        main_args = [current_weather, current_day_info, locale_info, count_disp]
    display_menu_template("Main Menu", main_args)
    outer_passed = False
    while not outer_passed:
        passed = False
        while not passed:
            save_status = BoontaEve.return_save_status()
            count_disp = prettify_holiday_count(holiday_cnt, unique, save_status)
            main_args = [current_weather, current_day_info, locale_info, count_disp]
            display_menu_template("Main Menu", main_args)
            print(templates[3])
            main_menu_choice = input("  Please Choose an Option >> ")
            passed = check_input(main_menu_choice, "number", 5)
        main_menu_choice = int(main_menu_choice)
        if main_menu_choice == 1:
            BoontaEve.input_holiday()
            holiday_cnt, unique = BoontaEve.num_holidays()
        elif main_menu_choice == 2:
            BoontaEve.remove_holiday()
            holiday_cnt, unique = BoontaEve.num_holidays()
        elif main_menu_choice == 3:
            display_menu_template("Save Menu", main_args)
            save_menu(BoontaEve)
        elif main_menu_choice == 4:
            passed = False
            while not passed:
                display_menu_template("Holiday Viewer", main_args)
                passed = BoontaEve.holiday_view_builder()
            if type(passed) == list:
                BoontaEve.display_week_holidays(passed)
            else:
                print(passed, "Not a list")
                raise SystemExit

        elif main_menu_choice == 5:
            outer_passed = check_exit()


clean_screen()
templates = get_templates()
print(templates[0])


if __name__ == "__main__":
    main()

    # Closing Sequence
    # display_menu_template('Closing',['','',''])
    clean_screen()
    print(templates[2])
    print("\n" * 2)
    print("Closing the Manager".center(78, " "))
    delay(1.5)
    clean_screen()
    print("\n" * 2)
    print("Goodbye!!".center(78, " "))
    print("May the fourth be with you.".center(78, " "))
    print("\n" * 3)


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
