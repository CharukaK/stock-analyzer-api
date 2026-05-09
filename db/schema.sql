CREATE TABLE IF NOT EXISTS symbols(
    symbol TEXT PRIMARY KEY,
    information TEXT,
    last_refreshed TEXT,
    time_zone TEXT
);

CREATE TABLE IF NOT EXISTS prices_monthly(
    symbol TEXT,
    month_start_date TEXT,
    last_refreshed TEXT,
    open REAL,
    close REAL,
    high REAL,
    low REAL,
    volume INTEGER,
    PRIMARY KEY (symbol, month_start_date),
    FOREIGN KEY (symbol) REFERENCES symbols (symbol)
);

