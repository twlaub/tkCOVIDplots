
import tkinter as tk
import pandas as pd
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

dataURL = 'https://covidtracking.com/api/v1/states/daily.csv'
# Create dictionary to match two-letter abrieviations in states with state names
StatesDict = {
'AK' : 'Alaska                  '.rstrip(),
'AL' : 'Alabama                 '.rstrip(),
'AR' : 'Arkansas                '.rstrip(),
'AS' : 'American Somoa          '.rstrip(),
'AZ' : 'Arizona                 '.rstrip(),
'CA' : 'California              '.rstrip(),
'CO' : 'Colorado                '.rstrip(),
'CT' : 'Connecticut             '.rstrip(),
'DC' : 'Washington DC           '.rstrip(),
'DE' : 'Delaware                '.rstrip(),
'FL' : 'Florida                 '.rstrip(),
'GA' : 'Georgia                 '.rstrip(),
'GU' : 'Guam                    '.rstrip(),
'HI' : 'Hawaii                  '.rstrip(),
'IA' : 'Iowa                    '.rstrip(),
'ID' : 'Idaho                   '.rstrip(),
'IL' : 'Illinois                '.rstrip(),
'IN' : 'Indiana                 '.rstrip(),
'KS' : 'Kansas                  '.rstrip(),
'KY' : 'Kentucky                '.rstrip(),
'LA' : 'Louisiana               '.rstrip(),
'MA' : 'Massachusetts           '.rstrip(),
'MD' : 'Maryland                '.rstrip(),
'ME' : 'Maine                   '.rstrip(),
'MI' : 'Michigan                '.rstrip(),
'MN' : 'Minnesota               '.rstrip(),
'MO' : 'Missouri                '.rstrip(),
'MP' : 'Northern Mariana Islands'.rstrip(),
'MS' : 'Mississippi             '.rstrip(),
'MT' : 'Montana                 '.rstrip(),
'NC' : 'North Carolina          '.rstrip(),
'ND' : 'North Dakota            '.rstrip(),
'NE' : 'Nebrask                 '.rstrip(),
'NH' : 'New Hampshire           '.rstrip(),
'NJ' : 'New Jersey              '.rstrip(),
'NM' : 'New Mexico              '.rstrip(),
'NV' : 'Nevada                  '.rstrip(),
'NY' : 'New York                '.rstrip(),
'OH' : 'Ohio                    '.rstrip(),
'OK' : 'Oklahoma                '.rstrip(),
'OR' : 'Oregon                  '.rstrip(),
'PA' : 'Pennsylvania            '.rstrip(),
'PR' : 'Puerto Rico             '.rstrip(),
'RI' : 'Rhode Island            '.rstrip(),
'SC' : 'South Carolina          '.rstrip(),
'SD' : 'South Dakota            '.rstrip(),
'TN' : 'Tennessee               '.rstrip(),
'TX' : 'Texas                   '.rstrip(),
'UT' : 'Utah                    '.rstrip(),
'VA' : 'Virginia                '.rstrip(),
'VI' : 'Virgin Islands          '.rstrip(),
'VT' : 'Vermont                 '.rstrip(),
'WA' : 'Washington              '.rstrip(),
'WI' : 'Wisconsin               '.rstrip(),
'WV' : 'West Virginia           '.rstrip(),
'WY' : 'Wyoming                 '.rstrip()
}

# Function to return key for any value in a dictionary
def getDictKey(val,myDict): 
    for key, value in myDict.items(): 
         if val == value:
             return key
    return None

# Function to do simple moving averages 
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
#  Code for what the "Show Plots" button does
############################################################
def doPlots( myData, myStates, myStatesCheck, myUSCheck, mycddCheck, myLinearCheck, myLogCheck, myCasesCheck, myDeathsCheck, myAverageCheck, myDataCheck, myAllStatesCases, myAllStatesDeaths ):
    # Get desired states
    finalDesiredStates = []
    for iState in range( len(myStatesCheck) ):
        if ( myStatesCheck[iState].get() ): finalDesiredStates.append( myStates[iState] )

    # Get data if Refresh Data is checked
    if ( myDataCheck.get() ):
        sys.stdout.write( 'Refreshing data\n' )
        sys.stdout.flush()
        us_state_df = getData( dataURL )
        # Check to see if States has changed, if so do what?
        #Get the list of states in the states column
        newStates = list( us_state_df['state'].unique() )
        newStates.sort()
        newStates = tuple( newStates )
        if ( newStates != myStates ):
            # Issue warning
            tk.tkMessageBox.showinfo( "Warning", "Available states has changed.\nRecommend restarting application." )
    else:
#        sys.stdout.write( 'Not refreshing data\n' )
#        sys.stdout.flush()
        us_state_df = myData

    # Sort data by ascending date because the rest of this routine assumes ascending date
    myData.sort_values(by=['date'], inplace=True)

    # Replace NaNs in columns with zeros
    us_state_df['positive'] = us_state_df['positive'].fillna(0)
    us_state_df['death'] = us_state_df['death'].fillna(0)

    all_states_cases=[]
    all_states_deaths=[]
    all_states_deathrates=[]
    all_states_length=[]
    all_dates=[]
    # Extract data for all states
    maxLength = 0
    maxIndex = 0
    index = 0
    # Extract data for all states
    maxLength = 0
    for iState in range(len(myStates)):
        state_df = us_state_df.loc[us_state_df['state'] == getDictKey( myStates[iState],StatesDict ) ]
        state_dates  = list( state_df['date'] )
        state_dates = [ int(x) for x in state_dates ]
        state_cases  = list( state_df['positive'] )
        state_cases = [ int(x) for x in state_cases ]
        state_deaths = list( state_df['death'] )
        state_deaths = [ int(x) for x in state_deaths ]
        state_deathrates=[0.]*len(state_cases)
        for i in range(len(state_cases)):
            state_deathrates[i] = 0.
            if ( state_cases[i] != 0 ): state_deathrates[i] = float(state_deaths[i])/float(state_cases[i])*100.
#        print( "iState,myStates[iState],StatesDict[iState] Key:",iState,myStates[iState],getDictKey( myStates[iState],StatesDict ) )
#        print( "{:>8s} {:>8s} {:>8s} {:>10s}".format("date","cases","deaths","deathrate") )
#        for thisDate,thisCase,thisDeath,thisRate in zip( state_dates,state_cases,state_deaths,state_deathrates):
#             print( "{:8d} {:8d} {:8d} {:10f}".format(thisDate,thisCase,thisDeath,thisRate) )
        all_states_length.append( len(state_dates) )
        all_states_cases.append( state_cases )
        all_states_deaths.append( state_deaths )
        all_states_deathrates.append( state_deathrates )
        if ( len(state_dates) > maxLength ):
            maxState = myStates[iState]
            maxLength = len(state_dates)
            maxIndex = index
            all_dates = state_dates
        index += 1

    # Fill in short states with dates and zeros
    for iState in range(len(myStates)):
        if ( len(all_states_cases[iState]) < maxLength ):
           for i in range(maxLength-len(all_states_cases[iState])):
               all_states_cases[iState].insert( 0, 0 )
               all_states_deaths[iState].insert( 0, 0 )
               all_states_deathrates[iState].insert( 0, 0.0 )

    # Put dashes in date strings
    temp = []
    for dateInt in all_dates:
        iYear = dateInt//10000
        iMonth = (dateInt-iYear*10000)//100
        iDay = dateInt-(iYear*10000)-(iMonth*100)
        temp.append( "{:4s}-{:2s}-{:2s}".format(str(iYear).zfill(4),str(iMonth).zfill(2),str(iDay).zfill(2) ) )
 #   print( temp )

    # Now convert string dates to python date objects using numpy
    # This will allow nice formatting of the date axis
    all_dates = mdates.num2date( mdates.datestr2num(temp) )

    plotWidth = 8.0
    plotHeight = 6.0
    averageColor=[ 'red'.rstrip(), 'magenta'.rstrip(), 'orange' ]

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
 #       print( "Entire US" )
 #       print( "{:>10s} {:>8s} {:>8s} {:>10s}".format("date","cases","deaths","deathrate") )
 #       for thisDate,thisCase,thisDeath,thisRate in zip( temp,us_cases,us_deaths,us_deathrates):
 #            print( "{:10s} {:8d} {:8d} {:10f}".format(thisDate,thisCase,thisDeath,thisRate) )

        # Plot the data
        # Set up the graph
#        print( "\nPlotting US data" )
        if ( mycddCheck.get() ):
        # Linear
            if ( myLinearCheck.get() ):
                plt.figure(num=iFig,figsize=(plotWidth, plotHeight))
                iFig += 1
                plt.xticks(rotation=45)
                plt.ylim(0,max(us_cases)*1.05)
                plt.grid()
                plt.plot(all_dates,us_cases, color='green'.rstrip(), label='US confirmed, number')
                plt.plot(all_dates,us_deaths, color='red'.rstrip(), label='US deaths, number')
                plt.plot(all_dates,us_deathrates, color='orange'.rstrip(), label='US deathrate, %')
                plt.legend(loc="upper left")
                plt.tight_layout()
                #plt.show()

            # Semilog
            if ( myLogCheck.get() ):
                plt.figure(num=iFig,figsize=(plotWidth, plotHeight))
                iFig += 1
                plt.xticks(rotation=45)
                plt.grid()
                plt.plot(all_dates,us_cases, color='green'.rstrip(), label='US confirmed, number')
                plt.plot(all_dates,us_deaths, color='red'.rstrip(), label='US deaths, number')
                plt.plot(all_dates,us_deathrates, color='orange'.rstrip(), label='US deathrate, %')
                plt.legend(loc="upper left")
                plt.yscale('log')
                plt.tight_layout()
                #plt.show()

        # US new cases chart
        if ( myCasesCheck.get() ):
            us_new_cases = [us_cases[0]]

            for cases1,cases2 in zip( us_cases[:-1], us_cases[1:] ):
                us_new_cases.append( cases2 - cases1 )
            
            plt.figure(num=iFig,figsize=(plotWidth, plotHeight))
            iFig += 1
            plt.ylabel('US New Cases')
            plt.xticks(rotation=45)
            plt.bar( all_dates, us_new_cases, label='daily' )

            # Get 5,7,9-day moving average of new cases
            dayAverageDates = all_dates
            for iDay in range(3):
                if ( myAverageCheck[iDay].get() ):
#                    print( (2*iDay+5),"day average" )            
                    dayAverage = dayAveraging( (2*iDay+5), us_new_cases )
                    labelText = str((2*iDay+5))+"-day"
                    plt.plot( dayAverageDates, dayAverage, averageColor[iDay], label=labelText )

            plt.legend(loc="upper left")
            plt.grid(axis='y')
            plt.tight_layout()
            #plt.show()

        # US new deaths chart
        if ( myDeathsCheck.get() ):
            us_new_deaths = [us_deaths[0]]
            for deaths1,deaths2 in zip( us_deaths[:-1], us_deaths[1:] ):
                us_new_deaths.append( deaths2 - deaths1 )

            plt.figure(num=iFig,figsize=(plotWidth, plotHeight))
            iFig += 1
            plt.ylabel('US New Deaths')
            plt.xticks(rotation=45)
            plt.bar( all_dates,us_new_deaths, label='daily' )

            # Get 5,7,9-day moving average of new deaths
            dayAverageDates = all_dates
            for iDay in range(3):
                if ( myAverageCheck[iDay].get() ):
#                    print( (2*iDay+5),"day average" )            
                    dayAverage = dayAveraging( (2*iDay+5), us_new_deaths )
                    labelText = str((2*iDay+5))+"-day"
                    plt.plot( dayAverageDates, dayAverage, averageColor[iDay], label=labelText )

            plt.legend(loc="upper left")
            plt.grid(axis='y')
            plt.tight_layout()
            #plt.show()

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
                # Set up the graph
                caseLabel=state+' confirmed, number'
                deathLabel=state+' deaths, number'
                rateLabel=state+' deathrate, %'
                # Linear
                if ( mycddCheck.get() ):
                    if ( myLinearCheck.get() ):
                        plt.figure(num=iFig,figsize=(plotWidth, plotHeight))
                        iFig += 1
                        plt.xticks(rotation=45)
                        plt.ylim(0,max(trimmed_cases)*1.05)
                        plt.grid()
                        caseLabel=state+' confirmed, number'
                        deathLabel=state+' deaths, number'
                        rateLabel=state+' deathrate, %'
                        plt.plot(trimmed_dates,trimmed_cases, color='green'.rstrip(), label=caseLabel )
                        plt.plot(trimmed_dates,trimmed_deaths, color='red'.rstrip(), label=deathLabel )
                        plt.plot(trimmed_dates,trimmed_deathrate, color='orange'.rstrip(), label=rateLabel )
                        plt.legend(loc="upper left")
                        plt.tight_layout()
                        #plt.show()

                    # Semilog
                    if ( myLogCheck.get() ):
                        plt.figure(num=iFig,figsize=(plotWidth, plotHeight))
                        iFig += 1
                        plt.xticks(rotation=45)
                        plt.grid()
                        plt.plot(trimmed_dates,trimmed_cases, color='green'.rstrip(), label=caseLabel )
                        plt.plot(trimmed_dates,trimmed_deaths, color='red'.rstrip(), label=deathLabel )
                        plt.plot(trimmed_dates,trimmed_deathrate, color='orange'.rstrip(), label=rateLabel )
                        plt.legend(loc="upper left")
                        plt.yscale('log')
                        plt.tight_layout()
                        #plt.show()

                # State new cases chart
                if ( myCasesCheck.get() ):
                    new_cases = [trimmed_cases[0]]
                    for cases1,cases2 in zip( trimmed_cases[0:-1], trimmed_cases[1:] ):
                        new_cases.append( cases2 - cases1 )
                    caseLabel=state+' New Cases'
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

                # State new deaths chart
                if ( myDeathsCheck.get() ):
                    new_deaths = [trimmed_deaths[0]]
                    for deaths1,deaths2 in zip( trimmed_deaths[:-1], trimmed_deaths[1:] ):
                        new_deaths.append( deaths2 - deaths1 )
                    deathLabel=state+' New Deaths'
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

                # Break iState loop
                break

    # Collect data for all states cases or deaths
    plotWidth=10
    if ( myAllStatesCases.get() ):
        allStatesCases = []
        for iState in range( len(myStates) ):
            allStatesCases.append( all_states_cases[iState][-1] )
#        print( 'len of myStates:'.rstrip(),len(myStates) )
#        print( 'len of allStatesCases'.rstrip(),len(allStatesCases) )
#        print( 'len of myStates[0]'.rstrip(),len(myStates[0]) )
#        print( 'len of allStatesCases[0]'.rstrip(),len(allStatesCases[0]) )
#        print( 'myStates[0]'.rstrip(),myStates[0] )
#        print( 'allStatesCases[0]'.rstrip(),allStatesCases[0] )
        plt.figure(num=iFig,figsize=(plotWidth, plotHeight))
        iFig += 1
        plt.grid(axis='y')
        plt.ylabel('Total Cases')
        plt.xticks(rotation=90)
        plt.bar( myStates, allStatesCases )
        plt.tight_layout()
    
    if ( myAllStatesDeaths.get() ):
        allStatesDeaths = []
        allStatesDeathrates = []
        for iState in range( len(myStates) ):
            allStatesDeaths.append( all_states_deaths[iState][-1] )
            allStatesDeathrates.append( all_states_deathrates[iState][-1] )
        # Deaths
        plt.figure(num=iFig,figsize=(plotWidth, plotHeight))
        iFig += 1
        plt.grid(axis='y')
        plt.ylabel('Total Deaths')
        plt.xticks(rotation=90)
        plt.bar( myStates, allStatesDeaths )
        plt.tight_layout()
        # DeathRates
        plt.figure(num=iFig,figsize=(plotWidth, plotHeight))
        iFig += 1
        plt.grid(axis='y')
        plt.ylabel('Deathrate %')
        plt.xticks(rotation=90)
        plt.bar( myStates, allStatesDeathrates )
        plt.tight_layout()
   
    plt.show()

    return

# Gets data every time it is called. The GUI depends depends on the states listed
# in the data the first time the data is retrieved. Subsequent retrievals will not
# change the GUI. If states are added to the data between data retrievals the results
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
#import tkinter as tk
mainWindow = tk.Tk()
mainWindow.configure( bg=mybg )

# Rename the mainWindow (title)
myTitle = "{:s} {:s}".format("COVID-19 Data Plotter: Data Source is",dataURL)
#mainWindow.title( "COVID-19 Data Plotter: Data Source is "+dataURL )
mainWindow.title( myTitle )

# Get pixels per point
# Never figured out how to use this info to size labels
#pixelsPerPoint = mainWindow.winfo_fpixels( '1p' )
#print( "pixelsPerPoint:",pixelsPerPoint )
#pointsPerChar=12
#pixelsPerChar = pointsPerChar*pixelsPerPoint
#print( "pixelsPerChar:",pixelsPerChar )
maxLabelLengh = len("Cases, Deaths, DeathRates:")

# loading data right from the source:
#import pandas as pd
us_state_df = getData( dataURL )

# Create the labels that name the data source
nRows = 0  # Initialize GUI grid row counter

# Spacer below title bar
tk.Label( mainWindow, text="", bg=mybg ).grid( row=nRows, column=0 )
nRows += 1

#Get the list of states in the states column
StatesAbbr = list( us_state_df['state'].unique() )
StatesAbbr.sort()
StatesAbbr = tuple( StatesAbbr )
States = []
for stateAbbr in StatesAbbr:
    States.append( StatesDict[stateAbbr] )
States.sort()
States = tuple( States )

# Find max length label (if a state is longer than max given above)
maxStateLength = 0
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
myFont=('Ariel'.rstrip(),pointsPerChar)
for iStart in range(0,nStates,nColsStates):
#    print( "nRows:",nRows )
#    print( "iStart:",iStart )
    for iCol in range(nColsStates):
        iState = iStart+iCol
        if ( iState >= nStates ): break
        statesCheckValue[iState] = tk.BooleanVar()
        statesCheckValue[iState].set(False)
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
cddCheckValue.set(True)
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
    dayAverageCheckValue[iCol].set(False)
    dayAverageCheck[iCol] = tk.Checkbutton( mainWindow, var=dayAverageCheckValue[iCol], bg=mybg )
    dayAverageCheck[iCol].grid( row=nRows, column=( iCol*2 ) )
    labelText = str( ((iCol+1)*2+3) ) + "-day Average"
    temp = tk.Label( mainWindow, text=labelText, font=myFont, fg="black", bg=mybg, width=stateLabelWidth, anchor="w" )
    temp.grid( row=nRows, column=( (iCol*2)+1 ) )
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
nRows += 1
# Add check box for refresh data
dataCheckValue = tk.BooleanVar()
dataCheckValue.set(False)
dataCheck = tk.Checkbutton( mainWindow, var=dataCheckValue, bg=mybg )
dataCheck.grid( row=nRows, column=0 )
dataCheckLabel = tk.Label( mainWindow, text="Refresh Data", font=myFont, fg="black", bg=mybg, width=stateLabelWidth, anchor="w" )
dataCheckLabel.grid( row=nRows, column=1 )
nRows += 1

# Add go button
goButton = tk.Button( mainWindow, text="Show Plots", font=myFont, fg="black", bg=mybg, \
    command=lambda:doPlots(us_state_df, States, statesCheckValue, usCheckValue, cddCheckValue, linearCheckValue, logCheckValue, casesCheckValue, deathsCheckValue, dayAverageCheckValue, dataCheckValue, allStatesCasesValue, allStatesDeathsValue ) )
goButton.grid( row=nRows, column=5 )
nRows += 1

# Spacer below go button
tk.Label( mainWindow, text="", bg=mybg ).grid( row=nRows, column=0 )
nRows += 1

# Start mian loop
mainWindow.mainloop()
