import pandas as pd
from ml_models import MultiCriteriaALSModel
def transform_to_prediction():
    df_beer = pd.read_csv('../../resources/beer_reviews_transformed.csv')
    (training, test) = df_beer.randomSplit([0.8, 0.2])
    review_weight = {
        'review_taste': 0.25,
        'review_appearance': 0.1,
        'review_palate': 0.2,
        'review_aroma': 0.15,
        'review_overall': 0.3
    }

    model = MultiCriteriaALSModel(
        'user_id', 
        'beer_id', 
        review_weight
    )

    model.fit(training)
    prediction = model.transform(test)
    prediction = prediction.select('user_id', 'beer_id', 'predict_combined_rating', 'init_combined_rating')
    prediction.toPandas().to_csv('../../resources/beer_reviews_prediction.csv', index=False)