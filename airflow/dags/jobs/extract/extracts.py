import pandas as pd
from spark_session import init_spark_session
def extract_from_csv():
    ss = init_spark_session()
    """Extract from CSV beers reviews then load into a dataframe, save it to a location"""
    df_beer = ss.read.csv('/opt/airflow/dags/resources/beer_reviews.csv',inferSchema=True,header=True)
    df_beer = df_beer.select([
        'beer_beerid', 
        'review_taste', 
        'review_appearance', 
        'review_palate', 
        'review_aroma', 
        'review_overall', 
        'review_profilename'
    ])
    df_beer = df_beer.withColumnRenamed('beer_beerid', 'beer_id')
    df_beer = df_beer.withColumnRenamed('review_profilename', 'user_id')
    df_beer = df_beer.dropna()

    #convert to pandas dataframe
    df_beer = df_beer.toPandas()
    df_beer['user_id'] = df_beer['user_id'].astype('category').cat.codes #each username is converted to a unique number
    df_beer.to_csv('/opt/airflow/dags/resources/beer_reviews_transformed.csv', index=False)
