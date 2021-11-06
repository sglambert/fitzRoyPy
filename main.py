import src.libs.code_loader as code_loader

# We create a resource object in with statement, this way we
# can release all the resources being used when the block ends
with code_loader.get_resources() as resources:
    # Define a logger once that will be passed around other classes
    logger = resources.logger

    # Define the path to the config file and the [section] we want to get credentials from
    config_file_path = '/some/full/path/to/fitzRoyPy/config/config_template.ini'
    section = 'credentials'

    # Load the config
    config = resources.get_config(config_file_path, section)

    # Create a connector object and pass the config to connect to a database
    database = resources.get_connector(config)

    # we setup the database connection in connector.py with the use of context mangers
    # We can now interact with the database in a with block
    with database as db:
        # This test query will return all the tables in our postgres db
        sql = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES;"
        db.execute(sql)
        all_tables = db.select_all(sql)
        print(all_tables)

    # Create a source object for the fitzRoy API via resources
    source = resources.get_source('fitzRoy')

    # Call any method from source.py to fetch data
    results = source.get_results(season=2020, round=1)
    # This will print results for season=2020, round=1
    print(results)
    # This will print the type of data 'results' returns. In this case it'll be a Pandas DataFrame
    print(type(results))
