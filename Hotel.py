import Facade

class Hotel:

  def __init__(self, id, country, address, postcode, town, stars, opened):
    self.id = id
    self.country = country
    self.address = address
    self.postcode = postcode
    self.town = town
    self.stars = stars
    self.opened = opened

  def get_hotels(conn):
    hotels = []

    cur = conn.cursor()

    cur.execute("""SELECT country.name, address, postcode, town, stars 
    FROM hotel 
    INNER JOIN country ON hotel.country = country.id
    WHERE open = 1""")
    
    for e in cur.fetchall():
        hotels.append({"country":e[0], "address":e[1], "postcode":e[2], "town":e[3], "stars":e[4] })
    
    cur.close()

    return hotels

  def create_table(conn):
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS hotel (
      id INTEGER PRIMARY KEY,
      country CHARACTER(2) NOT NULL,
      address TEXT NOT NULL,
      postcode TEXT NOT NULL,
      town TEXT NOT NULL,
      stars INTEGER NOT NULL,
      open SMALLINT NOT NULL
      )""")

  def load(self, conn):
    cur = conn.cursor()
    cur.execute("INSERT INTO hotel (id, country, address, postcode, town, stars, open) VALUES(%s, %s, %s, %s, %s, %s, %s)", (self.id, self.country, self.address, self.postcode, self.town, self.stars, self.opened))
        
  def reset_table(conn):
    Hotel.create_table(conn)
 
    data_cur = Facade.get_data_connection().cursor()

    data_cur.execute("""SELECT * FROM hotel""")
    for row in data_cur:
        hotel = Hotel(row[0],row[1],row[2],row[3],row[4],row[5],row[6])
        hotel.load(conn)

    data_cur.close()

  def drop_table(conn):
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS hotel")

