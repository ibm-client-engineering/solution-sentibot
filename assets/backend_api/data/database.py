from sqlalchemy import create_engine, insert, text, MetaData, select
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import pandas as pd
import datetime

class Database() :
    
    def __init__(self):

        self.engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost:5432/DB")
        self.conn = self.engine.connect()
        self.meta_data = MetaData(bind=self.conn)
        self.add_data = []

    def add(self, data) :
        """Add data to Postgres Database
        Args:
            data (List[List]): Data to add
        """
        query="INSERT INTO  articletable (source, title, body, published, link, category, summary)  VALUES(%s, %s, %s, %s, %s, %s)"
        for d in data :
            self.add_data.append(d)
        self.conn.execute(query,self.add_data)
        self.add_data = []

    def get_all(self) :
        """Get all records from articletable

                Returns:
            data: data stored in articletable
        """
        data = self.conn.execute("SELECT * FROM articletable").fetchall()
        final_data = []
        for _ in range(len(data)) :
            final_data.append({key: value for key, value in data._mapping.items()})
        return final_data
    
    def get(self, id) :
        """Get single article from articletable. If there is no article with that id, the function returns None
                Args:
            id Integer: article id (from the database)

                Returns:
            final_data: article identified by id
        """
        data = self.conn.execute(f"SELECT * FROM articletable WHERE ID={id}").fetchone()
        if data is not None :
            final_data = {key: value for key, value in data._mapping.items()}
            return final_data
        else :
            return None

    def get_today(self) :
        """Get all articles from the last 24 hours. If none exist, return None.

                Returns:
            final_data: articles from the last 24 hours
        """
        data = self.conn.execute(f"SELECT * FROM articletable WHERE PUBLISHED > NOW() - INTERVAL '1 DAY'").fetchall()
        final_data = []
        if data is not None :
            final_data = []
            for _ in range(len(data)) :
                final_data.append({key: value for key, value in data._mapping.items()})
            return final_data
        else :
            return None
        
    def check_exists(self, title) :
        """Check if an article with this title exists in the database

                Returns:
            exists: boolean
        """
        data = self.conn.execute(f"SELECT EXISTS(SELECT 1 FROM articletable WHERE TITLE='{title}')").fetchone()
        return data