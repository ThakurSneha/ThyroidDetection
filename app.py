from flask import Flask, render_template, request
from flask import Response
import os
from flask_cors import CORS, cross_origin
from predictFromModel import prediction
from trainingModel import trainModel
import flask_monitoringdashboard as dashboard
from training_Validation_Insertion import train_validation

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
dashboard.bind(app)
CORS(app)


@app.route("/", methods=["GET",'POST'])
@cross_origin()
def Home():
    return render_template("index.html")

@app.route("/train", methods=['POST'])
@cross_origin()
def trainRouteClient():

    try:
        if request.json['folderPath'] is not None:
            path = request.json['folderPath']
            train_valObj = train_validation(path) #object initialization

            train_valObj.train_validation() #calling the training_validation function


            trainModelObj = trainModel() #object initialization
            trainModelObj.trainingModel() #training the model for the filesin the table


    except ValueError:

        return Response("Error Occurred! %s" % ValueError)

    except KeyError:

        return Response("Error Occurred! %s" % KeyError)

    except Exception as e:
        return Response("Error Occurred! %s" % e)
    return Response("Training Successfull!!")


@app.route("/predict", methods = [ 'POST' ])
@cross_origin()
def predict():
    if request.method == "POST":
        try:
            if request.form:
                data_req = dict(request.form)
                data = data_req.values()
                data = [list(data)]
                pred = prediction(data)

                # predicting the output
                result = pred.predictionFromModel()
                return render_template("result.html",result=result[0])
            else:
                return "none"
        except Exception as e:
            error = {'error': e}
            return render_template("404.html",error=error)
    else:
        return render_template('404.html', error = "Something went wrong!! Try again.")


if __name__ == "__main__":
    app.run(debug=True)