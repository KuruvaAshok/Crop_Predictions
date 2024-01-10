from flask import Flask, render_template,jsonify,request 
import pickle
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/prediction',methods = ['GET','POST'])
def prediction():
    if request.method == 'POST':
        nitro = request.form.get('nitrogen')
        phos = request.form.get('phosphorus')
        potash = request.form.get('potassium')
        tem = request.form.get('temperature')
        humi = request.form.get('humidity')
        ph = request.form.get('ph')
        rainfall = request.form.get('rainfall')
        print(nitro,phos,potash,tem,humi,ph,rainfall)
        with open('model.pkl','rb') as model_file:
            mlmodel = pickle.load(model_file)
        res = mlmodel.predict([[float(nitro),float(phos),float(potash),float(tem),float(humi),float(ph),float(rainfall)]])
        print(res)
        return render_template("result.html",res=res[0])        
    else:
        return render_template('prediction.html')

#@app.route('/show-data')
#def showdata():
#   return render_template('showdata.html')

if __name__=='__main__':
    app.run(host = '0.0.0.0',port = 3386)
    #app.run()
   