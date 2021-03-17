
import tkinter as tk
import pandas as pd
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import plotly.express as px

# State abrieviations dictionary, already sorted alphabetically by state name
StatesToKeep = (
 'Alabama                 '.rstrip(),
 'Alaska                  '.rstrip(),
 'Arizona                 '.rstrip(),
 'Arkansas                '.rstrip(),
 'California              '.rstrip(),
 'Colorado                '.rstrip(),
 'Connecticut             '.rstrip(),
 'Delaware                '.rstrip(),
 'District of Columbia    '.rstrip(),
 'Florida                 '.rstrip(),
 'Georgia                 '.rstrip(),
 'Hawaii                  '.rstrip(),
 'Idaho                   '.rstrip(),
 'Illinois                '.rstrip(),
 'Indiana                 '.rstrip(),
 'Iowa                    '.rstrip(),
 'Kansas                  '.rstrip(),
 'Kentucky                '.rstrip(),
 'Louisiana               '.rstrip(),
 'Maine                   '.rstrip(),
 'Maryland                '.rstrip(),
 'Massachusetts           '.rstrip(),
 'Michigan                '.rstrip(),
 'Minnesota               '.rstrip(),
 'Mississippi             '.rstrip(),
 'Missouri                '.rstrip(),
 'Montana                 '.rstrip(),
 'Nebraska                '.rstrip(),
 'Nevada                  '.rstrip(),
 'New Hampshire           '.rstrip(),
 'New Jersey              '.rstrip(),
 'New Mexico              '.rstrip(),
 'New York                '.rstrip(),
 'North Carolina          '.rstrip(),
 'North Dakota            '.rstrip(),
 'Ohio                    '.rstrip(),
 'Oklahoma                '.rstrip(),
 'Oregon                  '.rstrip(),
 'Pennsylvania            '.rstrip(),
 'Rhode Island            '.rstrip(),
 'South Carolina          '.rstrip(),
 'South Dakota            '.rstrip(),
 'Tennessee               '.rstrip(),
 'Texas                   '.rstrip(),
 'Utah                    '.rstrip(),
 'Vermont                 '.rstrip(),
 'Virginia                '.rstrip(),
 'Washington              '.rstrip(),
 'West Virginia           '.rstrip(),
 'Wisconsin               '.rstrip(),
 'Wyoming                 '.rstrip()
)

# State abrieviations tuple, already sorted alphabetically according to state names
# Diamond Princess and Grand Princess may be cruise ships
States2Letter = (
'AL','AK','AZ','AR','CA','CO','CT','DE','DC','FL',
'GA','HI','ID','IL','IN','IA','KS','KY','LA','ME',
'MD','MA','MI','MN','MS','MO','MT','NE','NV','NH',
'NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI',
'SC','SD','TN','TX','UT','VT','VA','WA','WV','WI',
'WY' )


# Setting default plotting options
defaultStates = [ "New Mexico", "Texas" ]   # default desired states
defaultAvgOpts = [ False, True, False ]     # default daily averages
defaultCDD = False                          # default cases, deaths, deathrates
plotWidth8 = 8.0                            # default plot width
plotWidth10 = 10.0                          # default plot width
plotHeight = 6.0                            # default plot height
averageColor=[ 'red', 'magenta', 'orange' ] # default daily average plot colors
cddColors=[ 'green', 'red', 'orange' ]      # default daily average plot colors

############################################################
# Sorts two list by list1 and returns sorted lists
def sortLists( list1, list2 ):
    temp = zip(list1,list2)
    sorted_temp = sorted(temp)
    sorted1 = [ x for x,y in sorted_temp ]
    sorted2 = [ y for x,y in sorted_temp ]
    return sorted1,sorted2

############################################################
# Plots cumulative cases, deaths, and deathrates
def cddPlots( iFig, x, ys, colors, labels, linlog ):
    plt.figure( num=iFig, figsize=(plotWidth8, plotHeight) )
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
    plt.figure(num=iFig,figsize=(plotWidth8, plotHeight))

    # Daily bar chart
    plt.ylabel( plotLabel )
    plt.xticks(rotation=45)
    plt.bar( x, y, label='daily' )

    # Get 5,7,9-day moving averages
    for iDay in range(3):
        if ( averageCheck[iDay].get() ):
            dayAverage,slope,xs,ys = dayAveraging( (2*iDay+5), x, y )
            labelText = str((2*iDay+5))+"-day moving average"
            plt.plot( x, dayAverage, averageColor[iDay], label=labelText )
            xs = [ x[-(3*(2*iDay+5))-1], x[-1] ]
            labelText = str((3*(2*iDay+5)))+"-day slope = "+str(round(slope,2))+" /day"
            plt.plot( xs, ys, "black", label=labelText )
    plt.legend(loc="upper left")
    plt.grid(axis='y')
    plt.tight_layout()
    if ( negCheck.get() ): plt.ylim(bottom=0)

############################################################
# Plots new cases and deaths moving averages together on one plot
def dailyAverageDualScalePlots( iFig, x, cases, deaths, averageCheck, plotLabel, negCheck ):
    fig,ax = plt.subplots(num=iFig,figsize=(plotWidth8, plotHeight))
#    plt.figure(num=iFig,figsize=(plotWidth8, plotHeight))

    # y-axis label and x-axis tick orientation
    ax.set_ylabel( plotLabel+" new cases")
    plt.xticks(rotation=45)

    # Create twin object for two differen y-axis on the same plot
    ax2 = ax.twinx()
    ax2.set_ylabel( plotLabel+" new deaths")

    # Get 5,7,9-day moving averages
    for iDay in range(3):
        if ( averageCheck[iDay].get() ):
            casesAverage,slope,xs,ys = dayAveraging( (2*iDay+5), x, cases )
            deathsAverage,slope,xs,ys = dayAveraging( (2*iDay+5), x, deaths )
            casesLabelText = "cases "+str((2*iDay+5))+"-day moving average"
            deathsLabelText = "deaths "+str((2*iDay+5))+"-day moving average"
            ax.plot ( x, casesAverage, "black", label=casesLabelText )
            ax.legend( loc="upper left" )
            ax2.plot( x, deathsAverage, "red", label=deathsLabelText )
            ax2.legend( loc="lower right" )
#    fig.legend(loc="upper left")
#    fig.legend(loc="upper center")
#    ax.legend(loc="upper left")
#    ax2.legend(loc="upper left")
#    plt.sublots.legend(loc="upper left")
#    fig.grid(axis='y')
    fig.tight_layout()
    if ( negCheck.get() ):
        ax.set_ylim(bottom=0)
        ax2.set_ylim(bottom=0)

############################################################
def dayAveraging( mynDays, myX, myList ):
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
    # calculate slope of trendline using numpy
    deltaDays = myX[-1] - myX[0]
    offsetDays = int( deltaDays.total_seconds()/86400 )
    # Careful! This assumes the total length of the data in days is more than 3 time the averaging length
    # This is a bug that I have recognized but not fixed
    x = np.array( [ offsetDays+i for i in range( len(averagedDayList[-(3*mynDays)-1:-1]) ) ] )
    y = np.array( averagedDayList[-(3*mynDays)-1:-1] )
    slope,b = np.polyfit(x,y,1)
    ys = [ x[0]*slope + b, x[-1]*slope + b ]
    xs = [ x[0], x[-1] ]
    return averagedDayList, slope, xs, ys

############################################################
#  Code for what the "Show Plots" button does
############################################################
def doPlots( myCasesData, myDeathsData, myStates, myStatesCheck, myUSCheck, mycddCheck, myLinearCheck, myLogCheck, myCasesCheck, myDeathsCheck, myAverageCheck, myAverageDualScaleCheck, myAllStatesCases, myAllStatesDeaths, myNegCheck, myAllStatesSort, myMapCheck ):
    # Get desired states
    finalDesiredStates = []
    for iState in range( len(myStatesCheck) ):
        if ( myStatesCheck[iState].get() ): finalDesiredStates.append( myStates[iState] )

    # Extract data for all states
    all_states_cases=[]
    all_states_deaths=[]
    all_states_deathrates=[]
    all_states_length=[]
    all_states_population=[]
    all_dates=[]
    for iState in range(len(myStates)):
        state_JHDeaths_df = myDeathsData.loc[myDeathsData['Province_State'] == myStates[iState] ]
        state_JHCases_df  = myCasesData.loc[myCasesData['Province_State'] == myStates[iState] ]
        state_dates = list( state_JHDeaths_df)[12:] # if using cases start at 11
        state_cases = list( state_JHCases_df[state_dates].sum(axis=0) )
        state_deaths = list( state_JHDeaths_df[state_dates].sum(axis=0) )
        state_Population = state_JHDeaths_df['Population'].sum(axis=0)
        state_deathrates=[0.]*len(state_cases)
        for i in range(len(state_cases)):
            state_deathrates[i] = 0.
            if ( state_cases[i] != 0 ): state_deathrates[i] = float(state_deaths[i])/float(state_cases[i])*100.
        all_states_length.append( len(state_dates) )
        all_states_cases.append( state_cases )
        all_states_deaths.append( state_deaths )
        all_states_population.append( state_Population )
        all_states_deathrates.append( state_deathrates )
    all_dates = state_dates

    # Now convert string dates to python date objects using numpy
    # This will allow nice formatting of the date axis
    all_dates = mdates.num2date( mdates.datestr2num(all_dates) )


    iFig = 0
    # Calculate us total and plot
    if ( myUSCheck.get() ):
        us_cases = [0]*len(all_dates)
        us_deaths = [0]*len(all_dates)
        us_deathrates = [0.]*len(all_dates)
        for iDate in range(len(all_dates)):
            for iState in range(len(myStates)):
                us_cases[iDate]  += all_states_cases[iState][iDate]
                us_deaths[iDate] += all_states_deaths[iState][iDate]
            us_deathrates[iDate] = 0.
            if ( us_cases[iDate] != 0. ): us_deathrates[iDate] = float(us_deaths[iDate])/float(us_cases[iDate])*100.

        # Cases, Deaths, and Deathrates
        if ( mycddCheck.get() ):
            labels = [ 'US confirmed, number', 'US deaths, number', 'US deathrate, %' ]
            # Linear
            if ( myLinearCheck.get() ):
                cddPlots( iFig, all_dates, [ us_cases, us_deaths, us_deathrates ], cddColors, labels, 'linear' )
                iFig += 1
            # Semilog
            if ( myLogCheck.get() ):
                cddPlots( iFig, all_dates, [ us_cases, us_deaths, us_deathrates ], cddColors, labels, 'log' )
                iFig += 1

        # US new cases chart
        if ( myCasesCheck.get() ):
            us_new_cases = [us_cases[0]]

            for cases1,cases2 in zip( us_cases[:-1], us_cases[1:] ):
                us_new_cases.append( cases2 - cases1 )
            dailyPlots( iFig, all_dates, us_new_cases, myAverageCheck, 'US New Cases', myNegCheck )
            iFig += 1

        # US new deaths chart
        if ( myDeathsCheck.get() ):
            us_new_deaths = [us_deaths[0]]
            for deaths1,deaths2 in zip( us_deaths[:-1], us_deaths[1:] ):
                us_new_deaths.append( deaths2 - deaths1 )
            dailyPlots( iFig, all_dates, us_new_deaths, myAverageCheck, 'US New Deaths', myNegCheck )
            iFig += 1

        # US new cases & deaths averages on one plot
        if ( myAverageDualScaleCheck.get() and myCasesCheck.get() and myDeathsCheck.get() ):
            dailyAverageDualScalePlots( iFig, all_dates, us_new_cases, us_new_deaths, myAverageCheck, "US", myNegCheck )
            iFig += 1

    for state in finalDesiredStates:
        for iState in range(len(myStates)):
            if ( state == myStates[iState] ):
#                sys.stdout.write( "\nState: {:s}\n".format(state) )
                trimmed_dates=[]
                trimmed_cases=[]
                trimmed_deaths=[]
                trimmed_deathrate=[]
                for date,cases,deaths,deathrate in zip(all_dates,all_states_cases[iState],all_states_deaths[iState],all_states_deathrates[iState]):
                    if ( cases == 0 ): continue
                    trimmed_dates.append(date)
                    trimmed_cases.append(cases)
                    trimmed_deaths.append(deaths)
                    trimmed_deathrate.append(deathrate)
#                print( "\nPlotting",state,"data" )

                caseLabel=state+' confirmed, number'
                deathLabel=state+' deaths, number'
                rateLabel=state+' deathrate, %'
                labels = [ caseLabel, deathLabel, rateLabel ]

                # Cumulative cases, deaths, and deathrates
                if ( mycddCheck.get() ):
                    Ys = [ trimmed_cases, trimmed_deaths, trimmed_deathrate ]
                    # Linear
                    if ( myLinearCheck.get() ):
                        cddPlots( iFig, trimmed_dates, Ys, cddColors, labels, 'linear' )
                        iFig += 1
                    # Semilog
                    if ( myLogCheck.get() ):
                        cddPlots( iFig, trimmed_dates, Ys, cddColors, labels, 'log' )
                        iFig += 1

                # State new cases chart
                if ( myCasesCheck.get() ):
                    new_cases = [trimmed_cases[0]]
                    for cases1,cases2 in zip( trimmed_cases[0:-1], trimmed_cases[1:] ):
                        new_cases.append( cases2 - cases1 )
                    caseLabel=state+' New Cases'
                    dailyPlots( iFig, trimmed_dates, new_cases, myAverageCheck, caseLabel, myNegCheck )
                    iFig += 1

                # State new deaths chart
                if ( myDeathsCheck.get() ):
                    new_deaths = [trimmed_deaths[0]]
                    for deaths1,deaths2 in zip( trimmed_deaths[:-1], trimmed_deaths[1:] ):
                        new_deaths.append( deaths2 - deaths1 )
                    deathLabel=state+' New Deaths'
                    dailyPlots( iFig, trimmed_dates, new_deaths, myAverageCheck, deathLabel, myNegCheck )
                    iFig += 1

                # US new cases & deaths averages on one plot
                if ( myAverageDualScaleCheck.get() and myCasesCheck.get() and myDeathsCheck.get() ):
                   dailyAverageDualScalePlots( iFig, trimmed_dates, new_cases, new_deaths, myAverageCheck, state, myNegCheck )
                   iFig += 1

                # Break iState loop
                break

    # Collect data for all states cases or deaths
#    plotWidth=10
    if ( myAllStatesCases.get() ):
        us_population = sum(all_states_population)
        allStatesCases = []
        allStatesCasesPerCap = []
        for iState in range( len(myStates) ):
            allStatesCases.append( all_states_cases[iState][-1] )
            if ( all_states_population[iState] != 0 ):
                allStatesCasesPerCap.append( all_states_cases[iState][-1]/all_states_population[iState]*100000. )
            else:
                allStatesCasesPerCap.append( 0. )
#        print( 'len of myStates:',len(myStates) )
#        print( 'len of allStatesCases',len(allStatesCases) )
#        print( 'len of myStates[0]',len(myStates[0]) )
#        print( 'len of allStatesCases[0]',len(allStatesCases[0]) )
#        print( 'myStates[0]',myStates[0] )
#        print( 'allStatesCases[0]',allStatesCases[0] )
        plt.figure(num=iFig,figsize=(plotWidth10, plotHeight))
        iFig += 1
        plt.grid(axis='y')
        plt.ylabel('Total Cases')
        plt.xticks(rotation=90)
        allStatesCasesSorted = [ x for x in allStatesCases ]
        myStatesSorted = [ x for x in myStates ]
        if ( myAllStatesSort.get() ):
            allStatesCasesSorted,myStatesSorted = sortLists( allStatesCases,myStates )
        text = "Total US Cases: {:d}".format( us_cases[-1] )
        plt.text(0.5, 0.95*allStatesCasesSorted[-1], text, fontsize=12 )
        plt.bar( myStatesSorted, allStatesCasesSorted )
        plt.tight_layout()
        plt.figure(num=iFig,figsize=(plotWidth10, plotHeight))
        iFig += 1
        plt.grid(axis='y')
        plt.ylabel('Cases per 100,000')
        plt.xticks(rotation=90)
        allStatesCasesPerCapSorted = [ x for x in allStatesCasesPerCap ]
        myStatesSorted = [ x for x in myStates ]
        if ( myAllStatesSort.get() ):
            allStatesCasesPerCapSorted,myStatesSorted = sortLists( allStatesCasesPerCap,myStates )
        allStatesCasesPerCapSorted.append( us_cases[-1]/us_population*100000. )
        myStatesSorted.append( "United States" )
        plt.bar( myStatesSorted, allStatesCasesPerCapSorted )
        plt.tight_layout()
        # Map plot of cases and cases per cap
        if ( myMapCheck.get() ) :
            casesMap = px.choropleth(locations=States2Letter, locationmode="USA-states", color=allStatesCases, scope="usa", title="Cases")
            casesMap.show()
            casesPerCapMap = px.choropleth(locations=States2Letter, locationmode="USA-states", color=allStatesCasesPerCap, scope="usa", title="Per capita cases")
            casesPerCapMap.show()


    if ( myAllStatesDeaths.get() ):
        allStatesDeaths = []
        allStatesDeathrates = []
        allStatesDeathsPerCap = []
        for iState in range( len(myStates) ):
            allStatesDeaths.append( all_states_deaths[iState][-1] )
            allStatesDeathrates.append( all_states_deathrates[iState][-1] )
            if ( all_states_population[iState] != 0 ):
                allStatesDeathsPerCap.append( all_states_deaths[iState][-1]/all_states_population[iState]*100000. )
            else:
                allStatesDeathsPerCap.append( 0. )
        # Deaths
        plt.figure(num=iFig,figsize=(plotWidth10, plotHeight))
        iFig += 1
        plt.grid(axis='y')
        plt.ylabel('Total Deaths')
        plt.xticks(rotation=90)
        allStatesDeathsSorted = [ x for x in allStatesDeaths ]
        myStatesSorted = [ x for x in myStates ]
        if ( myAllStatesSort.get() ):
            allStatesDeathsSorted,myStatesSorted = sortLists( allStatesDeaths,myStates )
        text = "Total US Deaths: {:d}".format( int(us_deaths[-1]) )
        plt.text(0.5, 0.95*allStatesDeathsSorted[-1], text, fontsize=12 )
        plt.bar( myStatesSorted, allStatesDeathsSorted )
        plt.tight_layout()
        plt.figure(num=iFig,figsize=(plotWidth10, plotHeight))
        iFig += 1
        plt.grid(axis='y')
        plt.ylabel('Deaths per 100,000')
        plt.xticks(rotation=90)
        allStatesDeathsPerCapSorted = [ x for x in allStatesDeathsPerCap ]
        myStatesSorted = [ x for x in myStates ]
        if ( myAllStatesSort.get() ):
            allStatesDeathsPerCapSorted,myStatesSorted = sortLists( allStatesDeathsPerCap,myStates )
        allStatesDeathsPerCapSorted.append( us_deaths[-1]/us_population*100000. )
        myStatesSorted.append( "United States" )
        plt.bar( myStatesSorted, allStatesDeathsPerCapSorted )
        plt.tight_layout()
        # DeathRates
        plt.figure(num=iFig,figsize=(plotWidth10, plotHeight))
        iFig += 1
        plt.grid(axis='y')
        plt.ylabel('Deathrate %')
        plt.xticks(rotation=90)
        allStatesDeathratesSorted = [ x for x in allStatesDeathrates ]
        myStatesSorted = [ x for x in myStates ]
        if ( myAllStatesSort.get() ):
            temp = zip(allStatesDeathratesSorted,myStatesSorted)
            sorted_temp = sorted(temp)
            allStatesDeathratesSorted = [ x for x,y in sorted_temp ]
            myStatesSorted = [ y for x,y in sorted_temp ]
        allStatesDeathratesSorted.append( us_deathrates[-1] )
        myStatesSorted.append( "United States" )
        plt.bar( myStatesSorted, allStatesDeathratesSorted )
        plt.tight_layout()
        # Map plot of cases and cases per cap
        if ( myMapCheck.get() ) :
            deathsMap = px.choropleth(locations=States2Letter, locationmode="USA-states", color=allStatesDeaths, scope="usa", title="Deaths")
            deathsMap.show()
            deathsPerCapMap = px.choropleth(locations=States2Letter, locationmode="USA-states", color=allStatesDeathsPerCap, scope="usa", title="Per capita deaths")
            deathsPerCapMap.show()
            deathRateMap = px.choropleth(locations=States2Letter, locationmode="USA-states", color=allStatesDeathrates, scope="usa", title="Death Rate")
            deathRateMap.show()

    plt.show()

    return

############################################################
# Gets data every time it is called. The GUI depends on the states listed
# in the data the first time the data is retrieved. Subsequent retrievals will not
# change the GUI. If states are added to the data between data retrievals the results
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

# Look for defaults file and import if it exists
# Will override hardwired defaults at top of script
try:
    defaultFile = open("covidDefaults.py")
#    print( defaultStates )
    from covidDefaults import *
    import covidDefaults
#    print( defaultStates )
except IOError:
    pass

# Create the main window
mybg="light blue"
#import tkinter as tk
mainWindow = tk.Tk()
mainWindow.configure( bg=mybg )

# Set data files URL and file names
casesDataFile = 'time_series_covid19_confirmed_US.csv'
deathsDataFile = 'time_series_covid19_deaths_US.csv'
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

#Get the list of states in the states column
States = list( JHDeaths_df['Province_State'].unique() )
temp = [ state for state in States ]
for state in States:
    if ( state not in StatesToKeep ):
        temp.remove(state)
States = [ state for state in temp ]
States.sort()
States = tuple( States )
maxStateLength = 0

# Find max length label (if a state is longer than max given above)
for state in States:
   if ( len(state) > maxStateLength ): maxStateLength = len(state)
if ( maxLabelLengh > maxStateLength ): maxStateLength = maxLabelLengh
# Create State labels in nColsStates columns
nColsStates = 5
nStates = len(States)
if ( nStates%nColsStates == 0 ):
    nRowsStates = nStates//nColsStates
else:
    nRowsStates = nStates//nColsStates + 1

# Add State checkboxes
statesCheck = [None]*nStates
statesCheckValue = [None]*nStates
#points2pixels=0.08
#stateLabelWidth = int( maxStateLength*pointsPerChar*points2pixels)
stateLabelWidth = int( maxStateLength*0.9 )
#print( "stateLabelWidth:",stateLabelWidth )
#stateLabelWidth = int( maxStateLength*pixelsPerChar)
#print( "stateLabelWidth:",stateLabelWidth )
pointsPerChar=12
myFont=('Ariel',pointsPerChar)
for iStart in range(0,nStates,nColsStates):
#    print( "nRows:",nRows )
#    print( "iStart:",iStart )
    for iCol in range(nColsStates):
        iState = iStart+iCol
        if ( iState >= nStates ): break
        statesCheckValue[iState] = tk.BooleanVar()
        statesCheckValue[iState].set(False)
        if ( States[iState] in defaultStates ): statesCheckValue[iState].set(True)
        statesCheck[iState] = tk.Checkbutton( mainWindow, var=statesCheckValue[iState], bg=mybg )
        statesCheck[iState].grid( row=nRows, column=(2*iCol) )
        temp = tk.Label( mainWindow, text=States[iState], font=myFont, fg="black", bg=mybg, width=stateLabelWidth, anchor="w" )
        temp.grid( row=nRows, column=(2*(iCol+1)-1) )
    tk.Label( mainWindow, text="   ", fg=mybg, bg=mybg ).grid( row=nRows, column=2*nColsStates ) # padding right side
    nRows += 1
nRows += 1

# Add US checkbox
usCheckValue = tk.BooleanVar()
usCheckValue.set(True)
usCheck = tk.Checkbutton( mainWindow, var=usCheckValue, bg=mybg ).grid( row=nRows, column=0 )
usLabel = tk.Label( mainWindow, text="Entire US", font=myFont, fg="black", bg=mybg, width=stateLabelWidth, anchor="w" )
usLabel.grid( row=nRows, column=1 )
nRows += 1

# Add Plotting options
tk.Label( mainWindow, text="", bg=mybg ).grid( row=nRows, column=0 )
nRows += 1
plotLabel = tk.Label( mainWindow, text="Plotting options:", font=myFont, fg="black", bg=mybg, width=stateLabelWidth, anchor="w" )
plotLabel.grid( row=nRows, column=1 )
nRows += 1
tk.Label( mainWindow, text="", bg=mybg ).grid( row=nRows, column=0 )
nRows += 1
# Cases, Deaths, and Deathrate scale options
cddCheckValue = tk.BooleanVar()
#cddCheckValue.set(True)
cddCheckValue.set( defaultCDD )
#print( "cddCheckValue:",cddCheckValue.get() )
cddCheck = tk.Checkbutton( mainWindow, var=cddCheckValue, bg=mybg ).grid( row=nRows, column=0 )
plotLabel = tk.Label( mainWindow, text="Cases, Deaths, DeathRates:", font=myFont, fg="black", bg=mybg, width=stateLabelWidth, anchor="w" )
plotLabel.grid( row=nRows, column=1 )
linearCheckValue = tk.BooleanVar()
linearCheckValue.set(True)
linearCheck = tk.Checkbutton( mainWindow, var=linearCheckValue, bg=mybg ).grid( row=nRows, column=2 )
linearLabel = tk.Label( mainWindow, text="Linear scale", font=myFont, fg="black", bg=mybg, width=stateLabelWidth, anchor="w" )
linearLabel.grid( row=nRows, column=3 )
logCheckValue = tk.BooleanVar()
logCheckValue.set(True)
logCheck = tk.Checkbutton( mainWindow, var=logCheckValue, bg=mybg ).grid( row=nRows, column=4 )
logLabel = tk.Label( mainWindow, text="Semilog scale", font=myFont, fg="black", bg=mybg, width=stateLabelWidth, anchor="w" )
logLabel.grid( row=nRows, column=5 )
nRows += 1
# Daily plot options
casesCheckValue = tk.BooleanVar()
casesCheckValue.set(True)
dailyCasesCheck = tk.Checkbutton( mainWindow, var=casesCheckValue, bg=mybg ).grid( row=nRows, column=0 )
plotLabel = tk.Label( mainWindow, text="Daily new cases", font=myFont, fg="black", bg=mybg, width=stateLabelWidth, anchor="w" )
plotLabel.grid( row=nRows, column=1 )
nRows += 1
deathsCheckValue = tk.BooleanVar()
deathsCheckValue.set(True)
dailyDeathsCheck = tk.Checkbutton( mainWindow, var=deathsCheckValue, bg=mybg ).grid( row=nRows, column=0 )
plotLabel = tk.Label( mainWindow, text="Daily new deaths", font=myFont, fg="black", bg=mybg, width=stateLabelWidth, anchor="w" )
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
    temp = tk.Label( mainWindow, text=labelText, font=myFont, fg="black", bg=mybg, width=stateLabelWidth, anchor="w" )
    temp.grid( row=nRows, column=( (iCol*2)+1 ) )
dayAverageDualScaleValue=tk.BooleanVar()
dayAverageDualScaleValue.set(False)
dayAverageDualScaleCheck = tk.Checkbutton ( mainWindow, var=dayAverageDualScaleValue, bg=mybg )
dayAverageDualScaleCheck.grid( row=nRows, column=( len(dayAverageCheck)*2 ) )
temp = tk.Label( mainWindow, text="Averages on one plot", font=myFont, fg="black", bg=mybg, width=stateLabelWidth, anchor="w" )
temp.grid( row=nRows, column=( len(dayAverageCheck)*2+1 ) )
nRows += 1
# Add check box for all states comparison
allStatesCasesValue = tk.BooleanVar()
allStatesCasesValue.set(False)
allStatesCasesCheck = tk.Checkbutton( mainWindow, var=allStatesCasesValue, bg=mybg )
allStatesCasesCheck.grid( row=nRows, column=0 )
allStatesCasesLabel = tk.Label( mainWindow, text="All States Cases", font=myFont, fg="black", bg=mybg, width=stateLabelWidth, anchor="w" )
allStatesCasesLabel.grid( row=nRows, column=1 )
allStatesDeathsValue = tk.BooleanVar()
allStatesDeathsValue.set(False)
allStatesDeathsCheck = tk.Checkbutton( mainWindow, var=allStatesDeathsValue, bg=mybg )
allStatesDeathsCheck.grid( row=nRows, column=2 )
allStatesDeathsLabel = tk.Label( mainWindow, text="All States Deaths", font=myFont, fg="black", bg=mybg, width=stateLabelWidth, anchor="w" )
allStatesDeathsLabel.grid( row=nRows, column=3 )
allStatesSortValue = tk.BooleanVar()
allStatesSortValue.set(True)
allStatesSortCheck = tk.Checkbutton( mainWindow, var=allStatesSortValue, bg=mybg )
allStatesSortCheck.grid( row=nRows, column=4 )
allStatesSortLabel = tk.Label( mainWindow, text="Sorted", font=myFont, fg="black", bg=mybg, width=stateLabelWidth, anchor="w" )
allStatesSortLabel.grid( row=nRows, column=5 )
mapCheckValue = tk.BooleanVar()
mapCheckValue.set(False)
mapCheck = tk.Checkbutton( mainWindow, var=mapCheckValue, bg=mybg )
mapCheck.grid( row=nRows, column=6 )
mapCheckLabel = tk.Label( mainWindow, text="Map Plots (Browser)", font=myFont, fg="black", bg=mybg, width=stateLabelWidth, anchor="w" )
mapCheckLabel.grid( row=nRows, column=7 )
nRows += 1
# Add check box to suppress negatives
negCheckValue = tk.BooleanVar()
negCheckValue.set(True)
negCheck = tk.Checkbutton( mainWindow, var=negCheckValue, bg=mybg )
negCheck.grid( row=nRows, column=0 )
negCheckLabel = tk.Label( mainWindow, text="Suppress negatives", font=myFont, fg="black", bg=mybg, width=stateLabelWidth, anchor="w" )
negCheckLabel.grid( row=nRows, column=1 )
nRows += 1

# Add go button
goButton = tk.Button( mainWindow, text="Show Plots", font=myFont, fg="black", bg=mybg, \
    command=lambda:doPlots( JHCases_df, JHDeaths_df, States, statesCheckValue, usCheckValue, cddCheckValue, linearCheckValue, logCheckValue, casesCheckValue, deathsCheckValue, dayAverageCheckValue, dayAverageDualScaleValue, allStatesCasesValue, allStatesDeathsValue, negCheckValue, allStatesSortValue, mapCheckValue ) )
goButton.grid( row=nRows, column=5 )
nRows += 1

# Spacer below go button
tk.Label( mainWindow, text="", bg=mybg ).grid( row=nRows, column=0 )
nRows += 1

# Start mian loop
mainWindow.mainloop()
