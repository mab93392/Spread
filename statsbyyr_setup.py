import mysql.connector
import requests
import json

def statsbyyr_setup():
    # connects to database
    NHL_Data = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'fm2a85xm',
        database = 'NHL_Data',
        auth_plugin='mysql_native_password'
    )
    cur = NHL_Data.cursor()

    # pulls data from team table
    cur.execute("SELECT * FROM teams WHERE team_abv !='VGK'")
    team_list = cur.fetchall()

    # makes column statement for table creation
    soi_name = ['goalsPerGame','goalsAgainstPerGame','powerPlayPercentage','penaltyKillPercentage','shotsPerGame','shotsAllowed','faceOffWinPercentage','shootingPctg','savePctg']
    for i in range(0,len(soi_name)):
        if i == 0:
            col_nme = 'season INT, %s FLOAT' % soi_name[i]
        else: 
            col_nme += ', %s FLOAT' % soi_name[i]



    for team in team_list:
        team_abv = team[1]
        team_id = team[0]
        yr0_1 = 2014
        yr0_2 = 2015


        # creates team table 
        cur.execute('CREATE TABLE ' + team_abv + ' (' + col_nme + ')' )
        print(team_abv)
        print(team_id)
        # populates table by season
        for i in range(0,3):
            yr_1 = yr0_1 + i
            yr_2 = yr0_2 + i
            sn = str(yr_1) + str(yr_2)

            # pulls and organizes data
            url = 'https://statsapi.web.nhl.com/api/v1/teams/' + str(team_id) + '/stats?statsSingleseaon&season=' + sn
            data = json.loads(requests.get(url).content)
            stats = data['stats'][0]['splits'][0]['stat']
            soi = [stats.get(k) for k in soi_name]

            # makes column name statement for insertion
            col_stmt = 'season'
            for i in range(0,len(soi_name)):
                col_stmt += ', %s' % soi_name[i]

            # makes value statement for insertion
            val_stmt = '%s' % sn
            for i in range(0,len(soi)):
                val_stmt += ', %s' % soi[i]

            # inserts values
            cur.execute('INSERT INTO ' + str(team_abv) + ' (' + col_stmt + ') VALUES (' + val_stmt + ')')
            NHL_Data.commit()
      



