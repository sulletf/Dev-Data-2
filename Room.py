import Facade

class Room:

  def __init__(self, id_hotel, num, name, surface, num_persons):
    self.id_hotel = id_hotel
    self.num = num
    self.name = name
    self.surface = surface
    self.num_persons = num_persons

  def create_table(conn):
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS room (
      id_hotel integer NOT NULL,
      num INTEGER NOT NULL,
      name TEXT NOT NULL,
      surface INTEGER NOT NULL,
      num_persons INTEGER NOT NULL DEFAULT 0,
      FOREIGN KEY(id_hotel) REFERENCES hotel(id),
      PRIMARY KEY (id_hotel, num)
    )""")

  def load(self, conn):
    cur = conn.cursor()
    cur.execute("INSERT INTO room (id_hotel, num, name, surface, num_persons) VALUES(%s, %s, %s, %s, %s)", (self.id_hotel, self.num, self.name, self.surface, self.num_persons))
        
  def reset_table(conn):
    Room.create_table(conn)

    data_cur = Facade.get_data_connection().cursor()

    data_cur.execute("""SELECT * FROM room""")
    for row in data_cur:
        room = Room(row[0],row[1],row[2],row[3],row[4])
        room.load(conn)

    data_cur.close()

  def drop_table(conn):
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS room")

