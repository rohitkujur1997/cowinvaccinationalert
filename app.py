from flask import Flask,render_template,jsonify,request
from wtforms import SelectField
from flask_wtf import FlaskForm
import json
from cowin_api import CoWinAPI
cowin = CoWinAPI()

app = Flask(__name__)
app.config['SECRET_KEY']='rk'

#Data
with open("states.json") as s:
    states=json.load(s)

class Form(FlaskForm):
    state = SelectField('state',choices=[])
    district = SelectField('district',choices=[])

@app.route('/',methods=['GET','POST'])
def index():
    form = Form()
    form.state.choices=[states[i]['state_name'] for i in range(len(states))]
    #ices=[districts[j]['district_name'] for j in range]
    '''
    if request.method == 'POST':
        print(form.district.data)
    '''
    return render_template('index.html',form=form)

@app.route('/api/v1/<string:get_district>')
def districtbystate(get_district):
    state_id=[s['state_id'] for s in states if s['state_name']==get_district][0]
    with open("districts/"+str(state_id)+".json") as d:
        d=json.load(d)
    districtArray=[]
    ''''''
    for i in range(len(d)):
        #print(d[i]['district_name'])
        districtObj={}
        districtObj['code']='<option value='+str(d[i]['district_id'])+'>'+d[i]['district_name']+'</option>'
        '''
        districtObj['id']=d[i]['district_id']
        districtObj['districtname']=d[i]['district_name']
        districtObj['statename']=get_district
        districtObj['stateid']=state_id
        '''
        districtArray.append(districtObj)
    return jsonify({'districtstate': districtArray})

@app.route('/api/v1/<district_id>/<above18>/<above45>')
def avaibality(district_id,above18,above45):
    if above18=='false' and above45=='true':
        min_age_limit=45
    else:
        min_age_limit=18
    available_centers = cowin.get_availability_by_district(district_id)
    a=available_centers['centers']
    availabilityArray=[]
    for i in range(len(a)):
        if (a[i]['sessions'][0]['available_capacity'])>0:
            if (a[i]['sessions'][0]['min_age_limit'])==min_age_limit:
                availabilityObj={}
                availabilityObj['name_address']=a[i]['name']+", "+a[i]['address']+", "+a[i]['district_name']+", "+str(a[i]['pincode'])
                availabilityObj['fee_type']=a[i]['fee_type']
                availabilityObj['min_age_limit']=a[i]['sessions'][0]['min_age_limit']
                availabilityObj['vaccine']=a[i]['sessions'][0]['vaccine']
                availabilityObj['available_capacity_doses']=a[i]['sessions'][0]['available_capacity']
                availabilityObj['available_capacity_dose1']=a[i]['sessions'][0]['available_capacity_dose1']
                availabilityObj['available_capacity_dose2']=a[i]['sessions'][0]['available_capacity_dose2']
                availabilityArray.append(availabilityObj)       
    return jsonify({'centeravailability': availabilityArray})

if __name__ == '__main__':
    app.run(debug=True)