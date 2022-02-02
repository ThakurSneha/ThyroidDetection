from flask import Flask, request
from flask import Response
import os
from flask_cors import CORS, cross_origin
import flask_monitoringdashboard as dashboard

from training_Validation_Insertion import train_validation

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
dashboard.bind(app)
CORS(app)

@app.route("/train", methods=['POST'])
@cross_origin()
def trainRouteClient():

    try:
        if request.json['folderPath'] is not None:
            path = request.json['folderPath']
            train_valObj = train_validation(path) #object initialization

            train_valObj.train_validation() #calling the training_validation function


            # trainModelObj = trainModel() #object initialization
            # trainModelObj.trainingModel() #training the model for the filesin the table


    except ValueError:

        return Response("Error Occurred! %s" % ValueError)

    except KeyError:

        return Response("Error Occurred! %s" % KeyError)

    except Exception as e:
        return Response("Error Occurred! %s" % e)
    return Response("Training Successfull!!")

port = int(os.getenv("PORT"))
if __name__ == "__main__":
    app.run(debug=True)