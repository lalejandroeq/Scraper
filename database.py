import sqlite3

conn = sqlite3.connect('cars.db')
curs = conn.cursor()
# curs.execute("DROP TABLE cars_tb")
curs.execute("""CREATE TABLE cars_tb_2(
                crawler_id TEXT,
                car_id TEXT,
                site TEXT,
                marca TEXT,
                modelo TEXT,
                agno INT,
                moneda TEXT,
                precio INT,
                motor TEXT,
                kilometraje TEXT,
                color TEXT,
                transmision TEXT,
                link TEXT,
                insert_timestamp TIMESTAMP)
                """)
conn.commit()
conn.close()
