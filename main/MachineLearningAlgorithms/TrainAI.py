from test1.models import Questions, MLdata
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import scipy

##Step 1: Read CSV File
#df = pd.read_csv("test1/MachinelearningAlgorithms/MachineLearningDataSet.csv", encoding='cp1252')
#print(df.columns)

#features = ['index','title','slug','author','updated_on','body','created_on','status','tags','views','answers','upvotes','downvotes','isanswered','isclosed']
def combine_features(row):
	return str(row['index']) + " " + row['title'] + " " + row['slug'] + " " + row["author"] + " " + str(row["updated_on"]) + " " + str(row['body']) + " " + str(row['created_on']) + " " + str(row["status"]) + " " + row["tags"] + " " + str(row['views']) + " " + str(row['answers']) + " " + str(row["upvotes"]) + " " + str(row["downvotes"]) + " " + str(row["isanswered"]) + " " + str(row['isclosed'])
#df["combined_features"] = df.apply(combine_features,axis=1)
#print("Combined Features:", df["combined_features"].head())
#cv = CountVectorizer()
#count_matrix = cv.fit_transform(df["combined_features"])
#pickle.dump(count_matrix, open('test1/MachineLearningAlgorithms/Trained_AI_Model.sav', 'wb'))


def RetrainModel():
    loaded_model = pickle.load(open('test1/MachineLearningAlgorithms/Trained_AI_Model.sav', 'rb'))
    df2 = pd.read_csv("test1/MachineLearningAlgorithms/MachineLearningDataSet2.csv", encoding='cp1252')
    df2["combined_features"] = df2.apply(combine_features,axis=1)
    if loaded_model is None:
	    temp_model = loaded_model
    else:
        cv = CountVectorizer()
        prd = cv.fit_transform(df2["combined_features"])
        print(prd.shape)
        print(loaded_model.shape)
        diff_n_rows = loaded_model.shape[0] - prd.shape[0]
        prd_new  = scipy.sparse.vstack((prd, scipy.sparse.csr_matrix ((diff_n_rows,(prd.shape[1])))))
        temp_model_one = scipy.sparse.hstack((loaded_model, prd_new))
        diff_n_rows2 = temp_model_one.shape[1] - prd.shape[1]
        prd_new_left = scipy.sparse.hstack((prd, scipy.sparse.csr_matrix (((prd.shape[0]),diff_n_rows2))))
        temp_model = scipy.sparse.vstack((prd_new_left, temp_model_one))
        print(temp_model.shape)
    pickle.dump(temp_model, open('test1/MachineLearningAlgorithms/Trained_AI_Model.sav', 'wb'))
    return True

def InitialLoad(question_index):
    question_ids = []
    loaded_model = pickle.load(open('test1/MachineLearningAlgorithms/Trained_AI_Model.sav', 'rb'))
    print(loaded_model.shape)
    cosine_sim = cosine_similarity(loaded_model)
    similar_questions = list(enumerate(cosine_sim[question_index]))
    sorted_similar_questions = sorted(similar_questions, key=lambda x: x[1], reverse=True)
    for element in sorted_similar_questions:
        question_ids.append(get_index_from_id(element[0]))
    return  question_ids


def get_index_from_id(id):
     mldata = MLdata.objects.filter(ML_id = id)
     return mldata[0].index