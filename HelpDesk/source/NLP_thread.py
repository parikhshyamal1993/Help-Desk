import logging
import glob
import pickle
import pandas as pd
import numpy as np
# text Preprocessing
from sklearn.metrics.pairwise import cosine_similarity
import re
from gensim.models import KeyedVectors
import glob
import pickle
import pandas as pd
import numpy as np
#### use only if running the script firt time #####

contractions_dict = { "ain't": "are not","'s":" is","aren't": "are not","can't": "can not","can't've": "cannot have",
"'cause": "because","could've": "could have","couldn't": "could not","couldn't've": "could not have",
"didn't": "did not","doesn't": "does not","don't": "do not","hadn't": "had not","hadn't've": "had not have",
"hasn't": "has not","haven't": "have not","he'd": "he would","he'd've": "he would have","he'll": "he will",
"he'll've": "he will have","how'd": "how did","how'd'y": "how do you","how'll": "how will","i'd": "i would",
"i'd've": "i would have","i'll": "i will","i'll've": "i will have","i'm": "i am","i've": "i have",
"isn't": "is not","it'd": "it would","it'd've": "it would have","it'll": "it will","it'll've": "it will have",
"let's": "let us","ma'am": "madam","mayn't": "may not","might've": "might have","mightn't": "might not",
"mightn't've": "might not have","must've": "must have","mustn't": "must not","mustn't've": "must not have",
"needn't": "need not","needn't've": "need not have","o'clock": "of the clock","oughtn't": "ought not",
"oughtn't've": "ought not have","shan't": "shall not","sha'n't": "shall not",
"shan't've": "shall not have","she'd": "she would","she'd've": "she would have","she'll": "she will",
"she'll've": "she will have","should've": "should have","shouldn't": "should not",
"shouldn't've": "should not have","so've": "so have","that'd": "that would","that'd've": "that would have",
"there'd": "there would","there'd've": "there would have",
"they'd": "they would","they'd've": "they would have","they'll": "they will","they'll've": "they will have",
"they're": "they are","they've": "they have","to've": "to have","wasn't": "was not","we'd": "we would",
"we'd've": "we would have","we'll": "we will","we'll've": "we will have","we're": "we are","we've": "we have",
"weren't": "were not","what'll": "what will","what'll've": "what will have","what're": "what are",
"what've": "what have","when've": "when have","where'd": "where did",
"where've": "where have","who'll": "who will","who'll've": "who will have","who've": "who have",
"why've": "why have","will've": "will have","won't": "will not","won't've": "will not have",
"would've": "would have","wouldn't": "would not","wouldn't've": "would not have","y'all": "you all",
"y'all'd": "you all would","y'all'd've": "you all would have","y'all're": "you all are","y'all've": "you all have",
"you'd": "you would","you'd've": "you would have","you'll": "you will","you'll've": "you will have",
"you're": "you are","you've": "you have"}


### English Stop words ####
#stop_words = set(STOPWORDS).union(stopwords.words("english"))
#stop_words = stop_words.union(['let','mayn','ought','oughtn','shall'])

#print(f'Number of stops words: {len(stop_words)}')



class DataIngestion():
    '''
    This class reads all the text from the Data base folder.
    Text File should be coma(',') separeted where first columns 
    will contain file name and second contains title of the document  

    '''
    def __init__(self):
        '''
        constructor and initializer for data ingestion Pipeline 

        '''
        self.pathToFiles= '../Assets/DocumentEntry/'
        self.LoadPkl = '../Assets/DataBase/DataBase.pkl'
        
    def TextToPkl(self):
        db  = {}
        dbfile = open(self.LoadPkl, 'ab')
        for classes ,testFile  in  enumerate(glob.glob(self.pathToFiles+'*')):
            #print("Files:",testFile)
            #xDataDump = []
            with open(testFile ,"rt") as f:
                data_lines  = f.readlines()
                for l in data_lines:
                    li=l.split(',')
                    print("ID",li[0],"Lines:",li[1])
                    db[li[0]] = li[1]
        pickle.dump(db, dbfile)
        dbfile.close()
 
    def Load(self):
        dbfile = open(self.LoadPkl, 'rb')  
        db = pickle.load(dbfile)        
        dbfile.close()
        return db

class NLPPerformance():
    """
    This is the Feature exctractor class for genrating embedings of the title .
    after generating titles ,all the vectors are stored in a .pkl file 
    We can use database for this task.
    """
    def __init__(self):
        self.w2v_model = KeyedVectors.load_word2vec_format('../Assets/Model/GoogleNews-vectors-negative300.bin', binary=True,limit = 500000)
        

    def expand_contractions(self,text,contractions_dict=contractions_dict):
        """
        This function is compile comman verbs and lemmatic it.
        """
        contractions_re=re.compile('(%s)' % '|'.join(contractions_dict.keys()))
        def replace(match):
            return contractions_dict[match.group(0)]
        return contractions_re.sub(replace, text)

    def clean_text(self,text):
        """
        Pre - processing of text for removing Cap and special charactors
        """

        text=re.sub('\w*\d\w*','', text)
        text=re.sub('\n',' ',text)
        text=re.sub(r"http\S+", "", text)
        text=re.sub('[^a-z]',' ',text)
        return text


    def get_embedding_w2v(self,doc_tokens):
        '''
        Function is a tool for genrating embeddings vectors from the tokens
        
        '''
        embeddings = []
        if len(doc_tokens)<1:
            return np.zeros(300)
        else:
            for tok in doc_tokens:
                if tok in self.w2v_model:
                    embeddings.append(self.w2v_model[tok])
                else:
                    embeddings.append(np.random.rand(300))
           
        return np.mean(embeddings, axis=0)


    def ranking_ir(self,query):
    
        # pre-process Query
        query=query.lower()
        query=self.expand_contractions(query)
        query=self.clean_text(query)
        query=re.sub(' +',' ',query)

        # generating vector
        vector=self.get_embedding_w2v(query.split())

        return vector
    
    def Run(self,db):
        """
        Updating Database 
        """
        print("updating database..." )
        Vector_db=dict()
        
        for key in db:
            print("DB -" , db[key])
            vector = self.ranking_ir(db[key])
            Vector_db[db[key]]= [vector,key] 
                    
        dbfile = open('./temp.pkl', 'ab')
        pickle.dump(Vector_db, dbfile)
        dbfile.close() 
        print(" database upto date..." )

    
        
if __name__ == "__main__":

    filePrep = DataIngestion()
    filePrep.TextToPkl()
    db = filePrep.Load()
    print(db)
    objectD = NLPPerformance()
    objectD.Run(db)
    
