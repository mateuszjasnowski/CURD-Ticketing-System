import sys, subprocess, json
from tkinter import messagebox

try:
    import mysql.connector
except ImportError:
    subprocess.call([sys.executable, "-m", "pip", "install", 'mysql.connector'])
finally:
    import mysql.connector

with open('config.json') as f:
    configFile = json.load(f)

try:
  mydb = mysql.connector.connect(
    host=configFile['dbServer'],
    user=configFile['dbUserName'],
    passwd=configFile['dbUserPasswd'],
    database=configFile['dbName'],
    connect_timeout=10,
    auth_plugin='mysql_native_password'
  )
except:
  ('Cannot contect with node 1')
  messagebox.showerror(title='Błąd krytyczny',message='Nie można się połączyć z serwerm mysql')
  sys.exit()
finally:
  pass


def dataSelect(table,argument):
  dbCursor = mydb.cursor()
  query = []

  selectTable = 'SELECT * FROM '+table+' '+argument+';'
  dbCursor.execute(selectTable)

  for row in dbCursor:
    query.append(row)

  dbCursor.close()
  return(query)

def dataInsert(table,data):
  dbCursor = mydb.cursor()
  query = "INSERT INTO "+table+" VALUES (NULL,"+data+");"
  dbCursor.execute(query)
  mydb.commit()
  dbCursor.close()

def dataUpdate(table,rowIdName,ID,column,value):
  dbCursor = mydb.cursor()
  query = "UPDATE "+table+" SET "+column+" = "+value+" WHERE "+rowIdName+" = "+ID+";"
  dbCursor.execute(query)
  mydb.commit()
  dbCursor.close()

def dataDrop(table,rowIDName,ID):
  dbCursor = mydb.cursor()
  query = "DELETE FROM "+table+" WHERE "+table+"."+rowIDName+" = "+ID+";"
  dbCursor.execute(query)
  mydb.commit()
  dbCursor.close()