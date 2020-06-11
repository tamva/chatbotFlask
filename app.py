import numpy as np
from flask import Flask, request, make_response
import json
import pickle
from flask_cors import cross_origin

app = Flask(__name__)
model = pickle.load(open('rf.pkl', 'rb'))


@app.route('/')
def hello():
    return 'Hello World'


# geting and sending response to dialogflow
@app.route('/webhook', methods=['POST'])
@cross_origin()
def webhook():
    print('I am in!')

    req = request.get_json(silent=True, force=True)

    # print("Request:")
    # print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


# processing the request from dialogflow
def processRequest(req):

    result = req.get("queryResult")
    print('I am in!')

    parameters = result.get("parameters")

    ######## Season
    # season = parameters.get("season")
    # print(season)
    # if season == "Winter" :
    #     season = -1
    # elif season == "Spring":
    #     season = -0.33
    # elif season == "Summer":
    #     season = 0.33
    # elif season == "Fall":
    #     season = 1
    # else:
    #     season = 1
    #
    # print(season)
    ############ Age
    age = parameters.get("age")
    if (age>18 and age<36) :
        age = 0
    else :
        age = 1
    print(age)
    ############# disease
    disease = parameters.get("disease")
    if disease == 'Yes':
        disease = 0
    else:
        disease = 1
    print(disease)
    ############# accident
    accident = parameters.get("accident")
    if accident == 'Yes':
        accident = 0
    else :
        accident = 1
    print(accident)
    ############# surgery
    surgery = parameters.get("surgery")
    if surgery == 'Yes':
        surgery = 0
    else :
        surgery = 1
    print(surgery)
    ############# fever
    fever = parameters.get("fever")
    print(fever)
    if fever == 'Less' :
        fever = -1
    elif fever == 'More' :
        fever = 0
    elif fever == 'No':
        fever = 1
    else:
        fever = 1
    print(fever)
    ############# alcohol
    alcohol = parameters.get("alcohol")
    if alcohol == 'Yes':
        alcohol = 0
    else:
        alcohol = 1

    ############# smoke
    smoke = parameters.get("smoke")
    if smoke == 'Never':
        smoke = -1
    elif smoke == 'Occasional':
        smoke = 0
    else:
        smoke = 1
    ############# hourssit
    hourssit = parameters.get("hourssit")
    if hourssit <= 16:
        hourssit = 0
    else:
        hourssit = 1

    int_features = [season, age, disease, accident, surgery, fever, alcohol, smoke, hourssit]

    final_features = [np.array(int_features)]

    intent = result.get("intent").get('displayName')

    if (intent == 'Fertility'):
        prediction = model.predict(final_features)

        output = prediction[0]

        if (output == 'N'):
            diagnosis = 'Normal'
            fulfillmentText = "Your semen diagnosis seems to be  {} !".format(diagnosis)

        if (output == 'O'):
            diagnosis = 'Altered'
            fulfillmentText = "One of three semen categories seems to be  {} !".format(diagnosis)



        # log.write_log(sessionID, "Bot Says: "+fulfillmentText)
        return {
            "fulfillmentText": fulfillmentText
        }
    # else:
    #    log.write_log(sessionID, "Bot Says: " + result.fulfillmentText)


if __name__ == '__main__':
    app.run()