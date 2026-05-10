CREATE TABLE IF NOT EXISTS symbols(
    symbol TEXT PRIMARY KEY,
    last_refreshed TEXT,
    last_checked TEXT,
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

