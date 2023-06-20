from application import app
from flask import render_template, request
import pandas as pd
import json
import plotly
import plotly.express as px
import plotly.graph_objects as go
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

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

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/data')
def data():
    source_data = [
        {
            'title' : 'Nguồn dữ liệu tuyển dụng',
            'data' : [
                {
                    'title': 'LinkedIn',
                    'information':[
                        {
                            'title': 'Người dùng',
                            'value': '740+ M'
                        },
                        {
                            'title': 'Công ty',
                            'value': '50+ triệu'
                        },
                        {
                            'title': 'Ngôn ngữ',
                            'value': '24'
                        }
                    ],
                    'website': 'https://www.linkedin.com/jobs/search?trk=guest_homepage-basic_guest_nav_menu_jobs&position=1&pageNum=0'
                },
                {
                    'title': 'NodeFlair',
                    'information':[
                        {
                            'title': 'Người dùng',
                            'value': '4,000+'
                        },
                        {
                            'title': 'Công ty',
                            'value': '5,000+'
                        },
                        {
                            'title': 'Đối tác',
                            'value': '200+'
                        }
                    ],
                    'website': 'https://nodeflair.com/'
                }
            ]
        },

        {
            'title' : 'Nguồn dữ liệu khóa học',
        
            'data' : [
                {
                    'title': 'Coursera',
                    'information':[
                        {
                            'title': 'Khóa học',
                            'value': '4,000+'
                        },
                        {
                            'title': 'Người dùng',
                            'value': '82+ triệu'
                        },
                        {
                            'title': 'Đối tác',
                            'value': '200+'
                        }
                    ],
                    'website': 'https://www.coursera.org/?irclickid=wlvRjDSqHxyNUeaU9XwM0VgNUkASXR1pbw4DUw0&irgwc=1&utm_medium=partners&utm_source=impact&utm_campaign=2985301&utm_content=b2c'
                },
                {
                    'title': 'Udemy',
                    'information':[
                        {
                            'title': 'Khóa học',
                            'value': '65,000+'
                        },
                        {
                            'title': 'Người dùng',
                            'value': '20+ triệu'
                        },
                        {
                            'title': 'Quốc gia',
                            'value': '190+'
                        }
                    ],
                    'website': 'https://www.udemy.com/?ranMID=39197&ranEAID=yNfEamYSgXk&ranSiteID=yNfEamYSgXk-Q716xy3YHMHwt8IcQqpOnA&LSNPUBID=yNfEamYSgXk&utm_source=aff-campaign&utm_medium=udemyads&gclid=Cj0KCQjwyLGjBhDKARIsAFRNgW8Ng4w4tvTFvPbBKcXsbBwCk4SyZdluQ97e3dvxkn5X7DtUWHJqyQAaAv0KEALw_wcB'
                },
                {
                    'title': 'edX',
                    'information':[
                        {
                            'title': 'Khóa học',
                            'value': '3,000+'
                        },
                        {
                            'title': 'Người dùng',
                            'value': '38+ triệu'
                        },
                        {
                            'title': 'Đối tác',
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
            'name': 'Nguyễn Trần Minh Thư',
            'role': 'Giáo viên hướng dẫn',
            'image': '../static/img/businesswoman.png',
            'information':[
                {
                    'title': 'Trường',
                    'value': 'Đại học KHTN, ĐHQG-HCM'
                },
                {
                    'title': 'Khoa',
                    'value': 'Công nghệ thông tin'
                },
                {
                    'title': 'Học vị',
                    'value': 'Tiến sĩ'
                },
                {
                    'title': 'Nghề nghiệp',
                    'value': 'Giảng viên'
                },
                {
                    'title': 'Chuyên ngành',
                    'value': 'Hệ thống thông tin'
                },
                {
                    'title': 'Email',
                    'value': 'ntmthu@fit.hcmus.edu.vn'
                },
                {
                    'title': 'Sở thích',
                    'value': 'Đọc sách, Nấu ăn'
                }
            ]
        },
        {
            'name': 'Nguyễn Phạm Quang Dũng',
            'role': 'Trưởng nhóm',
            'image': '../static/img/man.png',
            'information':[
                {
                    'title': 'Trường',
                    'value': 'Đại học KHTN, ĐHQG-HCM'
                },
                {
                    'title': 'Khoa',
                    'value': 'Công nghệ thông tin'
                },
                {
                    'title': 'MSSV',
                    'value': '19120485'
                },
                {
                    'title': 'Chuyên ngành',
                    'value': 'Khoa học dữ liệu'
                },
                {
                    'title': 'Email',
                    'value': 'npqdung17@gmail.com'
                },
                {
                    'title': 'Định hướng',
                    'value': 'Data Engineer'
                },
                {
                    'title': 'Sở thích',
                    'value': 'Thể thao, Nấu ăn'
                }
            ]
        },
        {
            'name': 'Dương Thanh Hiệp',
            'role': 'Thành viên',
            'image': '../static/img/hacker.png',
            'information':[
                {
                    'title': 'Trường',
                    'value': 'Đại học KHTN, ĐHQG-HCM'
                },
                {
                    'title': 'Khoa',
                    'value': 'Công nghệ thông tin'
                },
                {
                    'title': 'MSSV',
                    'value': '19120505'
                },
                {
                    'title': 'Chuyên ngành',
                    'value': 'Khoa học máy tính'
                },
                {
                    'title': 'Email',
                    'value': 'thanhhiep0705@gmail.com'
                },
                {
                    'title': 'Định hướng',
                    'value': 'Web Developer'
                },
                {
                    'title': 'Sở thích',
                    'value': 'Du lịch, Thể thao'
                }
            ]
        },
        {
            'name': 'Nguyễn Thị Tiểu Mi',
            'role': 'Thành viên',
            'image': '../static/img/woman.png',
            'information':[
                {
                    'title': 'Trường',
                    'value': 'Đại học KHTN, ĐHQG-HCM'
                },
                {
                    'title': 'Khoa',
                    'value': 'Công nghệ thông tin'
                },
                {
                    'title': 'MSSV',
                    'value': '19120577'
                },
                {
                    'title': 'Chuyên ngành',
                    'value': 'Hệ thống thông tin'
                },
                {
                    'title': 'Email',
                    'value': 'tieumi2509@gmail.com'
                },
                {
                    'title': 'Định hướng',
                    'value': 'Web Developer'
                },
                {
                    'title': 'Sở thích',
                    'value': 'Đọc sách, Nấu ăn'
                }
            ]
        },
        {
            'name': 'Lê Thành Lộc',
            'role': 'Thành viên',
            'image': '../static/img/businessman.png',
            'information':[
                {
                    'title': 'Trường',
                    'value': 'Đại học KHTN, ĐHQG-HCM'
                },
                {
                    'title': 'Khoa',
                    'value': 'Công nghệ thông tin'
                },
                {
                    'title': 'MSSV',
                    'value': '19120562'
                },
                {
                    'title': 'Chuyên ngành',
                    'value': 'Khoa học dữ liệu'
                },
                {
                    'title': 'Email',
                    'value': 'lochcmus@gmail.com'
                },
                {
                    'title': 'Định hướng',
                    'value': 'Data Engineer'
                },
                {
                    'title': 'Sở thích',
                    'value': 'Hát, Du lịch'
                }
            ]
        },
        {
            'name': 'Nguyễn Thị Kim Ngân',
            'role': 'Thành viên',
            'image': '../static/img/girl.png',
            'information':[
                {
                    'title': 'Trường',
                    'value': 'Đại học KHTN, ĐHQG-HCM'
                },
                {
                    'title': 'Khoa',
                    'value': 'Công nghệ thông tin'
                },
                {
                    'title': 'MSSV',
                    'value': '19120598'
                },
                {
                    'title': 'Chuyên ngành',
                    'value': 'Hệ thống thông tin'
                },
                {
                    'title': 'Email',
                    'value': 'ntkn.mnkt@gmail.com'
                },
                {
                    'title': 'Định hướng',
                    'value': 'Web Developer'
                },
                {
                    'title': 'Sở thích',
                    'value': 'Đọc sách, Thể thao'
                }
            ]
        }
    ]
    return render_template('about.html', team_members=team_members)

@app.route('/course-finder', methods=['GET', 'POST'])
def courseFinder():
    session = cluster.connect()
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

@app.route('/job-finder', methods=['GET', 'POST'])
def jobFinder():
    session = cluster.connect()
    selected_options = request.form.getlist('selected_options')

    query = f'select title, industry, tool, programming_language, min_salary, max_salary, framework, link from {job_keyspace}.job_search;'
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
    session = cluster.connect()
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
            'name':'Total Enrollments by Subject',
            'chartId':'chart1',
            'dialogId': 'dialog-chart1',
            'graphData': graph1JSON,
            'graphDialogData': graph1_dialogJSON,
            'haveFilter': False,
            'filter': []
        },
        {
            'name':'Total Number of Courses by Subject',
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
            'name':'Average Course Duration by Subject and Level',
            'chartId':'chart4',
            'dialogId': 'dialog-chart4',
            'graphData': graph4JSON,
            'graphDialogData': graph4_dialogJSON,
            'haveFilter': False,
            'filter': []
        },
        {
            'name':'Top Technologies Being Taught',
            'chartId':'chart5',
            'dialogId': 'dialog-chart5',
            'graphData': graph5JSON,
            'graphDialogData': graph5_dialogJSON,
            'haveFilter': False,
            'filter': []
        },
        {
            'name':'Proportion of Programming Languages by Subject',
            'chartId':'chart6',
            'dialogId': 'dialog-chart6',
            'graphData': graph6JSON,
            'graphDialogData': graph6_dialogJSON,
            'haveFilter': True,
            'filter': listSubjects6
        },
        {
            'name':'Proportion Frameworks of Programming Languages by Subject',
            'chartId':'chart7',
            'dialogId': 'dialog-chart7',
            'graphData': graph7JSON,
            'graphDialogData': graph7_dialogJSON,
            'haveFilter': True,
            'filter': listSubjects7
        },
        {
            'name':'Proportion of Tools by Subject',
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
    session = cluster.connect()
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
            'name':'Number of Job Postings by Industry',
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
            'name':'Proportion of Programming Languages by Industry',
            'chartId':'chart3',
            'dialogId': 'dialog-chart3',
            'graphData': graph3JSON,
            'graphDialogData': graph3_dialogJSON,
            'haveFilter': True,
            'filter': listSubjects3
        },
        {
            'name':'Proportion of Frameworks by Industry',
            'chartId':'chart4',
            'dialogId': 'dialog-chart4',
            'graphData': graph4JSON,
            'graphDialogData': graph4_dialogJSON,
            'haveFilter': True,
            'filter': listSubjects4
        },
        {
            'name':'Proportion of Tools by Industry',
            'chartId':'chart5',
            'dialogId': 'dialog-chart5',
            'graphData': graph5JSON,
            'graphDialogData': graph5_dialogJSON,
            'haveFilter': True,
            'filter': listSubjects5
        },
        {
            'name':'Top In-Demand Technologies',
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
    fig.update_layout(showlegend=False,margin=dict(t=15, l=0))
    fig.update_traces(textposition='inside', textinfo='percent+label')
    
    fig_dialog = px.pie(df, names="Subject", values="Total Enroll", height=800, width= 1000)
    fig_dialog.update_traces(textposition='inside', textinfo='percent+value')
    return fig, fig_dialog

def course_graph2(session):
    query = f'select * from {course_keyspace}.subject_course;'
    result = session.execute(query)
    df = pd.DataFrame(list(result))
    df.columns = ['Subject', 'Total Courses']
    fig = px.pie(df, names="Subject", values="Total Courses",height= 420, width= 420)
    fig.update_layout(showlegend=False,margin=dict(t=15, l=0))
    fig.update_traces(textposition='inside', textinfo='percent+label')

    fig_dialog = px.pie(df, names="Subject", values="Total Courses", height=800, width= 1000)
    fig_dialog.update_traces(textposition='inside', textinfo='percent+label')
    return fig, fig_dialog

def course_graph3(session):
    query = f'select subject, level, time from {course_keyspace}.subject_level_time;'
    result = session.execute(query)
    df = pd.DataFrame(list(result))
    df.columns = ['Subject', 'Level', 'Time']
    fig = px.bar(df, x='Subject', y='Time', color='Level', barmode='stack', height=410, width=375)
    fig.update_layout( xaxis_title="Subject-Title", margin=dict(t=5, l=0))
    fig.update_traces(text=["{}-{}".format(x, color) for x, color in zip(df['Subject'], df['Level'])], textposition='inside')

    fig_dialog = px.bar(df, x='Subject', y='Time', color='Level', barmode='stack', height=650, width=1000)
    
    return fig, fig_dialog

def course_graph4(session):
    query = f'select subject, level, fee from {course_keyspace}.subject_level_fee;'
    result = session.execute(query)
    df = pd.DataFrame(list(result))
    df.columns = ['Subject', 'Level', 'Fee']
    fig = px.bar(df, x='Subject', y='Fee', color='Level', barmode='stack', height=410, width=375)
    fig.update_layout( xaxis={'visible': False, 'showticklabels': True}, margin=dict(t=5, l=0))
    fig_dialog = px.bar(df, x='Subject', y='Fee', color='Level', barmode='stack', height=650, width=1100)
    return fig, fig_dialog

def course_graph5(session):
    query = f'select * from {course_keyspace}.top_tech;'
    result = session.execute(query)
    df = pd.DataFrame(list(result))
    df.columns = ['Type', 'Name','Total Courses']
    df_limited = df.groupby('Type').apply(lambda x: x.nlargest(10, 'Total Courses')).reset_index(drop=True)
    fig = px.bar(df_limited, x='Type', y='Total Courses', color='Name', barmode='group', height=410, width=375)
    fig.update_layout( xaxis={'visible': False, 'showticklabels': True}, margin=dict(t=5, l=0))

    fig_dialog = px.bar(df_limited, x='Type', y='Total Courses', color='Name', barmode='group', height= 650, width =1100)
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
        fig.update_layout(showlegend=False, margin=dict(t=15, l=0))
        fig.update_traces(textposition='inside', textinfo='percent+label')
        list_fig.append(fig)

        fig_dialog = px.pie(df_language, names="Language", values="Courses", height=800, width= 1000)
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
        fig.update_layout(showlegend=False, margin=dict(t=15, l=0))
        fig.update_traces(textposition='inside', textinfo='percent+label')
        list_fig.append(fig)

        fig_dialog = px.pie(df_language, names="Framework", values="Courses", height=800, width= 1000)
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
        fig.update_layout(showlegend=False, margin=dict(t=15, l=0))
        fig.update_traces(textposition='inside', textinfo='percent+label')
        list_fig.append(fig)

        fig_dialog = px.pie(df_language, names="Tool", values="Courses", height=800, width= 1000)
        fig_dialog.update_traces(textposition='inside', textinfo='percent+label')
        list_fig_dialog.append(fig_dialog)

    return list_fig ,list_fig_dialog, list(enumerate(subjects_list))

def job_graph1(session):
    query = f'select industry,total_job from {job_keyspace}.industry_job;'
    result = session.execute(query)
    df = pd.DataFrame(list(result))
    df.columns = ['Industry', 'Total Postings']

    fig = px.pie(df, names="Industry", values="Total Postings",height= 420, width= 420)
    fig.update_layout(showlegend=False, margin=dict(t=15, l=0))
    fig.update_traces(textposition='inside', textinfo='percent+label')

    fig_dialog = px.pie(df, names="Industry", values="Total Postings", height=800, width= 1000)
    fig_dialog.update_traces(textposition='inside', textinfo='percent+label')
    return fig, fig_dialog

def job_graph2(session):
    query = f'select industry,min_salary, max_salary from {job_keyspace}.industry_salary;'
    result = session.execute(query)
    df = pd.DataFrame(list(result))
    df.columns = ['Industry', 'Min Salary', 'Max Salary']
    fig = px.bar(df, x='Industry', y=['Min Salary', 'Max Salary'], barmode='group', height=410, width=375)
    fig.update_layout(
        xaxis={'visible': False, 'showticklabels': True},
        showlegend=False, margin=dict(t=5, l=0)
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
        fig.update_layout(showlegend=False, margin=dict(t=15, l=0))
        fig.update_traces(textposition='inside', textinfo='percent+label')
        list_fig.append(fig)

        fig_dialog = px.pie(df_language, names="Programming Language", values="Total Postings", height=800, width= 1000)
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
        fig.update_layout(showlegend=False, margin=dict(t=15, l=0))
        fig.update_traces(textposition='inside', textinfo='percent+label')
        list_fig.append(fig)

        fig_dialog = px.pie(df_language, names="Framework", values="Total Postings", height=800, width= 1000)
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
        fig.update_layout(showlegend=False, margin=dict(t=15, l=0))
        fig.update_traces(textposition='inside', textinfo='percent+label')
        list_fig.append(fig)

        fig_dialog = px.pie(df_language, names="Tool", values="Total Postings", height=800, width= 1000)
        fig_dialog.update_traces(textposition='inside', textinfo='percent+label')
        list_fig_dialog.append(fig_dialog)

    return list_fig ,list_fig_dialog, list(enumerate(industries_list))

def job_graph6(session):
    query = f'select tech_type,tech_name,total_job from {job_keyspace}.top_tech;'
    result = session.execute(query)
    df = pd.DataFrame(list(result))
    df.columns = ['Tech Type', 'Tech Name','Total Postings']
    df_limited = df.groupby('Tech Type').apply(lambda x: x.nlargest(10, 'Total Postings')).reset_index(drop=True)
    fig = px.bar(df_limited, x='Tech Type', y='Total Postings', color='Tech Name', barmode='group', height=410, width=375)
    fig.update_layout( xaxis={'visible': False, 'showticklabels': True}, margin=dict(t=5, l=0))

    fig_dialog = px.bar(df_limited, x='Tech Type', y='Total Postings', color='Tech Name', barmode='group', height=650, width =1000)
    return fig, fig_dialog