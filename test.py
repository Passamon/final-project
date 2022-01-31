
import psycopg2

# forming connection
def inputt(inputss):
    conn = psycopg2.connect(user="mwtnjzht",
                                    password="fVSeF78PdfVJX-NQ9RDjAYdsHejAe11n",
                                    host="john.db.elephantsql.com",
                                    port="5432",
                                    database="mwtnjzht")
    # print (inputss)
    conn.autocommit = True
 
# creating a cursor
    cursor = conn.cursor()
 
# list of rows to be inserted
# values = ["0.18","0.1","0.1","0.003","0.54","0.1","0.1","0.1","0.1","0.1","0.1","0.1"]
# executing the sql statement
    cursor.executemany("INSERT INTO initialvalue VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", inputss)
    # cursor.executemany(insert)
# sql = ''' update  initialvalue  set
#           beta = '0.002' 
#         where rho = '0.1';'''
  
# cursor.execute(sql)
 
# select statement to display output
    sql1 = '''select * from initialvalue;'''
 
# executing sql statement
    cursor.execute(sql1)
 
# fetching rows
    for i in cursor.fetchall():
        print(i)
 
# commiting changes
    conn.commit()
 
# closing connection
    conn.close()



def inputvalue():
    values = ["0.18","0.1","0.1","0.003","0.54","0.1","0.11","0.1","0.1","0.1","0.1","0.1"]
    inputs = [(values[0],values[1],values[2],values[3],values[4],values[5],values[6],values[7],values[8],values[9],values[10],values[11],)]
    return inputt(inputs)

inputvalue()




