import sqlite3

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS characters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            class TEXT NOT NULL,
            strength INTEGER NOT NULL,
            dexterity INTEGER NOT NULL,
            constitution INTEGER NOT NULL,
            intelligence INTEGER NOT NULL,
            wisdom INTEGER NOT NULL,
            charisma INTEGER NOT NULL,
            backstory TEXT NOT NULL,
            backstory_type TEXT NOT NULL
        )
        ''')
        self.conn.commit()

    def get_all_character_names(self):
        self.cursor.execute('SELECT name FROM characters')
        character_names = self.cursor.fetchall()
        return [name[0] for name in character_names]

    def get_character_details(self, character_name):
        self.cursor.execute('SELECT * FROM characters WHERE name = ?', (character_name,))
        character_data = self.cursor.fetchone()
        if character_data:
            return {
                'name': character_data[1],
                'class': character_data[2],
                'strength': character_data[3],
                'dexterity': character_data[4],
                'constitution': character_data[5],
                'intelligence': character_data[6],
                'wisdom': character_data[7],
                'charisma': character_data[8],
                'backstory': character_data[9],
                'backstory_type': character_data[10]
            }
        return None

    def save_character_to_db(self, character):
        sql = '''
        INSERT INTO characters (name, class, strength, dexterity, constitution, intelligence, wisdom, charisma, backstory, backstory_type)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        self.cursor.execute(sql, (
            character['name'],
            character['class'],
            character.get('strength', 0),
            character.get('dexterity', 0),
            character.get('constitution', 0),
            character.get('intelligence', 0),
            character.get('wisdom', 0),
            character.get('charisma', 0),
            character['backstory'],
            character['backstory_type']
        ))
        self.conn.commit()

        return {
            'name': character['name'],
            'class': character['class'],
            'strength': character.get('strength', 0),
            'dexterity': character.get('dexterity', 0),
            'constitution': character.get('constitution', 0),
            'intelligence': character.get('intelligence', 0),
            'wisdom': character.get('wisdom', 0),
            'charisma': character.get('charisma', 0),
            'backstory': character['backstory'],
            'backstory_type': character['backstory_type']
        }