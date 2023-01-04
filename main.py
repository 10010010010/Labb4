import numpy as np
from pyscbwrapper import SCB
import matplotlib.pyplot as plt
import PySimpleGUI as GUI


# Bibliotek som innehåller ett API för att hämta data från Statistiska Centralbyrån (SCB):


# Du skall skapa funktionens parameterlista:
def generateGraphFile(xData, yData, observation):  #takes in x and y data obeseravtion = What the data stands for
    plt.ticklabel_format(useOffset=False, style="scientific") #For the program to show the whole y-axis
    plt.plot(xData, yData)
    plt.xlabel("year")
    plt.ylabel(observation)
    plt.savefig("SCB_DATA_" + observation.replace(" ", "_").upper() + ".png") # formating for the file name and saves the file as a png
    plt.close() #closes the window


def generateGraphData(scb, valueIndex, keyIndex):  #Scrapar scb hemsidan
    scbData = scb.get_data()
    # Filter out metadata:
    scbFetchData = scbData['data']
    xData = []
    yData = []
    for i in range(len(scbFetchData)):
        yData.append(float(scbFetchData[i]['values'][valueIndex]))
        xData.append(scbFetchData[i]['key'][keyIndex])
    print(xData, yData)
    return xData, yData


#  Antal invånare i Sverige mellan 2010 och 2021
scb = SCB('en', 'BE', 'BE0101', 'BE0101C', 'BefArealTathetKon')
scb.set_query(observations=["Population"], year=
["2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020",
 "2021"])
xData, yData = generateGraphData(scb, 0, 0)
generateGraphFile(xData, yData, "population") #generates graph 1

#  Antal registrerade personbilar i Sverige 2010-2021
scb = SCB('en', 'TK', 'TK1001', 'TK1001A', 'PersBilarA')
scb.set_query(region=["Sweden"], observations="Passenger cars in use", year=
["2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020",
 "2021"])
xData, yData = generateGraphData(scb, 0, 1)
generateGraphFile(xData, yData, "Passenger car in use") #Generates graph 2


def generateGraphicalInterface():

    fullLayout = [[GUI.Button("next", visible=True,key='-NXT-'), GUI.Button("previous", visible=False, key='-prev-')],  #Creats a deafualt layout for the GUI
                  [GUI.Image(filename="SCB_DATA_POPULATION.png", key='-IMG-')], [GUI.Button("close window")]] #Consists of two bottons and a image element

    window = GUI.Window("hello world", fullLayout, size=(500, 500), resizable=True,background_color="Green") #Creats the window
    while True:  #_____event loop________
        event, value = window.read() #creats two vital variables, event and value and maps them to the windows event and value
        if event == '-NXT-':  # if event == "Next"; change image and visability of buttons
            window['-IMG-'].update(filename="SCB_DATA_PASSENGER_CAR_IN_USE.png")
            window['-NXT-'].update(visible=False)  #previously true
            window['-prev-'].update(visible=True)  #previously false
        elif event == '-prev-':
            window['-IMG-'].update(filename="SCB_DATA_POPULATION.png") #if event == prevoius; change image, and switch visibliity of the buttons
            window['-prev-'].update(visible=False)
            window['-NXT-'].update(visible=True)
        elif event == GUI.WIN_CLOSED or event == "close window":  #if event == close window or the window if closed, exit event loop and window closes
            print("The window was closed")
            break
    window.close()


generateGraphicalInterface() # generates the GUI
