import random

def lightProperties(routeLength, numOfTrafficLights):
    spaceBetweenLights = routeLength / numOfTrafficLights #evenly spaces out the length for each light
    lightArrayOfDictionaries = [] 
    for x in range(numOfTrafficLights): #creates my dictionary with each light :)
        counter = x+1
        currentPositionMiles = counter * spaceBetweenLights
        currentCycleTimeSec = random.randint(50,90)
        currentRedDurationSec = random.randint(20,60)
        currentOffsetSec = random.randint(0,currentCycleTimeSec)

        light = {"id": x + 1, "positionMiles": currentPositionMiles, "cycleTimeInSeconds": currentCycleTimeSec, "redLightDurationInSeconds": currentRedDurationSec, "offsetInSeconds": currentOffsetSec} #storing the data as a dictionary of dictionaries so that I can have each light have many properties
        lightArrayOfDictionaries.append(light)

    return lightArrayOfDictionaries
    


def simulateCarMovement(routeLengthMiles, speedingDriver, steadyDriver, lights):
    steadyRedCount = 0
    steadyGreenCount = 0
    speederRedCount = 0
    speederGreenCount = 0

    for currentLight in lights: #loops through the array of lights
        currentLightPosition = currentLight["positionMiles"]
        currentLightCycleTime = currentLight["cycleTimeInSeconds"]
        currentLightOffset = currentLight["offsetInSeconds"]
        currentRedLightDuration = currentLight["redLightDurationInSeconds"]

        steadyDriverDistanceToNextLight = currentLightPosition - steadyDriver["positionMiles"] #tracking position per light
        steadyDriverTravelTime = (steadyDriverDistanceToNextLight / steadyDriver["speedMph"]) * 3600 #tracking time per light
        steadyDriver["timeElapsedSec"] += steadyDriverTravelTime
        steadyDriver["positionMiles"] = currentLightPosition

        speederDistanceToNextLight = currentLightPosition - speedingDriver["positionMiles"] #tracking position per light
        speederTravelTime = (speederDistanceToNextLight / speedingDriver["speedMph"]) * 3600 #tracking time per light
        speedingDriver["timeElapsedSec"] += speederTravelTime
        speedingDriver["positionMiles"] = currentLightPosition


        steadyDriverArrivalTime = steadyDriver["timeElapsedSec"]+currentLightOffset #Gives me the exact time of when in the light's cycle the driver arrives
        speedingDriverArrivalTime = speedingDriver["timeElapsedSec"]+currentLightOffset

        steadyLightTime = steadyDriverArrivalTime%currentLightCycleTime 
        if(steadyLightTime<currentRedLightDuration):
            #print("Steady driver hits red light")
            steadyWaitTime = currentRedLightDuration - steadyLightTime
            steadyDriver["timeElapsedSec"] += steadyWaitTime
            steadyRedCount+=1
        else:
            #print("Steady driver hits green light")
            steadyGreenCount+=1
            #print("Steady driver position: ", steadyDriver["positionMiles"], "Steady driver travel time: ", steadyDriver["timeElapsedSec"])

        
        speedingLightTime = speedingDriverArrivalTime%currentLightCycleTime
        if(speedingLightTime<currentRedLightDuration):
            #print("Speeder hits red light")
            speederWaitTime = currentRedLightDuration - speedingLightTime
            speedingDriver["timeElapsedSec"] += speederWaitTime
            speederRedCount+=1
        else:
            #print("Speeder hits green light")
            speederGreenCount+=1
        
        #print("Speeder position: ", speedingDriver["positionMiles"], "Speeder travel time: ", speedingDriver["timeElapsedSec"])
    
    print("\n--- Final Results ---")
    print(f"Steady Driver Total Time: {round(steadyDriver['timeElapsedSec'], 2)} seconds")
    print(f"Speeder Total Time: {round(speedingDriver['timeElapsedSec'], 2)} seconds")
    print(f"Time difference: {round(abs(steadyDriver['timeElapsedSec'] - speedingDriver['timeElapsedSec']), 2)} seconds")
    print(f"Steady Driver hit {steadyRedCount} red lights and {steadyGreenCount} green lights.")
    print(f"Speeder hit {speederRedCount} red lights and {speederGreenCount} green lights.")


 

def simulateDrive(routeLengthMiles, numOfLights): #main function
    print(f"Simulating a drive for {routeLengthMiles} miles...")
    speedingDriver={"id":"speedingDriver","speedMph":55,"positionMiles":0,"timeElapsedSec":0} #speeder
    steadyDriver={"id":"steadyDriver","speedMph":45,"positionMiles":0,"timeElapsedSec":0} #steady
    lights = lightProperties(routeLengthMiles,numOfLights) #calls the lightProperties function and returns the array of dictionaries with the properties for each light
    #print(lights) #just to output the properties in console
    return routeLengthMiles, speedingDriver, steadyDriver, lights


if __name__ == "__main__": #calls main 
    #totalTimeDifference=0
    #for x in range(10000):
    routeLengthMiles, speedingDriver, steadyDriver, lights = simulateDrive(10,20)
    simulateCarMovement(routeLengthMiles,speedingDriver,steadyDriver,lights)



