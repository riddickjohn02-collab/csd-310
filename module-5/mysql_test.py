
# Name: Robert Cuevas
# Date: November 18, 2026
# Assignment: CSD-310 Module 5 - Movies Setup
# Purpose: Test the connection to the MySQL movies database.

import mysql.connector
from mysql.connector import errorcode
from dotenv import dotenv_values
from pathlib import Path


# Read the database settings from the .env file
env_file = Path(__file__).with_name(".env")
secrets = dotenv_values(env_file)

# Configure the MySQL connection
config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"],
    "raise_on_warnings": True
}

db = None

# Attempt to connect to the database
try:
    db = mysql.connector.connect(**config)

    print("\nDatabase user {} connected to MySQL on host {} "
          "with database {}".format(
              config["user"],
              config["host"],
              config["database"]
          ))

    input("\nPress Enter to continue...")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("The supplied username or password are invalid.")

    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("The specified database does not exist.")

    else:
        print(err)

finally:
    # Close the connection safely
    if db is not None and db.is_connected():
        db.close()
