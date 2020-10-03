import os
from os import listdir
from os.path import isfile, join
import pandas as pd

class ExcelDF():
    def __init__(self, files):
        self.files = files
        self.dfList = []
        self.selectedState = ""
        self.selectedCities = []
        self.selectedAddresses= []

    # create data frame from excel files
    def buildDF(self):
        for idx, f in enumerate(self.files):
            df = pd.read_excel(f).assign(excel_file=idx)
            df['State'] = df['State'].str.strip().str.upper()
            df['City'] = df['City'].str.strip().str.upper()
            df['Address1'] = df['Address1'].str.strip().str.upper()

            self.dfList.append(df)

    # only allowed to pass in NY or NJ as state
    def filterByState(self, state):
        self.selectedState = state
        for idx, df in enumerate(self.dfList):
            self.dfList[idx] = df[df['State'] == state]

    # Adds a city to selectedCities list
    def addCityToFilter(self, city):
        if city not in self.selectedCities: self.selectedCities.append(city)

    # Removes a city from selectedCities list
    def removeCityFromFilter(self, city):
        if city in self.selectedCities: self.selectedCities.remove(city)

    # Adds an address to selectedAddresses list
    def addAddressToFilter(self, address):
        # Need to trim and uppercase because user input
        address = address.strip().upper()
        if address not in self.selectedAddresses: self.selectedAddresses.append(address)

    # Removes an address from selectedAddresses list
    def removeAddressFromFilter(self, address):
        address = address.strip().upper()
        if address in self.selectedAddresses: self.selectedAddresses.remove(address)

    # retrieves all cities from dataframe
    def retrieveAllCities(self):
        citySet = set()
        for df in self.dfList:
            citySet.update(df.City.unique())

        return sorted(list(citySet))

    # creates the current frame with all filters applied
    def currentFrame(self):

        # if no state parameter selected or no cities+addresses picked
        if not self.selectedState or (not self.selectedCities and not self.selectedAddresses):
            print("only state selected")
            return self.concatDFs(self.dfList)
        else:

            # state has been selected and either cities and/or addresses filter have been selected
            tmpList = []
            for df in self.dfList:
                # if both City and Address columns have applied filters
                if self.selectedCities and self.selectedAddresses:
                    print("all selected")
                    tmpList.append(df[(df['City'].isin(self.selectedCities)) & (df['Address1'].str.contains('|'.join(self.selectedAddresses)))])

                # if only City column has applied filter
                elif self.selectedCities:
                    print("only cities selected")
                    tmpList.append(df[df['City'].isin(self.selectedCities)])

                # if only Address column has applied filter
                else:
                    print("only address selected")
                    tmpList.append(df[df['Address'].str.contains('|'.join(self.selectedAddresses))])

            return self.concatDFs(tmpList)

    # concat dataframes into singular dataframe
    def concatDFs(self, dfList):
        return pd.concat(dfList)

    # occurs on user submit of changes to save data frame
    # will create a new excel file with all the changes using showCurrentFrame() method
    # will then iterate thru each frame in df, and remove row from excel files
    def saveDF(self):
        print("remove each record from previous excel file and save")
        print("save df as new excel file")



def testFiles():
    # path = './test-files'
    path = './test-files/necessary-files'
    files = [join(path, f) for f in listdir(path) if isfile(join(path, f)) and (not f.startswith('.') and not f.startswith('~'))]
    return files

files = testFiles()
excel_df = ExcelDF(files)
excel_df.buildDF()
excel_df.filterByState('NY')
print(excel_df.retrieveAllCities())

# print(excel_df.currentFrame())
# excel_df.addCityToFilter('BROOKLYN')
# excel_df.addCityToFilter('flushing')
# print(excel_df.currentFrame())
# # excel_df.removeCityFromFilter('torrinton')
# excel_df.addAddressToFilter('13')
# excel_df.addAddressToFilter('14')
# excel_df.addAddressToFilter('15')
# print(excel_df.currentFrame())
