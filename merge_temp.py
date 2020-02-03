import sqlite3
import sys, os

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None

def create_tables(conn):
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS temp (
        chpl_count integer, 

        width_0 real, 
        width_1 real, 
        width_2 real, 
        width_3 real, 
        width_4 real, 
        width_5 real, 
        width_6 real, 
        width_7 real, 

        height_0 real, 
        height_1 real, 
        height_2 real, 
        height_3 real, 
        height_4 real, 
        height_5 real, 
        height_6 real, 
        height_7 real,

        power_0 real, 
        power_1 real, 
        power_2 real, 
        power_3 real, 
        power_4 real, 
        power_5 real, 
        power_6 real, 
        power_7 real, 

        x_0 real,
        x_1 real,
        x_2 real,
        x_3 real,
        x_4 real,
        x_5 real,
        x_6 real,
        x_7 real,

        y_0 real,
        y_1 real,
        y_2 real,
        y_3 real,
        y_4 real,
        y_5 real,
        y_6 real,
        y_7 real,

        intsize integer,
        ltype text, 

        temp real,

        PRIMARY KEY (chpl_count,
        width_0, width_1, width_2, width_3, width_4, width_5, width_6, width_7,         
        height_0, height_1, height_2, height_3, height_4, height_5, height_6, height_7,        
        power_0, power_1, power_2, power_3, power_4, power_5, power_6, power_7, 
        x_0,x_1,x_2,x_3,x_4,x_5,x_6,x_7,
        y_0,y_1,y_2,y_3,y_4,y_5,y_6,y_7,
        intsize,ltype))
    ''')
    # cur.execute('''
    #         CREATE TABLE IF NOT EXISTS length (suite text, bench text, network text, intsize integer, ltype text, stage integer, org text, h_mm real, length real,
    #             PRIMARY KEY (bench, network, intsize, stage, org))
    # ''')

def add_temp(conn, entry):
    sql = ''' INSERT OR IGNORE INTO temp (chpl_count,
        width_0, width_1, width_2, width_3, width_4, width_5, width_6, width_7,         
        height_0, height_1, height_2, height_3, height_4, height_5, height_6, height_7,        
        power_0, power_1, power_2, power_3, power_4, power_5, power_6, power_7, 
        x_0,x_1,x_2,x_3,x_4,x_5,x_6,x_7,
        y_0,y_1,y_2,y_3,y_4,y_5,y_6,y_7,
        intsize,ltype, temp)
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, entry)
    return cur.lastrowid

# def add_length(conn, entry):
#     sql = ''' INSERT OR IGNORE INTO length (suite, bench, network, intsize, ltype, stage, org, h_mm, length)
#               VALUES(?,?,?,?,?,?,?,?,?) '''
#     cur = conn.cursor()
#     cur.execute(sql, entry)
#     return cur.lastrowid

# def inquiry_temp(conn, entry):
#     sql = "SELECT * FROM temp WHERE network = ? AND freq = ? AND stage = ? AND latency = ? AND org = ?"
#     cur = conn.cursor()
#     cur.execute(sql, entry)
#     return cur.fetchall()

# def inquiry_length(conn, entry):
#     sql = "SELECT * FROM length WHERE network = ? AND stage = ? AND org = ?"
#     cur = conn.cursor()
#     cur.execute(sql, entry)
#     return cur.fetchall()


if len(sys.argv)>1:
    path_root = sys.argv[1]
else:
    print ("usage: python merge_db.py [filename] [path]")
    exit()

filename = 'data_temp.sqlite3'
local_file = '/scratch/yenai/' + path_root + filename
os.system('mkdir -p /scratch/yenai/' + path_root)
conn2 = create_connection(local_file)
create_tables(conn2)
cur2 = conn2.cursor()
cur2.execute("SELECT count(*) FROM temp")
count_start = cur2.fetchone()[0]

for start_point in os.listdir(path_root):
    if os.path.isdir(path_root + start_point):
        print (path_root + start_point)
        from_file = path_root + start_point + '/' + filename
        if os.path.isfile(from_file):
            conn1 = create_connection(from_file)
            cur1 = conn1.cursor()

            # cur1.execute("SELECT count(*) FROM length")
            # count_from = cur1.fetchone()[0]
            # cur1.execute("SELECT * FROM length")
            # result = cur1.fetchall()
            # cur2.execute("SELECT count(*) FROM length")
            # count_start = cur2.fetchone()[0]
            # print '\tlength  start', count_start
            # for row in result:
            #     add_length(conn2,row)
            # conn2.commit()
            # cur2.execute("SELECT count(*) FROM length")
            # count_end = cur2.fetchone()[0]
            # print '\tlength  end  ', count_end
            # print '\tnew: ', count_from, '\t\trep: ', count_from  + count_start - count_end

            # cur1.execute("DELETE FROM temp WHERE temp=-273.15")
            cur1.execute("SELECT count(*) FROM temp")
            count_from = cur1.fetchone()[0]
            print (count_from)
            cur1.execute("SELECT * FROM temp")
            result = cur1.fetchall()
            conn1.close()

            for row in result:
                add_temp(conn2,row)
            conn2.commit()
            os.system('rm '+ from_file)

cur2.execute("SELECT count(*) FROM temp")
count_end = cur2.fetchone()[0]
print ('\ttemp    start', count_start)
print ('\ttemp    end  ', count_end)
print ('\tnew: ', count_end - count_start)
conn2.close()

to_file = path_root + filename
os.system('mv ' + local_file + ' ' + to_file)