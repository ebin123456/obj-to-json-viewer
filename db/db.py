import MySQLdb
import os 
import time
import zipfile
import shutil
global host
global db
global user
global password
host = "localhost"
db_name = "three"
user = "root"
password = ""

def save_to_db(file_name,new_name):
    db = MySQLdb.connect(host=host, user=user, passwd=password, db=db_name)
    time_str = time.strftime('%Y-%m-%d %H:%M:%S')
    sql = """INSERT INTO files (name, new_name,uploaded_at) VALUES (%s, %s,%s)"""
    tmp = [ (file_name, new_name,time_str )]
    cursor = db.cursor()
    cursor.executemany(sql, tmp)
    db.commit()
    db.close()
def get_models():
    db = MySQLdb.connect(host=host, user=user, passwd=password, db=db_name)
    sql = "SELECT * FROM files LIMIT 10"
    cursor = db.cursor()
    cursor.execute(sql)
    result = []
    columns = tuple( [d[0].decode('utf8') for d in cursor.description] )
    for row in cursor:
        result.append(dict(zip(columns, row)))
    return result    


def extract_zip(my_zip,my_dir):
	with zipfile.ZipFile(my_zip) as zip_file:
	    for member in zip_file.namelist():
	        filename = os.path.basename(member)
	        # skip directories
	        if not filename:
	            continue

	        # copy file (taken from zipfile's extract)
	        source = zip_file.open(member)
	        target = file(os.path.join(my_dir, filename), "wb")
	        with source, target:
	            shutil.copyfileobj(source, target)     