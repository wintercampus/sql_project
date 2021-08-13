# current output:
# PS C:\Users\huiwa\Documents>  c:; cd 'c:\Users\huiwa\Documents'; & 'C:\Users\huiwa\AppData\Local\Microsoft\WindowsApps\python3.9.exe' 'c:\Users\huiwa\.vscode\extensions\ms-python.python-2021.7.1060902895\pythonFiles\lib\python\debugpy\launcher' '56273' '--' 'c:\Users\huiwa\Documents\Untitled-1.py' 
#check out
#show inventory
#show transcation
#('macbook_pro', 10)
#

# I am using sqlite3 now because it is built-in. I will switch to MYSQL when the basic logic is ready.

# https://docs.python.org/3/library/sqlite3.html
# sqlite3 — DB-API 2.0 interface for SQLite databases¶
import sqlite3

db = 'warehouse1.db'

def create_db():
    conn = sqlite3.connect(db, timeout=1)
    curs = conn.cursor()

    # How do I check in SQLite whether a table exists? 
    # https://stackoverflow.com/questions/1601151/how-do-i-check-in-sqlite-whether-a-table-exists
    # If you're using SQLite version 3.3+ you can easily create a table with:
    table_name = "inventory"
    curs.execute('''CREATE TABLE IF NOT EXISTS inventory (name VARCHAR(20) PRIMARY KEY, count INT)''')
    
    # start with 10 items with 0 inventory each
    curs.execute('INSERT OR REPLACE INTO inventory VALUES("iphone_1", 0)')
    curs.execute('INSERT OR REPLACE INTO inventory VALUES("iphone_2", 0)')
    curs.execute('INSERT OR REPLACE INTO inventory VALUES("iphone_3", 0)')
    curs.execute('INSERT OR REPLACE INTO inventory VALUES("iphone_4", 0)')
    curs.execute('INSERT OR REPLACE INTO inventory VALUES("iphone_5", 0)')
    curs.execute('INSERT OR REPLACE INTO inventory VALUES("iphone_6", 0)')
    curs.execute('INSERT OR REPLACE INTO inventory VALUES("iphone_7", 0)')
    curs.execute('INSERT OR REPLACE INTO inventory VALUES("iphone_8", 0)')
    curs.execute('INSERT OR REPLACE INTO inventory VALUES("iphone_9", 0)')
    curs.execute('INSERT OR REPLACE INTO inventory VALUES("iphone_x", 0)')
    
    conn.commit()
    conn.close()

def show_inventory():
    print("show inventory")
    conn = sqlite3.connect(db, timeout=1)
    curs = conn.cursor()
    curs.execute('SELECT * from inventory ORDER BY count DESC')
    curs.fetchall()
    conn.commit()
    conn.close()

def show_transcation():
    print("show transcation")
    conn = sqlite3.connect(db, timeout=1)
    curs = conn.cursor()
    # https://stackoverflow.com/questions/12867140/python-mysqldb-get-the-result-of-fetchall-in-a-list
    # Python MySQLDB: Get the result of fetchall in a list
    #rows = curs.execute('SELECT * from inventory ORDER BY name')
    #conn.commit()
    #conn.close()
    #print(rows)
    for row in curs.execute('SELECT * FROM inventory ORDER BY name'):
        print(row) 

def check_in():
    print("check in")
    conn = sqlite3.connect(db, timeout=1)
    curs = conn.cursor()
    curs.execute('INSERT INTO inventory VALUES("macbook_pro", 10)')
    conn.commit()
    conn.close()

def check_out():
    print("check out")
    pass    


create_db()
#check_in()
check_out()
show_inventory()
show_transcation()
