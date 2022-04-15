import json
import os
import tempfile
import time
import shutil
import subprocess
from datetime import datetime
from pathlib import Path


homeDir = os.path.expanduser('~')
tempFile = '/tmp/tempAirTagFile' 
csvFileLocation="./airTags.csv"
sourceLastChanged=0

# Open CSV file and write header if needed
def openCsvFile(fileLocation):
  if not os.path.isfile(fileLocation):
    csvFile = open(fileLocation, "a")
    csvFile.write("datetime,name,model,serialnumber,producttype,productindentifier,vendoridentifier,antennapower,systemversion,batterystatus,locationpositiontype,locationlatitude,locationlongitude,locationtimestamp,locationverticalaccuracy,locationhorizontalaccuracy,locationfloorlevel,locationaltitude,locationisinaccurate,locationisold,locationfinished,addresslabel,addressstreetaddress,addresscountrycode,addressstatecode,addressadministrativearea,addressstreetname,addresslocality,addresscountry,addressareaofinterest0,addressareaofinterest1\n")
  else:
    csvFile = open(fileLocation, "a")
  return csvFile
  

def recordLocations(sourceLastChanged):
  print("Starting to read locations")

  try:

    currentTime=os.path.getmtime(homeDir + '/Library/Caches/com.apple.findmy.fmipcore/Items.data')
    if not currentTime > sourceLastChanged:
      print("Skipping file hasn't changed")
      return sourceLastChanged
    sourceLastChanged = currentTime
    shutil.copyfile(homeDir + '/Library/Caches/com.apple.findmy.fmipcore/Items.data', tempFile)
  except Exception as e: 
    print("Unable to copy file, check permissions")
    print(e)
    exit(2)

  with open(tempFile) as json_file:
      data = json.load(json_file)
      for t in data:

          print(".", end = '')

          name = t["name"]
          modelname = t["productType"]["productInformation"]["modelName"]
          serialnumber=t["serialNumber"]
          producttype=t["productType"]["type"]
          productindentifier=t["productType"]["productInformation"]["productIdentifier"]
          vendoridentifier=t["productType"]["productInformation"]["vendorIdentifier"]
          antennapower=t["productType"]["productInformation"]["antennaPower"]
          systemversion=t["systemVersion"]
          batterystatus=t["batteryStatus"]
          locationpositiontype=t["location"]["positionType"]
          locationlatitude=t["location"]["latitude"]
          locationlongitude=t["location"]["longitude"]
          locationtimestamp=t["location"]["timeStamp"]
          locationverticalaccuracy=t["location"]["verticalAccuracy"]
          locationhorizontalaccuracy=t["location"]["horizontalAccuracy"]
          locationfloorlevel=t["location"]["floorLevel"]
          locationaltitude=t["location"]["altitude"]
          locationisinaccurate=t["location"]["isInaccurate"]
          locationisold=t["location"]["isOld"]
          locationfinished=t["location"]["locationFinished"]
          addresslabel=t["address"]["label"]
          addressstreetaddress=t["address"]["streetAddress"]
          addresscountrycode=t["address"]["countryCode"]
          addressstatecode=t["address"]["stateCode"]
          addressadministrativearea=t["address"]["administrativeArea"]
          addressstreetname=t["address"]["streetName"]
          addresslocality=t["address"]["locality"]
          addresscountry=t["address"]["country"]
          try:
            addressareaofinterest0=t["address"]["areaOfInterest"][0]
          except Exception as e: 
            addressareaofinterest0=""        
          try:
            addressareaofinterest1=t["address"]["areaOfInterest"][1]
          except Exception as e: 
            addressareaofinterest1=""
          batterystatus=t["batteryStatus"]

          csvFile.writelines("\""+str(datetime.now().strftime("%Y-%m-%d  %T"))+"\",\""+str(name)+"\",\""+str(modelname)+"\",\""+str(serialnumber)+"\",\""+str(producttype)+"\",\""+str(productindentifier)+"\",\""+str(vendoridentifier)+"\",\""+str(antennapower)+"\",\""+str(systemversion)+"\",\""+str(batterystatus)+"\",\""+str(locationpositiontype)+"\",\""+str(locationlatitude)+"\",\""+str(locationlongitude)+"\",\""+str(locationtimestamp)+"\",\""+str(locationverticalaccuracy)+"\",\""+str(locationhorizontalaccuracy)+"\",\""+str(locationfloorlevel)+"\",\""+str(locationaltitude)+"\",\""+str(locationisinaccurate)+"\",\""+str(locationisold)+"\",\""+str(locationfinished)+"\",\""+str(addresslabel)+"\",\""+str(addressstreetaddress)+"\",\""+str(addresscountrycode)+"\",\""+str(addressstatecode)+"\",\""+str(addressadministrativearea)+"\",\""+str(addressstreetname)+"\",\""+str(addresslocality)+"\",\""+str(addresscountry)+"\",\""+str(addressareaofinterest0)+"\",\""+str(addressareaofinterest1)+"\"\n")

  
  print("\nDone, sleeping")
  return sourceLastChanged

def checkRunning():
  output = int(subprocess.getoutput('ps aux|grep "FindMy.app/Contents/MacOS/FindM[y]"|wc -l'))
  if output <= 0:
    print("FindMy not running so attempting to start")
    subprocess.getoutput("open /System/Applications/FindMy.app")


while True:
  checkRunning()
  csvFile = openCsvFile(csvFileLocation)
  sourceLastChanged = recordLocations(sourceLastChanged)
  time.sleep(60)
