import pandas as pd
from flask import Flask,render_template, request
from flask_mysqldb import MySQL
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'tt001031'
app.config['MYSQL_DB'] = 'test'
app.config['TIME_ZONE'] = 'Asia/Kuala_Lumpur'


 
mysql = MySQL(app)
 
@app.route('/getdata', methods = ['POST'])
def getdata():
    cursor = mysql.connection.cursor()
    content = request.json
    contentdate = content['date']
    date = datetime(int(contentdate[0:4]), int(contentdate[5:7]), int(contentdate[8:10]), 0, 0, 0)
    enddate = datetime(int(contentdate[0:4]), int(contentdate[5:7]), int(contentdate[8:10]), 23, 59, 59)
    date = date.strftime("%Y-%m-%d %H:%M:%S")
    enddate = enddate.strftime("%Y-%m-%d %H:%M:%S")
    print(date)
    # cursor.execute('''SELECT * FROM leftarm WHERE timestamp >= %s AND timestamp <= %s''',(date, enddate))
    cursor.execute('SELECT * FROM leftarm')
    data = cursor.fetchall()
    print("The Array is: ", data)
    cursor.close()
    return {'data': data}, 200

@app.route('/postdata', methods = ['POST'])
def postdata():
    content = request.json

    acc_x = content['acc_x']
    acc_y = content['acc_y']
    acc_z = content['acc_z']
    gyro_x = content['gyro_x']
    gyro_y = content['gyro_y']
    gyro_z = content['gyro_z']
    EMG = content['EMG']
    Seq = content['Seq']
    # print(r1)

    cursor = mysql.connection.cursor()
    cursor.execute(''''''''' INSERT INTO leftarm (acc_x,acc_y,acc_z,gyro_x,gyro_y,gyro_z,EMG,Seq) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)''''''''',(acc_x,acc_y,acc_z,gyro_x,gyro_y,gyro_z,EMG,Seq))
    mysql.connection.commit()
    cursor.close()
    return {'message': "done"}, 200

@app.route('/loaddata', methods = ['POST'])
def loaddata():
    content = request.json
    flag = content['flag']
    print(111)
    if flag == 1:
        data = pd.read_csv('leftarm.csv')  # read local CSV
        data1 = data.to_dict()  # convert dataframe to dict
        cursor = mysql.connection.cursor()
        print(1111)
        for i in range(len(data1['Id'])):
            user_info = {
                0: data1['Id'][i],
                1: data1['timestamp'][i],
                2: data1['acc_x'][i],
                3: data1['acc_y'][i],
                4: data1['acc_z'][i],
                5: data1['gyro_x'][i],
                6: data1['gyro_y'][i],
                7: data1['gyro_z'][i],
                8: data1['EMG'][i],
                9: data1['Seq'][i]

            }
            print(user_info)
            timestamp = user_info[1]
            acc_x = user_info[2]
            acc_y = user_info[3]
            acc_z = user_info[4]
            gyro_x = user_info[5]
            gyro_y = user_info[6]
            gyro_z = user_info[7]
            EMG = user_info[8]
            Seq = user_info[9]
            cursor.execute(
               ''''''''' INSERT INTO leftarm (timestamp,acc_x,acc_y,acc_z,gyro_x,gyro_y,gyro_z,EMG,Seq) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)''''''''',
               (timestamp,acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z, EMG, Seq))
            mysql.connection.commit()
            print(user_info)

        # print(r1)

        cursor.close()
        return {'message': "done"}, 200
    else :
        return {'message': "close"},200


app.run(host='localhost', port=5000)