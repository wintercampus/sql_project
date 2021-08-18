# I am using sqlite3 now because it is built-in. I will switch to MYSQL when the basic logic is ready.

# https://docs.python.org/3/library/sqlite3.html
# sqlite3 — DB-API 2.0 interface for SQLite databases¶
import sqlite3
from datetime import datetime

db = 'warehouse19.db'

items = ["iphone_1", "iphone_2", "iphone_3", "iphone_4", "iphone_5",
         "iphone_6", "iphone_7", "iphone_8", "iphone_9", "iphone_x"]

def create_db():
    conn = sqlite3.connect(db, timeout=1)
    curs = conn.cursor()

    # How do I check in SQLite whether a table exists? 
    # https://stackoverflow.com/questions/1601151/how-do-i-check-in-sqlite-whether-a-table-exists
    # If you're using SQLite version 3.3+ you can easily create a table with:
    table_name = "inventory"
    curs.execute('''CREATE TABLE IF NOT EXISTS inventory (name VARCHAR(20) PRIMARY KEY, count INT)''')

    # https://stackoverflow.com/questions/14461851/how-to-have-an-automatic-timestamp-in-sqlite
    curs.execute('''CREATE TABLE IF NOT EXISTS transcation (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                            name VARCHAR(20),
                                                            operation VARCHAR(20),
                                                            count INT,
                                                            datetime VARCHAR(40))''')
    # delete all existing transcations                                                               
    curs.execute('''DELETE FROM transcation''')

    # start with 10 items with 0 inventory each
    print("Initialize inventory")
    for item in items:
        insert_cmd = 'INSERT OR REPLACE INTO inventory VALUES("%s", 0)' % item
        print(insert_cmd)
        curs.execute(insert_cmd)
    print("done")
    conn.commit()
    conn.close()

def show_transcation():
    print("show transcation")
    conn = sqlite3.connect(db, timeout=1)
    curs = conn.cursor()
    for row in curs.execute('SELECT * FROM transcation ORDER BY id'):
        print(row) 
    conn.commit()
    conn.close()

def show_inventory():
    print("show inventory")
    conn = sqlite3.connect(db, timeout=1)
    curs = conn.cursor()
    # https://stackoverflow.com/questions/12867140/python-mysqldb-get-the-result-of-fetchall-in-a-list
    # Python MySQLDB: Get the result of fetchall in a list
    for row in curs.execute('SELECT * FROM inventory ORDER BY name'):
        print(row) 

def check_in(item, number):
    print("checking in", number, item)
    try:
        conn = sqlite3.connect(db, timeout=1)
        curs = conn.cursor()
        curs.execute('SELECT * FROM inventory WHERE name = "%s"' % (item))
        rows = curs.fetchall()
        cur_count = rows[0][1]  #' format : item_str count_str
        print("there are already", cur_count, item, "in inventory")
        print("adding", number, item,"to inventory")

        # update transcation
        now = datetime.now() # current date and time
        insert_tran_cmd = 'INSERT INTO transcation VALUES(NULL, "%s", "check-in", %d, "%s")' % (item, number, now.strftime("%m/%d/%Y, %H:%M:%S"))
        curs.execute(insert_tran_cmd)

        number += int(cur_count) 
        curs.execute('UPDATE inventory SET count = %d WHERE name = "%s"' % (number, item))
        conn.commit()
        conn.close()
        print("check-in done")
    except Exception as e:
        print("check-in failed")
        conn.close()

def check_out(item, number):
    print("trying to check out", number, item)
    conn = sqlite3.connect(db, timeout=1)
    curs = conn.cursor()
    curs.execute('SELECT * FROM inventory WHERE name = "%s"' % (item))
    rows = curs.fetchall()
    cur_count = rows[0][1]  #' format : item_str count_str
    print("there are ", cur_count, item, "in inventory")
    inv_count = int(cur_count)
    if (inv_count < number):
       print("no enough inventory to checkout") 
       return


    # update transcation
    now = datetime.now() # current date and time
    insert_tran_cmd = 'INSERT INTO transcation VALUES(NULL, "%s", "check-out", %d, "%s")' % (item, number, now.strftime("%m/%d/%Y, %H:%M:%S"))
    curs.execute(insert_tran_cmd)

    print("checking out", number, item,"from inventory")
    inv_count -= number
    curs.execute('UPDATE inventory SET count = %d WHERE name = "%s"' % (inv_count, item))
    conn.commit()
    conn.close()
    print("check-out done")

def test():
    create_db()
    check_in("iphone_x", 3)
    show_inventory()
    check_in("iphone_x", 5)
    show_inventory()
    check_out("iphone_x", 100)
    show_inventory()
    check_out("iphone_x", 2)
    show_inventory()
    show_transcation()

test()
