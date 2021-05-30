import time

from routes import execute_sql

if __name__ == '__main__':
    while True:
        sql = "SELECT * FROM sensor"
        results = execute_sql(sql, "select")
        sensor_list = []
        for result in results:
            result = list(result)
            if result[6]:
                if result[3]-1 <= 10:
                    sql = (
                        "UPDATE sensor SET ip = '%s', gps = '%s', energy = '%s', data_types = '%s', neighborhood_nodes = '%s', "
                        "status = '%s' "
                        "Where sensor_id = %s "
                        % (result[1], result[2], result[3], result[4], result[5], 0, result[0])
                    )
                    execute_sql(sql, "update")
                else:
                    sql = (
                        "UPDATE sensor SET ip = '%s', gps = '%s', energy = '%s', data_types = '%s', neighborhood_nodes = '%s', "
                        "status = '%s' "
                        "Where sensor_id = %s "
                        % (result[1], result[2], result[3]-1, result[4], result[5], result[6], result[0])
                    )
                    execute_sql(sql, "update")
        time.sleep(60)
