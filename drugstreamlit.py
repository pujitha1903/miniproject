#https://towardsdatascience.com/make-dataframes-interactive-in-streamlit-c3d0c4f84ccb
import streamlit as st
import requests
import pandas as pd
import requests
import plotly.express as px
from streamlit_option_menu import option_menu
from PIL import Image

def streamlit_menu(example=1):
    selected = option_menu(
                menu_title=None,  # required
                options=["Home","Dataset","Visualizations", "Prediction"],  # required
                icons=["house", "table", "map", "calculator"],  # optional
                menu_icon="cast",  # optional
                default_index=0,  # optional
                orientation="horizontal",
            )
    return selected

selected = streamlit_menu()
#with tab1:
if selected == "Home":
    st.title("CLASSIFICATION OF SEVERITY OF DRUG ADVERSE EFFECTS")
    st.write("The project idea was absorbed from the people that we see in our daily life. People are using different types of medicines for various diseases \
        Many of us know that these medicines will have side effects, but there is something that we need to look into, the adverse effects causing in long period of time. \
        In this project, we would like to classify the severity of adverse drug effects.")
    st.write("The data source: https://download.open.fda.gov/drug/event/2022q1/drug-event-0001-of-0035.json.zip (it is one of the file) There are more than 100 files, if we open the this link (https://open.fda.gov/data/downloads/). ")
    st.write("The data we are concentrating is 2022 data in 'Human Drug' section, 'Drug Adverse Events' sub-section.\
        The project covers the Data wrangling, Data Cleaning, Data Visualization, Data Modeling, Prediction.")

    col13, col15 = st.columns(2)
    with col13:
        st.subheader("Under the guidance of")
        # image3 = Image.open('1614283657796.jpeg')
        # st.image(image3, caption='Dr.Ozgur Ozturk')
    # with col14:
        st.write("Mr.S.Ch.Vijaya Bhaskar")
    with col15:
        st.subheader("By - ")
        # image1 = Image.open('IMG_8447.jpeg')
        # st.image(image1, caption='Sai Manoj Kalasani - FH55174')
        st.write("T.Vignesh")
        st.write("B.Sahithya")
        st.write("K.Pujitha")
        # image2 = Image.open('Shreya Patil.jpeg')
        # st.image(image2, caption='Shreya Patil - HG53212')
       
    #st.header("---------By Sai Manoj Kalasani - FH55174, Shreya Patil - HG53212")
if selected == "Dataset":
    st.title("DRUG ADVERSE EFFECTS DATASET")
    r=requests.get('http://127.0.0.1:5000/getusers')
    re= r.json()
    y= re['data']
    df= pd.DataFrame.from_dict(y, orient ='columns')
    # st.markdown('Dataset')
    st.write(df)
    
    rma = df['reactionmeddrapt'].unique()
    mcp = df['medicinalproduct'].unique()
    ddf = df['drugdosageform'].unique()
    dind = df['drugindication'].unique()
    options = st.selectbox('Questions about Dataset:', ('Rows & columns', 'Size of the file', 'Data description'))
    if options == 'Rows & columns':
        st.write(str(df.shape[0])+" Rows and "+str(df.shape[1])+" Columns")
    elif options == 'Size of the file':
        st.write("2.26 Gb")
    else:
        st.write("ACTION DRUG - Classification of drugs by their usage")
        st.write("AGE GROUP - Created a column by segregating the people into different categories of life.")
        st.write("DRUG DOSAGE FORM - The forms in which drug is given to the patients")
        st.write("DRUG INDICATION - Name of the disease on which the drug is given")
        st.write("FULFILLEXPEDITECRITERIA - Identifies expedited reports (those that were processed within 15 days).")
        st.write("MEDICINAL PRODUCT - Name of the product")
        st.write("PATIENT SEX - Gender of the patient")
        st.write("REACTION MEDDRAPT - Adverse reactions faced by the patients while using the respective drug")
        st.write("REACTION OUTCOME - Classification of reactions into different levels.")
        st.write("REPORT TYPE - Code indicating the circumstances under which the report was generated.")
        st.write("TARGET - Created column with combining all the levels of seriousness for multiclass classification")
# with tab2:
if selected == "Prediction":
    st.title("PREDICTION")
    col1,col2,col3 = st.columns(3)
    col4,col5,col6 = st.columns(3)
    col7,col8= st.columns(2)
    col9, col10 = st.columns(2)
    col11, col12 = st.columns(2)

    #conn= create_connection('ant.db')
    with col1:   
        reporttype = st.selectbox('Report type',['1','2','3'])
    with col2:
        fulfillexpeditecriteria = st.number_input('fulfill Expedite Criteria', 1, 6)
    with col3:
        patientsex= st.selectbox('Sex',['Male','Female'])
    with col4:
        reactionmeddrapt = st.selectbox('Reaction Meddrapt',['Neutrophil count decreased', 'Death','Dyskinesia', 'Catheterisation cardiac', 'Neck pain','Gastrointestinal wall thickening', 'Anaemia macrocytic','T-lymphocyte count decreased'])
    with col5:
        reactionoutcome = st.selectbox('Reaction Outcome',['1','2','3','4','5','6'])
    with col6:
        drugcharacterization = st.selectbox('Drug Characterization', ['1','2','3','4','5','6'])
    with col7:
        medicinalproduct = st.selectbox('Medicinal Product', ['RYTARY','NUPLAZID', 'ENTRESTO', 'DEFINITY', 'NORSPAN','PSEUDOEPHEDRINE HYDROCHLORIDE', 'DEXTROSE','VALPROATE SODIUM'])
    with col8:
        drugdosageform = st.selectbox('Dosage Form', ['Capsule', 'Tablet', 'Injection', 'Other', 'ENT_drops', 'Ointment','Inhale ', 'Implant', 'Oral', 'Patch','Investigational dosage form', 'Film'])
    with col9:
        drugindication = st.selectbox('Drug indication', ['Mental disorder','Parkinson^s disease', 'Product used for unknown indication','Stress echocardiogram', 'Device related infection','Plasmacytoma', 'Cardiac arrest'])
    with col10:
        actiondrug = st.slider('Action Drug',1, 6)
    with col11:
        age_group = st.selectbox('Age Group',['[0,20]', '[20,40]', '[40,60]', '[60,80]', '[80,99]'])


    def predict(event):
        resp = requests.post('http://127.0.0.1:5000/prediction', json={'data':[[reporttype, str(fulfillexpeditecriteria), patientsex, reactionmeddrapt, reactionoutcome, drugcharacterization, medicinalproduct, drugdosageform, drugindication, str(actiondrug), age_group]]})
        print("22222")
        print(resp)
        val = resp.json()
        target = val["Prediction"]
        print(target)
        return target

    target = predict(1)
    #print(target)
    col_1, col_2, col_3 = st.columns(3)
    with col_2:
        if st.button('PREDICT THE SERIOUSNESS'):
            #st.write("The predicted value is:", str(target))
            if target == 0:
                st.write("YOU ARE FINE...., NO ISSUE WITH THIS DRUG! YOU CAN USE IT ")
            elif target == 1:
                st.write("CONSULT A DOCTOR BEFORE YOU USE IT, IT CAN LEAD TO HOSPITALIZATION")
            elif target == 2:
                st.write("CAUTION!!, THIS CAN LEAD TO LIFE THREATENING OR DISABILING")
            else:
                st.write("HIGHLY NOT RECOMMENDED - THIS MAY CAUSE DEATH")
    
if selected == "Visualizations":
    add_radio = st.sidebar.radio("Visualizations",("Distribution Visualizations", "Seriousness by Dosage form"))
    if add_radio == "Distribution Visualizations":
        add_selectbox = st.sidebar.selectbox("Distribution Visualizations",("Gender", "Age", "Age & Gender"))
        # if add_selectbox == "Gender":
        #     image1 = Image.open('gender distribution.png')
        #     st.image(image1, caption='Gender Distribution Chart')
        # elif add_selectbox == "Age":
        #     image1 = Image.open('Age Group Distribution.png')
        #     st.image(image1, caption='Age Group Distribution Chart')
        # else:
        #     image1 = Image.open('Age Gender Distribution.png')
        #     st.image(image1, caption='Age Gender Distribution Chart')
    else:
        add_selectbox = st.sidebar.selectbox("Seriousness",("Death", "Hospitalization","Life threatening"))
        if add_selectbox == "Death":
            # image1 = Image.open('Death Seriousness.png')
            # st.image(image1, caption='Death seriousness by dosage form distribution Chart')
            pass
        elif add_selectbox == "Hospitalization":
            # image1 = Image.open('Hospitalization seriousness.png')
            pass
            # st.image(image1, caption='Hospitalization seriousness by dosage form distribution Chart')
        else:
            # image1 = Image.open('Life Threatening Seriousness.png')
            # st.image(image1, caption='Life threatening seriousness by dosage form distribution Chart')
            pass
       
        