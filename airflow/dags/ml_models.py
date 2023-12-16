from pyspark.ml.recommendation import ALS

class MultiCriteriaALSModel:
    def __init__(self, userCol, itemCol, rating_cols_with_weight: dict):
        self.ratingCols = list(rating_cols_with_weight.keys())
        self.rating_cols_with_weight = rating_cols_with_weight
        self.userCol = userCol
        self.itemCol = itemCol
        self.alss = {}
        self.models = {}
        self.predictions = {}
        self.combined_prediction = None
        self.recommendations = None
        for rCol in self.ratingCols:
            self.alss[rCol] = ALS(maxIter=5, regParam=0.01, userCol=userCol, itemCol=itemCol, ratingCol=rCol, coldStartStrategy="drop")
    
    def fit(self, training):
        for rCol in self.ratingCols:
            self.models[rCol] = self.alss[rCol].fit(training)

    def transform(self, testing):
        for rCol in self.ratingCols:
            self.predictions[rCol] = self.models[rCol].transform(testing)
            # Rename the prediction column to avoid conflict
            self.predictions[rCol] = self.predictions[rCol].withColumnRenamed("prediction", "prediction_" + rCol)
        
        first_col = self.ratingCols[0]
        self.combined_prediction = self.predictions[first_col].withColumn("init_combined_rating", \
                                                                          sum(self.predictions[first_col][rCol] * self.rating_cols_with_weight[rCol] \
                                                                              for rCol in self.ratingCols))\
                                                              .select(self.userCol, self.itemCol, "prediction_" + first_col, "init_combined_rating")
        for rCol in self.ratingCols[1:]:
            self.combined_prediction = self.combined_prediction\
                                                .join(
                                                    self.predictions[rCol].select(self.userCol, self.itemCol, "prediction_" + rCol), 
                                                    [self.userCol, self.itemCol]
                                                )
        self.combined_prediction = self.combined_prediction.withColumn("predict_combined_rating", \
                                                                       sum(self.combined_prediction["prediction_" + rCol] * self.rating_cols_with_weight[rCol] \
                                                                           for rCol in self.ratingCols))
        return self.combined_prediction
    
    def recommendForUser(self, userId, numItems):
        if self.combined_prediction is None:
            raise Exception("Please call transform() first!")
        return self.combined_prediction.filter(self.combined_prediction[self.userCol] == userId).orderBy("predict_combined_rating", ascending=False).limit(numItems).select(self.itemCol, "predict_combined_rating")
        # return self.combined_prediction.filter(self.combined_prediction == user).orderBy("predict_combined_rating", ascending=False).limit(numItems).select(self.itemCol)

    def recommendForAllUsers(self, numItems):
        from pyspark.sql import functions as F
        if self.combined_prediction is None:
            raise Exception("Please call transform() first!")
        return self.combined_prediction.groupBy(self.userCol).agg(F.collect_list(self.itemCol).alias("items"), F.collect_list("predict_combined_rating").alias("ratings")).select(self.userCol, "items", "ratings")
        
    