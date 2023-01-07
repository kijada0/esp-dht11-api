import os
import time
import requests
from datetime import datetime

url = "http://192.168.0.125/"
key = ""

file_name = "\\data.csv"

def main():
    print("Taking measurements ...")
    data = getData()
    saveData(data)
    print("Finished!")

def getData():
    print("Getting data ...")
    data_are_not_ready = True
    while data_are_not_ready:
        try:
            response = requests.get(url, timeout=5).json()
            if response["status"] == "OK":
                data_are_not_ready = False
                print("Response:\t", response)
                return response
            else:
                print("Data error: ", response["status"])
        except Exception as error:
            print("Request error: ", error)

        time.sleep(0.5)

def saveData(data):
    print("Saving data ...")
    dir = os.getcwd()
    print("File path:", dir + file_name)
    if os.path.exists(dir + file_name):
        file = open(dir + file_name, "a")
    else:
        print("Creating new file ...")
        file = open(dir + file_name, "w")
        file.write("date; time; temperature; humidity \n")

    line = ""

    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    hour = now.strftime("%H:%M:%S")
    line += date + "; " + hour + "; "

    temperature = data["temperature"]
    humidity = data["humidity"]
    line += str(round(temperature, 2)) + "; " + str(int(humidity))

    line += "\n"
    file.write(line)

main()


