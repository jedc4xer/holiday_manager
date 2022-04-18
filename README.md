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

    1. On startup, the environment is checked.
    - If a new environment is detected:
        - The small base list of holidays is loaded
        - Holidays are scraped from the web