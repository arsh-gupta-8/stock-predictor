# StockBot - A customisable ML stock trader

## Description
This is a personal project I initially created to predict the return of a stock for the next day, but it turned into a machine learning trading simulation as I implemented an API to paper trade and allow users to customise their training data to test bots of their own

## Current Strategy
- I currently have 20 stocks selected and they are ranked on their predicted return for the next day and the best 10 are selected
- The stocks are only bought if predicted to increase by 0.5%
- The stocks are sold if they have decreased in value by more than 1% or are predicted to decrease

## Want to try?
### Install
1. Clone the repository
2. Make sure you have python installed
3. Inside a virtual environment (or globally) use the command ***pip install -r requirements.txt***

### Customise and Use
1. Run the code and select option 1 to change which stocks you want to train your model with
2. After that, select option 2 to edit which stocks you want to test the model with
3. Then select option 3 to name and train the model with the selected stocks. This will save the model onto your device, the next time you run the program you can select option 4 and seelct your model rather than retraining it
4. You can then either choose option 5 to check the stastics or option 6 to back test ti, which will simulate the bot being used over the last year and show your profit
5. You can edit the Strategies.py file to create a function of your own strategy and then change the strategy being used in the paperTrade.py file

### Paper Trading
1. Create a .env file and create two fields with the exact names
ALPACA_API_KEY=
ALPACA_SECRET_KEY=
2. Create an account on alpaca - https://alpaca.markets/
3. Copy and paste the api key and secret key in the appropriate field
4. Before running the main.py file, Edit the stockNamesTrading array on line 69 selecting the stocks you want to trade
5. Then run the program and either load your model from option 4 or train your model from option 3
6. Select option 0. Entering in viewmode will not make any trades on your alpaca account, it will just show the predictions of each stock. Not entering in view mdoe will make trades depending on the predictions and strategy

Here is a visual of what the options menu looks like

<img width="295" height="162" alt="image" src="https://github.com/user-attachments/assets/1c58af86-e6b8-4d3d-9677-7aa53a6f3eab" />

## Future Updates
+ need to add file saving for selected train/test/papertrade stocks
+ need to add file for updated stocks so stock api not accessed everytime
