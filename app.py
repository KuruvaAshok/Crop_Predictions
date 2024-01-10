from flask import Flask, render_template,jsonify,request 
import pickle
import sqlite3
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
        conn = sqlite3.connect('cropdata.db')
        cur = conn.cursor()
        cur.execute(f'''Insert into crop values ({nitro},{phos},{potash},{tem},{humi},{ph},{rainfall},'{res[0]}')''')
        conn.commit()
        return render_template("result.html",res=res[0])        
    else:
        return render_template('prediction.html')

@app.route('/showdata',methods=['GET','POST'])
def showdata():
    conn =sqlite3.connect('cropdata.db')
    cur = conn.cursor()
    cur.execute("select * from crop")
    x = cur.fetchall()
    li = []
    for i in x:
        p = {}
        p['Nitrogen']= i[0]
        p['Phosporus']= i[1]
        p['Potassium']= i[2]
        p['Temparature']= i[3]
        p['Humidity']= i[4]
        p['Ph']= i[5]
        p['Rainfall']= i[6]
        p['Result']= i[7]
        li.append(p)       
    return render_template('showdata.html',data = li)

if __name__=='__main__':
    app.run(host = '0.0.0.0',port = 3386)
    # app.run(debug=False)
    
   

