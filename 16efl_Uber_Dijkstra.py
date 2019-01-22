import csv
import time

printB = False  # output print for solution
enbDyn = True  # Enable dynamic storing of previously found points
enbExp = False

global dynMemory
dynMemory = []


##################################################
# Importing Network#

def roadInput():
    pathMatrix = open('network.csv', 'r')  # open file in read form
    matrixReader = csv.reader(pathMatrix, delimiter=',')  # pull data with , delimiter
    pathData = []

    i = 0                                               # Move data in list of lists
    for row in matrixReader:
        for val in row:
            row[i] = int(row[i])
            i = i + 1
        i = 0
        pathData.append(row)

    global roadSize
    roadSize = len(pathData)
    return pathData


##################################################
# Schedule Import Start#

def scheduleImport():
    pathMatrix = open('supplementpickups.csv', 'r')  # open file in read form
    matrixReader = csv.reader(pathMatrix, delimiter=',')  # pull data with , delimeter
    pathData = []
    # Build request list
    i = 0

    for row in matrixReader:  # locations range from 1-50
        row[0] = int(row[0])  # adjusting to 0-49
        row[1] = int(row[1]) - 1
        row[2] = int(row[2]) - 1
        pathData.append(row)

    #print('Schedule Successfulling Stored')
    return pathData


##################################################


##################################################
# Uber Car Class#
##################################################
class Uber:  # Class with data such as...

    def __init__(self, identify):
        self.start = 0  # Location of pickup(Not useful currently)
        self.end = 0  # Location of drop off
        self.dropTime = 0  # Time of current delivery dropoff
        self.identity = identify  # Identifier for car


def timeFunc(grid, car, request):  # Determine the time to pick up passenger
    pathTime = dijkstras(grid, car.end, int(request[1]))
    if (car.dropTime > request[0]):  # If currently busy
        pathTime = pathTime + car.dropTime - request[0]  # Include time to drop off current pasenger
    return pathTime


##################################################


##################################################
# Dijkstras#
##################################################
def dijkstras(network, start, end):
    check, distFrom = dynCheck(start, end)
    if enbDyn and check:  # If dynamic storage is available check whehter path has been traversed before
        answer = distFrom
    else:
        # store more fastest time to each point from a chosen point
        distFrom = []
        finalizedSet = []

        count1 = 0
        while count1 < len(network):  # Currrently all dist. are unknown
            distFrom.append(float('inf'))  # setting inf. distance away
            finalizedSet.append(False)  # set false to confirmed shortest distance
            count1 = count1 + 1
        distFrom[start] = 0  # distance to starting point is now 0

        count2 = 0
        while count2 < (len(network)):  # find the shortest path to all points
            minimum = minDistance(distFrom, finalizedSet)  # pick vertex shortest distance from the column
            finalizedSet[minimum] = True  # set picked vertex to True
            count4 = 0
            while (count4 < len(network)):  # if a shorter distance is found, update val of finalizedSet
                if (finalizedSet[count4] == False and network[minimum][count4] and distFrom[minimum] != 2147483647 and distFrom[minimum] + network[minimum][count4] < distFrom[count4]):
                    distFrom[count4] = distFrom[minimum] + network[minimum][count4]
                count4 = count4 + 1
            count2 = count2 + 1
        answer = printSolution(distFrom, start, end)
    return answer


def minDistance(distFrom, finalizedSet):
    min = 2147483647  # Set min to max of int so its not accidentally chosen

    count3 = 0
    while (count3 < roadSize):  # Chose minimum distance
        if (finalizedSet[count3] == False and distFrom[count3] <= min):
            min = distFrom[count3]
            minIndex = count3
        count3 = count3 + 1
    return minIndex


def printSolution(distFrom, start, end):
    # print("Vertex Distance from source \n")
    counter5 = 0
    while (counter5 < roadSize):
        if printB:
            print(counter5 + 1, '   ', distFrom[counter5])
        dynMemory.append([start, counter5, distFrom[counter5]])
        counter5 = counter5 + 1

    distToEnd = distFrom[end]
    return distToEnd
##################################################


###############################################
# Dynamic Val Check
###############################################
def dynCheck(start, end):
    for val in dynMemory:                               #Go through all prev. paths and check if done before
        if ((val[0] == start and val[1] == end) or (val[1]==start and val[0]==end)):
            return True, val[2]
    return False, 0
##################################################

##################################################
#Update Vehicle Location#
##################################################
def carUpdate(car, end, req):
    travelTime = dijkstras(network, car.end, end)
    car.dropTime = req[0] + travelTime
    car.start = car.end
    car.end = end
#################################################


def main():
    global enbExp
    global enbDyn
    enbExp = False  #Enable/Disable experimental. DO NOT USE WITH MORE THAN 2 CARS
                    #Also specifically designed for the given network. WIll not work properly on other networks

    enbDyn = True   #Enable/Disable dynamic memory KEEP ON FOR EFFICIENT RUN TIMES
    numCars=2       #Define the number of cars

    # print("E=F")
    # for i in range(2,54,4):
    #     calcRun(i)
    # print("E=T")
    # enbExp = True
    # for i in range(2,54,4):
    #     calcRun(i)
    # enbExp = False
    # enbDyn = True
    # print("E=F")
    # for i in range(2, 25):
    #     calcRun(i)
    # print("E=T")
    # enbExp = True
    # for i in range(2, 25):
    #     calcRun(i)
    enbExp = False
    enbDyn = True
    print("Official Solution")
    calcRun(2)
    enbExp = True
    print("\nExperimental:Optimal Nodes")
    print("Not consider the official solution due to volatility of answer but kept in due to the interest in concept")
    calcRun(2)



##################################################
# Scheduling#
##################################################
def calcRun(numCars):
    global network
    botBunch=[36,25,9,42,2,40,21,27,39,12,34,29,48,1,28,46,3,7,45,0,44,4,6,35,37] #List of nodes defined to be in Group A
    #numCars = 2                                        #This value defines the number of cars
    listCars = []                                       #Define dynamic # cars variables
    for i in range(numCars):
        listCars.append(Uber(i))

    totalTime = 0
    #Val to store total wait time
    network = roadInput()
    requests = scheduleImport()

    startT = time.time()                                #Count time to run program
    for req in requests:
        minTime = 2147483647
        for i in range(numCars):                        #Choose car which can arrive fastest
            pickupTime = timeFunc(network, listCars[i], req)
            if pickupTime < minTime:
                minTime = pickupTime
                minCar = i

        travelTime = dijkstras(network, req[1], req[2]) #Update car locations and trip times
        totalTime = totalTime + minTime
        listCars[minCar].dropTime = req[0] + minTime + travelTime
        listCars[minCar].start = req[1]
        listCars[minCar].end = req[2]
        if enbExp==True:                                #Experimental: Optimal Node
            if req[2] in botBunch:                      #If car is travel to a node in Group A
                if minCar==1 and listCars[0].dropTime< req[0]: #Send other car to optimal node in Group B
                    carUpdate(listCars[0],12,req)

                if minCar==0:
                    carUpdate(listCars[1],12,req)

            elif listCars[1].dropTime< req[0]:          #Else if car is traveling node in Group B
                if minCar==1:                           #Send other car to Group A optimal node
                    carUpdate(listCars[0],26,req)

                if minCar==0:
                    carUpdate(listCars[1],26,req)

        #print("Car", minCar, ":", minTime)

    print("\nTotal wait time is: ",totalTime)
    #print(totalTime)
    endT = time.time()
    runtT = endT - startT
    print("Program wait time: ", runtT)
    #print(runtT)


if __name__ == "__main__":
    main()
