import pandas
import numpy as np
import matplotlib as plt
import moonraker as server
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
def main():
    while True:
        try:
            df = pandas.read_csv('printertimes.csv')
            break
        except:
            print("No data found, making right now!")
            makeDatabase()

    x = df.drop('estimated time', axis = 1)
    y =df['estimated time']
    
    X_train, X_test, y_train, y_test = train_test_split(x,y, test_size=.2, random_state=0)

    regressor = LinearRegression()

    regressor.fit(X_train, y_train)
    
    regressor.fit(X_test, y_test)

    ytest = regressor.predict(X_test)
    print(X_test)
    print(pandas.DataFrame(ytest, columns=['Predicted']))

def makeDatabase(): #this function uses the directoryContents function and gcodeMetadata to find and collect metadata for all gcode files (ie. print time).
    dir_contents = server.directoryContents('http://10.7.1.215', 'gcodes')
    dir_file_amount = len(dir_contents)
    datatypes = ["estimated_time", "layer_height", "object_height", "filament_total"]
    
    estimated_times = []
    layer_heights = []
    object_height = []
    filament_total = []

    data_dict = {
            'estimated time' : estimated_times,
            'layer height' : layer_heights,
            'object height' : object_height,
            'filament used' : filament_total
        }
    
    for file in range(dir_file_amount - 1): #
        name = dir_contents[file]['path']
        metadata = server.gcodeMetadata('http://10.7.1.215', name)
        try:
            if metadata[datatypes[0]]:
                estimated_times.append(metadata[datatypes[0]])
            if metadata[datatypes[1]]:
                layer_heights.append(metadata[datatypes[1]])
            if metadata[datatypes[2]]:
                object_height.append(metadata[datatypes[2]])
            if metadata[datatypes[3]]:
                filament_total.append(metadata[datatypes[3]])
        except:
            print(f"{name} does not work for this.")
    data = pandas.DataFrame(data_dict)
    data.to_csv('printertimes.csv')

    return data







main()

