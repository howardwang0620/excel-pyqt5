import os
from os import listdir
from os.path import isfile, join
import pandas as pd

class ExcelModel:
    def __init__(self, files=None):
        if files:
            self.files = files
        else:
            self.files = []

        self.dfList = []
        # self.saved = dataframe;

        self.selectedState = None
        self.selectedCities = []
        self.selectedAddress = None
        self.outputList = []

    # add file to self.files, returns true if added
    def addFile(self, file):
        if file not in self.files:
            self.files.append(file)
            return True
        else:
            return False

    # remove file from self.files, returns true if removed
    def removeFile(self, file):
        if file in self.files:
            self.files.remove(file)
            return True
        else:
            return False

    # getter for files
    def getFiles(self):
        return self.files

    def setState(self, state):
        self.selectedState = state

    # create data frame from excel files
    # NEVER REBUILD DF AFTER ITS BUILT
    def buildDF(self):

        self.dfList.clear()
        self.selectedState = None
        self.selectedCities.clear()
        self.selectedAddress = None
        # build df by filtering by state
        for idx, f in enumerate(self.files):
            # df = pd.read_excel(f).assign(id=idx)
            df = pd.read_excel(f)

            # assign id -> (index of file)_(row_num)
            df['id'] = str(idx) + "_" + df.index.astype(str)

            # filter on state
            df['State'] = df['State'].str.strip().str.upper()
            # df = df[df['State'] == self.selectedState]

            df['City'] = df['City'].str.strip().str.upper()
            df['Address1'] = df['Address1'].str.strip().str.upper()

            self.dfList.append(df)

    # (DEPRECATED) only allowed to pass in NY or NJ as state
    # def filterByState(self, state):
    #     self.selectedState = state
    #     for idx, df in enumerate(self.dfList):
    #         self.dfList[idx] = df[df['State'] == state]

    # Adds a city to selectedCities list
    def addCityToFilter(self, city):
        if city not in self.selectedCities:
            self.selectedCities.append(city)

    # Removes a city from selectedCities list
    def removeCityFromFilter(self, city):
        if city in self.selectedCities:
            self.selectedCities.remove(city)

    def setAddress(self, address):
        address = address.strip()
        self.selectedAddress = address

    # DEPRECATED, SELECTEDADDRESSES(LIST) IS NOW A SELECTEDADDRESS(STR)
    # # Adds an address to selectedAddresses list
    # def addAddressToFilter(self, address):
    #     # Need to trim and uppercase because user input
    #     address = address.strip().upper()
    #     if address not in self.selectedAddresses:
    #         self.selectedAddresses.append(address)
    #
    # # Removes an address from selectedAddresses list
    # def removeAddressFromFilter(self, address):
    #     address = address.strip().upper()
    #     if address in self.selectedAddresses:
    #         self.selectedAddresses.remove(address)

    # retrieves all cities from dataframe
    def getAllCities(self):
        citySet = set()
        for df in self.dfList:
            df = df[df['State'] == self.selectedState]
            citySet.update(df.City.unique())

        return sorted(list(citySet))

    # creates the current frame with all filters applied
    def currentFrame(self):
        # if no state parameter selected or no cities+addresses picked
        if not self.selectedState or not self.selectedCities:
            # print("no frame possible -> no state or no city")
            return None
        else:

            # this means there is a state and city
            tmpList = []
            for df in self.dfList:
                # if both City and Address columns have applied filters
                if self.selectedAddress:
                    # print("all selected")
                    tmpList.append(df[(df['State'] == self.selectedState) & \
                                      (df['City'].isin(self.selectedCities)) & \
                                      (df['Address1'].str.contains(self.selectedAddress, case=False))])

                # if only City column has applied filter
                elif self.selectedCities:
                    # print("only cities selected")
                    tmpList.append(df[(df['State'] == self.selectedState) & \
                                   (df['City'].isin(self.selectedCities))])

                # # if only Address column has applied filter
                # elif self.selectedAddresses:
                #     print("only address selected")
                #     tmpList.append(df[(df['State'] == self.selectedState) & \
                #                    (df['Address'].str.contains('|'.join(self.selectedAddresses)))])

            return self.concatDFs(tmpList)

    # adds selected rows to output list
    def addToOutputList(self, df):
        self.outputList.append(df)

    def removeFromOutputList(self, idx):
        #remove from outputlist of id, should be index
        print("remove from output list")

    # concat dataframes into singular dataframe
    def concatDFs(self, dfList):
        return pd.concat(dfList)

    # occurs on user submit of changes to save data frame
    # will create a new excel file with all the changes using showCurrentFrame() method
    # will then iterate thru each frame in df, and remove row from excel files
    def saveDF(self):
        self.concatDFs(self.outputList)
        print("remove each record from previous excel file and save")
        print("save df as new excel file")



def testFiles():
    # path = './test-files'
    # path = './test-files/necessary-files'
    path = './excel-files'
    files = [join(path, f) for f in listdir(path) if isfile(join(path, f)) and (not f.startswith('.') and not f.startswith('~'))]
    return files


# files = testFiles()
# print("generating frames...")
# excel_df = ExcelModel()
# excel_df.setFiles(files)
# excel_df.buildDF()
# print("done!")
#
# excel_df.filterByState('NY')
#
# print(excel_df.retrieveAllCities())
#
#
# print(excel_df.currentFrame())
# excel_df.addCityToFilter('BROOKLYN')
# excel_df.addCityToFilter('flushing')
# print(excel_df.currentFrame())
# # excel_df.removeCityFromFilter('torrinton')
# excel_df.addAddressToFilter('13')
# excel_df.addAddressToFilter('14')
# excel_df.addAddressToFilter('15')
# print(excel_df.currentFrame())
