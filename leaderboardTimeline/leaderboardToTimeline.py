import re
from datetime import datetime
import operator
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import dates as pltDate
import pylab


class Time(object):

    name = ""
    time = datetime
    date = datetime

    def __init__(self, name, time, date):

        self.name = name
        try:
            self.time = datetime.strptime(time, '%H:%M:%S')
        except ValueError:
            self.time = datetime.strptime(time, '%M:%S')
        self.date = datetime.strptime(date, '(%d/%m/%y)')


def readInTimes(file):

    gameTimes = []
    currentCategory = []

    for line in file:

        if len(line.split()) == 1:
            if len(currentCategory) > 1:
                currentCategory = sorted(currentCategory, key=operator.attrgetter("date"))
                gameTimes.append(currentCategory)
            gameTimes.append(line)
            currentCategory = []

        elif not line.strip():
            continue

        else:

            runnerTimes = line.replace(",", "").replace("??", "01")
            runnerTimes = runnerTimes.split()
            name = runnerTimes[0]

            index = 1
            while index < len(runnerTimes):

                currentCategory.append(Time(name,
                                            runnerTimes[index],
                                            runnerTimes[index+1]))
                index += 2

    gameTimes.append(currentCategory)
    return gameTimes

fileNames = ["jak1.txt",
             "jak2.txt",
             "jak3.txt",
             "jakx.txt",
             "tlf.txt",
             "trifecta.txt"]

for file in fileNames:

    pastTimes = readInTimes(open(file))

    category = 0
    while category < len(pastTimes):

        categoryName = pastTimes[category].replace("\n", "").replace(":", "")
        currentWR = datetime.strptime("23:59:59", '%H:%M:%S')
        times = []
        labels = []
        dates = []

        for time in pastTimes[category + 1]:

            if time.time < currentWR:
                currentWR = time.time
                times.append(time.time)
                labels.append(time.name)
                dates.append(time.date)

        fig = plt.figure(figsize=(50, 50))
        ax = fig.add_subplot(111)
        ax.xaxis.set_major_formatter(pltDate.DateFormatter('%Y-%m-%d'))
        ax.grid()

        plt.plot(dates, times, "r-", linewidth=2)

        labelIndex = 0
        for xy in zip(dates, times):
            try:
                ax.annotate(labels[labelIndex] + " - " + xy[1].strftime("%H:%M:%S"),
                            xy=xy,
                            textcoords='data')
            except ValueError:
                ax.annotate(labels[labelIndex] + " - " + xy[1].strftime("%M:%S"),
                            xy=xy,
                            textcoords='data')

            labelIndex += 1

        cur_axes = plt.gca()
        cur_axes.axes.get_yaxis().set_ticklabels([])
        plt.xlabel('Date')
        plt.ylabel('Time')
        plt.title(categoryName + " - Last Updated October 31st 2015 by Tomjak")
        plt.savefig("Output/" + categoryName + ".png")

        category += 2

