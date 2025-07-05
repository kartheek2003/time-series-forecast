from flask import Flask , render_template , request,send_file
import pandas as pd
import os

from src.time_series.components.prediction import PredictionComponent
from src.time_series.config.configuration import ConfigurationManager
from src.time_series.entity.config_entity import Prediction

app = Flask(__name__)

@app.route("/train",methods = ['POST','GET'])
def trainRoute():
    os.system("python main.py")
    return "Training done successfully"

@app.route("/",methods = ['POST','GET'])
def index():
    if request.method == "POST" :
        try : 
            file = request.files['file']
            model_type = request.form['model']
            periods = int(request.form['periods'])

            df = pd.read_csv(file , parse_dates= ['Month'],index_col='Month')
            config = ConfigurationManager()
            predict_config = config.get_prediction_config()
            predictor = PredictionComponent(config= predict_config)


            if model_type == "prophet":
                buf = predictor.prediction_with_prophet(data=df , periods = periods)

            else :
                buf = predictor.prediction_with_auto_arima(data=df , periods= periods)
                
            return send_file(buf, mimetype='image/png')

        except Exception as e:
            return render_template("index.html" , error = str(e))
        
    return render_template("index.html")
    


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)