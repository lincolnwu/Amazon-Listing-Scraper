import psycopg2
import configparser 

def config(filename='database.ini', section='postgresql'):
    # Create a parser for database amazon_search
    parser = configparser.ConfigParser()
    # Read in config file
    parser.read(filename)

    db = {}

    if (parser.has_section(section)):
        if parser.has_section(section):
            params = parser.items(section)
        
        for param in params:
            db[param[0]] = param[1]

    else:
        raise Exception(f"{section} not found in {filename}")

    return db


def store_db(product_asin, product_name, product_price, product_ratings, product_ratings_num, product_link):
    conn = None

    params = config()
    conn = psycopg2.connect(**params)
    print('Connecting to PostgreSQL database...')

    curr = conn.cursor()

    # Create table with unique ASINs
    createSQL = '''CREATE TABLE IF NOT EXISTS search_result (
                        asin TEXT,
                        name TEXT,
                        price REAL,
                        ratings TEXT,
                        ratings_num TEXT,
                        details_link TEXT,
                        UNIQUE (asin)
                    );
                '''
    curr.execute(createSQL)
    print("QUERY: search_result table created...")
    
    # Insert data into table
    # If duplicate is present, do nothing (since it will result in an error code)
    insertSQL = '''INSERT INTO search_result (
                    asin,
                    name,
                    price,
                    ratings,
                    ratings_num,
                    details_link
                ) VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING'''
    
    varsList = list(zip(product_asin, product_name, product_price, product_ratings, product_ratings_num, product_link))
    curr.executemany(insertSQL, varsList)
    print("QUERY: data inserted into table...")
    conn.commit()
    conn.close()
    print("Session ending....")