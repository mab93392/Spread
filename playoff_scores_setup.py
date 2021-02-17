import mysql.connector
import requests
import json

def playoff_scores_setup():
    # connects to database
    NHL_Data = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'fm2a85xm',
        database = 'NHL_Data',
        auth_plugin='mysql_native_password'
    )
    cur = NHL_Data.cursor()

    # creates table
    col_stmt = '(game_id INT, home_id VARCHAR(5), home_points INT, away_id VARCHAR(5), away_points INT)'
    cur.execute('CREATE TABLE playoff_scores ' + col_stmt)

    # for each year
    for i in range(0,3): # 2 yrs
        yr = 2014 + i
        
        # for each matchup
        for j in range(0,8): # 8 match ups
            mtch = 1 + j

            # for each game
            for k in range(0,4): # 4 games
                game = 1 + k
                game_id = str(yr) + '0301' + str(mtch) + str(game)

                # pulls data
                url = 'https://statsapi.web.nhl.com/api/v1/game/' + game_id + '/linescore'
                data = json.loads(requests.get(url).content)

                # organizes home data
                hm_tm = data['teams']['home']['team']['id']
                hm_pts = data['teams']['home']['goals']

                # organizes away data
                a_tm = data['teams']['away']['team']['id']
                a_pts = data['teams']['away']['goals']

                # populates table
                col_names = '(game_id, home_id, home_points, away_id, away_points)'
                vals = ('(%s, %s, %s, %s, %s)') % (game_id,hm_tm,hm_pts,a_tm,a_pts)
                cur.execute('INSERT INTO playoff_scores ' + col_names + ' VALUES ' + vals)
                NHL_Data.commit()



