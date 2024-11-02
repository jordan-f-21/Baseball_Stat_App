import matplotlib.pyplot as plt
import matplotlib as plt2
import mlbstatsapi
from flask import Flask, render_template, request, Response
from io import BytesIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
plt2.use('Agg')

mlb = mlbstatsapi.Mlb()

app = Flask(__name__)

categories = [
              "gamesplayed", "flyouts", "groundouts", "airouts", "runs", "doubles", "triples", "homeruns", "strikeouts", "baseonballs", 
              "intentionalwalks", "hits", "hitbypitch", "avg", "atbats", "obp", "slg", "ops", "caughtstealing", "stolenbases", 
              "stolenbasepercentage", "groundintodoubleplay", "groundintotripleplay", "numberofpitches", "plateappearances", "totalbases",
              "rbi", "leftonbases", "sacbunts", "sacflies", "babip", "groundoutstoairouts", "catchersinterference", "atbatsperhomerun"
             ]
stats = ['season']
groups = ['hitting']

@app.route('/')
def index():
    return render_template('index.html')

def returnStat(index, playerID, season):
    stat_dict = mlb.get_player_stats(playerID, stats=stats, groups=groups, **season)
    playerData = (stat_dict['hitting']['season'].__dict__['splits'])
    playerStatData = list(playerData[0].stat.__dict__.items())[index]
    key, value = playerStatData  
    return value

def setX_and_setY_axes(index, playerID):
    seasonList = [2020, 2021, 2022, 2023, 2024]
    statList = []
    for year in seasonList:
        params = {'season': year}
        statList.append(returnStat(index, playerID, params))
    return seasonList, statList

def getId(name):
    return mlb.get_people_id(name)[0]

def getStat(element):
    for stat in categories:
        if stat == element:
            return categories.index(stat)

@app.route('/graph', methods=['POST', 'GET'])  
def showGraph():
    if request.method == 'POST':
        stat = request.form['stat']
        playerName = request.form['name']
        x, y = setX_and_setY_axes(getStat(stat), getId(playerName))
        '''
        plt.bar(x, y)
        plt.title(playerName + "'s " + stat)
        plt.xlabel("Season")
        plt.ylabel("# of " + stat)
        plt.show()
        '''
        fig, ax = plt.subplots()
        ax.bar(x, y)
        ax.set_title(playerName + "'s " + stat)
        ax.set_xlabel("Season")
        ax.set_ylabel("# of " + stat)
        output = BytesIO()
        FigureCanvas(fig).print_png(output)
    
        # Return the plot as a PNG image
        return Response(output.getvalue(), mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)

