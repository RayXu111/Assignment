import sqlite3

# Create a connection to the SQLite database
conn = sqlite3.connect('stephen_king_adaptations.db')
cursor = conn.cursor()

# Create the 'stephen_king_adaptations_table' table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS stephen_king_adaptations_table (
        movieID INTEGER PRIMARY KEY AUTOINCREMENT,
        movieName TEXT NOT NULL,
        movieYear INTEGER NOT NULL,
        imdbRating REAL NOT NULL
    )
''')
conn.commit()

# Function to insert data into the database
def insert_movie(movieName, movieYear, imdbRating):
    cursor.execute('''
        INSERT INTO stephen_king_adaptations_table (movieName, movieYear, imdbRating)
        VALUES (?, ?, ?)
    ''', (movieName, movieYear, imdbRating))
    conn.commit()

# Read the content of the file into a list and insert it into the database
with open('stephen_king_adaptations.txt', 'r') as file:
    for line in file:
        data = line.strip().split(',')
        if len(data) == 4:
            movieName, movieYear, imdbRating = data[1], int(data[2]), float(data[3])
            insert_movie(movieName, movieYear, imdbRating)

# Function to search for movies by name
def search_by_name(movie_name):
    cursor.execute('SELECT * FROM stephen_king_adaptations_table WHERE movieName = ?', (movie_name,))
    result = cursor.fetchall()
    return result

# Function to search for movies by year
def search_by_year(year):
    cursor.execute('SELECT * FROM stephen_king_adaptations_table WHERE movieYear = ?', (year,))
    result = cursor.fetchall()
    return result

# Function to search for movies by rating
def search_by_rating(min_rating):
    cursor.execute('SELECT * FROM stephen_king_adaptations_table WHERE imdbRating >= ?', (min_rating,))
    result = cursor.fetchall()
    return result

# Main loop for user interaction
while True:
    print("\nOptions:")
    print("1. Search by Movie Name")
    print("2. Search by Movie Year")
    print("3. Search by IMDb Rating")
    print("4. STOP")

    choice = input("Enter your choice: ")

    if choice == '1':
        movie_name = input("Enter the name of the movie: ")
        result = search_by_name(movie_name)
        if result:
            for row in result:
                print(f"Movie Name: {row[1]}, Year: {row[2]}, IMDb Rating: {row[3]}")
        else:
            print('No such movie exists in our database')
    elif choice == '2':
        year = input("Enter the year: ")
        result = search_by_year(year)
        if result:
            for row in result:
                print(f"Movie Name: {row[1]}, Year: {row[2]}, IMDb Rating: {row[3]}")
        else:
            print('No movies were found for that year in our database')
    elif choice == '3':
        min_rating = float(input("Enter the minimum IMDb rating: "))
        result = search_by_rating(min_rating)
        if result:
            for row in result:
                print(f"Movie Name: {row[1]}, Year: {row[2]}, IMDb Rating: {row[3]}")
        else:
            print('No movies at or above that rating were found in the database')
    elif choice == '4':
        break
    else:
        print("Invalid choice. Please choose a valid option.")

# Close the database connection
conn.close()
