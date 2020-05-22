import sys, subprocess
from tkinter import messagebox

try:
    import mysql.connector
except ImportError:
    subprocess.call([sys.executable, "-m", "pip", "install", 'mysql.connector'])
finally:
    import mysql.connector
'''
try:
  mydb = mysql.connector.connect(
    host="localhost",
    user="curd_bot",
    passwd="96y2YkmrmDbLEjkI",
    database="curd",
    connect_timeout=10,
    auth_plugin='mysql_native_password'
  )
except:
  print('Cannot contect with node 1')
  messagebox.showerror(title='Błąd krytyczny',message='Nie można się połączyć z serwerm #1')
  try:
    mydb = mysql.connector.connect(
      host="25.2.41.178",
      user="curd_bot",
      passwd="96y2YkmrmDbLEjkI",
      database="curd",
      connect_timeout=10
    )
  except:
    print('Cannot contect with node 2 nither')
    messagebox.showerror(title='Błąd krytyczny',message='Nie można się połączyć z serwerm #2')
    try:
      mydb = mysql.connector.connect(
        host="192.168.0.150",
        user="curd_bot",
        passwd="96y2YkmrmDbLEjkI",
        database="curd",
        connect_timeout=10
      )
    except:
      quit('Cannot contect with node 3 nither')
      messagebox.showerror(title='Błąd krytyczny',message='Nie można się połączyć z serwerm #3')
      sys.exit()'''


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