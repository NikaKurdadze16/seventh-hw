import sqlite3
import random

book_names = []
for book_number in range(10):
    book_names.append(f'bookN{book_number + 1}')


def book_generator(number_of_books):
    books = []
    for _ in range(number_of_books):
        book_name = random.choice(book_names)
        cover_type = random.choice(['უბრალო', 'გაფორმებული', 'თხელი', 'სქელი'])
        book_type = random.choice(['სათავგადასავლო', 'რომანი', 'ისტორიული', 'საბავშვო'])
        number_of_pages = random.randint(100, 500)
        books.append((book_name, cover_type, book_type, number_of_pages))
    return books


conn = sqlite3.connect('books.db')
cursor = conn.cursor()


cursor.execute('''CREATE TABLE IF NOT EXISTS books
                  (book_name TEXT, cover_type TEXT, book_type TEXT, number_of_pages INT)''')

rnd_books = book_generator(10)
cursor.executemany('''INSERT INTO books (book_name, cover_type, book_type, number_of_pages)
                      VALUES (?, ?, ?, ?)''', rnd_books)


def calculate_average_pages():
    cursor.execute("SELECT AVG(number_of_pages) FROM books")
    average_pages = cursor.fetchone()[0]
    return average_pages


def find_book_with_most_pages():
    cursor.execute("SELECT number_of_pages FROM books ORDER BY number_of_pages DESC LIMIT 1")
    most_pages = cursor.fetchone()
    if most_pages:
        return most_pages[0]
    else:
        return None


print(f"average number of books is {calculate_average_pages()}, "
      f"and the highest number of pages among those books is{find_book_with_most_pages()}")

conn.commit()
conn.close()
