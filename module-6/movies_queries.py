
# Name: Robert Cuevas
# Date: November 18, 2026
# Assignment: CSD-310 Module 6 - Movies: Table Queries
# Purpose: Connect to the MySQL movies database and display
# studio, genre, and film information using four SQL queries.

import mysql.connector
from mysql.connector import errorcode
from dotenv import dotenv_values
from pathlib import Path


# Read the database settings from the Module 5 .env file
env_file = Path(__file__).resolve().parent.parent / "module-5" / ".env"
secrets = dotenv_values(env_file)

# Configure the MySQL database connection
config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"],
    "raise_on_warnings": True
}

db = None
cursor = None

try:
    # Connect to the movies database
    db = mysql.connector.connect(**config)
    cursor = db.cursor()

    print("\nConnected to the MySQL movies database.")

    # Query 1: Display all records in the studio table
    print("\n-- DISPLAYING STUDIO RECORDS --")

    cursor.execute("SELECT * FROM studio")

    studios = cursor.fetchall()

    for studio in studios:
        print("Studio ID: {}".format(studio[0]))
        print("Studio Name: {}\n".format(studio[1]))

    # Query 2: Display all records in the genre table
    print("\n-- DISPLAYING GENRE RECORDS --")

    cursor.execute("SELECT * FROM genre")

    genres = cursor.fetchall()

    for genre in genres:
        print("Genre ID: {}".format(genre[0]))
        print("Genre Name: {}\n".format(genre[1]))

    # Query 3: Display films shorter than two hours
    print("\n-- FILMS WITH A RUNTIME LESS THAN 2 HOURS --")

    cursor.execute(
        "SELECT film_name, film_runtime "
        "FROM film "
        "WHERE film_runtime < 120 "
        "ORDER BY film_runtime"
    )

    short_films = cursor.fetchall()

    for film in short_films:
        print("Film Name: {}".format(film[0]))
        print("Runtime: {} minutes\n".format(film[1]))

    # Query 4: Display films grouped together by director
    print("\n-- FILMS GROUPED BY DIRECTOR --")

    cursor.execute(
        "SELECT film_director, film_name "
        "FROM film "
        "ORDER BY film_director, film_name"
    )

    films = cursor.fetchall()
    previous_director = None

    for film in films:
        director = film[0]
        film_name = film[1]

        if director != previous_director:
            print("\nDirector: {}".format(director))
            previous_director = director

        print("  Film Name: {}".format(film_name))

    print("\nAll four queries completed successfully.")

except mysql.connector.Error as err:
    # Handle common MySQL errors
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("The supplied username or password are invalid.")

    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("The specified database does not exist.")

    else:
        print("MySQL Error:", err)

finally:
    # Close the cursor and connection safely
    if cursor is not None:
        cursor.close()

    if db is not None and db.is_connected():
        db.close()
        print("\nDatabase connection closed.")
