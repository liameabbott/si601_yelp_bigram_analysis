
# -*- coding: utf-8 -*-
# !/usr/bin/python


import json
import sqlite3 as sqlite


def bar_business_generator():
    """Generator function that opens Yelp Academic 'business' dataset and
       yields (business id, avg star rating) tuple for every business in the
       dataset categorized as a bar."""

    with open('yelp_academic_dataset_business.json', 'rU') as f:
        while True:
            line = f.readline()
            if not line:
                break
            line_dict = json.loads(line)
            if 'Bars' in line_dict['categories']:
                bar_id = line_dict['business_id']
                avg_star_rating = line_dict['stars']
                yield (bar_id, avg_star_rating)


def review_generator():
    """Generator function that opens Yelp Academic 'reviews' dataset and yields
       (business id, star rating, review text) tuple for every review in the
       dataset. Dataset does not include category of businesses reviewed, so
       we cannot filter out the reviews of only bars yet!"""

    with open('yelp_academic_dataset_review.json', 'rU') as f:
        while True:
            line = f.readline()
            if not line:
                break
            line_dict = json.loads(line)
            biz_id = line_dict['business_id']
            stars = line_dict['stars']
            review = line_dict['text']
            yield (biz_id, stars, review)


# Create sqlite database on disk to hold and combine data from disparate Yelp
# business and reviews datasets.
with sqlite.connect('si601_project_database_leabbott.db') as con:

    cur = con.cursor()

    # Create business table in database.
    cur.execute("DROP TABLE IF EXISTS business")
    cur.execute("CREATE TABLE business(id TEXT, star_rating REAL)")

    # Create reviews table in database.
    cur.execute("DROP TABLE IF EXISTS reviews")
    cur.execute("CREATE TABLE reviews(id TEXT, stars REAL, review TEXT)")

    # Write (business id, avg star rating) for all bars into a table.
    bars = bar_business_generator()
    cur.executemany("INSERT INTO business VALUES(?, ?)", bars)

    # Write (business id, star rating, review text) for all reviews into table.
    reviews = review_generator()
    cur.executemany("INSERT INTO reviews VALUES(?, ?, ?)", reviews)

    # Create indices for each table based on business id
    cur.execute("CREATE INDEX IF NOT EXISTS index_business_id ON business(id)")
    cur.execute("CREATE INDEX IF NOT EXISTS index_reviews_id ON reviews(id)")

    # Join business and reviews tables on business id. Select star rating and
    # review text for all reviews of businesses categorized as bars in the
    # business dataset. Write (star rating, review text) tuples into a list.
    cur.execute("""SELECT r.stars, r.review
                    FROM reviews AS r JOIN business AS b ON (r.id=b.id)""")
    bar_reviews = cur.fetchall()

    # Create positive and negative review lists, where positive reviews are all
    # 5-star reviews and negative reviews are reviews with 2 or fewer stars.
    pos_reviews = [review[1].encode('utf8').replace('\n', '\s')
                   for review in bar_reviews if review[0] == 5.0]
    neg_reviews = [review[1].encode('utf8').replace('\n', '\s')
                   for review in bar_reviews if review[0] <= 2.0]

    # Write positive reviews list to a .txt file.
    with open('pos_reviews.txt', 'wb') as f:
        for line in pos_reviews:
            f.write(line + '\n')

    # Write negative reviews list to a .txt file.
    with open('neg_reviews.txt', 'wb') as f:
        for line in neg_reviews:
            f.write(line + '\n')
