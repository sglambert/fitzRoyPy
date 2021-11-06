# fitzRoyPy

fitzRoyPy is a Python wrapper for the fitzRoy API with an inbuilt data engineering library.

The aim of this repository is to not only provide Python functionality to fetch data from the fitzRoy API, 
but also to provide backend data engineering tools useful in the extraction, transformation, loading and 
analysis of data.

## Requirements

* Python3
* R
* fitzRoy package
* RStudio (Optional)
* Docker (Optional)
* Postgres (Optional)

*The fitzRoy GitHub repository gives instructions on how to install the API. 
However, if you're not familiar with installing R packages the simplest way to install the package 
for use with Python is by firstly installing Rstudio and then installing fitzRoy through Rstudio. 
There’s probably a better and much simpler way to install fitzRoy though!*

## Getting Started

* Install Python packages in ```requirements.txt```
* Create a ```.env``` file in the project root directory with the following parameters:
```
  DB_USER=<db_user>
  DB_PASSWORD=<db_password>
  DB=<db_name>
  DB_PORTS=<some_port:some_port>
```

Running the command ``` docker compose up ``` in terminal in the project root directory will 
execute the instructions in the ```docker-compose.yml``` file. These instructions include creating a Postgres container using the environment variables in the .env file.

Once Docker has built the Postgres container you can then interact with the database. If you’re going to use a data visualisation tool like pgAdmin, Dbeaver, DataGrips, etc. then the connection details will be the same as what’s in the ```.env``` file.

To reiterate though, you don't need to use Docker and/or Postgres to use this wrapper. They have been provided as a way to organise the data.

## Usage
The main wrapper functionality can be found in source.py. When we create an instance of the source class we need to pass in the R package we want to use. 
In this case that might look like this: ``` fitzroy = Source('fitzRoy') ```

Once we have an instance of the Source class we are free to call any of the fitzRoy fetch functions.

To avoid polluting the namespace we've changed the name of these fetch functions in the wrapper to 'get' functions. 

The table below shows each fetch function in the fitzRoy API and the equivalent function in this repository. 

fitzRoy fetch function | fitzRoyPy Source method |
--- | --- |
```fetch_player_stats``` | ```get_player_stats``` |
```fetch_fixture``` | ```get_fixture``` |
```fetch_lineup``` | ```get_lineup``` |
```fetch_results``` | ```get_results``` |
```fetch_ladder``` | ```get_ladder``` |
```fetch_player_details``` | ```get_player_details``` |

When we call these functions we can specify the same keyword arguments as we would if we were using the fitzRoy package.

Those are: ``` season, round, source, comp, etc.```. If we don't pass any of the keyword arguments to our get Source methods, the fitzRoy API will return the default argument(s).

Essentially, what we're doing with each of these get methods is converting R DataFrames to Pandas DataFrames.

The following code is an example on how the entire repository can be used.

```
import src.libs.code_loader as code_loader

# We create a resource object in with statement, this way we
# can release all the resources being used when the block ends
with code_loader.get_resources() as resources:
    
    # Define a logger once that will be passed around other classes
    logger = resources.logger

    # Define the path to the config file and the [section] we want to get credentials from
    config_file_path = '/some/path/to/data_engineering_library/config/config_template.ini'
    section = 'credentials'

    # Load the config 
    config = resources.get_config(config_file_path, section)

    # Create a connector object and pass the config to connect to a database
    database = resources.get_connector(config)

    # we setup the database connection in connector.py with the use of context managers
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
```

## Roadmap
1) Create a simpler way to install the fitzRoy package through Python.
2) Add automated tests, particularly those around data collection from the fitzRoy API.
3) Add data analysis functionality (e.g. Feature, Analysis, and Statistics classes).
4) Actually do some data analysis!
5) Add functionality to create database tables.
6) Add validations.

## Contributing
Any contributions are much appreciated! If you have a suggestion that would make this project better, 
please feel free to fork the repo and create a pull request. 

    Fork the Project
    Create your Feature Branch (git checkout -b feature/featureName)
    Commit your Changes (git commit -m 'Add some feature')
    Push to the Branch (git push origin feature/featureName)
    Open a Pull Request

Alternatively, you can also open an issue with the tag "enhancement".

There are several improvements I'd like to implement, particularly around the data engineering side. I've added these
to the Roadmap (above).

## License
Distributed under the MIT License. Please see [MIT](https://choosealicense.com/licenses/mit/) for more details.

## Contact
Sammy Lambert - sam.gervase.lambert@gmail.com

## Acknowledgements
[fitzRoy](https://github.com/jimmyday12/fitzRoy)
