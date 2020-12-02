from .models import Questions, MLdata
from django.db.models import Max

def CreateDS(id):
    f = open("test1/MachineLearningAlgorithms/MachineLearningDataSet2.csv", "w")
    f.write("id,index,title,slug,author,updated_on,body,created_on,status,tags,views,answers,upvotes,downvotes,isanswered,isclosed\n")
    Main_data = Questions.objects.filter(id=id)
    latest_id = MLdata.objects.aggregate(Max('ML_id'))
    latest_id = latest_id['ML_id__max'] + 1
    for Data_all in Main_data:
        clean_body = Data_all.body.replace(",", "|")
        clean_body = clean_body.encode('utf-8').strip()
        csv_format = str(latest_id) + "," + str(Data_all.id) + "," + Data_all.title + "," + Data_all.slug + "," + str(Data_all.author) + "," + str(Data_all.updated_on) + "," + str(clean_body) + "," + str(Data_all.created_on) + "," + str(Data_all.status) + "," + str(Data_all.tags) + "," + str(Data_all.views) + "," + str(Data_all.answers) + "," + str(Data_all.upvotes) + "," + str(Data_all.downvotes) + "," + str(Data_all.isanswered) + "," + str(Data_all.isclosed) + "\n"
        f.write(csv_format)
    f.close()
    return latest_id
