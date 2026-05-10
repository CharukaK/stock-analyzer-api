# Stock Analyzer API
This API provide a market summary for a given stock symbol and a year

data is sourced from the following third party API:
`https://www.alphavantage.co/documentation/#monthly`

## API

```hurl
GET /symbols/IBM/annual/2005

returns:
{
"high": "80.8700",
"low": "76.0600",
"volume": "139457800"
}
```

The API should provide information on high, low, and volume by aggregating 12 monthly data
points for the particular stock symbol provided

```
definitions:
    - high => the highest price for {symbol} within {year}
    - low => the lowest price for {symbol} within {year}
    - volume => the aggregated sum of volume traded monthly for {symbol} within {year}
```

**Error codes**
- 42x => input validation error
- 404 => no data found
- 5xx => server errors/including communication with the 3rd party api

## Setting up for development

Run the following command to setup the development environment
```sh
make install-dev
```

after installation run the command `source .venv/bin/activate`

this will initialize the python virtual environment to attached to the project

**Setting up env file**
copy the `.env.example` to `.env` using the following command
```bash
cp .env.example .env
```

and fill in the required information

you would require the following variables in order to run the application
- **ALPHAVANTAGE_URL** => AlphaVantage base url
- **ALPHAVANTAGE_API_KEY** => AlphaVantage api key
- **DATABASE_URL** => path to sqlite database file
- **DEBUG** => Enable debug logging or not (True/False)

after setting up the file to use the following command to start the development server
```
make run-dev
```

Inorder to run the production server use the following command
```
make run
```

To run test use:
```
make test
```

## Project structure

```
.
├── app                             # root
│   ├── clients                     # contains implementation of external api clients
│   ├── core                        # env configuration
│   ├── dependencies.py             # lifecycle dependencies
│   ├── main.py                     # starting point
│   ├── models                      # data classes for serialization/deserialization
│   ├── routes                      # API route definitions
│   └── services                    # service implementation
├── conftest.py
├── db                              # sql schema
├── doc                             # planning documentation
├── Makefile
├── README.md
├── requirements-dev.txt            # dependencies + dev dependencies
├── requirements.txt                # runtime dependencies
└── tests                           # tests
```

## Database Schema

```sql
TABLE symbols(
    symbol TEXT PRIMARY KEY,
    last_refreshed TEXT,
    last_checked TEXT,
    time_zone TEXT
)

TABLE prices_monthly(       -- month_start_date + symbol is used as primary key
    symbol TEXT,            -- foreign key
    month_start_date TEXT,  
    last_refreshed TEXT,
    open REAL,
    close REAL,
    high REAL,
    low REAL,
    volume INTEGER,
);

```

## 3rd party dependencies used
- Pydantic: helps with type checking and data validation
- FastAPI: framework for building APIs
- Pydantic Settings: helps with managing environment variable and configurations
- httpx: provides a HTTP client with async capabilities
- aiosqlite: provides an async wrapper capabilities sqlite

