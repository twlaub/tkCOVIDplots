
import tkinter as tk
import pandas as pd
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def dayAveraging( mynDays, myList ):
    halfDays = mynDays//2  # integer division
    averagedDayList=[]
    sevenDayCases=[]
    for i in range( halfDays ):
        averagedDayList.append( sum( myList[0:(halfDays+1+i)] )/float(halfDays+1+i) )
#        print( i )
#        print( myList[0:(halfDays+1+i)] )
#        print( sum( myList[0:(halfDays+1+i)] ), sum( myList[0:(halfDays+1+i)] )/float(halfDays+1+i) )
    for i in range( halfDays,len(myList)-halfDays ):
        averagedDayList.append( sum( myList[i-halfDays:i+halfDays] )/mynDays )
    for i in range( halfDays,0,-1 ):
        averagedDayList.append( sum( myList[(-1*(i+halfDays+1)):-1] )/float(i+halfDays) )
#        print( i )
#        print( myList[(-1*(i+halfDays+1)):-1] )
#        print( sum( myList[(-1*(i+halfDays+1)):-1] ), sum( myList[(-1*(i+halfDays+1)):-1] )/float(i+halfDays) )
    return averagedDayList


############################################################
#  Code for what the doPlots button does
############################################################
def doPlots( myCountries, myCountriesCheck, mycddCheck, myLinearCheck, myLogCheck, myCasesCheck, myDeathsCheck, myAverageCheck ):
    # Get desired countries
    finalDesiredCountries = []
    for iCountry in range( len(myCountriesCheck) ):
        if ( myCountriesCheck[iCountry].get() ): finalDesiredCountries.append( myCountries[iCountry] )

    # Get data everytime doPlots is clicked
    # Desired data column headings: location, date, total_cases, total_deaths
    who_world_df = getData( dataURL )
    # Check to see if Countries has changed, if so do what?
    #Get the list of countries in the location column
    newCountries = list( who_world_df['location'].unique() )
    newCountries.sort()
    newCountries = tuple( Countries )
    if ( newCountries != myCountries ):
        # Issue warning
        tk.tkMessageBox.showinfo( "Warning", "Available countries has changed.\nRecommend restarting application." )

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

    # Fill in short countries with dates and zeros
    for iCountry in range(len(Countries)):
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
Countries = tuple( Countries )
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

# Add go button
goButton = tk.Button( mainWindow, text="Show Plots", font=myFont, fg="black", bg=mybg, \
    command=lambda:doPlots(Countries, countriesCheckValue, cddCheckValue, linearCheckValue, logCheckValue, casesCheckValue, deathsCheckValue, dayAverageCheckValue ) )
goButton.grid( row=nRows, column=5 )
nRows += 1

# Spacer below go button
tk.Label( mainWindow, text="", bg=mybg ).grid( row=nRows, column=0 )
nRows += 1

# Start main loop
mainWindow.mainloop()
