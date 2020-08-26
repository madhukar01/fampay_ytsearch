from rethinkdb import RethinkDB


###############################################################################
# Database setup script
###############################################################################
def setup_database():
    r = RethinkDB()
    r.connect(host='localhost', port=28015).repl()

    try:
        # Create databases
        r.db_create('platform').run()
        # Create tables
        r.db('platform').table_create('videos',
                                      primary_key='video_id').run()
    except Exception as e:
        print(e)
    else:
        print('Database setup successful')


if __name__ == '__main__':
    setup_database()
