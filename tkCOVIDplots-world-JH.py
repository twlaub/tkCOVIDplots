
import tkinter as tk
import pandas as pd
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

#defaultCountries = ( "New Mexico", "Texas" )   # default desired countries
defaultAvgOpts = ( False, True, False )     # default daily averages
defaultCDD = False                          # default cases, deaths, deathrates
plotWidth = 8.0                             # default plot width
plotHeight = 6.0                            # default plot height
averageColor=[ 'red', 'magenta', 'orange' ] # default daily average plot colors
cddColors=[ 'green', 'red', 'orange' ]      # default daily average plot colors

############################################################
# Plots cumulative cases, deaths, and deathrates
def cddPlots( iFig, x, ys, colors, labels, linlog ):
    plt.figure( num=iFig, figsize=(plotWidth, plotHeight) )
    plt.xticks(rotation=45)
    if( linlog == 'linear' ): plt.ylim(0,max(ys[0])*1.05)
    plt.grid()
    for thisY,thisColor,thisLabel in zip( ys,colors,labels ):
        plt.plot( x, thisY, color=thisColor, label=thisLabel )
    plt.legend(loc="upper left")
    plt.yscale( linlog )
    plt.tight_layout()

############################################################
# Plots new cases and deaths along with daily moving averages
def dailyPlots( iFig, x, y, averageCheck, plotLabel, negCheck ):
    plt.figure(num=iFig,figsize=(plotWidth, plotHeight))

    # Daily bar chart
    plt.ylabel( plotLabel )
    plt.xticks(rotation=45)
    plt.bar( x, y, label='daily' )

    # Get 5,7,9-day moving averages
    for iDay in range(3):
        if ( averageCheck[iDay].get() ):
            dayAverage = dayAveraging( (2*iDay+5), y )
            labelText = str((2*iDay+5))+"-day"
            plt.plot( x, dayAverage, averageColor[iDay], label=labelText )
    plt.legend(loc="upper left")
    plt.grid(axis='y')
    plt.tight_layout()
    if ( negCheck.get() ): plt.ylim(bottom=0)

############################################################
def dayAveraging( mynDays, myList ):
    halfDays = mynDays//2  # integer division
    averagedDayList=[]
    # Handle the beginning of the list where there is not a full nDays data to average
    for i in range( halfDays ):
        averagedDayList.append( float(sum( myList[0:(halfDays+1+i)] ))/float(halfDays+1+i) )
    # Handle the middle of the list were a full nDays worth of datat is available to average
    for i in range( halfDays,len(myList)-halfDays ):
        averagedDayList.append( float(sum( myList[i-halfDays:i+halfDays+1] ))/float(mynDays) )
    # Handle the end of the list where there is not a full nDays data to average
    for i in range( halfDays,0,-1 ):
        averagedDayList.append( float(sum( myList[(len(myList)-halfDays-i):len(myList)] ))/float(i+halfDays) )
    return averagedDayList


############################################################
#  Code for what the doPlots button does
############################################################
def doPlots( myCasesData, myDeathsData, myCountries, myCountriesCheck, mycddCheck, myLinearCheck, myLogCheck, myCasesCheck, myDeathsCheck, myAverageCheck, myWorldCheck ):
    # dummy negcheck
    myNegCheck = tk.BooleanVar()
    myNegCheck.set(True)

    # Get desired countries
    finalDesiredCountries = []
    for iCountry in range( len(myCountriesCheck) ):
        if ( myCountriesCheck[iCountry].get() ): finalDesiredCountries.append( myCountries[iCountry] )

    all_countries_cases=[]
    all_countries_deaths=[]
    all_countries_deathrates=[]
    all_countries_length=[]
    all_dates=[]
    # Extract data for all countries
    maxLength = 0
    maxIndex = 0
    index = 0
    # Extract data for all countries
    maxLength = 0
    for iCountry in range(len(myCountries)):
        country_JHDeaths_df = myDeathsData.loc[myDeathsData['Country/Region'] == myCountries[iCountry] ]
        country_JHCases_df  = myCasesData.loc[myCasesData['Country/Region'] == myCountries[iCountry] ]
        country_dates = list( country_JHDeaths_df)[4:] # if using cases start at 11
        country_cases = list( country_JHCases_df[country_dates].sum(axis=0) )
        country_deaths = list( country_JHDeaths_df[country_dates].sum(axis=0) )
        country_deathrates=[0.]*len(country_cases)
        for i in range(len(country_cases)):
            country_deathrates[i] = 0.
            if ( country_cases[i] != 0 ): country_deathrates[i] = float(country_deaths[i])/float(country_cases[i])*100.
        all_countries_length.append( len(country_dates) )
        all_countries_cases.append( country_cases )
        all_countries_deaths.append( country_deaths )
        all_countries_deathrates.append( country_deathrates )
    all_dates = country_dates

    # Now convert string dates to python date objects using numpy
    # This will allow nice formatting of the date axis
    all_dates = mdates.num2date( mdates.datestr2num(all_dates) )

    iFig = 0
    for country in finalDesiredCountries:
        for iCountry in range(len(myCountries)):
            if ( country == myCountries[iCountry] ):
#                sys.stdout.write( "\nCountry: {:s}\n".format(country) )
                trimmed_dates=[]
                trimmed_cases=[]
                trimmed_deaths=[]
                trimmed_deathrate=[]
                for date,cases,deaths,deathrate in zip(all_dates,all_countries_cases[iCountry],all_countries_deaths[iCountry],all_countries_deathrates[iCountry]):
                    if ( cases == 0 ): continue
                    trimmed_dates.append(date)
                    trimmed_cases.append(cases)
                    trimmed_deaths.append(deaths)
                    trimmed_deathrate.append(deathrate)
#                print( "\nPlotting",country,"data" )
                # Set up the graph
                caseLabel=country+' confirmed, number'
                deathLabel=country+' deaths, number'
                rateLabel=country+' deathrate, %'
                # Linear
                if ( mycddCheck.get() ):
                    labels = [ caseLabel, deathLabel, rateLabel ]
                    # Linear
                    if ( myLinearCheck.get() ):
                        cddPlots( iFig, trimmed_dates, [ trimmed_cases, trimmed_deaths, trimmed_deathrate ], cddColors, labels, 'linear' )
                        iFig += 1
                    # Semilog
                    if ( myLogCheck.get() ):
                        cddPlots( iFig, trimmed_dates, [ trimmed_cases, trimmed_deaths, trimmed_deathrate ], cddColors, labels, 'log' )
                        iFig += 1
                
                # Country new cases chart
                if ( myCasesCheck.get() ):
                    new_cases = [trimmed_cases[0]]
                    for cases1,cases2 in zip( trimmed_cases[0:-1], trimmed_cases[1:] ):
                        new_cases.append( cases2 - cases1 )
                    caseLabel=country+' New Cases'
                    dailyPlots( iFig, trimmed_dates, new_cases, myAverageCheck, caseLabel, myNegCheck )
                    iFig += 1

                # Country new deaths chart
                if ( myDeathsCheck.get() ):
                    new_deaths = [trimmed_deaths[0]]
                    for deaths1,deaths2 in zip( trimmed_deaths[:-1], trimmed_deaths[1:] ):
                        new_deaths.append( deaths2 - deaths1 )
                    deathLabel=country+' New Deaths'
                    dailyPlots( iFig, trimmed_dates, new_deaths, myAverageCheck, deathLabel, myNegCheck )
                    iFig += 1

                # Break iCountry loop
                break

    if ( myWorldCheck.get() ):
#       Sum for world total (less US)
        world_cases = [0.]*len(all_dates)
        world_deaths = [0.]*len(all_dates)
        world_deathrates = [0.]*len(all_dates)
        for iDate in range( len(all_dates) ):
            for iCountry in range( len(myCountries) ):
                world_cases[iDate] += all_countries_cases[iCountry][iDate]
                world_deaths[iDate] += all_countries_deaths[iCountry][iDate]
            if ( world_cases[iDate] != 0 ): world_deathrates[iDate] = float(world_deaths[iDate])/float(world_cases[iDate])*100.
#        for iDate in range( len(all_dates) ):
#            world_cases[iDate] = sum( all_countries_cases[0:len(myCountries)][iDate] )
#            world_deaths[iDate] = sum( all_countries_deaths[0:len(myCountries)][iDate] )
#            if ( world_cases[iDate] != 0 ): world_deathrates[iDate] = float(world_deaths[iDate])/float(world_cases[iDate])*100.

        if ( mycddCheck.get() ):
            caseLabel='World w/o USA confirmed, number'
            deathLabel='World w/o USA deaths, number'
            rateLabel='World w/o USA deathrate, %'
            labels = [ caseLabel, deathLabel, rateLabel ]
            # Linear
            if ( myLinearCheck.get() ):
                cddPlots( iFig, all_dates, [ world_cases, world_deaths, world_deathrates ], cddColors, labels, 'linear' )
                iFig += 1
            # Semilog
            if ( myLogCheck.get() ):
                cddPlots( iFig, all_dates, [ world_cases, world_deaths, world_deathrates ], cddColors, labels, 'log' )
                iFig += 1

            # New cases chart
            if ( myCasesCheck.get() ):
                new_cases = [world_cases[0]]
                for cases1,cases2 in zip( world_cases[0:-1], world_cases[1:] ):
                    new_cases.append( cases2 - cases1 )
                caseLabel='World w/o USA New Cases'
                dailyPlots( iFig, all_dates, new_cases, myAverageCheck, caseLabel, myNegCheck )
                iFig += 1
                
            # New deaths chart
            if ( myDeathsCheck.get() ):
                new_deaths = [world_deaths[0]]
                for deaths1,deaths2 in zip( world_deaths[:-1], world_deaths[1:] ):
                    new_deaths.append( deaths2 - deaths1 )
                deathLabel='World w/o USA New Deaths'
                dailyPlots( iFig, all_dates, new_deaths, myAverageCheck, deathLabel, myNegCheck )
                iFig += 1

    plt.show()

    return

############################################################
# Gets data every time it is called. The GUI depends on the countries listed
# in the data the first time the data is retrieved. Subsequent retrievals will not
# change the GUI. If countries are added to the data between data retrievals the results
# of the plots may be mislabeled.
def getData(dataURL,dataFile):
    import pandas as pd
    import wget
    # Delete data file is it exists
    if os.path.exists(dataFile):
        os.remove(dataFile)
    wget.download( dataURL+dataFile )
    return pd.read_csv( dataFile )

############################################################
############################################################
#  Main program section
############################################################
############################################################

# Silence warning about leaving too many plots open
plt.rcParams.update({'figure.max_open_warning': 0})

# Create the main window
mybg="light blue"
mainWindow = tk.Tk()
mainWindow.configure( bg=mybg )

# Set data files URL and file names
casesDataFile  = 'time_series_covid19_confirmed_global.csv'
deathsDataFile = 'time_series_covid19_deaths_global.csv'
dataURL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/'

# Rename the mainWindow (title)
mainWindow.title( "COVID-19 Data Plotter: Data Source is "+dataURL )

# Get pixels per point
# Never figured out how to use this info to size labels
#pixelsPerPoint = mainWindow.winfo_fpixels( '1p' )
#print( "pixelsPerPoint:",pixelsPerPoint )
#pointsPerChar=12
#pixelsPerChar = pointsPerChar*pixelsPerPoint
#print( "pixelsPerChar:",pixelsPerChar )
maxLabelLengh = len("Cases, Deaths, DeathRates:")

# loading data right from the sources:
JHDeaths_df = getData( dataURL,deathsDataFile )
JHCases_df = getData( dataURL,casesDataFile )

# Create the labels that name the data source
nRows = 0  # Initialize GUI grid row counter

# Spacer below title bar
tk.Label( mainWindow, text="", bg=mybg ).grid( row=nRows, column=0 )
nRows += 1

#Get the list of countries in the 'location' column
Countries = list( JHCases_df['Country/Region'].unique() )
Countries.sort()
#Countries = tuple( Countries )
maxCountryLength = 0

# Find max length label (if a country is longer than max given above)
for country in Countries:
   if ( len(country) > maxCountryLength ): maxCountryLength = len(country)
if ( maxLabelLengh > maxCountryLength ): maxCountryLength = maxLabelLengh
# Create Country labels in nColsCountries columns
#nColsCountries = 5
nColsCountries = 8
nCountries = len(Countries)
if ( nCountries%nColsCountries == 0 ):
    nRowsCountries = nCountries//nColsCountries
else:
    nRowsCountries = nCountries//nColsCountries + 1

# Add Country checkboxes
countriesCheck = [None]*nCountries
countriesCheckValue = [None]*nCountries
#points2pixels=0.08
#countryLabelWidth = int( maxCountryLength*pointsPerChar*points2pixels)
countryLabelWidth = int( maxCountryLength*0.9 )
#print( "countryLabelWidth:",countryLabelWidth )
#countryLabelWidth = int( maxCountryLength*pixelsPerChar)
#print( "countryLabelWidth:",countryLabelWidth )
pointsPerChar=12
myFont=('Ariel',pointsPerChar)
for iStart in range(0,nCountries,nColsCountries):
#    print( "nRows:",nRows )
#    print( "iStart:",iStart )
    for iCol in range(nColsCountries):
        iCountry = iStart+iCol
        if ( iCountry >= nCountries ): break
        countriesCheckValue[iCountry] = tk.BooleanVar()
        countriesCheckValue[iCountry].set(False)
        countriesCheck[iCountry] = tk.Checkbutton( mainWindow, var=countriesCheckValue[iCountry], bg=mybg )
        countriesCheck[iCountry].grid( row=nRows, column=(2*iCol) )
        temp = tk.Label( mainWindow, text=Countries[iCountry], font=myFont, fg="black", bg=mybg, width=countryLabelWidth, anchor="w" )
        temp.grid( row=nRows, column=(2*(iCol+1)-1) )
    tk.Label( mainWindow, text="   ", fg=mybg, bg=mybg ).grid( row=nRows, column=2*nColsCountries ) # padding right side
    nRows += 1
nRows += 1

# Add World sum checkbox
worldWithoutUSACheckValue = tk.BooleanVar()
#worldWithoutUSACheckValue.set(False)
worldWithoutUSACheckValue.set(True)
worldWithoutUSACheck = tk.Checkbutton( mainWindow, var=worldWithoutUSACheckValue, bg=mybg ).grid( row=nRows, column=0 )
plotLabel = tk.Label( mainWindow, text="World Without USA", font=myFont, fg="black", bg=mybg, width=countryLabelWidth, anchor="w" )
plotLabel.grid( row=nRows, column=1 )
nRows += 1

# Add Plotting options
tk.Label( mainWindow, text="", bg=mybg ).grid( row=nRows, column=0 )
nRows += 1
plotLabel = tk.Label( mainWindow, text="Plotting options:", font=myFont, fg="black", bg=mybg, width=countryLabelWidth, anchor="w" )
plotLabel.grid( row=nRows, column=1 )
nRows += 1
tk.Label( mainWindow, text="", bg=mybg ).grid( row=nRows, column=0 )
nRows += 1

# Cases, Deaths, and Deathrate scale options
cddCheckValue = tk.BooleanVar()
#cddCheckValue.set(True)
cddCheckValue.set( defaultCDD )
cddCheck = tk.Checkbutton( mainWindow, var=cddCheckValue, bg=mybg ).grid( row=nRows, column=0 )
plotLabel = tk.Label( mainWindow, text="Cases, Deaths, DeathRates:", font=myFont, fg="black", bg=mybg, width=countryLabelWidth, anchor="w" )
plotLabel.grid( row=nRows, column=1 )
linearCheckValue = tk.BooleanVar()
linearCheckValue.set(True)
linearCheck = tk.Checkbutton( mainWindow, var=linearCheckValue, bg=mybg ).grid( row=nRows, column=2 )
linearLabel = tk.Label( mainWindow, text="Linear scale", font=myFont, fg="black", bg=mybg, width=countryLabelWidth, anchor="w" )
linearLabel.grid( row=nRows, column=3 )
logCheckValue = tk.BooleanVar()
logCheckValue.set(True)
logCheck = tk.Checkbutton( mainWindow, var=logCheckValue, bg=mybg ).grid( row=nRows, column=4 )
logLabel = tk.Label( mainWindow, text="Semilog scale", font=myFont, fg="black", bg=mybg, width=countryLabelWidth, anchor="w" )
logLabel.grid( row=nRows, column=5 )
nRows += 1

# Daily plot options
casesCheckValue = tk.BooleanVar()
casesCheckValue.set(True)
dailyCasesCheck = tk.Checkbutton( mainWindow, var=casesCheckValue, bg=mybg ).grid( row=nRows, column=0 )
plotLabel = tk.Label( mainWindow, text="Daily new cases", font=myFont, fg="black", bg=mybg, width=countryLabelWidth, anchor="w" )
plotLabel.grid( row=nRows, column=1 )
nRows += 1
deathsCheckValue = tk.BooleanVar()
deathsCheckValue.set(True)
dailyDeathsCheck = tk.Checkbutton( mainWindow, var=deathsCheckValue, bg=mybg ).grid( row=nRows, column=0 )
plotLabel = tk.Label( mainWindow, text="Daily new deaths", font=myFont, fg="black", bg=mybg, width=countryLabelWidth, anchor="w" )
plotLabel.grid( row=nRows, column=1 )
nRows += 1

# Add check boxes for moving averages
dayAverageCheck = [None]*3
dayAverageCheckValue = [None]*3
for iCol in range( len(dayAverageCheck) ):
    dayAverageCheckValue[iCol] = tk.BooleanVar()
#    dayAverageCheckValue[iCol].set(False)
    dayAverageCheckValue[iCol].set( defaultAvgOpts[iCol] )
    dayAverageCheck[iCol] = tk.Checkbutton( mainWindow, var=dayAverageCheckValue[iCol], bg=mybg )
    dayAverageCheck[iCol].grid( row=nRows, column=( iCol*2 ) )
    labelText = str( ((iCol+1)*2+3) ) + "-day Average"
    temp = tk.Label( mainWindow, text=labelText, font=myFont, fg="black", bg=mybg, width=countryLabelWidth, anchor="w" )
    temp.grid( row=nRows, column=( (iCol*2)+1 ) )
nRows += 1

# Add go button
goButton = tk.Button( mainWindow, text="Show Plots", font=myFont, fg="black", bg=mybg, \
    command=lambda:doPlots( JHCases_df, JHDeaths_df, Countries, countriesCheckValue, cddCheckValue, linearCheckValue, logCheckValue, casesCheckValue, deathsCheckValue, dayAverageCheckValue, worldWithoutUSACheckValue ) )
goButton.grid( row=nRows, column=5 )
nRows += 1

# Spacer below go button
tk.Label( mainWindow, text="", bg=mybg ).grid( row=nRows, column=0 )
nRows += 1

# Start main loop
mainWindow.mainloop()
