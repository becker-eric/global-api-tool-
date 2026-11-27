Cross-border Meeting Planner

This is a small Python program that helps two people in different time zones find a meeting time. It uses the Open-Meteo API to find time zones and the Nager.Date API to check public holidays.

What you need

You need Python 3.9 or higher. On Windows: tzdata package.

Install tzdata on Windows

Open a terminal and type: pip install tzdata

On macOS and Linux you usually do not need this.

How to start the program

Open a terminal in the project folder and type: python main.py

What the program asks for

The program asks for your country code, for example DE. Then it asks for your city, for example Mainz. Then it asks for the other persons country code, for example US. Then it asks for the other persons city, for example Chicago. Then it asks for the start date in yyyy-mm-dd format. Then it asks for your available time slots in yyyy-mm-dd hh:mm - hh:mm format. Then it asks for the other persons available time slots. Type done when you are finished with the slots.

Example

Your country code: DE
Your city: Mainz
Other country code: US
Other city: Chicago
Start date (yyyy-mm-dd): 2026-12-03

Own available slots. Format: yyyy-mm-dd hh:mm - hh:mm, done for finish.

    2026-12-03 09:00 - 18:00
    done

Other available slots. Format: yyyy-mm-dd hh:mm - hh:mm, done for finish.

    2026-12-03 08:00 - 12:00
    done

Suggested meeting slots:

2026-12-03:
Own time: 15:00 - 18:00
Other time: 08:00 - 12:00

Files in this project

The result is saved as results.txt in the project folder.

Errors the program handles

The program handles wrong date format, wrong time slot format, city not found, no internet connection, and a start date on Friday, Saturday, or Sunday.

Security note

No passwords or API keys are stored in this repository. The program only sends city and country code to the APIs. All personal data stays on your computer.
