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
course_keyspace = 'course_data'
job_keyspace = 'job_data'

cloud_config= {
    'secure_connect_bundle': bundlepath
}
auth_provider = PlainTextAuthProvider(clientId, clientSecret)
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect()

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

    query = f'select name, subject, enroll, programming_language, fee, framework, level, rating, link from {course_keyspace}.course_search;'
    rs = session.execute(query)
    df = pd.DataFrame(list(rs))

    courses = pd.DataFrame([])
    
    if len(selected_options) != 0:
        courses = courseFilter(selected_options,df)

    top_course = getTopCourses(df)

    #get filter data
    filter_data = getCourseFilterData(df)

    return render_template('course-finder.html', courses = courses , top_course = top_course, selected_options = selected_options,filter_data = filter_data)

@app.route('/job-finder')
def jobSearch():
    selected_options = request.form.getlist('selected_options')

    query = f'select title, industry, enroll, programming_language, min_salary, max_salary, framework, link from {job_keyspace}.job_search;'
    rs = session.execute(query)
    df = pd.DataFrame(list(rs))

    jobs = pd.DataFrame([])
    
    if len(selected_options) != 0:
        jobs = courseFilter(selected_options,df)

    top_job = getTopJob(df)

    #get filter data
    filter_data = getJobFilterData(df)

    return render_template('job-finder.html', jobs = jobs , top_job = top_job, selected_options = selected_options,filter_data = filter_data)

@app.route('/course-visualization')
def courseVisualization():
    
    fig1, fig1_dialog = course_graph1(session)
    graph1JSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
    graph1_dialogJSON = json.dumps(fig1_dialog, cls=plotly.utils.PlotlyJSONEncoder)

    # Graph two
    fig2, fig2_dialog = course_graph2(session)
    graph2JSON = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    graph2_dialogJSON = json.dumps(fig2_dialog, cls=plotly.utils.PlotlyJSONEncoder)

    # Graph three
    fig3, fig3_dialog = course_graph3(session)
    graph3JSON = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
    graph3_dialogJSON = json.dumps(fig3_dialog, cls=plotly.utils.PlotlyJSONEncoder)

    fig4, fig4_dialog = course_graph4(session)
    graph4JSON = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
    graph4_dialogJSON = json.dumps(fig4_dialog, cls=plotly.utils.PlotlyJSONEncoder)

    fig5, fig5_dialog = course_graph5(session)
    graph5JSON = json.dumps(fig5, cls=plotly.utils.PlotlyJSONEncoder)
    graph5_dialogJSON = json.dumps(fig5_dialog, cls=plotly.utils.PlotlyJSONEncoder)

    fig6, fig6_dialog,listSubjects6  = course_graph6(session)
    graph6JSON = json.dumps(fig6, cls=plotly.utils.PlotlyJSONEncoder)
    graph6_dialogJSON = json.dumps(fig6_dialog, cls=plotly.utils.PlotlyJSONEncoder)

    fig7, fig7_dialog,listSubjects7  = course_graph7(session)
    graph7JSON = json.dumps(fig7, cls=plotly.utils.PlotlyJSONEncoder)
    graph7_dialogJSON = json.dumps(fig7_dialog, cls=plotly.utils.PlotlyJSONEncoder)


    fig8, fig8_dialog,listSubjects8  = course_graph8(session)
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
    return render_template('course-visualization.html', graphsData=graphsData)

@app.route('/job-visualization')
def jobVisualization():
    fig1, fig1_dialog = job_graph1(session)
    graph1JSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
    graph1_dialogJSON = json.dumps(fig1_dialog, cls=plotly.utils.PlotlyJSONEncoder)

    # Graph two
    fig2, fig2_dialog = job_graph2(session)
    graph2JSON = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    graph2_dialogJSON = json.dumps(fig2_dialog, cls=plotly.utils.PlotlyJSONEncoder)

    # Graph three
    fig3, fig3_dialog,listSubjects3  = job_graph3(session)
    graph3JSON = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
    graph3_dialogJSON = json.dumps(fig3_dialog, cls=plotly.utils.PlotlyJSONEncoder)

    fig4, fig4_dialog,listSubjects4  = job_graph4(session)
    graph4JSON = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
    graph4_dialogJSON = json.dumps(fig4_dialog, cls=plotly.utils.PlotlyJSONEncoder)

    fig5, fig5_dialog,listSubjects5  = job_graph5(session)
    graph5JSON = json.dumps(fig5, cls=plotly.utils.PlotlyJSONEncoder)
    graph5_dialogJSON = json.dumps(fig5_dialog, cls=plotly.utils.PlotlyJSONEncoder)


    fig6, fig6_dialog = job_graph6(session)
    graph6JSON = json.dumps(fig6, cls=plotly.utils.PlotlyJSONEncoder)
    graph6_dialogJSON = json.dumps(fig6_dialog, cls=plotly.utils.PlotlyJSONEncoder)


    graphsData = [
        {
            'name':'Postings by Industry',
            'chartId':'chart1',
            'dialogId': 'dialog-chart1',
            'graphData': graph1JSON,
            'graphDialogData': graph1_dialogJSON,
            'haveFilter': False,
            'filter': []
        },
        {
            'name':'Salary Range by Industry',
            'chartId':'chart2',
            'dialogId': 'dialog-chart2',
            'graphData': graph2JSON,
            'graphDialogData': graph2_dialogJSON,
            'haveFilter': False,
            'filter': []
        },

        {
            'name':'Proportion of programming languages',
            'chartId':'chart3',
            'dialogId': 'dialog-chart3',
            'graphData': graph3JSON,
            'graphDialogData': graph3_dialogJSON,
            'haveFilter': True,
            'filter': listSubjects3
        },
        {
            'name':'Proportion of frameworks',
            'chartId':'chart4',
            'dialogId': 'dialog-chart4',
            'graphData': graph4JSON,
            'graphDialogData': graph4_dialogJSON,
            'haveFilter': True,
            'filter': listSubjects4
        },
        {
            'name':'Proportion of tools',
            'chartId':'chart5',
            'dialogId': 'dialog-chart5',
            'graphData': graph5JSON,
            'graphDialogData': graph5_dialogJSON,
            'haveFilter': True,
            'filter': listSubjects5
        },
                {
            'name':'Top Technologies',
            'chartId':'chart6',
            'dialogId': 'dialog-chart6',
            'graphData': graph6JSON,
            'graphDialogData': graph6_dialogJSON,
            'haveFilter': False,
            'filter': []
        },
    ]

    return render_template('job-visualization.html', graphsData=graphsData)


def getTopCourses(df):
    df_top = df.sort_values(by = 'rating', ascending=False).head(10)
    return df_top

def courseFilter(options, df):
    subjects = []
    frameworks = []
    programming_languages = []
    levels = []
    for key in options:
        if key.find('Subject') != -1:
            value = key.split(':')[1].strip().lower()
            subjects.append(value)
        if key.find('Framework') != - 1:
            value = key.split(':')[1].strip().lower()
            frameworks.append(value)
        if key.find('Programing Language') != - 1:
            value = key.split(':')[1].strip().lower()
            programming_languages.append(value)
        if key.find('Level') != - 1:
            value = key.split(':')[1].strip().lower()
            levels.append(value)

    conditions = []
    if subjects:
        conditions.append(df['subject'].isin(subjects))
    if levels:
        conditions.append(df['level'].isin(levels))
    if programming_languages:
        programming_language_condition = df['programming_language'].apply(lambda x: any(language in x.split(', ') for language in programming_languages))
        conditions.append(programming_language_condition)
    if frameworks:
        framework_condition = df['framework'].apply(lambda x: any(framework in x.split(', ') for framework in frameworks))
        conditions.append(framework_condition)

    # Áp dụng các điều kiện tìm kiếm (nếu có ít nhất một điều kiện)
    if conditions:
        filtered_df = df[conditions[0]]
        for condition in conditions[1:]:
            filtered_df = filtered_df[condition]
    else:
        filtered_df = df

    return filtered_df

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

def getCourseFilterData(df):
    subjects = [x.title() for x in df.subject.unique()]
    levels = [x.title() for x in df.level.unique()]
    frameworks = getNormalizedArray(df.framework.unique())
    languages = getNormalizedArray(df.programming_language.unique())

    filter_data = [
        {
            'name': 'Subject',
            'value': subjects
        },
        {
            'name': 'Level',
            'value': levels
        },
        {
            'name': 'Framework',
            'value': frameworks
        },
        {
            'name': 'Programing Language',
            'value': languages
        }
    ]
    return filter_data

def getTopJob(df):
    df_top = df.sort_values(by = 'max_salary', ascending=False).head(10)
    return df_top

def jobFilter(options, df):
    industries = []
    frameworks = []
    programming_languages = []
    tools = []
    for key in options:
        if key.find('Industry') != -1:
            value = key.split(':')[1].strip().lower()
            industries.append(value)
        if key.find('Framework') != - 1:
            value = key.split(':')[1].strip().lower()
            frameworks.append(value)
        if key.find('Programing Language') != - 1:
            value = key.split(':')[1].strip().lower()
            programming_languages.append(value)
        if key.find('Tool') != - 1:
            value = key.split(':')[1].strip().lower()
            tools.append(value)

    conditions = []
    if industries:
        conditions.append(df['industry'].isin(industries))
    if programming_languages:
        programming_language_condition = df['programming_language'].apply(lambda x: any(language in x.split(', ') for language in programming_languages))
        conditions.append(programming_language_condition)
    if frameworks:
        framework_condition = df['framework'].apply(lambda x: any(framework in x.split(', ') for framework in frameworks))
        conditions.append(framework_condition)
    if tools:
        tool_condition = df['tool'].apply(lambda x: any(tool in x.split(', ') for tool in tools))
        conditions.append(tool_condition)

    # Áp dụng các điều kiện tìm kiếm (nếu có ít nhất một điều kiện)
    if conditions:
        filtered_df = df[conditions[0]]
        for condition in conditions[1:]:
            filtered_df = filtered_df[condition]
    else:
        filtered_df = df

    return filtered_df

def getJobFilterData(df):
    industries = [x.title() for x in df.industry.unique()]
    frameworks = getNormalizedArray(df.framework.unique())
    languages = getNormalizedArray(df.programming_language.unique())
    tools = getNormalizedArray(df.tool.unique())

    filter_data = [
        {
            'name': 'Industry',
            'value': industries
        },
        {
            'name': 'Framework',
            'value': frameworks
        },
        {
            'name': 'Programing Language',
            'value': languages
        },
                {
            'name': 'Tool',
            'value': tools
        },
    ]
    return filter_data

def course_graph1(session):
    query = f'select * from {course_keyspace}.subject_enroll;'
    result = session.execute(query)
    df = pd.DataFrame(list(result))
    df.columns = ['Subject', 'Total Enroll']
    fig = px.pie(df, names="Subject", values="Total Enroll", height= 420, width= 420)
    fig.update_layout(showlegend=False, margin=dict(t=35, l=0))
    fig.update_traces(textposition='inside', textinfo='percent')
    
    fig_dialog = px.pie(df, names="Subject", values="Total Enroll", height=1100, width= 1100)
    fig_dialog.update_layout( legend=dict(orientation = "h", yanchor="bottom",y=-1.1,xanchor="left", x=0), margin=dict(l=275, r=275, t=15, b=15))
    fig_dialog.update_traces(textposition='inside', textinfo='percent+label')
    return fig, fig_dialog

def course_graph2(session):
    query = f'select * from {course_keyspace}.subject_course;'
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

def course_graph3(session):
    query = f'select subject, level, time from {course_keyspace}.subject_level_time;'
    result = session.execute(query)
    df = pd.DataFrame(list(result))
    df.columns = ['Subject', 'Level', 'Time']
    fig = px.bar(df, x='Subject', y='Time', color='Level', barmode='stack', height=450, width=350)
    fig.update_layout(xaxis={'visible': False, 'showticklabels': True}, margin=dict(t=0, l=0))

    fig_dialog = px.bar(df, x='Subject', y='Time', color='Level', barmode='stack', height=1100, width=1100)
    fig_dialog.update_layout( margin=dict(l=0,r=0, t=50, b=15))
    
    return fig, fig_dialog

def course_graph4(session):
    query = f'select subject, level, fee from {course_keyspace}.subject_level_fee;'
    result = session.execute(query)
    df = pd.DataFrame(list(result))
    df.columns = ['Subject', 'Level', 'Fee']
    fig = px.bar(df, x='Subject', y='Fee', color='Level', barmode='stack', height=450, width=350)
    fig.update_layout( xaxis={'visible': False, 'showticklabels': True}, margin=dict(t=0, l=0))
    fig_dialog = px.bar(df, x='Subject', y='Fee', color='Level', barmode='stack', height=1100, width=1100)
    fig_dialog.update_layout(margin=dict(l=0,r=0, t=50, b=15))
    return fig, fig_dialog

def course_graph5(session):
    query = f'select * from {course_keyspace}.top_tech;'
    result = session.execute(query)
    df = pd.DataFrame(list(result))
    df.columns = ['Type', 'Name','Total Courses']
    df_limited = df.groupby('Type').apply(lambda x: x.nlargest(10, 'Total Courses')).reset_index(drop=True)
    fig = px.bar(df_limited, x='Type', y='Total Courses', color='Name', barmode='group', height=450, width=350)
    fig.update_layout( xaxis={'visible': False, 'showticklabels': True}, margin=dict(t=0, l=0))

    fig_dialog = px.bar(df_limited, x='Type', y='Total Courses', color='Name', barmode='group', height=1100, width =1100)
    fig_dialog.update_layout(margin=dict(l=0,r=0, t=50, b=15))
    return fig, fig_dialog

def course_graph6(session):
    query = f'select subject,programming_language,total_course from {course_keyspace}.subject_language_course;'
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

def course_graph7(session):
    query = f'select subject,framework,total_course from {course_keyspace}.subject_framework_course;'
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

def course_graph8(session):
    query = f'select subject,tool,total_course from {course_keyspace}.subject_tool_course;'
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

def job_graph1(session):
    query = f'select industry,total_job from {job_keyspace}.industry_job;'
    result = session.execute(query)
    df = pd.DataFrame(list(result))
    df.columns = ['Industry', 'Total Postings']

    fig = px.pie(df, names="Industry", values="Total Postings",height= 420, width= 420)
    fig.update_layout(showlegend=False, margin=dict(t=35, l=0))
    fig.update_traces(textposition='inside', textinfo='percent')

    fig_dialog = px.pie(df, names="Industry", values="Total Postings", height=1100, width= 1100)
    fig_dialog.update_layout(legend=dict(orientation = "h", yanchor="bottom",y=-1.1,xanchor="left", x=0), margin=dict(l=275, r=275, t=15, b=15))
    fig_dialog.update_traces(textposition='inside', textinfo='percent+label')
    return fig, fig_dialog

def job_graph2(session):
    query = f'select industry,min_salary, max_salary from {job_keyspace}.industry_salary;'
    result = session.execute(query)
    df = pd.DataFrame(list(result))
    df.columns = ['Industry', 'Min Salary', 'Max Salary']
    fig = px.bar(df, x='Industry', y=['Min Salary', 'Max Salary'], barmode='group')
    # Cấu hình tiêu đề và trục
    fig.update_layout(
        title='Salary Range by Industry',
        xaxis_title='Industry',
        yaxis_title='Salary',
        showlegend=False, margin=dict(t=35, l=0)
    )

    fig_dialog = px.bar(df, x='Industry', y=['Min Salary', 'Max Salary'], barmode='group')
    fig_dialog.update_layout(
        title='Salary Range by Industry',
        xaxis_title='Industry',
        yaxis_title='Salary'
    )
    return fig, fig_dialog

def job_graph3(session):
    query = f'select industry,programming_language,total_job from {job_keyspace}.industry_language_job;'
    result = session.execute(query)
    df = pd.DataFrame(list(result))
    df.columns = ['Industry', 'Programming Language', 'Total Postings']
    industries_list = df['Industry'].unique().tolist()
    list_fig = []
    list_fig_dialog = []
    for industry in industries_list:
        df_language = df[df['Industry'] == industry]
        fig = px.pie(df_language, names="Programming Language", values="Total Postings", height= 420, width= 420)
        fig.update_layout(showlegend=False, margin=dict(t=35, l=0))
        fig.update_traces(textposition='inside', textinfo='percent')
        list_fig.append(fig)

        fig_dialog = px.pie(df_language, names="Programming Language", values="Total Postings", height=1100, width= 1100)
        fig_dialog.update_layout(legend=dict(orientation = "h", yanchor="bottom",y=-1.1,xanchor="left", x=0), margin=dict(l=275, r=275, t=15, b=15))
        fig_dialog.update_traces(textposition='inside', textinfo='percent+label')
        list_fig_dialog.append(fig_dialog)

    return list_fig ,list_fig_dialog, list(enumerate(industries_list))

def job_graph4(session):
    query = f'select industry,framework,total_job from {job_keyspace}.industry_framework_job;'
    result = session.execute(query)
    df = pd.DataFrame(list(result))
    df.columns = ['Industry', 'Framework', 'Total Postings']
    industries_list = df['Industry'].unique().tolist()
    list_fig = []
    list_fig_dialog = []
    for industry in industries_list:
        df_language = df[df['Industry'] == industry]
        fig = px.pie(df_language, names="Framework", values="Total Postings", height= 420, width= 420)
        fig.update_layout(showlegend=False, margin=dict(t=35, l=0))
        fig.update_traces(textposition='inside', textinfo='percent')
        list_fig.append(fig)

        fig_dialog = px.pie(df_language, names="Framework", values="Total Postings", height=1100, width= 1100)
        fig_dialog.update_layout(legend=dict(orientation = "h", yanchor="bottom",y=-1.1,xanchor="left", x=0), margin=dict(l=275, r=275, t=15, b=15))
        fig_dialog.update_traces(textposition='inside', textinfo='percent+label')
        list_fig_dialog.append(fig_dialog)

    return list_fig ,list_fig_dialog, list(enumerate(industries_list))

def job_graph5(session):
    query = f'select industry,tool,total_job from {job_keyspace}.industry_tool_job;'
    result = session.execute(query)
    df = pd.DataFrame(list(result))
    df.columns = ['Industry', 'Tool', 'Total Postings']
    industries_list = df['Industry'].unique().tolist()
    list_fig = []
    list_fig_dialog = []
    for industry in industries_list:
        df_language = df[df['Industry'] == industry]
        fig = px.pie(df_language, names="Tool", values="Total Postings", height= 420, width= 420)
        fig.update_layout(showlegend=False, margin=dict(t=35, l=0))
        fig.update_traces(textposition='inside', textinfo='percent')
        list_fig.append(fig)

        fig_dialog = px.pie(df_language, names="Tool", values="Total Postings", height=1100, width= 1100)
        fig_dialog.update_layout(legend=dict(orientation = "h", yanchor="bottom",y=-1.1,xanchor="left", x=0), margin=dict(l=275, r=275, t=15, b=15))
        fig_dialog.update_traces(textposition='inside', textinfo='percent+label')
        list_fig_dialog.append(fig_dialog)

    return list_fig ,list_fig_dialog, list(enumerate(industries_list))

def job_graph6(session):
    query = f'select tech_type,tech_name,total_job from {job_keyspace}.top_tech;'
    result = session.execute(query)
    df = pd.DataFrame(list(result))
    df.columns = ['Tech Type', 'Tech Name','Total Postings']
    df_limited = df.groupby('Tech Type').apply(lambda x: x.nlargest(10, 'Total Postings')).reset_index(drop=True)
    fig = px.bar(df_limited, x='Tech Type', y='Total Postings', color='Tech Name', barmode='group', height=450, width=350)
    fig.update_layout( xaxis={'visible': False, 'showticklabels': True}, margin=dict(t=0, l=0))

    fig_dialog = px.bar(df_limited, x='Tech Type', y='Total Postings', color='Tech Name', barmode='group', height=1100, width =1100)
    fig_dialog.update_layout(margin=dict(l=0,r=0, t=50, b=15))
    return fig, fig_dialog