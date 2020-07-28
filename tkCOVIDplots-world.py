
import tkinter as tk
import pandas as pd
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def dayAveraging( mynDays, myList ):
    halfDays = mynDays//2  # integer division
    averagedDayList=[]
    # Handle the beginning of the list where there is not a full nDays data to average
#    print( "\n\n",mynDays,"day average" )
#    print("\nBeginning of list")
    for i in range( halfDays ):
        averagedDayList.append( float(sum( myList[0:(halfDays+1+i)] ))/float(halfDays+1+i) )
#        print( "Index:", i )
#        print( "Partial list:",myList[0:(halfDays+1+i)] )
#        print( "Divisor",(halfDays+1+i) )
#        print( "Sum,Avg:",sum( myList[0:(halfDays+1+i)] ), float(sum( myList[0:(halfDays+1+i)] ))/float(halfDays+1+i) )
    # Handle the middle of the list were a full nDays worth of datat is available to average
#    print("\nMiddle of list")
    for i in range( halfDays,len(myList)-halfDays ):
        averagedDayList.append( float(sum( myList[i-halfDays:i+halfDays+1] ))/float(mynDays) )
#        print( "Index:", i )
#        print( "Partial list:",myList[i-halfDays:i+halfDays+1] )
#        print( "Divisor",mynDays )
#        print( "Sum,Avg:",sum( myList[i-halfDays:i+halfDays+1] ), float(sum( myList[i-halfDays:i+halfDays+1] ))/float(mynDays) )
    # Handle the end of the list where there is not a full nDays data to average
#    print("\nEnd of list")
#    print( "Length of list:",len(myList) )
    for i in range( halfDays,0,-1 ):
        averagedDayList.append( float(sum( myList[(len(myList)-halfDays-i):len(myList)] ))/float(i+halfDays) )
#        print( "Index:",len(myList) - i )
#        print( "Partial list:",myList[(len(myList)-halfDays-i):len(myList)] )
#        print( "Divisor",(i+halfDays) )
#        print( "Sum,Avg:",sum( myList[(len(myList)-halfDays-i):len(myList)] ), float(sum( myList[(len(myList)-halfDays-i):len(myList)] ))/float(i+halfDays) )
    return averagedDayList


############################################################
#  Code for what the doPlots button does
############################################################
def doPlots( myData, myCountries, myCountriesCheck, mycddCheck, myLinearCheck, myLogCheck, myCasesCheck, myDeathsCheck, myAverageCheck, myDataCheck, myWorldWithoutUSA ):
    # Get desired countries
    finalDesiredCountries = []
    for iCountry in range( len(myCountriesCheck) ):
        if ( myCountriesCheck[iCountry].get() ): finalDesiredCountries.append( myCountries[iCountry] )

    # Get data if Refresh Data is checked
    # Desired data column headings: location, date, total_cases, total_deaths
    if ( myDataCheck.get() ):
        sys.stdout.write( 'Refreshing data\n' )
        sys.stdout.flush()
        who_world_df = getData( dataURL )
        # Check to see if Countries has changed, if so do what?
        #Get the list of countries in the location column
        newCountries = list( who_world_df['location'].unique() )
        newCountries.sort()
#        newCountries = tuple( newCountries )
        if ( newCountries != myCountries ):
            # Issue warning
            tk.tkMessageBox.showinfo( "Warning", "Available countries has changed.\nRecommend restarting application." )
    else:
#        sys.stdout.write( 'Not refreshing data\n' )
#        sys.stdout.flush()
        who_world_df = myData

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
        country_df = who_world_df.loc[who_world_df['location'] == myCountries[iCountry] ]
        country_dates  = list( country_df['date'] )
        country_cases  = list( country_df['total_cases'] )
        country_deaths = list( country_df['total_deaths'] )
        country_deathrates=[0.]*len(country_cases)
        for i in range(len(country_cases)):
            country_deathrates[i] = 0.
            if ( country_cases[i] != 0 ): country_deathrates[i] = float(country_deaths[i])/float(country_cases[i])*100.
        all_countries_length.append( len(country_dates) )
        all_countries_cases.append( country_cases )
        all_countries_deaths.append( country_deaths )
        all_countries_deathrates.append( country_deathrates )
        if ( len(country_dates) > maxLength ):
            maxCountry = myCountries[iCountry]
            maxLength = len(country_dates)
            maxIndex = index
            all_dates = country_dates
        index += 1

    # Create World less USA data and append to downloaded data
    # Relying on 'World' and 'United States' labels not to change
    # Find 'World' and 'United States'
    if ( myWorldWithoutUSA.get() ):
        iWorld = -1
        iUSA = -1
        for iCountry in range(len(myCountries)):
            if ( myCountries[iCountry] == 'World' ): iWorld = iCountry
            if ( myCountries[iCountry] == 'United States' ): iUSA = iCountry
        worldLessUSA = False
        if ( (iWorld != -1) and (iUSA != -1) ): worldLessUSA = True
        # Create world less USA data
        if ( worldLessUSA ):
            worldLessUSACases = []
            for world,usa in zip( all_countries_cases[iWorld],all_countries_cases[iUSA] ):
                worldLessUSACases.append( world - usa )
            worldLessUSADeaths = []
            for world,usa in zip( all_countries_deaths[iWorld],all_countries_deaths[iUSA] ):
                worldLessUSADeaths.append( world - usa )
            worldLessUSADeathrates = []
            for cases,deaths in zip( worldLessUSACases, worldLessUSADeaths ):
                if ( cases != 0 ): 
                    worldLessUSADeathrates.append( float(deaths)/float(cases)*100. )
                else:
                    worldLessUSADeathrates.append( 0.0 )
            # Append World Less USA data to downloaded data
            myCountries.append( 'World Without USA' )
            finalDesiredCountries.append( 'World Without USA' )
            all_countries_cases.append( worldLessUSACases )
            all_countries_deaths.append( worldLessUSADeaths )
            all_countries_deathrates.append( worldLessUSADeathrates )

    # Fill in short countries with dates and zeros, don't think this is necessary but doing anyway
    for iCountry in range(len(myCountries)):
        if ( len(all_countries_cases[iCountry]) < maxLength ):
           for i in range(maxLength-len(all_countries_cases[iCountry])):
               all_countries_cases[iCountry].insert( 0, 0 )
               all_countries_deaths[iCountry].insert( 0, 0 )
               all_countries_deathrates[iCountry].insert( 0, 0.0 )

    # Now convert string dates to python date objects using numpy
    # This will allow nice formatting of the date axis
    all_dates = mdates.num2date( mdates.datestr2num(all_dates) )

    plotWidth = 8.0
    plotHeight = 6.0
    averageColor=[ 'red', 'magenta', 'orange' ]

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
                    if ( myLinearCheck.get() ):
                        plt.figure(num=iFig,figsize=(plotWidth, plotHeight))
                        iFig += 1
                        plt.xticks(rotation=45)
                        plt.ylim(0,max(trimmed_cases)*1.05)
                        plt.grid()
                        caseLabel=country+' confirmed, number'
                        deathLabel=country+' deaths, number'
                        rateLabel=country+' deathrate, %'
                        plt.plot(trimmed_dates,trimmed_cases, color='green', label=caseLabel )
                        plt.plot(trimmed_dates,trimmed_deaths, color='red', label=deathLabel )
                        plt.plot(trimmed_dates,trimmed_deathrate, color='orange', label=rateLabel )
                        plt.legend(loc="upper left")
                        plt.tight_layout()
                        #plt.show()

                    # Semilog
                    if ( myLogCheck.get() ):
                        plt.figure(num=iFig,figsize=(plotWidth, plotHeight))
                        iFig += 1
                        plt.xticks(rotation=45)
                        plt.grid()
                        plt.plot(trimmed_dates,trimmed_cases, color='green', label=caseLabel )
                        plt.plot(trimmed_dates,trimmed_deaths, color='red', label=deathLabel )
                        plt.plot(trimmed_dates,trimmed_deathrate, color='orange', label=rateLabel )
                        plt.legend(loc="upper left")
                        plt.yscale('log')
                        plt.tight_layout()
                        #plt.show()

                # Country new cases chart
                if ( myCasesCheck.get() ):
                    new_cases = [trimmed_cases[0]]
                    for cases1,cases2 in zip( trimmed_cases[0:-1], trimmed_cases[1:] ):
                        new_cases.append( cases2 - cases1 )
                    caseLabel=country+' New Cases'
                    plt.figure(num=iFig,figsize=(plotWidth, plotHeight))
                    iFig += 1
                    plt.grid(axis='y')
                    plt.ylabel(caseLabel)
                    plt.xticks(rotation=45)
                    plt.bar( trimmed_dates, new_cases, label='daily' )
                     
                    # Get 5,7,9-day moving average of new cases
                    dayAverageDates = trimmed_dates
                    for iDay in range(3):
                        if ( myAverageCheck[iDay].get() ):
#                            print( (2*iDay+5),"day average" )            
                            dayAverage = dayAveraging( (2*iDay+5), new_cases )
                            labelText = str((2*iDay+5))+"-day"
                            plt.plot( dayAverageDates, dayAverage, averageColor[iDay], label=labelText )

                    plt.legend(loc="upper left")
                    plt.tight_layout()
                    #plt.show()

                # Country new deaths chart
                if ( myDeathsCheck.get() ):
                    new_deaths = [trimmed_deaths[0]]
                    for deaths1,deaths2 in zip( trimmed_deaths[:-1], trimmed_deaths[1:] ):
                        new_deaths.append( deaths2 - deaths1 )
                    deathLabel=country+' New Deaths'
                    plt.figure(num=iFig,figsize=(plotWidth, plotHeight))
                    iFig += 1
                    plt.grid(axis='y')
                    plt.ylabel(deathLabel)
                    plt.xticks(rotation=45)
                    plt.bar( trimmed_dates, new_deaths, label='daily' )
                     
                    # Get 5,7,9-day moving average of new deaths
                    dayAverageDates = trimmed_dates
                    for iDay in range(3):
                        if ( myAverageCheck[iDay].get() ):
#                            print( (2*iDay+5),"day average" )            
                            dayAverage = dayAveraging( (2*iDay+5), new_deaths )
                            labelText = str((2*iDay+5))+"-day"
                            plt.plot( dayAverageDates, dayAverage, averageColor[iDay], label=labelText )

                    plt.legend(loc="upper left")
                    plt.tight_layout()
                    #plt.show()

                # Break iCountry loop
                break

    plt.show()

    return

# Gets data every time it is called. The GUI depends depends on the countries listed
# in the data the first time the data is retrieved. Subsequent retrievals will not
# change the GUI. If countries are added to the data between data retrievals the results
# of the plots may be mislabeled.
def getData(dataURL):
#    import pandas as pd
    return pd.read_csv( dataURL )

############################################################
#  Main program section
############################################################

# Silence warning about leaving too many plots open
plt.rcParams.update({'figure.max_open_warning': 0})

# Create the main window
mybg="light blue"
mainWindow = tk.Tk()
mainWindow.configure( bg=mybg )

# Rename the mainWindow (title)
#dataURL = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv'
dataURL = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
mainWindow.title( "COVID-19 Data Plotter: Data Source is "+dataURL )

# Get pixels per point
# Never figured out how to use this info to size labels
#pixelsPerPoint = mainWindow.winfo_fpixels( '1p' )
#print( "pixelsPerPoint:",pixelsPerPoint )
#pointsPerChar=12
#pixelsPerChar = pointsPerChar*pixelsPerPoint
#print( "pixelsPerChar:",pixelsPerChar )
maxLabelLengh = len("Cases, Deaths, DeathRates:")

# loading data right from the source:
#Column headings
# iso_code, continent, ***location***, ***date***, ***total_cases***, new_cases, ***total_deaths***, new_deaths, total_cases_per_million, 
#new_cases_per_million, total_deaths_per_million, new_deaths_per_million, total_tests, new_tests, total_tests_per_thousand,
# new_tests_per_thousand, new_tests_smoothed, new_tests_smoothed_per_thousand, tests_units, stringency_index, population,
# population_density, median_age, aged_65_older, aged_70_older, gdp_per_capita, extreme_poverty, cvd_death_rate,
# diabetes_prevalence, female_smokers, male_smokers, handwashing_facilities, hospital_beds_per_thousand, life_expectancy
# Desired data: ***location***, ***date***, ***total_cases***, ***total_deaths***

who_world_df = getData( dataURL )

# Create the labels that name the data source
nRows = 0  # Initialize GUI grid row counter

# Spacer below title bar
tk.Label( mainWindow, text="", bg=mybg ).grid( row=nRows, column=0 )
nRows += 1

#Get the list of countries in the 'location' column
Countries = list( who_world_df['location'].unique() )
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
# World less USA plot option
worldWithoutUSACheckValue = tk.BooleanVar()
worldWithoutUSACheckValue.set(False)
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
cddCheckValue.set(True)
#print( "cddCheckValue:",cddCheckValue.get() )
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
    dayAverageCheckValue[iCol].set(False)
    dayAverageCheck[iCol] = tk.Checkbutton( mainWindow, var=dayAverageCheckValue[iCol], bg=mybg )
    dayAverageCheck[iCol].grid( row=nRows, column=( iCol*2 ) )
    labelText = str( ((iCol+1)*2+3) ) + "-day Average"
    temp = tk.Label( mainWindow, text=labelText, font=myFont, fg="black", bg=mybg, width=countryLabelWidth, anchor="w" )
    temp.grid( row=nRows, column=( (iCol*2)+1 ) )
nRows += 1
# Add check box for refresh data
dataCheckValue = tk.BooleanVar()
dataCheckValue.set(False)
dataCheck = tk.Checkbutton( mainWindow, var=dataCheckValue, bg=mybg )
dataCheck.grid( row=nRows, column=0 )
dataCheckLabel = tk.Label( mainWindow, text="Refresh Data", font=myFont, fg="black", bg=mybg, width=countryLabelWidth, anchor="w" )
dataCheckLabel.grid( row=nRows, column=1 )
nRows += 1

# Add go button
goButton = tk.Button( mainWindow, text="Show Plots", font=myFont, fg="black", bg=mybg, \
    command=lambda:doPlots( who_world_df, Countries, countriesCheckValue, cddCheckValue, linearCheckValue, logCheckValue, casesCheckValue, deathsCheckValue, dayAverageCheckValue, dataCheckValue, worldWithoutUSACheckValue ) )
goButton.grid( row=nRows, column=5 )
nRows += 1

# Spacer below go button
tk.Label( mainWindow, text="", bg=mybg ).grid( row=nRows, column=0 )
nRows += 1

# Start main loop
mainWindow.mainloop()
