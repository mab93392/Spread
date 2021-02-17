import mysql.connector
import numpy as np

def vs_stats_setup(): 
    # connects to database
    NHL_Data = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'fm2a85xm',
        database = 'NHL_Data',
        auth_plugin='mysql_native_password'
    )
    cur = NHL_Data.cursor()

    cur.execute('SELECT * FROM playoff_scores')
    game_stats = cur.fetchall()
    stat_names = ['goalsPerGame','goalsAgainstPerGame','powerPlayPercentage','penaltyKillPercentage','shotsPerGame','shotsAllowed','faceOffWinPercentage','shootingPctg','savePctg']


    for i in range(0,len(stat_names)):
        if i == 0:
            col_stmt = 'score_diff INT, %s FLOAT' % stat_names[i]
            col_name = 'score_diff, %s' % stat_names[i]
        else:
            col_stmt += ', %s FLOAT' % stat_names[i]
            col_name += ', %s' % stat_names[i]
    cur.execute('CREATE TABLE vs_stats (' + col_stmt + ')')

    for game in game_stats:
        
        # generates season input
        yr_fall = str(game[0]).split('030')[0]
        yr_spring = int(yr_fall) + 1
        season = str(yr_fall) + str(yr_spring)


        home_id = game[1]
        cur.execute('SELECT team_abv FROM teams WHERE team_id = %s' % home_id)
        hmabv_pull = cur.fetchall()
        home_abv = hmabv_pull[0][0]
        home_score = game[2]
        cur.execute('SELECT * FROM ' + str(home_abv) +   ' WHERE season = %s' % season)
        home_stats = cur.fetchall()

        away_id = game[3]
        cur.execute('SELECT team_abv FROM teams WHERE team_id = %s' % away_id)
        awayabdv_pull = cur.fetchall()
        away_abv = awayabdv_pull[0][0]
        away_score = game[4]
        cur.execute("SELECT * FROM " + str(away_abv) +  " WHERE season = '%s'" % season)
        away_stats = cur.fetchall()

        
        for j in range(1,10):
            if j == 1: 
                stat_diff = '%s' % (home_stats[0][j]-away_stats[0][j])
            else: 
                stat_diff += ', %s' % (home_stats[0][j]-away_stats[0][j])

        score_diff = home_score - away_score
        vals = str(score_diff) + ', ' + stat_diff

        cur.execute('INSERT INTO vs_stats (' + col_name + ') VALUES (' + vals +')')

    NHL_Data.commit()

