import streamlit
import requests



def run():

    html_temp ="""


    """
    Link = 'http://192.168.29.80:5000'

    streamlit.markdown(html_temp)
    streamlit.title("Welcome to Help Desk")
    query = streamlit.text_input("Enter your question")
    if streamlit.button("update database"):
        streamlit.success("Updating Database")
        Outs = requests.get(Link+'/UpdateDB')
        streamlit.success("DataBase Upto Date")
    if streamlit.button("Help Desk"):
        if len(query)>= 3:
            Outs = requests.get(Link+'/Qsection/'+str(query))
            if Outs.status_code == 200:
                Title , FileOutput=Outs.json()
                streamlit.success("Question : ­{}".format(query))
                streamlit.success("Title : {}".format(Title))
                streamlit.success("Content : {}".format(FileOutput))
            

if __name__=='__main__':
    run()
