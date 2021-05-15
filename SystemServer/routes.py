# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file: routes.py
# @date: 2021/04/24
"""
这里定义路由: https://dormousehole.readthedocs.io/en/stable/quickstart.html#id6
模板使用: https://dormousehole.readthedocs.io/en/stable/quickstart.html#id10
如果路由太多可以使用蓝图来进行分组: https://dormousehole.readthedocs.io/en/stable/tutorial/views.html

@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello():
    return 'Hello, World'

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return 'Subpath %s' % subpath
"""
import time
from datetime import datetime
import os
import sqlite3
import random
from flask import Flask, request, json
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)

if not os.path.exists("database/db.sqlite"):
    if not os.path.exists("database"):
        os.mkdir("database")
    conn = sqlite3.connect("database/db.sqlite")
    with open("schema.sql", "rb") as f:
        conn.executescript(f.read().decode("utf8"))

database_dir = os.path.join(os.getcwd(), "database", "db.sqlite")


def execute_sql(sql, choice):
    """
    执行sql语句
    :param sql:
    :param choice: 'select'， 'update', 'insert', 'delete'
    :return:
    """
    my_db = sqlite3.connect(database_dir)
    my_cursor = my_db.cursor()
    my_cursor.execute(sql)
    results = []
    if choice == "select":
        results = my_cursor.fetchall()
    else:
        my_db.commit()
    my_cursor.close()
    my_db.close()
    return results


@app.route("/")
def hello_world():
    sensor_id = 2
    ip = "192.168.0.111"
    gps = ",".join(str(i) for i in [2, 8])
    energy = 90
    data_types = ",".join(["temperature", "humidity"])
    neighborhood_nodes = ",".join(str(i) for i in [1])

    return "Hello, World!"


@app.route("/login", methods=["POST"])
def login():
    data = json.loads(request.form["data"])
    print(data)
    account = data["account"]
    password = data["password"]
    sql = "SELECT * FROM identity WHERE account = '%s'" % account
    results = execute_sql(sql, "select")
    if results:
        if results[0][2] == password:
            return {"flag": 1, "message": "login success!", "verification": "jl"}
    return {"flag": 0, "message": "wrong account or password!"}


@app.route("/update_sensor", methods=["POST"])
def update_sensor():
    data = json.loads(request.form["data"])
    print(data)
    sensor_id = data["sensor_id"]
    ip = data["ip"]
    gps = data["gps"]
    energy = data["energy"]
    data_types = data["data_types"]
    neighborhood_nodes = data["neighborhood_nodes"]
    status = data["status"]
    print(status)
    sql = "SELECT * FROM sensor WHERE sensor_id = '%s'" % sensor_id
    results = execute_sql(sql, "select")
    if results:
        print(321)
        sql = (
            "UPDATE sensor SET ip = '%s', gps = '%s', energy = '%s', data_types = '%s', neighborhood_nodes = '%s', "
            "status = '%s' "
            "Where sensor_id = %s "
            % (ip, gps, energy, data_types, neighborhood_nodes, status, sensor_id)
        )
        execute_sql(sql, "update")
        return {"flag": 1, "message": "success!"}
    else:
        sql = (
            "INSERT INTO sensor (sensor_id,ip,gps,energy,data_types,neighborhood_nodes,status) VALUES ('%s','%s','%s',"
            "'%s','%s', "
            "'%s','%s') "
            % (sensor_id, ip, gps, energy, data_types, neighborhood_nodes, status)
        )
        execute_sql(sql, "insert")
        return {"flag": 1, "message": "success!"}


@app.route("/get_sensor_list", methods=["POST"])
def get_sensor_list():
    sql = "SELECT * FROM sensor"
    results = execute_sql(sql, "select")
    sensor_list = []
    for result in results:
        result = list(result)
        sensor_list.append(
            {"sensor_id": result[0], "ip": result[1], "gps": result[2], "energy": result[3], "data_types": result[4],
             "neighborhood_nodes": result[5], "status": result[6]})
    # sql = "SELECT sensor_id FROM sensor WHERE data_types LIKE '%humidity%'"
    # results = execute_sql(sql, "select")
    # print(results[0][0])
    return {"sensor_list": sensor_list}


@app.route("/insert_environment", methods=["POST"])
def insert_environment():
    data = json.loads(request.form["data"])
    print(data)
    sensor_id = data["sensor_id"]
    temperature = data["temperature"]
    humidity = data["humidity"]
    year = data["year"]
    month = data["month"]
    date = data["date"]
    hour = data["hour"]
    sql = (
        "INSERT INTO environment (sensor_id,temperature,humidity,year, month, date, hour) VALUES ('%s','%s','%s',"
        "'%s','%s','%s','%s') " % (sensor_id, temperature, humidity, year, month, date, hour)
    )
    execute_sql(sql, "insert")
    return {"flag": 1, "message": "success!"}


# @app.route("/get_environment_list", methods=["POST"])
# def get_environment_list():
#     data = json.loads(request.form["data"])
#     print(data)
#     sensor_id = data["sensor_id"]
#     sql = "SELECT * FROM environment WHERE sensor_id = '%s'" % sensor_id
#     results = execute_sql(sql, "select")
#     environment_list = []
#     for result in results:
#         result = list(result)
#         environment_list.append(
#             {"sensor_id": result[0], "temperature": result[1], "humidity": result[2], "record_time": result[3], })
#     return {"environment_list": environment_list}


@app.route("/get_humidity", methods=["POST"])
def get_humidity():
    data = json.loads(request.form["data"])
    print(data)
    year = data["year"]
    month = data["month"]
    date = data["date"]
    humidity_data = {
        "sensors": [],
        "values": []
    }

    sql = "SELECT sensor_id FROM sensor WHERE data_types LIKE '%humidity%'"
    results = execute_sql(sql, "select")
    print(results[0][0])
    for result in results:
        humidity_data["sensors"].append(result[0])
        sql = "SELECT * FROM environment WHERE sensor_id = '%s' " % result[0]
        results2 = execute_sql(sql, "select")
        x = []
        for result2 in results2:
            result2 = list(result2)
            y = str(result2[4]) + "/" + str(result2[5]) + "/" + str(result2[6]) + " " + str(result2[7]) + ":00:00"

            x.append([y, result2[3]])
        humidity_data["values"].append(x)
    print

    return {"humidity_data": humidity_data}


@app.route("/get_temperature", methods=["POST"])
def get_temperature():
    data = json.loads(request.form["data"])
    print(data)
    year = data["year"]
    month = data["month"]
    date = data["date"]
    temperature_data = {
        "sensors": [],
        "values": []
    }

    sql = "SELECT sensor_id FROM sensor WHERE data_types LIKE '%temperature%'"
    results = execute_sql(sql, "select")
    print(results[0][0])
    for result in results:
        temperature_data["sensors"].append(result[0])
        sql = "SELECT * FROM environment WHERE sensor_id = '%s' " % result[0]
        results2 = execute_sql(sql, "select")
        x = []
        for result2 in results2:
            result2 = list(result2)
            y = str(result2[4]) + "/" + str(result2[5]) + "/" + str(result2[6]) + " " + str(result2[7]) + ":00:00"

            x.append([y, result2[2]])
        temperature_data["values"].append(x)
    print

    return {"temperature_data": temperature_data}

# @app.route("/qwe", methods=["GET"])
# def qwe():
#     hour6 = 6 * 3600
#     base = datetime(2021, 1, 1).timestamp()
#     for i in range(500):
#         base += hour6
#         now = datetime.fromtimestamp(base)
# 
#         sql = (
#             "INSERT INTO environment (sensor_id,temperature,year, month, date, hour) VALUES ('%s','%s','%s','%s',"
#             "'%s','%s') " % (
#                 1, random.randint(0, 35), now.strftime('%Y'), now.strftime('%m'), now.strftime('%d'),
#                 now.strftime('%H'))
#         )
#         execute_sql(sql, "insert")
# 
#     base = datetime(2021, 1, 1).timestamp()
#     for i in range(500):
#         base += hour6
#         now = datetime.fromtimestamp(base)
# 
#         sql = (
#             "INSERT INTO environment (sensor_id,temperature,year, month, date, hour) VALUES ('%s','%s','%s','%s',"
#             "'%s','%s') " % (
#                 2, random.randint(0, 35), now.strftime('%Y'), now.strftime('%m'), now.strftime('%d'),
#                 now.strftime('%H'))
#         )
#         execute_sql(sql, "insert")
# 
#     base = datetime(2021, 1, 1).timestamp()
#     for i in range(500):
#         base += hour6
#         now = datetime.fromtimestamp(base)
# 
#         sql = (
#             "INSERT INTO environment (sensor_id,humidity,year, month, date, hour) VALUES ('%s','%s','%s','%s','%s',"
#             "'%s') " % (
#                 3, random.randint(0, 35), now.strftime('%Y'), now.strftime('%m'), now.strftime('%d'),
#                 now.strftime('%H'))
#         )
#         execute_sql(sql, "insert")
# 
#     base = datetime(2021, 1, 1).timestamp()
#     for i in range(500):
#         base += hour6
#         now = datetime.fromtimestamp(base)
# 
#         sql = (
#             "INSERT INTO environment (sensor_id,humidity,year, month, date, hour) VALUES ('%s','%s','%s','%s','%s',"
#             "'%s') " % (
#                 4, random.randint(0, 35), now.strftime('%Y'), now.strftime('%m'), now.strftime('%d'),
#                 now.strftime('%H'))
#         )
#         execute_sql(sql, "insert")
# 
#     base = datetime(2021, 1, 1).timestamp()
#     for i in range(500):
#         base += hour6
#         now = datetime.fromtimestamp(base)
# 
#         sql = (
#             "INSERT INTO environment (sensor_id,temperature,humidity,year, month, date, hour) VALUES ('%s','%s','%s',"
#             "'%s','%s','%s','%s') " % (
#                 5, random.randint(0, 35), random.randint(20, 35), now.strftime('%Y'), now.strftime('%m'),
#                 now.strftime('%d'),
#                 now.strftime('%H'))
#         )
#         execute_sql(sql, "insert")
# 
#     base = datetime(2021, 1, 1).timestamp()
#     for i in range(500):
#         base += hour6
#         now = datetime.fromtimestamp(base)
#         sql = (
#             "INSERT INTO environment (sensor_id,temperature,humidity,year, month, date, hour) VALUES ('%s','%s','%s',"
#             "'%s','%s','%s','%s') " % (
#                 6, random.randint(0, 35), random.randint(20, 35), now.strftime('%Y'), now.strftime('%m'),
#                 now.strftime('%d'),
#                 now.strftime('%H'))
#         )
#         execute_sql(sql, "insert")
# 
#     return "123"
