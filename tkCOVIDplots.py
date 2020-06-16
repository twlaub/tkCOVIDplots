
import tkinter as tk
import pandas as pd
import sys
import numpy as np
#from matplotlib import pyplot as plt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


############################################################
#  Code for what the button does
############################################################
def doPlots( myStates, myStatesCheck, myUSCheck, mycddCheck, myLinearCheck, myLogCheck, myCasesCheck, myDeathsCheck, myAverageCheck ):
#    import pandas as pd
    # Get desired states
    finalDesiredStates = []
    for iState in range( len(myStatesCheck) ):
        if ( myStatesCheck[iState].get() ): finalDesiredStates.append( myStates[iState] )

    # Get data everytime doPlots is clicked
    nyt_us_state_df = getData( dataURL )
    # Check to see if States has changed, if so do what?
    #Get the list of states in the states column
    newStates = list( nyt_us_state_df['state'].unique() )
    newStates.sort()
    newStates = tuple( States )
    if ( newStates != myStates ):
        # Issue warning
        tk.tkMessageBox.showinfo( "Warning", "Available states has changed.\nRecommend restarting application." )
    
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
    for iState in range(len(States)):
        state_df = nyt_us_state_df.loc[nyt_us_state_df['state'] == States[iState] ]
        state_dates  = list( state_df['date'] )
        state_cases  = list( state_df['cases'] )
        state_deaths = list( state_df['deaths'] )
    #    state_deathrates = [ float(d)/float(c)*100. for c,d in zip( state_cases,state_deaths ) if d != 0 ]
        state_deathrates=[0.]*len(state_cases)
        for i in range(len(state_cases)):
            state_deathrates[i] = 0.
            if ( state_cases[i] != 0 ): state_deathrates[i] = float(state_deaths[i])/float(state_cases[i])*100.
        all_states_length.append( len(state_dates) )
        all_states_cases.append( state_cases )
        all_states_deaths.append( state_deaths )
        all_states_deathrates.append( state_deathrates )
        if ( len(state_dates) > maxLength ):
            maxState = States[iState]
            maxLength = len(state_dates)
            maxIndex = index
            all_dates = state_dates
        index += 1

    # Fill in short states with dates and zeros
    for iState in range(len(States)):
        if ( len(all_states_cases[iState]) < maxLength ):
           for i in range(maxLength-len(all_states_cases[iState])):
               all_states_cases[iState].insert( 0, 0 )
               all_states_deaths[iState].insert( 0, 0 )
               all_states_deathrates[iState].insert( 0, 0.0 )

    # Now convert string dates to python date objects using numpy
    # This will allow nice formatting of the date axis
    all_dates = mdates.num2date( mdates.datestr2num(all_dates) )
    
    plotWidth = 8.0
    plotHeight = 6.0

    iFig = 0
    # Calculate us total and plot
    if ( myUSCheck.get() ):
        us_cases = [0]*len(all_dates)
        us_deaths = [0]*len(all_dates)
        us_deathrates = [0.]*len(all_dates)
        for iDate in range(len(all_dates)):
            for iState in range(len(States)):
                us_cases[iDate]  += all_states_cases[iState][iDate]
                us_deaths[iDate] += all_states_deaths[iState][iDate]
            us_deathrates[iDate] = 0.
            if ( us_cases[iDate] != 0. ): us_deathrates[iDate] = float(us_deaths[iDate])/float(us_cases[iDate])*100.

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
                plt.plot(all_dates,us_cases, color='green', label='US confirmed, number')
                plt.plot(all_dates,us_deaths, color='red', label='US deaths, number')
                plt.plot(all_dates,us_deathrates, color='orange', label='US deathrate, %')
                plt.legend(loc="upper left")
                plt.tight_layout()
                #plt.show()

            # Semilog
            if ( myLogCheck.get() ):
                plt.figure(num=iFig,figsize=(plotWidth, plotHeight))
                iFig += 1
                plt.xticks(rotation=45)
                plt.grid()
                plt.plot(all_dates,us_cases, color='green', label='US confirmed, number')
                plt.plot(all_dates,us_deaths, color='red', label='US deaths, number')
                plt.plot(all_dates,us_deathrates, color='orange', label='US deathrate, %')
                plt.legend(loc="upper left")
                plt.yscale('log')
                plt.tight_layout()
                #plt.show()

        # US new cases bar chart
        if ( myCasesCheck.get() ):
            us_new_cases = [us_cases[0]]
            for cases1,cases2 in zip( us_cases[:-1], us_cases[1:] ):
                us_new_cases.append( cases2 - cases1 )
            # Get 5-day moving average of new cases
            if ( myAverageCheck[0].get() ):
                fiveDayDates=[]
                fiveDayCases=[]
                for i in range( 2,len(us_new_cases)-2 ):
                    fiveDayDates.append( all_dates[i] )
                    fiveDayCases.append( sum( us_new_cases[i-2:i+2] )/5.0 )
            # Get 7-day moving average of new cases
            if ( myAverageCheck[1].get() ):
                sevenDayDates=[]
                sevenDayCases=[]
                for i in range( 3,len(us_new_cases)-3 ):
                    sevenDayDates.append( all_dates[i] )
                    sevenDayCases.append( sum( us_new_cases[i-3:i+3] )/7.0 )
            # Get 9-day moving average of new cases
            if ( myAverageCheck[2].get() ):
                nineDayDates=[]
                nineDayCases=[]
                for i in range( 4,len(us_new_cases)-4 ):
                    nineDayDates.append( all_dates[i] )
                    nineDayCases.append( sum( us_new_cases[i-4:i+4] )/9.0 )
            plt.figure(num=iFig,figsize=(plotWidth, plotHeight))
            iFig += 1
            plt.ylabel('US New Cases')
            plt.xticks(rotation=45)
            plt.bar( all_dates,us_new_cases, label='daily' )
            if ( myAverageCheck[0].get() ): plt.plot(fiveDayDates,fiveDayCases,'r',label='5-day')
            if ( myAverageCheck[1].get() ): plt.plot(sevenDayDates,sevenDayCases,'magenta',label='7-day')
            if ( myAverageCheck[2].get() ): plt.plot(nineDayDates,nineDayCases,'orange',label='9-day')
            plt.legend(loc="upper left")
            plt.grid(axis='y')
            plt.tight_layout()
            #plt.show()

        # US new deaths bar chart
        if ( myDeathsCheck.get() ):
            us_new_deaths = [us_deaths[0]]
            for deaths1,deaths2 in zip( us_deaths[:-1], us_deaths[1:] ):
                us_new_deaths.append( deaths2 - deaths1 )
            if ( myAverageCheck[0].get() ):
            # Get 5-day moving average of new deaths
                fiveDayDates=[]
                fiveDayDeaths=[]
                for i in range( 2,len(us_new_deaths)-2 ):
                    fiveDayDates.append( all_dates[i] )
                    fiveDayDeaths.append( sum( us_new_deaths[i-2:i+2] )/5.0 )
            # Get 7-day moving average of new deaths
            if ( myAverageCheck[1].get() ):
                sevenDayDates=[]
                sevenDayDeaths=[]
                for i in range( 3,len(us_new_deaths)-3 ):
                    sevenDayDates.append( all_dates[i] )
                    sevenDayDeaths.append( sum( us_new_deaths[i-3:i+3] )/7.0 )
            # Get 9-day moving average of new deaths
            if ( myAverageCheck[2].get() ):
                nineDayDates=[]
                nineDayDeaths=[]
                for i in range( 4,len(us_new_cases)-4 ):
                    nineDayDates.append( all_dates[i] )
                    nineDayDeaths.append( sum( us_new_deaths[i-4:i+4] )/9.0 )
            plt.figure(num=iFig,figsize=(plotWidth, plotHeight))
            iFig += 1
            plt.ylabel('US New Deaths')
            plt.xticks(rotation=45)
            plt.bar( all_dates,us_new_deaths, label='daily' )
            if ( myAverageCheck[0].get() ): plt.plot(fiveDayDates,fiveDayDeaths,'r',label='5-day')
            if ( myAverageCheck[1].get() ): plt.plot(sevenDayDates,sevenDayDeaths,'magenta',label='7-day')
            if ( myAverageCheck[2].get() ): plt.plot(nineDayDates,nineDayDeaths,'orange',label='9-day')
            plt.legend(loc="upper left")
            plt.grid(axis='y')
            plt.tight_layout()
            #plt.show()

    for state in finalDesiredStates:
        for iState in range(len(States)):
            if ( state == States[iState] ):
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

                # State new cases bar chart
                if ( myCasesCheck.get() ):
                    new_cases = [trimmed_cases[0]]
                    for cases1,cases2 in zip( trimmed_cases[0:-1], trimmed_cases[1:] ):
                        new_cases.append( cases2 - cases1 )
                    # Get 5-day moving average of new cases
                    if ( myAverageCheck[0].get() ):
                        fiveDayDates=[]
                        fiveDayCases=[]
                        for i in range( 2,len(new_cases)-2 ):
                            fiveDayDates.append( trimmed_dates[i] )
                            fiveDayCases.append( sum( new_cases[i-2:i+2] )/5.0 )
                    # Get 7-day moving average of new cases
                    if ( myAverageCheck[1].get() ):
                        sevenDayDates=[]
                        sevenDayCases=[]
                        for i in range( 3,len(new_cases)-3 ):
                            sevenDayDates.append( trimmed_dates[i] )
                            sevenDayCases.append( sum( new_cases[i-3:i+3] )/7.0 )
                    # Get 9-day moving average of new cases
                    if ( myAverageCheck[2].get() ):
                        nineDayDates=[]
                        nineDayCases=[]
                        for i in range( 4,len(new_cases)-4 ):
                            nineDayDates.append( trimmed_dates[i] )
                            nineDayCases.append( sum( new_cases[i-4:i+4] )/9.0 )
                    caseLabel=state+' New Cases'
                    plt.figure(num=iFig,figsize=(plotWidth, plotHeight))
                    iFig += 1
                    plt.grid(axis='y')
                    plt.ylabel(caseLabel)
                    plt.xticks(rotation=45)
                    plt.bar( trimmed_dates, new_cases, label='daily' )
                    if ( myAverageCheck[0].get() ): plt.plot(fiveDayDates,fiveDayCases,'r',label='5-day')
                    if ( myAverageCheck[1].get() ): plt.plot(sevenDayDates,sevenDayCases,'magenta',label='7-day')
                    if ( myAverageCheck[2].get() ): plt.plot(nineDayDates,nineDayCases,'orange',label='9-day')
                    plt.legend(loc="upper left")
                    plt.tight_layout()
                    #plt.show()

                # State new deaths bar chart
                if ( myDeathsCheck.get() ):
                    new_deaths = [trimmed_deaths[0]]
                    for deaths1,deaths2 in zip( trimmed_deaths[:-1], trimmed_deaths[1:] ):
                        new_deaths.append( deaths2 - deaths1 )
                    # Get 5-day moving average of new deaths
                    if ( myAverageCheck[0].get() ):
                        fiveDayDates=[]
                        fiveDayDeaths=[]
                        for i in range( 2,len(new_deaths)-2 ):
                            fiveDayDates.append( trimmed_dates[i] )
                            fiveDayDeaths.append( sum( new_deaths[i-2:i+2] )/5.0 )
                    # Get 7-day moving average of new deaths
                    if ( myAverageCheck[1].get() ):
                        sevenDayDates=[]
                        sevenDayDeaths=[]
                        for i in range( 3,len(new_cases)-3 ):
                            sevenDayDates.append( trimmed_dates[i] )
                            sevenDayDeaths.append( sum( new_deaths[i-3:i+3] )/7.0 )
                    if ( myAverageCheck[2].get() ):
                        nineDayDates=[]
                        nineDayDeaths=[]
                        for i in range( 4,len(new_deaths)-4 ):
                            nineDayDates.append( trimmed_dates[i] )
                            nineDayDeaths.append( sum( new_deaths[i-4:i+4] )/9.0 )
                    deathLabel=state+' New Deaths'
                    plt.figure(num=iFig,figsize=(plotWidth, plotHeight))
                    iFig += 1
                    plt.grid(axis='y')
                    plt.ylabel(deathLabel)
                    plt.xticks(rotation=45)
                    plt.bar( trimmed_dates, new_deaths, label='daily' )
                    if ( myAverageCheck[0].get() ): plt.plot(fiveDayDates,fiveDayDeaths,'r',label='5-day')
                    if ( myAverageCheck[1].get() ): plt.plot(sevenDayDates,sevenDayDeaths,'magenta',label='7-day')
                    if ( myAverageCheck[2].get() ): plt.plot(nineDayDates,nineDayDeaths,'orange',label='9-day')
                    plt.legend(loc="upper left")
                    plt.tight_layout()
                    #plt.show()
#                sys.stdout.write( "{:>10s} {:>7s} {:>7s} {:>7s} {:>7s}\n".format( "date", "cases", "deaths", "ncases", "ndeaths" ) )
#                for date,case,death,ncase,ndeath in zip( trimmed_dates, trimmed_cases, trimmed_deaths, new_cases, new_deaths ):
#                    sys.stdout.write( "{:10s} {:7d} {:7d} {:7d} {:7d}\n".format( date, case, death, ncase, ndeath ) )

                # Break iState loop
                break
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

# Create the main window
mybg="light blue"
#import tkinter as tk
mainWindow = tk.Tk()
mainWindow.configure( bg=mybg )

# Rename the mainWindow (title)
dataURL = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv'
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
#import pandas as pd
dataURL = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv'
nyt_us_state_df = getData( dataURL )

# Create the labels that name the data source
nRows = 0  # Initialize GUI grid row counter

# Spacer below title bar
tk.Label( mainWindow, text="", bg=mybg ).grid( row=nRows, column=0 )
nRows += 1

#Get the list of states in the states column
States = list( nyt_us_state_df['state'].unique() )
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

# Add go button
goButton = tk.Button( mainWindow, text="Show Plots", font=myFont, fg="black", bg=mybg, \
    command=lambda:doPlots(States, statesCheckValue, usCheckValue, cddCheckValue, linearCheckValue, logCheckValue, casesCheckValue, deathsCheckValue, dayAverageCheckValue ) )
goButton.grid( row=nRows, column=5 )
nRows += 1

# Spacer below go button
tk.Label( mainWindow, text="", bg=mybg ).grid( row=nRows, column=0 )
nRows += 1

# Start mian loop
mainWindow.mainloop()
