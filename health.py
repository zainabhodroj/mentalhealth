import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.express as px
import hydralit_components as hc
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import plotly.express as px
import time
import requests
from streamlit_lottie import st_lottie
import json
import matplotlib.pyplot as plt 

# Streamlit Style Settings
def webapp_style():
    hide_streamlit_style = """
                <style>
                    #MainMenu {
                                visibility: none;
                            }
                    footer {
                            visibility: hidden;
                            }
                    footer:after {
                                content:'Made by Zainab Hodroj ❤️'; 
                                visibility: visible;
                                display: block;
                                position: relative;
                                text-align: center;
                                padding: 15px;
                                top: 2px;
                                }
    
                </style>
                """
    markdown = st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    return markdown

#defining lottie function to visualize animated pictures
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)


def upload():

    # Dispaly Upload File Widget
    uploaded = st.file_uploader(label="Upload your own data", type=["csv"])

    # Save the file in internal memory of streamlit
    if 'file' not in st.session_state:
        st.session_state['file'] = None


    st.session_state['file'] = uploaded

    if 'table' not in st.session_state:
        st.session_state['table'] = None 
    
        
    if uploaded is not None:
        st.session_state['table'] = pd.read_csv(uploaded)
        return st.session_state['table']
    else:
        st.session_state['table'] = pd.read_csv('mental_health.csv')
        return st.session_state['table']



#setting configuration of the page and expanding it
st.set_page_config(layout='wide', initial_sidebar_state='collapsed', page_title='Mental Health in Tech')
st.expander('Expander')


#creating menu data which will be used in navigation bar specifying the pages of the dashboard
menu_data = [
    {'label': "Home", 'icon': 'bi bi-house-fill'},
    {'label': 'Data', 'icon': 'bi bi-bar-chart'},
    {'label':"EDA", 'icon':'bi bi-search'},
    {'label':"MHD Prediction", 'icon': 'bi bi-clipboard-data'},
    ]

over_theme = {'txc_inactive': 'white','menu_background':'rgb(255, 57, 210)', 'option_active':'white'}


#inserting hydralit component: nagivation bar
menu_id = hc.nav_bar(
    menu_definition=menu_data,
    override_theme=over_theme,
    hide_streamlit_markers=False,
    sticky_nav=True, #at the top or not
    sticky_mode='pinned', #jumpy or not-jumpy, but sticky or pinned
)

#editing first page of the dashboard with images, titles, and text
if menu_id == 'Home':
    col1, col2 = st.columns(2)
    #col1.image('churn.png')
    with col1:
        st.title('Mental Health in Tech')
        st.write('Mental health is a state of mental well-being that enables people to cope with the stresses of life, realize their abilities, learn well and work well, and contribute to their community. It is an integral component of health and well-being that underpins our individual and collective abilities to make decisions, build relationships and shape the world we live in. Mental health is a basic human right. And it is crucial to personal, community and socio-economic development.')
        st.write("It is more than the absence of mental disorders. It exists on a complex continuum, which is experienced differently from one person to the next, with varying degrees of difficulty and distress and potentially very different social and clinical outcomes.")
        m = st.markdown("""
        <style>
            div.stButton > button:first-child {
            color: #fff;
            background-color: rgb(112, 230, 220);
            }
        </style>""", unsafe_allow_html=True)
        st.write("---")

    with col2:
        lottie_home= load_lottiefile("meditating.json")
        st_lottie(lottie_home)
        



#BREAK
#editing second page which is about the data
if menu_id == 'Data':
    #add option to choose own data or given data defined earlier
    upload()
    col1, col2 = st.columns([2,1])

    with col1:
        lottie_data= load_lottiefile("therapy.json")
        st_lottie(lottie_data)

    with col2:
        st.title("Let's Take a Look at the Data")
        st.markdown("""
        <style>
        .change-font {
        font-size:20px !important;
        }
        </style>
        """, unsafe_allow_html=True)
        st.markdown('<p class="change-font">Mental Health is a very important matter that only now is starting to arrise within the tech community.. </p>', unsafe_allow_html=True)
        st.markdown('<p class="change-font">Their are different factors that can affect a someones mental health including family history, employment status, and resources available.</p>', unsafe_allow_html=True)
        df= pd.read_csv(r'mental_health.csv')
        st.write("Data was obtained from the Kaggle-[OSMI Mental Health in Tech Survey](https://www.kaggle.com/datasets/osmihelp/osmi-mental-health-in-tech-survey-2019) ", unsafe_allow_html=True)
        if st.checkbox('Dataset'):
            st.dataframe(df.head(5))
        if st.checkbox('Statistics'):
            st.dataframe(df.describe())




#BREAK
#3rd page which is about the EDA
if menu_id == 'EDA':
    col1, col2, col3 = st.columns([1,1,1])
    
    with col1:
        # clean "Gender" column
        df = pd.read_csv('mental_health.csv')
        import seaborn as sns
        # Filtering and renaming data
        industry_support_mh = pd.DataFrame(df["Overall, how well do you think the tech industry supports employees with mental health issues?"])
        industry_support_mh = industry_support_mh.rename(columns=
                                                 {"Overall, how well do you think the tech industry supports employees with mental health issues?": 
                                                  "Tech Industry Support to Mental Health Issues"})
        # Creating a count plot 
        plt.figure(figsize=(10,5))
        sns.set_style("ticks")
        ax1 = sns.countplot(x="Tech Industry Support to Mental Health Issues", data=industry_support_mh, 
                    color = 'salmon', saturation = 0.7)
        sns.despine()

    # Formatting chart axes, title, size
        plt.title('Overall Tech Industry Support to Mental Health Issues', size = 16)
        plt.xlabel('Response Score 0:Lowest to 5:Highest', size = 12)
        plt.ylabel('Number of Participants', size = 12)

    # Formatting to show counts and percentages on the bars
        total = float(len(industry_support_mh))
        for p in ax1.patches:
            height = p.get_height()
            ax1.text(p.get_x()+p.get_width()/2.,
                height + 1,
                '{:1.0f}'.format(height) + ' (' + '{:1.0f}'.format(100*(height/total)) + '%' + ')',
                ha="center", size=11, color = 'black') 
        st.pyplot(plt)
        st.write("Response for score 3 has the highest votes with 40% of the participants")   
        st.write("16% of the participants have responded between 4-5.")
    
        # Suffering from mental disorders
        suffered = pd.DataFrame(df.filter(items=[ 'Do you *currently* have a mental health disorder?', 
                                            'Have you had a mental health disorder in the past?' ]))

        suffered = suffered.rename(columns= {'Do you *currently* have a mental health disorder?': 'Currently', 
                                            'Have you had a mental health disorder in the past?': 'Past'})

        # Currently
        suffered_current = pd.DataFrame(suffered[['Currently']])
        suffered_current['Illness Period'] = 'Current'
        suffered_current = suffered_current.rename(columns= {'Currently': 'Response'})

        # In the past
        suffered_past = pd.DataFrame(suffered[['Past']])
        suffered_past['Illness Period'] = 'Past'
        suffered_past = suffered_past.rename(columns= {'Past': 'Response'})

        # Combined current and past
        suffered_all = suffered_current.append(suffered_past)
        suffered_all['Participants'] = 1


        # Count Plot
        g = sns.catplot(x="Response", hue="Illness Period", data=suffered_all, kind="count", palette = "pastel");
        sns.set_style("ticks")
        sns.despine()

        # Formatting chart axes, title, size
        plt.title('Suffering from Mental Disorder', size = 16)
        plt.xlabel('Response', size = 12)
        plt.ylabel('Number of Participants', size = 12)
        st.pyplot(plt)
        st.write("42% are currently suffering from a mental disorder or have suffered in the past.")
        st.write("29% are unsure if they have ever suffered from a mental disorder in the past/at present.")
    
    with col2:  
        # Coverage
        coverage = pd.DataFrame(df["Does your employer provide mental health benefits as part of healthcare coverage?"])
        coverage['Participants'] = 1
        coverage = coverage.rename(columns= {"Does your employer provide mental health benefits as part of healthcare coverage?": 
                                     "Coverage"})
        # Awareness
        awareness = pd.DataFrame(df["Do you know the options for mental health care available under your employer-provided health coverage?"])
        awareness['Participants'] = 1
        awareness = awareness.rename(columns= 
                                      {"Do you know the options for mental health care available under your employer-provided health coverage?": 
                                       "Awareness"})
        # Discussions
        discussions = pd.DataFrame(df["Has your employer ever formally discussed mental health (for example, as part of a wellness campaign or other official communication)?"])
        discussions['Participants'] = 1
        discussions = discussions.rename(columns= 
                                      {"Has your employer ever formally discussed mental health (for example, as part of a wellness campaign or other official communication)?": 
                                       "Discussions"})
        # Help Resources
        resources = pd.DataFrame(df["Does your employer offer resources to learn more about mental health disorders and options for seeking help?"])
        resources['Participants'] = 1
        resources = resources.rename(columns= 
                                      {"Does your employer offer resources to learn more about mental health disorders and options for seeking help?": 
                                       "Resources"})

        # Aggregate Number of Participants by Response type
        coverage = coverage.groupby(['Coverage']).Participants.agg('sum').to_frame('Participants Count').reset_index()
        awareness = awareness.groupby(['Awareness']).Participants.agg('sum').to_frame('Participants Count').reset_index()
        discussions = discussions.groupby(['Discussions']).Participants.agg('sum').to_frame('Participants Count').reset_index()
        resources = resources.groupby(['Resources']).Participants.agg('sum').to_frame('Participants Count').reset_index()

        # Filter Positive Responses for Funnel Visualization
        coverage = coverage[coverage['Coverage'] == 'Yes']
        coverage = coverage.rename(columns= {"Coverage" : "Response"})
        coverage['Stage'] = "Coverage"

        awareness = awareness[awareness['Awareness'] == 'Yes']
        awareness = awareness.rename(columns= {"Awareness" : "Response"})
        awareness['Stage'] = "Awareness"

        discussions = discussions[discussions['Discussions'] == 'Yes']
        discussions = discussions.rename(columns= {"Discussions" : "Response"})
        discussions['Stage'] = "Discussions"

        resources = resources[resources['Resources'] == 'Yes']
        resources = resources.rename(columns= {"Resources" : "Response"})
        resources['Stage'] = "Help Resources"

        # Combine Positive Responses for all 4 Stages
        all_stages = coverage.append(awareness)
        all_stages = all_stages.append(discussions)
        all_stages = all_stages.append(resources)
        all_stages['Total Participants'] = df.shape[0]
        all_stages['% Participants'] = round(100 * all_stages['Participants Count']/all_stages['Total Participants'],0)

        # All Stages combined
        all_stages = all_stages[['Stage', 'Response', 'Participants Count', 'Total Participants', '% Participants']]
    

        # Bar chart for % Participants Comparison
        plt.figure(figsize=(7,4))
        graph = sns.barplot(x="Stage", y="% Participants", data=all_stages, palette="Blues_d", saturation = 0.7)
        sns.set_style("ticks")
        sns.despine()

        # Formatting chart axes, title, size
        plt.title('Medical Coverage and Help Resources for Mental Health Issues', size = 16)
        plt.xlabel('Stages', size = 14)
        plt.ylabel('% of Participants', size = 14)


        # Formatting to show counts and percentages on the bars
        for p in graph.patches:
            graph.annotate('{:.0f}'.format(p.get_height()) + '%', (p.get_x()+0.3, p.get_height()),
                    ha='center', va='bottom',
                    color= 'black', size = 12) 
        st.pyplot(plt)
        st.write("The number of participants decreases as we move down the stages from coverage at 47% to offering help resources at 29%.")
    
    
        # Physical Health Importance
        physical_importance = pd.DataFrame(df["Overall, how much importance does your employer place on physical health?"])
        physical_importance['Participants'] = 1
        physical_importance['Health Type'] = 'Physical'
        physical_importance = physical_importance.rename(columns= {"Overall, how much importance does your employer place on physical health?": 
                                     "Importance Level"})

        physical_importance = physical_importance.groupby(['Importance Level', 'Health Type']).Participants.agg('sum').to_frame('Participants Count').reset_index()

        # Mental Health Importance
        mental_importance = pd.DataFrame(df["Overall, how much importance does your employer place on mental health?"])
        mental_importance['Participants'] = 1
        mental_importance['Health Type'] = 'Mental'
        mental_importance = mental_importance.rename(columns= {"Overall, how much importance does your employer place on mental health?": 
                                     "Importance Level"})

        mental_importance = mental_importance.groupby(['Importance Level', 'Health Type']).Participants.agg('sum').to_frame('Participants Count').reset_index()

        # Number of Participants by Response type
        importance = physical_importance.append(mental_importance)
        compare_importance = pd.merge(physical_importance, mental_importance, how='outer', on=['Importance Level']) 
        compare_importance = compare_importance.rename(columns= {'Participants Count_x': 'Physical Health', 'Participants Count_y': 'Mental Health'})
        # Grouped bar chart
        plt.figure(figsize=(20,14))
        sns.set_style("ticks")
        ax = sns.barplot(x="Importance Level", y="Participants Count", hue="Health Type", data=importance, palette = "Paired")
        sns.despine()

        # Formatting chart axes, title, size
        plt.title('Importance Mental vs Physical Health', size = 16)
        plt.xlabel('Importance by Employer', size = 12)
        plt.ylabel('Number of Participants', size = 12)

        st.pyplot(plt)
        st.write("The importance given by employers to physical health has higher distribution between scores 5 to 10 with the highest at 5.")
        st.write("And the Importance to mental health has higher values between scores 3 to 7 with the highest at 5")
    
    with col3:
        # Leave Policy
        leave = pd.DataFrame(df["If a mental health issue prompted you to request a medical leave from work, how easy or difficult would it be to ask for that leave?"])
        leave['Participants'] = 1
        leave = leave.rename(columns= {"If a mental health issue prompted you to request a medical leave from work, how easy or difficult would it be to ask for that leave?": 
                                     "Leave Difficulty"})


        #Tabular Output - Aggregate Number of Participants by Response type
        total_participants = df.shape[0]
        leave = leave.groupby(['Leave Difficulty']).Participants.agg('sum').to_frame('Participants Count').reset_index()
        leave['% Participants'] = round(100 * leave['Participants Count']/total_participants,0)

    # Creating a count plot 
        plt.figure(figsize=(12,6))
        sns.set_style("ticks")
        ax1 = sns.countplot(x="If a mental health issue prompted you to request a medical leave from work, how easy or difficult would it be to ask for that leave?", 
                    data=df, 
                    palette="Blues_d", saturation = 0.7,
                    order = df['If a mental health issue prompted you to request a medical leave from work, how easy or difficult would it be to ask for that leave?'].value_counts().index)
        sns.despine()

        # Formatting chart axes, title, size
        plt.title('Difficulty in asking for leave for mental health issues', size = 16)
        plt.xlabel('Leave Difficulty', size = 12)
        plt.ylabel('Number of Participants', size = 12)

    # Formatting to show counts and percentages on the bars
        total = total_participants
        for p in ax1.patches:
            height = p.get_height()
            ax1.text(p.get_x()+p.get_width()/2.,
                height + 1,
                '{:1.0f}'.format(height) + ' (' + '{:1.0f}'.format(100*(height/total)) + '%' + ')',
                ha="center", size=11, color = 'black') 
        st.pyplot(plt)
        st.write("About 44% of the participants find it relatively easy to ask for leaves for mental health, while 19% find it relatively difficult.And 30% of the participants are neutral/unaware of the difficulty they may pose while asking for time off")
        
        
#Break        
# 4th page Prediction
if menu_id == 'MHD Prediction':
    # load assets (lotties animation)
    lottie1 = load_lottiefile("predict.json")
    #1 Create header and title
    with st.container():
        st.title("Mental Health Disorder (MHD) Prediction")
    col1, col2 = st.columns((1,1))
    with col1:
        st.write("""Mental health disorders (MHD) are spread everywhere. Nearly 800 million people live with an MHD. It is therefore not surprising that MHDs are essential axes of global health. 
                 [Check Out the dataset here](https://www.kaggle.com/datasets/osmihelp/osmi-mental-health-in-tech-survey-2019)""")
        st.write("We have created a model that targets the recognition of mental health disorders. It will help assess the risk of whether an individual currently has MHD or not. But will not replace seeking medical attention.")
        #adding animation and figures to the right column
    with col2:
        st_lottie(lottie1, height=300, width=800, key="mental health")
        #3 create the second part with the input questions
        st.write("---")
        #add header for the input part

        #adding input options 
    col1, col2 = st.columns([2.5,1])
    with col1:
            st.subheader("Please complete this questionnaire and click on MHD TEST")
            age = st.number_input("What is your age?", min_value=18, max_value=65, step=1)
            mhd_in_the_past = st.selectbox('Have you had a mental health disorder in the past?',
        ('Yes', 'Maybe', 'No'))
            mhd_coworkers_discussion = st.selectbox('Would you feel comfortable discussing a mental health disorder with your coworkers?',
        ('Yes', 'Maybe', 'No'))
            mhd_diagnosis = st.selectbox('Have you been diagnosed with a mental health condition by a medical professional?',
        ('Yes', 'No'))
            gender = st.selectbox('What is your gender?',
        ('female', 'male', 'others'))
            mhd_family_history = st.selectbox('Do you have a family history of mental illness?',
        ('No', 'Yes', 'I do not know'))
            mhd_interview = st.selectbox('Would you bring up a mental health issue with a potential employer in an interview?',
        ('Maybe', 'No', 'Yes'))
            prev_employer_mhd_seriousness = st.selectbox('Did you feel that your previous employers took mental health as seriously as physical health?',
        ('None did', 'I do not know', 'Some did', 'Yes, they all did'))
            mhd_unsupportive_response = st.selectbox('Have you observed or experienced an unsupportive or badly handled response to a mental health issue in your current or previous workplace?',
        ('No', 'Maybe/Not sure', 'Yes, I observed', 'Yes, I experienced'))
            mhd_work_interfere = st.selectbox('If you have a mental health issue, do you feel that it interferes with your work when NOT being treated effectively?',
        ('Never', 'Not applicable to me', 'Rarely', 'Sometimes', 'Often'))
            #4 load model and create new dataframe
            with st.container():
                import pickle
            loaded_model = pickle.load(open('mhd_classifier_rf.sav', 'rb'))
            # 5 assigning values to the new df
            with st.container():
                new_df = pd.DataFrame({
                    'age':[age],
                    'mhd_in_the_past':[mhd_in_the_past], 
                    'mhd_coworkers_discussion':[mhd_coworkers_discussion], 
                    'mhd_diagnosis':[mhd_diagnosis],
                    'gender':[gender],
                    'mhd_family_history':[mhd_family_history], 
                    'mhd_interview':[mhd_interview], 
                    'prev_employer_mhd_seriousness':[prev_employer_mhd_seriousness],
                    'mhd_unsupportive_response':[mhd_unsupportive_response], 
                    'mh_work_interfere':[mhd_work_interfere]
                    })

    # 6 predict_proba(new_df) and create botton for diagnosis
    if st.button('MHD TEST'):
         diagnosis = (pd.DataFrame(loaded_model.predict_proba(new_df)) * 100).round(decimals = 1)
         st.write(f'There is {diagnosis.iat[0,2]} % chance that you currently have a MHD') 
             
            


    
#BREAK
webapp_style()
