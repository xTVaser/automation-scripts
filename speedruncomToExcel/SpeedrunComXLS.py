import xlwt
import json
import requests
import time
from datetime import datetime

style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on',
    num_format_str='#,##0.00')
style1 = xlwt.easyxf(num_format_str='D-MMM-YY')

wb = xlwt.Workbook()
ws = wb.add_sheet('A Test Sheet')

ws.write(0, 0, "Game Name")
ws.write(0, 1, "Category")

ws.write(1, 0, "Position")
ws.write(1, 1, "Runner")
ws.write(1, 2, "Time")
ws.write(1, 3, "Video Links")
ws.write(1, 4, "Date")
ws.write(1, 5, "Platform")
ws.write(1, 6, "Region")
ws.write(1, 7, "Runner Comment")
ws.write(1, 8, "SR.com Link")

userInput = input("Enter the name of the game: ")
request = requests.get(url="http://www.speedrun.com/api/v1/games?name=" + userInput)
game_data = request.json()['data']

while len(game_data) <= 0:
    userInput = input("Game not Found, try again: ")
    request = requests.get(url="http://www.speedrun.com/api/v1/games?name=" + userInput)
    game_data = request.json()['data']

gameID = game_data[0]['id']
categoryLink = game_data[0]['links'][3]['uri']

request = requests.get(url=categoryLink)
categories = request.json()['data']

categoryNum = 0

for category in categories:
    print(str(categoryNum) + ") " + category['name'])
    categoryNum += 1

userInput = int(input("Select a Category: "))

while userInput < 0 and userInput > categoryNum:
    userInput = input("Invalid Choice, try again: ")

request = requests.get(url="http://www.speedrun.com/api/v1/leaderboards/"
                           + gameID + "/category/"
                           + categories[userInput]['id']
                           + "?max=200") #Does not support pagination yet
api_data = request.json()['data']
runs = api_data['runs']

request = requests.get(url="http://www.speedrun.com/api/v1/platforms?max=200")
platform_data = request.json()['data']
platforms = dict()

for platform in platform_data:
    platforms[platform['id']] = platform['name']

request = requests.get(url="http://www.speedrun.com/api/v1/regions?max=200")
region_data = request.json()['data']
regions = dict()

for region in region_data:
    regions[region['id']] = region['name']


currentRow = 2

for run in runs:
    ws.write(currentRow, 0, run['place'])

    runInfo = run['run']

    if runInfo['players'][0]['rel'] == "guest":
        ws.write(currentRow, 1, runInfo['players'][0]['name'])
    else:
        request = requests.get(url="http://www.speedrun.com/api/v1/users/"+runInfo['players'][0]['id'])
        userName = request.json()['data']['names']['international']
        ws.write(currentRow, 1, userName) #Call API to get the User's Actual Name

    ws.write(currentRow, 2, time.strftime('%H:%M:%S', time.gmtime(runInfo['times']['primary_t'])))

    if runInfo['videos'] is not None:
        videoLinks = runInfo['videos']['links']

        for link in videoLinks:
            ws.write(currentRow, 3, link['uri'])

    else:
        ws.write(currentRow, 3, "No Video")

    ws.write(currentRow, 4, runInfo['date'])

    ws.write(currentRow, 5, platforms[runInfo['system']['platform']]) #Call API to Match up Platform IDs
    ws.write(currentRow, 6, regions[runInfo['system']['region']]) #Same here

    ws.write(currentRow, 7, runInfo['comment'])

    ws.write(currentRow, 8, runInfo['weblink'])

    currentRow += 1

wb.save('example.xls')