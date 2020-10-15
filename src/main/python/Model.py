from os import makedirs, path
import xlsxwriter
import pandas as pd
import copy


class ExcelModel:
    def __init__(self, files=None):
        if files:
            self.files = files
        else:
            self.files = []

        self.dfList = []
        self.backups = []
        self.outDFList = []

        self.selectedState = ""
        self.selectedCities = []
        self.selectedInvoice = ""
        self.selectedAddress = ""

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
        self.backups.clear()
        self.outDFList.clear()
        self.selectedState = ""
        self.selectedCities.clear()
        self.selectedInvoice = ""
        self.selectedAddress = ""

        # build df by filtering by state
        for idx, f in enumerate(self.files):
            df = pd.read_excel(f)

            df['file_num'] = idx
            df['row_num'] = df.index
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

        # back up original files
        self.backups = copy.deepcopy(self.dfList)

    # set selectedState to inputted state
    def setState(self, state):
        self.selectedState = state

    # Adds a city to selectedCities list
    def addCity(self, city):
        if city not in self.selectedCities:
            self.selectedCities.append(city)

    # Removes a city from selectedCities list
    def removeCity(self, city):
        if city in self.selectedCities:
            self.selectedCities.remove(city)

    # retrieves all cities from dataframe
    def getAllCities(self):
        citySet = set()
        for df in self.dfList:
            df = df[df['State'] == self.selectedState]
            citySet.update(df.City.unique())
        return sorted(list(citySet))

    # Sets cities list
    def setCities(self, cities):
        self.selectedCities = cities

    def setInvoice(self, invoice):
        invoice = invoice.strip()
        self.selectedInvoice = invoice

    # sets address for filter
    def setAddress(self, address):
        address = address.strip()
        self.selectedAddress = address

    # creates the current frame with all filters applied accordingly
    def currentFrame(self):

        # if state and cities provided
        if self.selectedState and self.selectedCities:
            tmpList = []
            for df in self.dfList:
                tmpList.append(df[(df['State'] == self.selectedState) &
                                  (df['City'].isin(self.selectedCities)) &
                                  (df['Invoice NO'].str.contains(self.selectedInvoice, case=False)) &
                                  (df['Address1'].str.contains(self.selectedAddress, case=False))])

            df = self.concatDFs(tmpList)
            if not df.empty:
                return df

        # no state and city selected or empty dataframe
        return None

    # returns current frame for output DF
    def outputFrame(self):
        df = self.concatDFs(self.outDFList)
        if not df.empty:
            return df
        else:
            return None

    # adds selected ids to output list
    def addToOutputList(self, ids):
        for id in ids:
            fileIndex = int(id.split("_")[0])
            inDF = self.dfList[fileIndex]
            row = inDF.loc[[id]]
            inDF.drop(id, inplace=True)
            outDF = self.concatDFs([self.outDFList[fileIndex], row])
            self.outDFList[fileIndex] = outDF

    # removes selected ids from output list
    def removeFromOutputList(self, ids):
        for id in ids:
            fileIndex = int(id.split("_")[0])
            outDF = self.outDFList[fileIndex]
            row = outDF.loc[[id]]
            outDF.drop(id, inplace=True)
            inDF = self.concatDFs([self.dfList[fileIndex], row])
            self.dfList[fileIndex] = inDF

    # concat dataframes into singular dataframe
    def concatDFs(self, list):
        return pd.concat(list).sort_values(by=['file_num', 'row_num'])

    # occurs on user submit of changes to save data frame
    # writes all changes to new excel file and old input files as well
    def finish(self, outputFile, timestamp):
        try:
            # build backup directory in outputfile location if not there
            backupPath = self.createBackupDirectory(outputFile)

            for i in range(len(self.files)):
                file = self.files[i]
                self.saveDF(file, self.dfList[i])

                # backup old files
                self.saveBackup(backupPath, file, timestamp, self.backups[i])

            # save output df
            self.saveDF(outputFile, self.concatDFs(self.outDFList))

        except xlsxwriter.exceptions.FileCreateError:
            message = ("Error saving Excel File: {}, ".format(file),
                       "it could possibly be open in another process")
            return {"status_code": False, "message": message}

        except KeyError as e:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(e).__name__, e.args)
            # message = "Current data for this instance has changed, please restart the application"
            return {"status_code": False, "message": message}

        except Exception as e:
            print("exception raised")
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(e).__name__, e.args)
            return {"status_code": False, "message": message}

        else:
            return {"status_code": True, "message": outputFile}

    # create backup directory to place files in
    # will reside in same directory as output file
    def createBackupDirectory(self, outputFile):
        backupPath = path.join(path.dirname(
            path.abspath(outputFile)), 'backups')
        if not path.exists(backupPath):
            makedirs(backupPath)

        return backupPath

    def saveBackup(self, backupPath, copyFile, timestamp, df):
        # create file name for backup
        fileSplit = path.basename(copyFile).rsplit(".", 1)
        name = "{}-backup".format(fileSplit[0])[:26]
        fileSplit[0] = name
        backupFileName = ".".join(fileSplit)
        backupFile = path.join(backupPath, backupFileName)

        # Reformat + append timestamp and save
        if 'timestamp' not in df.columns:
            df.loc[df.index[0], 'timestamp'] = timestamp

        # save
        self.saveDF(backupFile, df)

    def saveDF(self, file, df):
        # reformat df
        df = self.reformatDF(df)

        # create excel writer and write df to excel file
        writer = pd.ExcelWriter(file, engine='xlsxwriter',
                                datetime_format='mm/dd/YYYY')
        sheet_name = path.basename(file)
        df.to_excel(writer, sheet_name=sheet_name, index=False)

        # auto adjust excel columns
        wb = writer.book
        ws = writer.sheets[sheet_name]
        self.reformatExcel(wb, ws, df)

        writer.save()

    def reformatDF(self, df):
        tmp = df.drop(columns=['file_num', 'row_num'], inplace=False)
        tmp.reset_index(drop=True, inplace=True)

        tmp['Require Date'] = pd.to_datetime(tmp['Require Date'])
        tmp['Sales Date'] = pd.to_datetime(tmp['Sales Date'])

        return tmp

    def reformatExcel(self, wb, ws, df):
        for idx, col in enumerate(df):
            series = df[col]
            max_len = max((
                series.astype(str).map(len).max(),  # len of largest item
                len(str(series.name))  # len of column name/header
            )) + 1  # adding a little extra space
            ws.set_column(idx, idx, max_len)  # set column width
        wb.set_size(16095, 9660)


# def testFiles():
#     # path = './test-files'
#     # path = './test-files/necessary-files'
#     p = path.abspath('./excel-files')
#     files = [path.join(p, f) for f in listdir(p) if path.isfile(path.join(p, f)) and (
#         not f.startswith('.') and not f.startswith('~'))]
#     return files
#
# files = testFiles()
# em = ExcelModel(files)
# em.buildDF()
# em.reformatDF(em.backups[0])
#
# print(em.backups[0])
# em.finish(
#     '/Users/howardwang/Desktop/excel-application/excel-files/dsca.xls')
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
