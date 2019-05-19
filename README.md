# Fake_ HSR

this is a midterm project in PKU Introduction to the database (Honor track). This project try to used sql to do something like what [hsreplay.net](hsreplay.net) do

See my [Project Report](report/report.md)(Chinese) for more detail.

## usage

```shell
pip install -r requirement  # install requirement
export FLASK_APP=app.py  # setting the environment
flask --help  # see what command HSR have
```

### For MacOS User
Maybe you need to execute `export DYLD_LIBRARY_PATH=/usr/local/mysql-8.0.15-macos10.14-x86_64/lib/:$DYLD_LIBRARY_PATH` if you meet some error about pymysql.

To run this project, you need to add a [mysql user config file](https://dev.mysql.com/doc/refman/8.0/en/option-files.html) like this in the project dirctionary.

```
[client]
host = XXX
port = XXX
user = XXX
password = XXX
database = XXX
```

Then run

```shell
flask create-table  # create the data table
flask insert-data  # insert the cards and desks data
```

Now we can `flask run` to see the project.
