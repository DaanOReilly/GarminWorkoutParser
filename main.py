import os
import argparse, sys
import xml.etree.ElementTree as ET
import datetime
import time

# parsing the arguments for FTP and ZwiftID
parser=argparse.ArgumentParser()
parser.add_argument("-f", "--ftp", help="FTP value used to convert the power zones from fixed values to percentage of FTP (default: 200)")
parser.add_argument("-i", "--zwiftid", help="ZwiftID used to save the zwo file in the correct Zwift workout directory (default: output)")
args=parser.parse_args()

# Pupulating the global variables with the arguments or default values
ftp             = int(args.ftp) if args.ftp else 200
zwiftdirectory  = "C:\\Users\\"+ os.getlogin() +"\\AppData\\Local\\Zwift\\Workouts\\" + args.zwiftid if args.zwiftid else "output"

#reading the workout.txt file
f1 = open("input\\workout.txt", "r+") 
workoutData = f1.read()
f1.close()

# Workout name and datetime convertion
date_str = datetime.datetime.strptime(workoutData.splitlines()[1].split(' - ')[0].strip(), "%d %B %Y").date().isoformat()
workout_name = date_str + '_' + workoutData.splitlines()[0].strip()

# Creating the xml frame
root        = ET.Element('workout_file')
author      = ET.SubElement(root, 'author')
name        = ET.SubElement(root, 'name')
description = ET.SubElement(root, 'description')
sportType   = ET.SubElement(root, 'sportType')
tags        = ET.SubElement(root, 'tags')
workout     = ET.SubElement(root, 'workout')

# Populating the xml frame with data from workout.txt
author.text = os.getlogin()
name.text = workout_name
descText = workoutData.splitlines()[2].strip() + " - " + workoutData.splitlines()[3].strip()
    
sportType.text = "bike"

if "Notes" in workoutData:
    linecursor = workoutData.splitlines().index("Notes")
    description.text = workoutData.splitlines()[linecursor].strip() + " " + workoutData.splitlines()[linecursor+1].strip()

if "Warm up" in workoutData:
    warmup = ET.SubElement(workout, 'Warmup')
    linecursor = workoutData.splitlines().index("Warm up")
    t = workoutData.splitlines()[linecursor+1].strip()
    if len(t) == 5:
        d = time.strptime(t, "%M:%S")
        duration = datetime.timedelta(minutes=d.tm_min, seconds=d.tm_sec).total_seconds()
    else:
        d = time.strptime(t, "%H:%M:%S")
        duration = datetime.timedelta(hours=d.tm_hour,minutes=d.tm_min, seconds=d.tm_sec).total_seconds()
    warmup.set("Duration", str(int(duration)))
    warmup.set("PowerLow", str(round(float(workoutData.splitlines()[linecursor+3].split('-')[0].strip())/ftp, 2)))
    warmup.set("PowerHigh", str(round(float(workoutData.splitlines()[linecursor+3].split('-')[1].split(' ')[0].strip())/ftp, 2)))
    # warmup.set("Pace", "0")

if "Bike" in workoutData:
    if "Times" in workoutData:
        IntervalsT = ET.SubElement(workout, 'IntervalsT')
        linecursor = workoutData.splitlines().index("Bike")
        IntervalsT.set("Repeat", str(int(workoutData.splitlines()[linecursor-1].split(' ')[0].strip())))

        linecursor = workoutData.splitlines().index("Bike")
        tod = workoutData.splitlines()[linecursor+1].strip()
        if len(tod) <= 5:
            d = time.strptime(tod, "%M:%S")
            duration = datetime.timedelta(minutes=d.tm_min, seconds=d.tm_sec).total_seconds()
        else:
            d = time.strptime(tod, "%H:%M:%S")
            duration = datetime.timedelta(hours=d.tm_hour,minutes=d.tm_min, seconds=d.tm_sec).total_seconds()
        IntervalsT.set("OnDuration", str(int(duration)))
        IntervalsT.set("OnPower", str(round(float(int(workoutData.splitlines()[linecursor+3].split('-')[0].strip()) + int(workoutData.splitlines()[linecursor+3].split('-')[1].split(' ')[0].strip())) // 2 / ftp, 2)))
        
        linecursor = workoutData.splitlines().index("Recover")
        tor = workoutData.splitlines()[linecursor+1].strip()
        if len(tor) <= 5:
            d = time.strptime(tor, "%M:%S")
            duration = datetime.timedelta(minutes=d.tm_min, seconds=d.tm_sec).total_seconds()
        else:
            d = time.strptime(tor, "%H:%M:%S")
            duration = datetime.timedelta(hours=d.tm_hour,minutes=d.tm_min, seconds=d.tm_sec).total_seconds()
        IntervalsT.set("OffDuration", str(int(duration)))
        IntervalsT.set("OffPower", str(round(float(int(workoutData.splitlines()[linecursor+3].split('-')[0].strip()) + int(workoutData.splitlines()[linecursor+3].split('-')[1].split(' ')[0].strip())) // 2 / ftp, 2)))
    else:
        SteadyState = ET.SubElement(workout, 'SteadyState')
        linecursor = workoutData.splitlines().index("Bike")
        t = workoutData.splitlines()[linecursor+1].strip()
        if len(t) <= 5:
            d = time.strptime(t, "%M:%S")
            duration = datetime.timedelta(minutes=d.tm_min, seconds=d.tm_sec).total_seconds()
        else:
            d = time.strptime(t, "%H:%M:%S")
            duration = datetime.timedelta(hours=d.tm_hour,minutes=d.tm_min, seconds=d.tm_sec).total_seconds()
        SteadyState.set("Duration", str(int(duration)))
        SteadyState.set("Power", str(round(float(int(workoutData.splitlines()[linecursor+3].split('-')[0].strip()) + int(workoutData.splitlines()[linecursor+3].split('-')[1].split(' ')[0].strip())) // 2 / ftp, 2)))

if "Cool down" in workoutData:
    cooldwon = ET.SubElement(workout, 'Cooldown')
    linecursor = workoutData.splitlines().index("Cool down")
    t = workoutData.splitlines()[linecursor+1].strip()
    if len(t) == 5:
        d = time.strptime(t, "%M:%S")
        duration = datetime.timedelta(minutes=d.tm_min, seconds=d.tm_sec).total_seconds()
    else:
        d = time.strptime(t, "%H:%M:%S")
        duration = datetime.timedelta(hours=d.tm_hour,minutes=d.tm_min, seconds=d.tm_sec).total_seconds()
    cooldwon.set("Duration", str(int(duration)))
    cooldwon.set("PowerLow", str(round(float(workoutData.splitlines()[linecursor+3].split('-')[1].split(' ')[0].strip())/ftp, 2)))
    cooldwon.set("PowerHigh", str(round(float(workoutData.splitlines()[linecursor+3].split('-')[0].strip())/ftp, 2)))
    # cooldwon.set("Pace", "0")

# Saving the zwo file
xml_data = ET.tostring(root)
with open(zwiftdirectory + "\\" + workout_name + ".zwo", "wb") as f:
    f.write(xml_data)