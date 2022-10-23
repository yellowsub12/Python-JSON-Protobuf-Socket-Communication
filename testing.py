import numpy as np


ProcessedData = [1,2,3,4,5,6,7,8,9,10]
def MathShit(DataAnalytics):
        if DataAnalytics == 'avg':
            DataAnalyticsAnswer = sum(ProcessedData)/len(ProcessedData)
        elif DataAnalytics == 'std':
            DataAnalyticsAnswer = np.std(ProcessedData)
        elif DataAnalytics == 'max':
            DataAnalyticsAnswer = max(ProcessedData)
        elif DataAnalytics == 'min':
            DataAnalyticsAnswer = min(ProcessedData)
        elif DataAnalytics == '10p':
            DataAnalyticsAnswer = np.percentile(ProcessedData,10)
        elif DataAnalytics == '50p':
            DataAnalyticsAnswer = np.percentile(ProcessedData,50)
        elif DataAnalytics == '95p':
            DataAnalyticsAnswer = np.percentile(ProcessedData,90)
        elif DataAnalytics == '99p':
            DataAnalyticsAnswer = np.percentile(ProcessedData,95)
        else:
            DataAnalyticsAnswer = 0
        print (DataAnalyticsAnswer)

MathShit('99p')