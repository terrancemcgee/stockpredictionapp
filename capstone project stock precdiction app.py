from pyspark.sql import SQLContext
import base64
import pandas as pd
from google.cloud import bigquery
from sklearn.preprocessing import MinMaxScaler
from tensorflow import keras
from tensorflow.python.lib.io import file_io
import pymysql
def iex_predict(event, context):
 “””Triggered from a message on a Cloud Pub/Sub topic.
 Args:
 event (dict): Event payload.
 context (google.cloud.functions.Context): Metadata for the event.
 “””
 pubsub_message = base64.b64decode(event[‘data’]).decode(‘utf-8’)
 stock_symbol = “SPY”
 
 query = ‘select * from iex_history.’ + stock_symbol
 client = bigquery.Client()
 
 df = (
 client.query(query)
 .result()
 .to_dataframe()
 )
 
 scaler = MinMaxScaler()
 tmp = scaler.fit_transform(df)
 
 model_file = file_io.FileIO(‘gs://yourbucket/model.h5’, mode=’rb’)
 temp_model_location = ‘./temp_model.h5’
 temp_model_file = open(temp_model_location, ‘wb’)
 temp_model_file.write(model_file.read())
 temp_model_file.close()
 model_file.close()
 model = keras.models.load_model(temp_model_location)
 
 result = model.predict(tmp)
 scaler.fit(df.avg.values.reshape(-1,1))
 result = scaler.inverse_transform(result.reshape(-1,1))
 result = [stock_symbol, df.tail(1).avg.values[0], result]
 
 cnx = pymysql.connect(user=’usr’, password=’pwd’,
 host=’host’, db=’iex_predict’)
 
 with cnx.cursor() as cursor:
   cursor.executemany(‘INSERT INTO iex_predict values (%s, %s, %s);’, results)
   cnx.commit()
 cnx.close()
