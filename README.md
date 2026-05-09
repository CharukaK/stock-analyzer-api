# Stock Analyzer API

Simple API to give you insights on a particular Stock name

tech spec: [link](./doc/dev.md)

## Setting up for development

Run the following command to setup the development environment

```sh
make install-dev
```

after installation run the command `source .venv/bin/activate`

this will initialize the python virtual environment to attached to the project

Run the following command to start the development server
```
make run-dev
```

For testing run
```
make test
```


## Project structure

```
.
├── app                             # root
│   ├── clients                     # contains implementation of clients(db, api)
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

