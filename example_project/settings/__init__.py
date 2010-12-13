# Project dirs
import os.path

PROJECT_ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__), '../'))
DEVZONE_ROOT = os.path.realpath(os.path.join(PROJECT_ROOT, '../'))
DB_FILE = os.path.join(PROJECT_ROOT, '.db')

def parse_db():
    if not os.path.exists( DB_FILE ):
        return None

    databases = dict()
    for line in open( DB_FILE ).readlines():
        if line.startswith('#') or not len(line.strip()):
            continue
        name, backend, connect_data = line.split()
        user_data, db_data = connect_data.split('@')
        user, password = user_data.split(':')
        host, db_name = db_data.split('/')
        databases[ name ] = dict(
                ENGINE = backend,
                NAME = db_name,
                HOST = host,
                USER = user,
                PASSWORD = password,
        )
    return databases
