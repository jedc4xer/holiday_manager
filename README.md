# holiday_manager
Repository for files pertaining to the Dev10 Holiday Manager Assessment

Introduction:
    
    This program is designed to assist a small group of users with planning
    activities around holidays, and to display any relevant weather. 
    
Structure:

    There are 3 classes:
    - Holiday
        - This class is used to define each holiday object.
        
    - WeatherReport
        - This class gathers and holds the weather for later use.
        
    - HolidayList
        - This is the primary Holiday Manager Class. 
        
        It manages each holiday object, imports and exports data, 
        runs scrapes if necessary, and displays information to the
        end user. 
            
Script Sequence:

    1. On startup, the weather is collected.
    2. Then the environment is checked.
        - If a new environment is detected:
            - The small base list of holidays is loaded
            - Holidays are scraped from the web
    3. Summary infomation is determined and displayed to the user.
    4. A menu is provided to the user. 
    5. Any data changes are recognized and reported to the user.
    6. A user can view the data.
        - Current (Defaults to the week that contains the current day)
        - Filters are available by Year, Month, and Week
        - If there is weather available for the picked period, the user
            is given the option to include the weather in the output.
    7. A user can explore the menu paths and explore at will.
    8. On exit, if a user has not saved, they are warned and given the option.