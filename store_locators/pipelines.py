import pymysql
import scrapy
from datetime import datetime

db_params = {
    'host': 'localhost',
    'user': 'root',
    'password': 'actowiz',
    'db': 'store_locators'
}


class StoreLocatorsPipeline:
    def __init__(self):
        self.db_params = db_params

        # Establish a database connection
        self.connection = pymysql.connect(**self.db_params)
        self.cursor = self.connection.cursor()

    def open_spider(self, spider):
        # Create table if not exists
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {spider.name}_{datetime.now().strftime('%Y%m%d')} (
            index_id INT AUTO_INCREMENT PRIMARY KEY,
            store_id VARCHAR(255),
            name VARCHAR(255),
            latitude VARCHAR(255),
            longitude VARCHAR(255),
            street VARCHAR(255),
            city VARCHAR(255),
            state VARCHAR(255),
            zip_code VARCHAR(20),
            county VARCHAR(255),
            phone VARCHAR(50),
            open_hours TEXT,
            url TEXT,
            provider VARCHAR(255),
            category VARCHAR(255),
            updated_date VARCHAR(255),
            country VARCHAR(255),
            status VARCHAR(255),
            direction_url TEXT,
            UNIQUE (store_id)
        )
        """
        self.cursor.execute(create_table_query)
        self.connection.commit()

    def close_spider(self, spider):
        # Close the database connection
        self.connection.close()

    def process_item(self, item, spider):
        # Extract the fields from the item dict
        fields = ', '.join(item.keys())
        placeholders = ', '.join(['%s'] * len(item))

        # Insert query with dynamic fields and placeholders
        insert_query = f"INSERT IGNORE INTO {spider.name}_{datetime.now().strftime('%Y%m%d')} ({fields}) VALUES ({placeholders})"

        # Execute the query with values directly from the item
        self.cursor.execute(insert_query, list(item.values()))
        self.connection.commit()

        return item
