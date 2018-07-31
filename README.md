# Modeling NBA Regular Season Over/Under 

### What are you trying to do? Articulate your objectives using absolutely no jargon.
I am trying to model the over/under scores of NBA regular season games. This involves predicting the total points scored in a single game.

### How has this problem been solved before?
This has been solved before by looking at individual player performance and how it affects the team overall. Since basketball has evolved over the years, from relying on big men to now relying more on shooters, only more recent seasons are used (past 15-20 seasons). There are also more advanced statistics that can be used, such as player positioning, efficiency vs. different heights, etc.

### What is new about your approach, why do you think it will be successful?
Since this has been so widely modeled, and because I do not have an extended period of time for this capstone project I will not be able to approach this problem in a new way. I will use points per game (PPG), assists per game (APG), steals per game (SPG), rebounds per game (RPG), blocks per game (BPG), possessions per game, etc.

### If you're successful, what will the impact be?
With the Supreme Court’s ruling on sports betting, many places will want to be able to model this line as accurately as possible, because it is a very popular type of bet. On the other side of the coin, there are many people who would like to be able to make more informed bets.

### How will you present your work?
Most likely, I will present this with slides, and a well-documented jupyter notebook to refer to for more code, methods, and reasons. However, I do not like powerpoints so I hope to find a better option.

### What are your data sources? What is the size of your dataset, and what is your storage format?
The data comes from ESPN box scores. I have scraped the past 15 regular seasons and stored them as CSV files. These are about 3 megabytes each, for a total of 45 megabytes

### What are potential problems with your capstone, and what have you done to mitigate these problems?
Problems that may occur involve factoring in injuries, fatigue, resting players, and home court advantage.  The period in which the game occurs will almost surely have a big effect on the scores.

### What is the next thing you need to work on?
Doing EDA is the next step in the process. Also, a few season failed when scraping so I need to go back through those season.
