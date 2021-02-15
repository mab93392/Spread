import mysql.connector
import requests
import json


def teams_setup():
    # connects to database
    NHL_Data = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "fm2a85xm",
        database = 'NHL_Data',
        auth_plugin='mysql_native_password'
    )
    cur = NHL_Data.cursor()

    # creates table
    cur.execute('CREATE TABLE teams (team_id INT, team_abv VARCHAR(5))')

    #  fetches data from API then coverts to dict
    data = requests.get('https://statsapi.web.nhl.com/api/v1/teams')
    content = data.content
    data = json.loads(content)
    
    # populates table
    for i in range(0,len(data['teams'])):
        name = data['teams'][i]['abbreviation']
        id = data['teams'][i]['id']
        cur.execute("INSERT INTO teams(team_id,team_abv) VALUES(%s,'%s')" % (id,name))

    NHL_Data.commit()

