# Copyright 2020 Google, LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flask import Flask
import os
import uuid
import traceback
#from typing import Generator

import pg8000
import sqlalchemy
from google.cloud.sql.connector import Connector, IPTypes
from sqlalchemy.engine import URL
from sqlalchemy import inspect, text, create_engine
#from google.cloud import logging
#from google.logging.type import log_severity_pb2 as severity


#logging_client = logging.Client()
#log_name = "python_sql_iam"
#logger = logging_client.logger(log_name)

# [END cloud_sql_connector_postgres_pg8000_iam_auth]

table_name = f"books_{uuid.uuid4().hex}"


app = Flask(__name__)


@app.route("/")
def hello_world():
    name = os.environ.get("NAME", "World")
    return f"Hello {name}!"

@app.route("/postgres")
def postgres_test():
    return run_sql()



def init_connection_engine() -> sqlalchemy.engine.Engine:
    # initialize Connector object for connections to Cloud SQL
    def getconn() -> pg8000.dbapi.Connection:
        pgconname=os.environ["DB_HOST"]
        username=os.environ["DB_IAM_USER"]
        dbname=os.environ["DB_DATABASE"]
        print(f"DB_HOST: {pgconname}")
        print(f"DB_IAM_USER: {username}")
        print(f"DB_DATABASE: {dbname}")
        with Connector(
            ip_type=IPTypes.PRIVATE,
            enable_iam_auth=True,
            timeout=30) as connector:
            conn: pg8000.dbapi.Connection = connector.connect(
                pgconname,
                "pg8000",
                user=username,
                db=dbname,
                enable_iam_auth=True,
            )
            print(f"connector returning : {conn}")
            return conn

    # create SQLAlchemy connection pool
    pool = sqlalchemy.create_engine(
        "postgresql+pg8000://",
        creator=getconn,
        execution_options={"isolation_level": "AUTOCOMMIT"},
        pool_size=10,
        max_overflow=20,
        pool_timeout=100,
        pool_recycle=1800,
    )
    pool.dialect.description_encoding = None
    print(f"Pool returning : {pool}")
    return pool


# [END cloud_sql_connector_postgres_pg8000_iam_auth]


def run_sql():
    try:
        #logger.log_text("The Cloud Function has been triggered!", severity="INFO")

        print("Creating connection pool")
        pool = init_connection_engine()
        print("Created connection pool")

        select_stmt1 = sqlalchemy.text(f"SELECT NOW() as now")
        select_stmt2 = sqlalchemy.text(f"SELECT current_user as user")
        select_stmt3 = sqlalchemy.text(f"SELECT session_user as user")

        select_result ="";
        print("Connecting to DB")
        with pool.connect() as db_conn:
            print("Connected to DB")
            print(f"Executing {select_stmt1}")
            row = db_conn.execute(select_stmt1).fetchone()
            select_result +="Now:{}".format(row.now)
            print(row)
            print(f"Executing {select_stmt2}")
            row = db_conn.execute(select_stmt2).fetchone()
            select_result +="; User: {}".format(row.user)
            print(row)
            print(f"Executing {select_stmt3}")
            row = db_conn.execute(select_stmt3).fetchone()
            select_result +="; User: {}".format(row.user)
            print(row)
            print("closing connection")
            db_conn.close()
            print("Closed connection")
        return select_result
    except:
#       logger.log_text("This is a warning from 'python_application_name'!", severity=severity.ERROR)
        print('Exception while sql operation')
        # printing stack trace
        traceback.print_exc()
    finally:
        print('finally disposing')
        pool.dispose()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
# [END cloudbuild_python_flask]
