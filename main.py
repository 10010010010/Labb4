import numpy as np
from pyscbwrapper import SCB
import matplotlib.pyplot as plt
import PySimpleGUI as GUI


# Bibliotek som innehåller ett API för att hämta data från Statistiska Centralbyrån (SCB):


# Du skall skapa funktionens parameterlista:
def generateGraphFile(xData, yData, observation: str):
    plottingDict = {tuple(xData): yData}
    for i in plottingDict:
        plt.ticklabel_format(useOffset=False, style="plain")
        plt.plot(i, plottingDict[i])
    plt.xlabel("year")
    plt.ylabel(observation)
    plt.savefig("SCB_DATA_" + observation.replace(" ", "_").upper() + ".png")
    plt.close()


def generateGraphData(scb, valueIndex, keyIndex):
    scbData = []
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


# Alternativ 1: Antal invånare i Sverige mellan 2010 och 2021
scb = SCB('en', 'BE', 'BE0101', 'BE0101C', 'BefArealTathetKon')
scb.set_query(observations=["Population"], year=
["2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020",
 "2021"])
xData, yData = generateGraphData(scb, 0, 0)
generateGraphFile(xData, yData, "population")

# Alternativ 3: Antal registrerade personbilar i Sverige 2010-2021
scb = SCB('en', 'TK', 'TK1001', 'TK1001A', 'PersBilarA')
scb.set_query(region=["Sweden"], observations="Passenger cars in use", year=
["2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020",
 "2021"])
xData, yData = generateGraphData(scb, 0, 1)
generateGraphFile(xData, yData, "Passenger car in use")  # här sker anropet till funktionen som du skriver färdigt ovan.


def generateGraphicalInterface():

    fullLayout = [[GUI.Button("next", visible=True,key='-NXT-'), GUI.Button("previous", visible=False, key='-prev-')],
                  [GUI.Image(filename="SCB_DATA_POPULATION.png", size=(640,480), key='-IMG-')], [GUI.Button("close window")]]

    window = GUI.Window("hello world", fullLayout, size=(500, 500), resizable=True)
    while True:
        event, value = window.read()
        if event == '-NXT-':
            window['-IMG-'].update(filename="SCB_DATA_PASSENGER_CAR_IN_USE.png")
            window['-NXT-'].update(visible=False)
            window['-prev-'].update(visible=True)
        elif event == '-prev-':
            window['-IMG-'].update(filename="SCB_DATA_POPULATION.png")
            window['-prev-'].update(visible=False)
            window['-NXT-'].update(visible=True)
        elif event == GUI.WIN_CLOSED or event == "close window":
            print("The window was closed")
            break
    window.close()


generateGraphicalInterface()
