import random
import time
from datetime import datetime

from routes import execute_sql

if __name__ == '__main__':
    hour6 = 6 * 3600 
    sql = "SELECT * FROM environment order by id desc limit 1"
    results = execute_sql(sql, "select")
    print(results)
    
    base = datetime(results[0][6], results[0][7], results[0][8], results[0][9]).timestamp()
    while True:
        base += hour6
        now = datetime.fromtimestamp(base)
        print(now)
        sql = "SELECT * FROM sensor"
        sensors = execute_sql(sql, "select")
        for sensor in sensors:
            sensor = list(sensor)
            sensor_id = sensor[0]
            data_types = sensor[4]
            temperature = ""
            humidity = ""
            combustibleGas = ""
            smoke = ""
            if "temperature" in data_types:
                temperature = random.randint(0, 35)
            if "humidity" in data_types:
                humidity = random.randint(0, 35)
            if "combustibleGas" in data_types:
                combustibleGas = random.randint(0, 35)
            if "smoke" in data_types:
                smoke = random.randint(0, 35)
            sql = (
                "INSERT INTO environment (sensor_id,temperature,humidity,combustibleGas,smoke,year, month, date, "
                "hour) VALUES ('%s','%s','%s','%s','%s','%s','%s', "
                "'%s','%s') " % (
                    sensor_id, temperature, humidity, combustibleGas, smoke, now.strftime('%Y'), now.strftime('%m'),
                    now.strftime('%d'),
                    now.strftime('%H'))
            )
            execute_sql(sql, "insert")
        time.sleep(60)
