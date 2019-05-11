# Fake_ HSR

this is a midterm project in PKU Introduction to the database (Honor track). This project try to used sql to do something like what [hsreplay.net](hsreplay.net) do

## usage

```shell
pip install -r requirement  # install requirement
./env.sh  # setting the environment
flask --help  # see what command HSR have
```

To run the project, you need to add a `config.json` like this (This will be change into [mysql user config file](https://dev.mysql.com/doc/refman/8.0/en/option-files.html) later)

```json
{
  "address": XXX,
  "user": XXX,
  "password": XXX,
  "database": XXX
}
```

Then run

```shell
flask create-table  # create the data table
flask insert-data  # insert the cards and desks data
```

Now we can `flask run` to see the project.
