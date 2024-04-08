import sqlite3 as sql


class DbWorker:
    async def connect(self, db_name):
        self.con = sql.connect(db_name)
        self.cur = self.con.cursor()

        # Table for cakes
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS 
        cakes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cake_name TEXT,
        description TEXT,
        photo_file_id TEXT,
        price_per_kg TEXT
        )""")

        # Table for admins
        self.cur.execute("""CREATE TABLE IF NOT EXISTS 
        admins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        admin_id TEXT,
        name TEXT
        )""")

        # Table for passwords
        self.cur.execute("""CREATE TABLE IF NOT EXISTS 
        passwords (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        password TEXT,
        description TEXT
        )""")

    async def add_cake(self, cake_name, description, photo_file_id, price_per_kg):
        self.cur.execute(f"""INSERT INTO cakes 
        (cake_name, description, photo_file_id, price_per_kg) 
        VALUES 
        ('{cake_name}', '{description}', '{photo_file_id}', '{price_per_kg}')""")
        self.con.commit()

    async def del_cake(self, cake_name):
        self.cur.execute(f"""DELETE FROM cakes WHERE 
                cake_name = '{cake_name}'""")
        self.con.commit()

    async def get_cakes(self):
        data = self.cur.execute("""SELECT * FROM cakes""").fetchall()
        return data

    async def add_admin(self, admin_id, name):
        # print(f"""INSERT INTO admins (admin_id, name) VALUES
        # ({admin_id}, {name})""")
        self.cur.execute(f"""INSERT INTO admins ( admin_id, name ) VALUES ('{admin_id}', '{name}')""")
        self.con.commit()

    async def del_admin(self, name):
        self.cur.execute(f"""DELETE FROM admins WHERE 
                name = '{name}'""")
        self.con.commit()

    async def get_admins(self):
        data = self.cur.execute("""SELECT * FROM admins""").fetchall()
        return data

    async def update_password(self, password, description):
        # self.cur.execute(f"""UPDATE passwords
        # SET password = '{password}'
        # WHERE description = '{description}'""")
        # self.con.commit()
        await self.del_password(description)
        await self.add_password(password, description)

    async def get_password(self, description):
        data = self.cur.execute(f"""SELECT * FROM passwords WHERE description = '{description}'""").fetchall()
        return data

    async def add_password(self, password, description):
        self.cur.execute(f"""INSERT INTO passwords (password, description) VALUES 
                ('{password}', '{description}')""")
        self.con.commit()

    async def del_password(self, description):
        self.cur.execute(f"""DELETE FROM passwords WHERE 
                        description = '{description}'""")
        self.con.commit()

    async def shutdown(self):
        self.con.commit()
        self.cur.close()
        self.con.close()
