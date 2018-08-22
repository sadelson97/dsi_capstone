# Modeling NBA Regular Season Over/Under 

### Project Goals
I am trying to model the over/under scores of NBA regular season games. This involves predicting the total points scored in a single game.

### Background and Motivation
I have been a huge fan of the NBA for as long as I can remember. After the supreme court ruling on sports betting, I want build a model that can beat Vegas's prediction. 

For this project, I chose to focus on a rolling means approach. This takes each teams last 6 games and averages their statistics before making a prediction for the total score.

### How has this problem been solved before?
This has been solved before by looking at team performance and how different types of opponents match up with a team. Since basketball has evolved over the years, from relying on big men to now relying more on shooters, only more recent seasons are used (past 15-20 seasons). There are also more advanced statistics that can be used, such as player positioning, efficiency vs. different heights, etc.

To build my model, I use basic team statistics such as points per game (PPG), assists per game (APG), steals per game (SPG), rebounds per game (RPG), blocks per game (BPG), possessions per game, etc. along with other statistics that I feature engineered.

### Data Collection
I used BeautifulSoup to scrape ESPN boxscores since the 2004 season and then stored them as CSV files. Each season is about 3 megabytes, for a total of 45 megabytes.

The way the data is collected is as individual player statistics, so feature engineering is required to get the data into the team statistics that I need it to be in.

### If you're successful, what will the impact be?
With the Supreme Court’s ruling on sports betting, many places will want to be able to model this line as accurately as possible, because it is a very popular type of bet. On the other side of the coin, there are many people who would like to be able to make more informed bets.

### Model results
The final model I used was a Lasso model. It picked up obvious statistics such as average points per game and field goal attempts, but it also picked up some of my feature engineered statistics

My model predictions are, on average, 14.07 points from the actual score while Vegas's predictions are 13.75 points from the actual.
![picture](blob/master/model_result_pics/Pictureclipping.pictClipping)

### Future Work
In order to obtain better results, I need to continue doing feature engineering. This includes, but is not limited to, creating features for resting/injury of top scorers, team fatigue, and other defensive statistics. There are also statistics that I would not be able to feature engineer with the data that I have, such as average time per possession, average shot distance, drives per game, and others. As these could be important features, I need to collect more data.
