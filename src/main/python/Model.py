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
        self.outDFList = [];

        self.selectedState = None
        self.selectedCities = []
        self.selectedAddress = None

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

    # create data frame from excel files
    # Never rebuildDF in same instance
    def buildDF(self):

        self.dfList.clear()
        self.selectedState = None
        self.selectedCities.clear()
        self.selectedAddress = None
        # build df by filtering by state
        for idx, f in enumerate(self.files):
            # df = pd.read_excel(f).assign(id=idx)
            df = pd.read_excel(f)

            df['file_num'] = idx
            df['row_num'] = df.index

            # assign id -> (file_num)_(row_num)
            # df['id'] = str(idx) + "_" + df.index.astype(str)
            df['id'] = str(idx) + "_" + df.index.astype(str)
            df.set_index(['id'], inplace=True)

            # reformatting
            df['Require Date'] = df['Require Date'].dt.strftime('%m/%d/%Y')
            df['Sales Date'] = df['Sales Date'].dt.strftime('%m/%d/%Y')
            df['State'] = df['State'].str.strip().str.upper()
            df['City'] = df['City'].str.strip().str.upper()
            df['Address1'] = df['Address1'].str.strip().str.upper()

            self.dfList.append(df)
            self.outDFList.append(pd.DataFrame())

    # set selectedState to inputted state
    def setState(self, state):
        self.selectedState = state

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

    # (DEPRECATED)
    # only allowed to pass in NY or NJ as state
    # def filterByState(self, state):
    #     self.selectedState = state
    #     for idx, df in enumerate(self.dfList):
    #         self.dfList[idx] = df[df['State'] == state]

    # (DEPRECATED) SELECTEDADDRESSES(LIST) IS NOW A SELECTEDADDRESS(STR)
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

    # creates the current frame with all filters applied accordingly
    def currentFrame(self):

        # if state and cities provided
        if self.selectedState and self.selectedCities:
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

            return self.concatDFs(tmpList)

        # no state and city selected
        else:
            # print("no frame possible -> no state or no city")
            return None

    # adds selected ids to output list
    def addToOutputList(self, ids):
        ids.sort(reverse=True)
        for id in ids:
            # print("ADD:", id)
            fileIndex = int(id.split("_")[0])
            inDF = self.dfList[fileIndex]
            row = inDF.loc[[id]]
            inDF.drop(id, inplace=True)
            outDF = pd.concat([self.outDFList[fileIndex], row]).sort_values(by=['file_num', 'row_num'])
            self.outDFList[fileIndex] = outDF

    # removes selected ids from output list
    def removeFromOutputList(self, ids):
        ids.sort(reverse=True)
        for id in ids:
            # print("REMOVE:", id)
            fileIndex = int(id.split("_")[0])
            outDF = self.outDFList[fileIndex]
            row = outDF.loc[[id]]
            outDF.drop(id, inplace=True)
            inDF = self.concatDFs([self.dfList[fileIndex], row])
            self.dfList[fileIndex] = inDF

    def outputFrame(self):
        return self.concatDFs(self.outDFList)

    # concat dataframes into singular dataframe
    def concatDFs(self, dfList):
        return pd.concat(dfList).sort_values(by=['file_num', 'row_num'])

    # occurs on user submit of changes to save data frame
    # will create a new excel file with all the changes using showCurrentFrame() method
    # will then iterate thru each frame in df, and remove row from excel files
    # should figure out handling for concatenating empty DF Lists
    def finish(self, outputFile):
        self.concatDFs(self.outDFList)
        for i in range(len(self.files)):
            file = self.files[i]
            inDF = self.reformatDF(self.dfList[i])
            self.saveDF(file, inDF)

        outDF = self.reformatDF(self.concatDFs(self.outDFList))
        self.saveDF(outputFile, outDF)

    # CANNOT USE '/' IN FILE NAME
    def saveDF(self, file, df):
        writer = pd.ExcelWriter(file, engine='xlsxwriter', datetime_format='mm/dd/YYYY')
        sheet_name = file.rsplit("/", 1)[1]
        df.to_excel(writer, sheet_name=sheet_name, index=False)

        #auto adjust excel columns
        worksheet = writer.sheets[sheet_name]
        for idx, col in enumerate(df):
            series = df[col]
            max_len = max((
                series.astype(str).map(len).max(),  # len of largest item
                len(str(series.name))  # len of column name/header
            )) + 1  # adding a little extra space
            worksheet.set_column(idx, idx, max_len)  # set column width

        writer.save()

    def reformatDF(self, df):
        df.reset_index(drop=True, inplace=True)
        df.drop(columns=['file_num', 'row_num'], inplace=True)
        df['Require Date'] = pd.to_datetime(df['Require Date'])
        df['Sales Date'] = pd.to_datetime(df['Sales Date'])
        return df



def testFiles():
    # path = './test-files'
    # path = './test-files/necessary-files'
    path = './excel-files'
    files = [join(path, f) for f in listdir(path) if isfile(join(path, f)) and (not f.startswith('.') and not f.startswith('~'))]
    return files


# files = testFiles()
# print("generating frames...")
# excel_df = ExcelModel(files)
# excel_df.buildDF()
# print("done!")
# excel_df.setState('NY')
# excel_df.addCityToFilter('BROOKLYN')
# excel_df.addToOutputList(['0_5', '0_6'])
# print(excel_df.currentFrame())
# print(excel_df.outputFrame())
# outputPath = '/Users/howardwang/Desktop/excel-application/excel-files/saves/output1.xlsx'
# excel_df.finish(outputPath)
