from NLP_thread import NLPPerformance ,DataIngestion
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os

##### Q&A Imports #######


class TopicInference():
    def __init__(self,):
        self.filePrep = DataIngestion()
        self.db = self.filePrep.Load()
        self.objectD = NLPPerformance()
        dbfile = open("./temp.pkl", 'rb')  
        self.Vdb = pickle.load(dbfile)        
        dbfile.close()
        self.DBfilePath = "../Assets/DocumentLibrary/"
    


    def AdminDbUpdate(self):

        """
        After adding documents to the libray run Update utility to add new entries to
        database
        """
        os.system('rm -r ../Assets/DataBase/DataBase.pkl')
        os.system('rm -r ../Assets/DataBase/temp.pkl')
        self.filePrep.TextToPkl()
        self.db = self.filePrep.Load()
        self.objectD.Run(self.db)
        dbfile = open("./temp.pkl", 'rb')  
        self.Vdb = pickle.load(dbfile)        
        dbfile.close()
        
    def Inference(self,query):
        
        Output = ''
        vector1 = self.objectD.ranking_ir(query)
        minCount =0
        Filemane = ''
        Title = ''
        for key in self.Vdb:
            
            sec= cosine_similarity(np.array(vector1).reshape(1, -1),np.array(self.Vdb[key][0]).reshape(1, -1))
            if sec >minCount:
                minCount=sec
                Filemane = str(self.Vdb[key][1]) 
                Title= key
        if len(Title) >3:
            with open(self.DBfilePath+'/'+(Filemane)+'.txt','rt') as file:
                print(self.DBfilePath+'/'+(Filemane)+'.txt')
                lines = file.readlines()
                for l in lines:
                    Output += l

        
        return Title,Output

    def run(self,InputDocs):
        outs = self.Inference(InputDocs)
        return outs



if __name__ =="__main__":
    app = TopicInference()
    query = "What L&T technology services"
    Title , Document = app.run(query)
    print(Title , Document , '\n')
