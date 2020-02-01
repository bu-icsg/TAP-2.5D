import sqlite3
import sys, os
import glob
import configparser

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

if len(sys.argv) > 1:
	syst = sys.argv[1]
else:
	print ('need to specify syst')
	exit()
if len(sys.argv) > 2:
	path = sys.argv[2]
else:
	# path = 'outputs/Dec2019/'+ syst + '/nppl/adpTWv2/0.8/45/0/'
	print ('need path')
	exit()

conn = create_connection(path + 'data' + '.sqlite3')
# create tables if NOT exist
create_tables(conn)

cur = conn.cursor()
cur.execute("SELECT count(*) FROM temp")
result = cur.fetchone()
print ('temp start', result)
# cur.execute("SELECT count(*) FROM length")
# result = cur.fetchone()
# print 'length start', result

if os.path.isfile(path + 'step.txt'):
	filename = 'configs/sys_' + syst + '.cfg'
	config = configparser.ConfigParser()
	config.read(filename)
	chiplet_count = config.getint('chiplets', 'chiplet_count')
	interposer_size = config.getfloat('interposer', 'intp_size')
	link_type = config.get('interposer', 'link_type')
	power = list(map(float, config.get('chiplets', 'powers').split(',')))
	zeros = [0] * (8 - chiplet_count)
	with open(path + 'step.txt', 'r') as LOG:
		a = LOG.readline()
		while a:
			temp = float(LOG.readline())
			length = float(LOG.readline())
			x = list(map(float, LOG.readline().split('\n')[0].strip('[]').split(',')))
			y = list(map(float, LOG.readline().split('\n')[0].strip('[]').split(',')))
			width = list(map(float, LOG.readline().split('\n')[0].strip('[]').split(',')))
			height = list(map(float, LOG.readline().split('\n')[0].strip('[]').split(',')))
			entry = tuple([chiplet_count] + width + zeros + height + zeros + power + zeros + x + zeros + y + zeros + [interposer_size, link_type, temp])
			add_temp(conn, entry)
			conn.commit()
			a = LOG.readline()
	os.system('mv '+path + 'step.txt '+path+'step_ac.txt')
cur.execute("SELECT count(*) FROM temp")
result = cur.fetchone()
print ('temp end', result)
conn.close()

# path_h = path + str(h) +'ov/'
# if os.path.isdir(path_h):
#     s_intp = os.listdir(path_h)
#     for s in s_intp:
#         path_s = path_h + s + '/'
#         intsize = int(s[0:2])
#         print h,s
#         if os.path.isdir(path_s):
#             orgs = os.listdir(path_s)
#             for org in orgs:
#                 path_org = path_s + org + '/'
#                 if os.path.isdir(path_org):
#                     nets = os.listdir(path_org)
#                     for network in nets:
#                         if network in networks:
#                             path_network = path_org + network + '/128bit/'
#                             if os.path.isdir(path_network):
#                                 stages = os.listdir(path_network)
#                                 for stg in stages:
#                                     path_stage = path_network + stg + '/'
#                                     if stg == '1stage':
#                                         ltype = 'nppl'
#                                         stage = 1
#                                     else:
#                                         ltype = 'ppl'
#                                         stage = int(stg[0])
#                                     if os.path.isfile(path_stage + 'Obj.txt'):
#                                         print path_stage
#                                         with open(path_stage + 'Obj.txt', 'r') as OBJ:
#                                             length = int(OBJ.readline())
#                                         add_length(conn,(suite, bench, network, intsize, ltype, stage, org, h, length))
#                                         conn.commit()
#                                     files = os.listdir(path_stage)
#                                     if glob.glob(path_stage+'*cycle.steady'):
#                                         for f in files:
#                                             if len(f)>20:
#                                                 if f[-12:] == 'cycle.steady':
#                                                     sp = f.split('_')
#                                                     freq = int(sp[1])
#                                                     latency = int(sp[-1][0])
#                                                     temp = ReadTemp(path_stage, f)
#                                                     # print freq, latency, temp
#                                                     add_temp(conn, (suite, bench, network, intsize, freq, ltype, stage, latency, org, h, temp))
#                                                     conn.commit()
#                                                 elif f[-12:] == 'ycle1.steady':
#                                                     sp = f.split('_')
#                                                     freq = int(sp[1])
#                                                     latency = int(sp[-1][0])
#                                                     temp = ReadTemp(path_stage, f)
#                                                     # print freq, latency, temp
#                                                     add_leakage(conn, (suite, bench, network, intsize, freq, ltype, stage, latency, org, h, temp))
#                                                     conn.commit()
#                                     os.system('rm -r '+path_stage)
#                                     n += 1
#                                     if n> n_del :
#                                         print 'not finish'
#                                         conn.commit()
#                                         conn.close()
#                                         exit()
#                                 os.system('rm -r '+path_network)
#                     os.system('rm -r '+path_org)
#             os.system('rm -r '+path_s)
#     os.system('rm -r '+path_h)
 

# cur.execute("SELECT count(*) FROM length")
# result = cur.fetchone()
# print 'length end',result
# print ('finish')
# add_temp(conn,(suite, bench, network, intsize, freq, ltype, stage, latency, org, h_mm, temp))
# add_length(conn,(suite, bench, network, intsize, freq, ltype, stage, latency, org, h_mm, length))

# conn.commit()
# conn.close()