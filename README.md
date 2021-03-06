# tkCOVIDplots

NOTE: Only tkCOVIDplots-USA-JH is still maintained among the USA plotting scripts.

There are now four scripts. The original is just for the United States and
is now named tkCOVIDplots-USA.py. A second script is also for the United States
but uses a different data source and is name tkCOVIDplots-USA2.py. The third
script is also for the US but uses Johns Hopkins data. The fourth 
script is for the entire world and is named tkCOVIDplots-world.py. A fifth
script is also world states but using Johns Hopkins (-JH) data.
The interface is as described below for all three scripts.

This script goes and gets the United States COVID-19 data from the
New York times database. There is a GUI where you can select the 
types of plots you want and for which states. Selection is by 
check boxes. Everytime you click the doPlots button all plots are 
sent to the screen at the same time. You must close each plot individually. 
You can refresh the data by checking the Refresh Data checkbox.

For the USA plots defaults can be specified in a file called covidDefaults.py.
If this file exists, then the values specified in that file will be the default.
See the covidDefaults in the repo for an example.

Since there are already so many of these COVID-19 plotters available
I make no copyright claim. You are free to use, modify, pass around,
incorporate without licensing issues.
