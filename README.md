# GarminWorkoutParser
A Python project to generate multiple formats baased on planned Gamrin workouts.
In case you have a format that is not covered by the script, feel free to create an Issue.

## Usage
1. Change `input\workout.txt` to the text of your workout from your garmin calendar\
    Example:
    >Tempo\
    >16 June 2026 - 55 Minutes\
    >Notes\
    >30:00@145W\
    >Warm up\
    >10:00\
    >Total Time\
    >79-115 W\
    >Intensity Target\
    >Bike\
    >30:00\
    >Total Time\
    >132-159 W\
    >Intensity Target\
    >Cool down\
    >15:00\
    >Total Time\
    >79-115 W\
    >Intensity Target
2. run the script with your parameters `py .\main.py -f 200 -i 1234567`
    - if no FTP is passed workout will be generated using default value 200.
    - if no ZwiftID is passed workout will be saved to `output` folder.

## Help
usage: `main.py [-h] [-f FTP] [-i ZWIFTID]`

options:\
  -h, --help            show this help message and exit\
  -f, --ftp FTP         FTP value used to convert the power zones from fixed values to percentage of FTP (default: 200)\
  -i, --zwiftid ZWIFTID
                        ZwiftID used to save the zwo file in the correct Zwift workout directory (default: output)

## Libraries
Currently no extrenal libraries are used.

## Roadmap
- Scraping workouts from Garmin calendar
- API Integration Zwift once available
- API Integration GFarmin once available
- Create executable prograam