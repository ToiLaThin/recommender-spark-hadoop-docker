from pyspark.ml.recommendation import ALS

class MultiCriteriaALSModel:
    def __init__(self, userCol, itemCol, ratingColsWithWeights: dict):
        self.ratingCols = list(ratingColsWithWeights.keys())
        self.ratingColsWithWeights = ratingColsWithWeights
        self.userCol = userCol
        self.itemCol = itemCol
        self.alss = {}
        self.models = {}
        self.predictions = {}
        self.combined_prediction = None
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
                                                                          sum(self.predictions[first_col][rCol] * self.ratingColsWithWeights[rCol] \
                                                                              for rCol in self.ratingCols))\
                                                              .select(self.userCol, self.itemCol, "prediction_" + first_col, "init_combined_rating")
        for rCol in self.ratingCols[1:]:
            self.combined_prediction = self.combined_prediction\
                                                .join(
                                                    self.predictions[rCol].select(self.userCol, self.itemCol, "prediction_" + rCol), 
                                                    [self.userCol, self.itemCol]
                                                )
        self.combined_prediction = self.combined_prediction.withColumn("predict_combined_rating", \
                                                                       sum(self.combined_prediction["prediction_" + rCol] * self.ratingColsWithWeights[rCol] \
                                                                           for rCol in self.ratingCols))
        return self.combined_prediction
    
    def recommendForUser(self, user, numItems):
        # return self.combined_prediction.filter(self.combined_prediction == user).orderBy("predict_combined_rating", ascending=False).limit(numItems).select(self.itemCol)
        pass
    