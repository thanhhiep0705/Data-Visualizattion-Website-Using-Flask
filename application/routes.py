import os
import re
from tkinter import Widget
from application import app
from flask import render_template, request
import pandas as pd
import json
import plotly
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import logging
import numpy as np

app.config['ACTIVE_TAB'] = '/'
bundlepath = 'application/secure-connect-course-data.zip'
clientId = 'URRrzRFMRvuBIZmLFumeqhvl'
clientSecret = '++uM_E,5pH2kGnzZTqpYGU,E,GimsdCU5g_XtTckupaBmIkeMT9kaxAP82SgAr72t4w.I4zUsq.TU6.z4xihUYHgG4Y6AOiPjl-mRNk.6DxLYngZT025ZWF05+Hqo1l5'
keyspace = 'course_data'

@app.route('/')
def index():
    return render_template('home.html')


@app.route('/manage-crawler')
def test():
# Dữ liệu mẫu
    x_data = [1, 2, 3, 4, 5]
    y_data = [10, 15, 7, 12, 8]
    

    # Tạo biểu đồ
    fig = go.Figure(data=go.Scatter(x=x_data, y=y_data, mode='lines'))

    # Tạo bộ lọc
    dropdown_filter = go.layout.Updatemenu(
        buttons=list([
            dict(label='Tất cả',
                method='update',
                args=[{'visible': [True]},
                    {'title': 'Tất cả'}]),
            dict(label='Dữ liệu 1',
                method='update',
                args=[{'visible': [True, False, False, False, False]},
                    {'title': 'Dữ liệu 1'}]),
            dict(label='Dữ liệu 2',
                method='update',
                args=[{'visible': [False, True, False, False, False]},
                    {'title': 'Dữ liệu 2'}])
        ]),
        direction='down',
        showactive=True
    )

    # Cập nhật layout của biểu đồ
    fig.update_layout(
        title='Biểu đồ với bộ lọc',
        updatemenus=[dropdown_filter],
        autosize=False,
        width=500,
        height=500
    )
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # Hiển thị biểu đồ
    return render_template('manage-crawler.html', graphJSON = graphJSON)

@app.route('/data')
def data():
    source_data = [
        {
            'title' : 'Job Postings Data',
            'data' : [
                {
                    'title': 'LinkedIn',
                    'information':[
                        {
                            'title': 'Members',
                            'value': '740+ M'
                        },
                        {
                            'title': 'Companies',
                            'value': '50+ M'
                        },
                        {
                            'title': 'Languages',
                            'value': '24'
                        }
                    ],
                    'website': 'https://www.linkedin.com/jobs/search?trk=guest_homepage-basic_guest_nav_menu_jobs&position=1&pageNum=0'
                },
                {
                    'title': 'NodeFlair',
                    'information':[
                        {
                            'title': 'Members',
                            'value': '4,000+'
                        },
                        {
                            'title': 'Companies',
                            'value': '5,000+'
                        },
                        {
                            'title': 'Partners',
                            'value': '200+'
                        }
                    ],
                    'website': 'https://nodeflair.com/'
                }
            ]
        },

        {
            'title' : 'Courses Data',
        
            'data' : [
                {
                    'title': 'Coursera',
                    'information':[
                        {
                            'title': 'Courses',
                            'value': '4,000+'
                        },
                        {
                            'title': 'Learners',
                            'value': '82+ M'
                        },
                        {
                            'title': 'Partners',
                            'value': '200+'
                        }
                    ],
                    'website': 'https://www.coursera.org/?irclickid=wlvRjDSqHxyNUeaU9XwM0VgNUkASXR1pbw4DUw0&irgwc=1&utm_medium=partners&utm_source=impact&utm_campaign=2985301&utm_content=b2c'
                },
                {
                    'title': 'Udemy',
                    'information':[
                        {
                            'title': 'Courses',
                            'value': '130,000+'
                        },
                        {
                            'title': 'Learners',
                            'value': '40+ M'
                        },
                        {
                            'title': 'Countries',
                            'value': '190+'
                        }
                    ],
                    'website': 'https://www.udemy.com/?ranMID=39197&ranEAID=yNfEamYSgXk&ranSiteID=yNfEamYSgXk-Q716xy3YHMHwt8IcQqpOnA&LSNPUBID=yNfEamYSgXk&utm_source=aff-campaign&utm_medium=udemyads&gclid=Cj0KCQjwyLGjBhDKARIsAFRNgW8Ng4w4tvTFvPbBKcXsbBwCk4SyZdluQ97e3dvxkn5X7DtUWHJqyQAaAv0KEALw_wcB'
                },
                {
                    'title': 'edX',
                    'information':[
                        {
                            'title': 'Courses',
                            'value': '3,000+'
                        },
                        {
                            'title': 'Learners',
                            'value': '38+ M'
                        },
                        {
                            'title': 'Partners',
                            'value': '120+'
                        }
                    ],
                    'website': 'https://www.edx.org/?irclickid=wlvRjDSqHxyNUeaU9XwM0VgNUkASXW0Zbw4DUw0&utm_source=affiliate&utm_medium=Ecom%20EWAY&utm_campaign=Online%20Tracking%20Link_&utm_content=ONLINE_TRACKING_LINK&irgwc=1'
                }
            ]
        }
    ]
    return render_template('data.html', source_data = source_data)

@app.route('/about')
def about():
    team_members = [
        {
            'name': 'Nguyen Tran Minh Thu',
            'role': 'Instructor',
            'image': '../static/img/businesswoman.png',
            'information':[
                {
                    'title': 'University',
                    'value': 'University of Science'
                },
                {
                    'title': 'Degree',
                    'value': 'Doctor'
                },
                {
                    'title': 'Job',
                    'value': 'Lecturers'
                },
                {
                    'title': 'Major',
                    'value': 'Information System'
                },
                {
                    'title': 'Email',
                    'value': 'ntmthu@fit.hcmus.edu.vn'
                },
                {
                    'title': 'Hobbies',
                    'value': 'Reading, Cooking'
                }
            ]
        },
        {
            'name': 'Nguyen Pham Quang Dung',
            'role': 'Team Leader',
            'image': '../static/img/man.png',
            'information':[
                {
                    'title': 'University',
                    'value': 'University of Science'
                },
                {
                    'title': 'StudentID',
                    'value': '19120485'
                },
                {
                    'title': 'Major',
                    'value': 'Data Science'
                },
                {
                    'title': 'Email',
                    'value': 'npqdung17@gmail.com'
                },
                {
                    'title': 'Future Job',
                    'value': 'Data Engineer'
                },
                {
                    'title': 'Hobbies',
                    'value': 'Hiking, Cooking'
                }
            ]
        },
        {
            'name': 'Duong Thanh Hiep',
            'role': 'Team Member',
            'image': '../static/img/hacker.png',
            'information':[
                {
                    'title': 'University',
                    'value': 'University of Science'
                },
                {
                    'title': 'StudentID',
                    'value': '19120505'
                },
                {
                    'title': 'Major',
                    'value': 'Computer Science'
                },
                {
                    'title': 'Email',
                    'value': 'hiep0705@gmail.com'
                },
                {
                    'title': 'Future Job',
                    'value': 'Web Developer'
                },
                {
                    'title': 'Hobbies',
                    'value': 'Traveling, Football'
                }
            ]
        },
        {
            'name': 'Nguyen Thi Tieu Mi',
            'role': 'Team Member',
            'image': '../static/img/woman.png',
            'information':[
                {
                    'title': 'University',
                    'value': 'University of Science'
                },
                {
                    'title': 'StudentID',
                    'value': '19120577'
                },
                {
                    'title': 'Major',
                    'value': 'Information System'
                },
                {
                    'title': 'Email',
                    'value': 'tieumi2509@gmail.com'
                },
                {
                    'title': 'Future Job',
                    'value': 'Web Developer'
                },
                {
                    'title': 'Hobbies',
                    'value': 'Reading, Cooking'
                }
            ]
        },
        {
            'name': 'Le Thanh Loc',
            'role': 'Team Member',
            'image': '../static/img/businessman.png',
            'information':[
                {
                    'title': 'University',
                    'value': 'University of Science'
                },
                {
                    'title': 'StudentID',
                    'value': '19120562'
                },
                {
                    'title': 'Major',
                    'value': 'Information System'
                },
                {
                    'title': 'Email',
                    'value': 'lochcmus@gmail.com'
                },
                {
                    'title': 'Future Job',
                    'value': 'Data Engineer'
                },
                {
                    'title': 'Hobbies',
                    'value': 'Singing, Traveling'
                }
            ]
        },
        {
            'name': 'Nguyen Thi Kim Ngan',
            'role': 'Team Member',
            'image': '../static/img/girl.png',
            'information':[
                {
                    'title': 'University',
                    'value': 'University of Science'
                },
                {
                    'title': 'StudentID',
                    'value': '19120598'
                },
                {
                    'title': 'Major',
                    'value': 'Information System'
                },
                {
                    'title': 'Email',
                    'value': 'ntkn.mnkt@gmail.com'
                },
                {
                    'title': 'Future Job',
                    'value': 'Web Developer'
                },
                {
                    'title': 'Hobbies',
                    'value': 'Reading, Hiking'
                }
            ]
        }
    ]
    return render_template('about.html', team_members=team_members)

@app.route('/course-finder', methods=['GET', 'POST'])
def courseFinder():
    selected_options = request.form.getlist('selected_options')
    print(selected_options)

    cloud_config= {
        'secure_connect_bundle': bundlepath
    }
    auth_provider = PlainTextAuthProvider(clientId, clientSecret)
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    session = cluster.connect()

    query = 'select name, subject, enroll, organization, language, fee, framework, level, rating, link from sample.course;'
    rs = session.execute(query)
    df = pd.DataFrame(list(rs))
    
    course = getSelectedCourses(selected_options,df)

    # course = df.head(5)
    top_course = getTopCourses(df)

    #get filter data

    filter_datas = getFilterData(df)

    return render_template('course-finder.html', course = course , top_course = top_course, selected_options = selected_options,filter_datas = filter_datas)

def getTopCourses(df):
    df_top = df.sort_values(by = 'rating', ascending=False).head(10)
    return df_top

def getSelectedCourses(options, df):
    subjects = []
    frameworks = []
    languages = []
    levels = []
    for key in options:
        if key.find('Subjects') != -1:
            value = key.split(':')[1].strip().lower()
            subjects.append(value)
        if key.find('Frameworks') != - 1:
            value = key.split(':')[1].strip().lower()
            frameworks.append(value)
        if key.find('Programing Language') != - 1:
            value = key.split(':')[1].strip().lower()
            frameworks.append(value)
        if key.find('Level') != - 1:
            value = key.split(':')[1].strip().lower()
            levels.append(value)
    
    #get equivalent courses from df
    df_subject = pd.DataFrame()
    df_framework = pd.DataFrame()
    df_language = pd.DataFrame()
    df_level = pd.DataFrame()
    df_course = pd.DataFrame()
    if (len(subjects) != 0):
        for subject in subjects:
            temp = df.loc[df['subject'].map(str.lower).str.contains(subject)]
            df_subject = df_subject.append(temp, ignore_index=False)
    
    if (len(frameworks) != 0):
        for framework in frameworks:
            temp = df.loc[df['framework'].map(str.lower).str.contains(framework)]
            df_framework = df_framework.append(temp, ignore_index=False)
    
    if (len(languages) != 0):
        for language in languages:
            temp = df.loc[df['language'].map(str.lower).str.contains(language)]
            df_language = df_language.append(temp, ignore_index=False)
    
    if (len(levels) != 0):
        for level in levels:
            temp = df.loc[df['level'].map(str.lower).str.contains(level)]
            df_level = df_level.append(temp, ignore_index=False)

    #check empty
    if (df_subject.empty == False):
        df_course = df_course.append(df_subject)
    
    if (df_framework.empty == False):
        df_course = df_course.append(df_framework)

    if (df_language.empty == False):
        df_course = df_course.append(df_language)
    
    if (df_level.empty == False):
        df_course = df_course.append(df_level)

    df_course = df_course.drop_duplicates(keep='first')

    return df_course

def getNormalizedArray(array):
    result = []
    for row in array:
        rs=[]
        if row.find(',') != -1:
            rs = row.split(",")
            rs = list(map(str.strip, rs))
            for item in rs:
                if item.title().strip() not in result:
                    result.append(item.title())
        else: 
            if row.title().strip() not in result:
                result.append(row.title().strip())

    return result

def getFilterData(df):
    subjects = [x.title() for x in df.subject.unique()]
    levels = [x.title() for x in df.level.unique()]
    frameworks = getNormalizedArray(df.framework.unique())
    languages = getNormalizedArray(df.language.unique())

    filter_datas = [
        {
            'name': 'Subjects',
            'value': subjects
            # [
            #     'Computer Science', 'Web Development', 'Data Science', 'Microservices', 'Mobile Development', 'Business'
            # ]
        },
        {
            'name': 'Frameworks',
            'value': frameworks
            # [
            #     'VueJS', 'ReactJS', 'AngularJS', 'JQuery', 'MySQL', 'Django','LaravelJS'
            # ]
        },
        {
            'name': 'Programing Language',
            'value': languages
            # [
            #     'Python', 'Java', 'JavaScript', 'C++','Julia', 'Scala'
            # ]
        },
        
        {
            'name': 'Level',
            'value': levels
            # [
            #     'Beginner', 'Intermediate','Advanced'
            # ]
        }
    ]
    return filter_datas

@app.route('/job-finder')
def jobSearch():
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the file path for the CSV file
    csv_path = os.path.join(current_dir, 'static', 'Job.csv')

    # Load the CSV file into a DataFrame
    df = pd.read_csv(csv_path, encoding='latin1')
    job = df.head(5)
    top_job = df.head(5)

    return render_template('job-finder.html', job = job , top_job = top_job)

@app.route('/course-visualization')
def courseVisualization():
    cloud_config= {
        'secure_connect_bundle': bundlepath
    }
    auth_provider = PlainTextAuthProvider(clientId, clientSecret)
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    session = cluster.connect()
    
    fig1, fig1_dialog = graph1(session)
    graph1JSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
    graph1_dialogJSON = json.dumps(fig1_dialog, cls=plotly.utils.PlotlyJSONEncoder)

    # Graph two
    fig2, fig2_dialog = graph2(session)
    graph2JSON = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    graph2_dialogJSON = json.dumps(fig2_dialog, cls=plotly.utils.PlotlyJSONEncoder)

    # Graph three
    fig3, fig3_dialog = graph3(session)
    graph3JSON = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
    graph3_dialogJSON = json.dumps(fig3_dialog, cls=plotly.utils.PlotlyJSONEncoder)

    fig4, fig4_dialog = graph4(session)
    graph4JSON = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
    graph4_dialogJSON = json.dumps(fig4_dialog, cls=plotly.utils.PlotlyJSONEncoder)

    fig5, fig5_dialog = graph5(session)
    graph5JSON = json.dumps(fig5, cls=plotly.utils.PlotlyJSONEncoder)
    graph5_dialogJSON = json.dumps(fig5_dialog, cls=plotly.utils.PlotlyJSONEncoder)

    fig6, fig6_dialog,listSubjects6  = graph6(session)
    graph6JSON = json.dumps(fig6, cls=plotly.utils.PlotlyJSONEncoder)
    graph6_dialogJSON = json.dumps(fig6_dialog, cls=plotly.utils.PlotlyJSONEncoder)

    fig7, fig7_dialog,listSubjects7  = graph7(session)
    graph7JSON = json.dumps(fig7, cls=plotly.utils.PlotlyJSONEncoder)
    graph7_dialogJSON = json.dumps(fig7_dialog, cls=plotly.utils.PlotlyJSONEncoder)


    fig8, fig8_dialog,listSubjects8  = graph8(session)
    graph8JSON = json.dumps(fig8, cls=plotly.utils.PlotlyJSONEncoder)
    graph8_dialogJSON = json.dumps(fig8_dialog, cls=plotly.utils.PlotlyJSONEncoder)


    graphsData = [
        {
            'name':'Enrolls by Subject',
            'chartId':'chart1',
            'dialogId': 'dialog-chart1',
            'graphData': graph1JSON,
            'graphDialogData': graph1_dialogJSON,
            'haveFilter': False,
            'filter': []
        },
        {
            'name':'Courses by Subject',
            'chartId':'chart2',
            'dialogId': 'dialog-chart2',
            'graphData': graph2JSON,
            'graphDialogData': graph2_dialogJSON,
            'haveFilter': False,
            'filter': []
        },
        {
            'name':'Average Time by Subject',
            'chartId':'chart3',
            'dialogId': 'dialog-chart3',
            'graphData': graph3JSON,
            'graphDialogData': graph3_dialogJSON,
            'haveFilter': False,
            'filter': []
        },
        {
            'name':'Average Fee by Subject',
            'chartId':'chart4',
            'dialogId': 'dialog-chart4',
            'graphData': graph4JSON,
            'graphDialogData': graph4_dialogJSON,
            'haveFilter': False,
            'filter': []
        },
        {
            'name':'Top Technologies',
            'chartId':'chart5',
            'dialogId': 'dialog-chart5',
            'graphData': graph5JSON,
            'graphDialogData': graph5_dialogJSON,
            'haveFilter': False,
            'filter': []
        },
        {
            'name':'Proportion of programming languages',
            'chartId':'chart6',
            'dialogId': 'dialog-chart6',
            'graphData': graph6JSON,
            'graphDialogData': graph6_dialogJSON,
            'haveFilter': True,
            'filter': listSubjects6
        },
        {
            'name':'Proportion of frameworks',
            'chartId':'chart7',
            'dialogId': 'dialog-chart7',
            'graphData': graph7JSON,
            'graphDialogData': graph7_dialogJSON,
            'haveFilter': True,
            'filter': listSubjects7
        },
        {
            'name':'Proportion of tools',
            'chartId':'chart8',
            'dialogId': 'dialog-chart8',
            'graphData': graph8JSON,
            'graphDialogData': graph8_dialogJSON,
            'haveFilter': True,
            'filter': listSubjects8
        },
    ]

    session.shutdown()
    cluster.shutdown()
    return render_template('course-visualization.html', graphsData=graphsData)

def convert_to_hours(time):
    match = re.match(r'(\d+(?:\.\d+)?)', str(time))
    if match:
        return float(match.group(1))
    return None

def convert_to_fee(fee):
    if isinstance(fee, str):
        match = re.search(r'\d+\.\d+|\d+', fee)
        if match:
            return float(match.group())
    return 0

#thong ke so luong hoc vien theo tưng linh vuc (subject)
def graph1(session):
    query = f'select * from {keyspace}.subject_enroll;'
    result = session.execute(query)
    df = pd.DataFrame(list(result))
    df.columns = ['Subject', 'Total Enroll']
    fig = px.pie(df, names="Subject", values="Total Enroll", height= 420, width= 420)
    fig.update_layout(showlegend=False, margin=dict(t=35, l=0))
    fig.update_traces(textposition='inside', textinfo='percent')
    
    fig_dialog = px.pie(df, names="Subject", values="Total Enroll", height=1100, width= 1100)
    fig_dialog.update_layout( legend=dict(orientation = "h", yanchor="bottom",y=-1.1,xanchor="left", x=0), margin=dict(l=275, r=275, t=15, b=15))
    fig_dialog.update_traces(textposition='inside', textinfo='percent+label')
    # dropdown_options = [dict(label='All',
    #                     method='update',
    #                     args=[{'visible': [True] * len(df_subject_enroll)}])]
    # for subject in df_subject_enroll['Subject']:
    #     dropdown_options.append({'label': subject, 'method': 'update', 'args': [{'visible': [subject == item for item in df_subject_enroll['Subject'].tolist()]}]})

    # # Add the dropdown menu to the layout
    # fig_dialog.update_layout(
    #     updatemenus=[
    #         dict(
    #             buttons=dropdown_options,
    #             direction='down',
    #             showactive=True,
    #             xanchor='left',
    #             yanchor='top',
    #         ),
    #     ]
    # )

    return fig, fig_dialog

def graph2(session):
    query = f'select * from {keyspace}.subject_course;'
    result = session.execute(query)
    df = pd.DataFrame(list(result))
    df.columns = ['Subject', 'Total Courses']
    fig = px.pie(df, names="Subject", values="Total Courses",height= 420, width= 420)
    fig.update_layout(showlegend=False, margin=dict(t=35, l=0))
    fig.update_traces(textposition='inside', textinfo='percent')

    fig_dialog = px.pie(df, names="Subject", values="Total Courses", height=1100, width= 1100)
    fig_dialog.update_layout(legend=dict(orientation = "h", yanchor="bottom",y=-1.1,xanchor="left", x=0), margin=dict(l=275, r=275, t=15, b=15))
    fig_dialog.update_traces(textposition='inside', textinfo='percent+label')
    return fig, fig_dialog

def graph3(session):
    query = f'select subject, level, time from {keyspace}.subject_level_time;'
    result = session.execute(query)
    df = pd.DataFrame(list(result))
    df.columns = ['Subject', 'Level', 'Time']
    fig = px.bar(df, x='Subject', y='Time', color='Level', barmode='stack', height=450, width=350)
    fig.update_layout(xaxis={'visible': False, 'showticklabels': True}, margin=dict(t=0, l=0))

    fig_dialog = px.bar(df, x='Subject', y='Time', color='Level', barmode='stack', height=1100, width=1100)
    fig_dialog.update_layout( margin=dict(l=0,r=0, t=50, b=15))
    
    return fig, fig_dialog

def graph4(session):
    query = f'select subject, level, fee from {keyspace}.subject_level_fee;'
    result = session.execute(query)
    df = pd.DataFrame(list(result))
    df.columns = ['Subject', 'Level', 'Fee']
    fig = px.bar(df, x='Subject', y='Fee', color='Level', barmode='stack', height=450, width=350)
    fig.update_layout( xaxis={'visible': False, 'showticklabels': True}, margin=dict(t=0, l=0))
    fig_dialog = px.bar(df, x='Subject', y='Fee', color='Level', barmode='stack', height=1100, width=1100)
    fig_dialog.update_layout(margin=dict(l=0,r=0, t=50, b=15))
    return fig, fig_dialog

def graph5(session):
    query = f'select * from {keyspace}.top_tech;'
    result = session.execute(query)
    df = pd.DataFrame(list(result))
    df.columns = ['Type', 'Name','Total Courses']
    df_limited = df.groupby('Type').apply(lambda x: x.nlargest(10, 'Total Courses')).reset_index(drop=True)
    # subjects_to_plot = df_subject_time['Subject'].unique()[10:20]
    # df_subject_time = df_subject_time.query('Subject in @subjects_to_plot')
    fig = px.bar(df_limited, x='Type', y='Total Courses', color='Name', barmode='group', height=450, width=350)
    fig.update_layout( xaxis={'visible': False, 'showticklabels': True}, margin=dict(t=0, l=0))
    # fig = px.bar(df, x="Subject", y="Total Courses", color='Subject', height=450, width=350)
    # fig.update_layout( xaxis={'visible': False}, margin=dict(t=0, l=0))

    fig_dialog = px.bar(df_limited, x='Type', y='Total Courses', color='Name', barmode='group', height=1100, width =1100)
    fig_dialog.update_layout(margin=dict(l=0,r=0, t=50, b=15))
    return fig, fig_dialog

def graph6(session):
    query = f'select subject,programming_language,total_course from {keyspace}.subject_language_course;'
    result = session.execute(query)
    df = pd.DataFrame(list(result))
    df.columns = ['Subject', 'Language', 'Courses']
    subjects_list = df['Subject'].unique().tolist()
    list_fig = []
    list_fig_dialog = []
    for subject in df['Subject'].unique().tolist():
        df_language = df[df['Subject'] == subject]
        fig = px.pie(df_language, names="Language", values="Courses", height= 420, width= 420)
        fig.update_layout(showlegend=False, margin=dict(t=35, l=0))
        fig.update_traces(textposition='inside', textinfo='percent')
        list_fig.append(fig)

        fig_dialog = px.pie(df_language, names="Language", values="Courses", height=1100, width= 1100)
        fig_dialog.update_layout(legend=dict(orientation = "h", yanchor="bottom",y=-1.1,xanchor="left", x=0), margin=dict(l=275, r=275, t=15, b=15))
        fig_dialog.update_traces(textposition='inside', textinfo='percent+label')
        list_fig_dialog.append(fig_dialog)


    return list_fig ,list_fig_dialog, list(enumerate(subjects_list))

def graph7(session):
    query = f'select subject,framework,total_course from {keyspace}.subject_framework_course;'
    result = session.execute(query)
    df = pd.DataFrame(list(result))
    df.columns = ['Subject', 'Framework', 'Courses']
    subjects_list = df['Subject'].unique().tolist()
    list_fig = []
    list_fig_dialog = []
    for subject in df['Subject'].unique().tolist():
        df_language = df[df['Subject'] == subject]
        fig = px.pie(df_language, names="Framework", values="Courses", height= 420, width= 420)
        fig.update_layout(showlegend=False, margin=dict(t=35, l=0))
        fig.update_traces(textposition='inside', textinfo='percent')
        list_fig.append(fig)

        fig_dialog = px.pie(df_language, names="Framework", values="Courses", height=1100, width= 1100)
        fig_dialog.update_layout(legend=dict(orientation = "h", yanchor="bottom",y=-1.1,xanchor="left", x=0), margin=dict(l=275, r=275, t=15, b=15))
        fig_dialog.update_traces(textposition='inside', textinfo='percent+label')
        list_fig_dialog.append(fig_dialog)

    return list_fig ,list_fig_dialog, list(enumerate(subjects_list))

def graph8(session):
    query = f'select subject,tool,total_course from {keyspace}.subject_tool_course;'
    result = session.execute(query)
    df = pd.DataFrame(list(result))
    df.columns = ['Subject', 'Tool', 'Courses']
    subjects_list = df['Subject'].unique().tolist()
    list_fig = []
    list_fig_dialog = []
    for subject in df['Subject'].unique().tolist():
        df_language = df[df['Subject'] == subject]
        fig = px.pie(df_language, names="Tool", values="Courses", height= 420, width= 420)
        fig.update_layout(showlegend=False, margin=dict(t=35, l=0))
        fig.update_traces(textposition='inside', textinfo='percent')
        list_fig.append(fig)

        fig_dialog = px.pie(df_language, names="Tool", values="Courses", height=1100, width= 1100)
        fig_dialog.update_layout(legend=dict(orientation = "h", yanchor="bottom",y=-1.1,xanchor="left", x=0), margin=dict(l=275, r=275, t=15, b=15))
        fig_dialog.update_traces(textposition='inside', textinfo='percent+label')
        list_fig_dialog.append(fig_dialog)

    return list_fig ,list_fig_dialog, list(enumerate(subjects_list))

# def graph7():
#     CASSANDRA_IP = '127.0.0.1'
#     cluster = Cluster([CASSANDRA_IP])
#     session = cluster.connect()
#     rows = session.execute("SELECT release_version FROM system.local")
#     for row in rows:
#         print(row.release_version)



@app.route('/job-visualization')
def jobVisualization():
    # Graph One
    df = px.data.medals_wide()
    fig1 = px.bar(df, x="nation", y=["gold", "silver", "bronze"])
    graph1JSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)

    # Graph two
    df = px.data.iris()
    fig2 = px.scatter_3d(df, x='sepal_length', y='sepal_width', z='petal_width',
              color='species')
    graph2JSON = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)

    # Graph three
    df = px.data.gapminder().query("continent=='Oceania'")
    fig3 = px.line(df, x="year", y="lifeExp", color='country')
    graph3JSON = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)

    #Graph four
    data_canada = px.data.gapminder().query("country == 'Canada'")
    fig4 = px.bar(data_canada, x='year', y='pop')
    graph4JSON = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)

    graphsData = [
        {
            'name':'Chart 1',
            'chartId':'chart1',
            'dialogId': 'dialog-chart1',
            'graphData': graph1JSON,
            'graphDialogData': graph1JSON
        },
        {
            'name':'Chart 2',
            'chartId':'chart2',
            'dialogId': 'dialog-chart2',
            'graphData': graph2JSON,
            'graphDialogData': graph1JSON
        },
        {
            'name':'Chart 3',
            'chartId':'chart3',
            'dialogId': 'dialog-chart3',
            'graphData': graph3JSON,
            'graphDialogData': graph1JSON
        },
                {
            'name':'Chart 4',
            'chartId':'chart4',
            'dialogId': 'dialog-chart4',
            'graphData': graph4JSON,
            'graphDialogData': graph1JSON
        }
        ]

    return render_template('job-visualization.html', graphsData=graphsData)


