from rethinkdb import RethinkDB

r = RethinkDB()
r.connect(host='localhost', port=28015).repl()

try:
    # Create databases
    r.db_create('platform').run()
    # Create tables
    r.db('platform').table_create('videos',
                                  primary_key='task_id').run()
except Exception as e:
    print(e)
else:
    print('Database setup successful')
