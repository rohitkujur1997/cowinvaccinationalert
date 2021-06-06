from cowin_api import CoWinAPI
cowin = CoWinAPI()

def createDistrictJSON():
    for i in range(1,37):
        file=open("districts/"+str(i)+".json","w")
        d = str(cowin.get_districts(i)['districts'])
        d=d.replace("'", '"')
        file.write(str(d))
        file.close()

def createStateJSON():
    file=open("states.json","w")
    states = str(cowin.get_states()['states'])
    states=states.replace("'", '"')
    file.write(str(states))
    file.close()

createDistrictJSON()
createStateJSON()