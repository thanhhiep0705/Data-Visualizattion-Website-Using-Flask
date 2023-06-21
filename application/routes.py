from application import app
from flask import render_template, request, g
import pandas as pd
import json
import plotly
import plotly.express as px
import plotly.graph_objects as go
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

app.config['ACTIVE_TAB'] = '/'
list_course_keyspace = ['course_data','course_coursera','course_udemy','course_edx' ]
list_jobposting_keyspace = ['jobposting_data','jobposting_linkedin', 'jobposting_nodeflair','jobposting_dice' ]

@app.before_request
def before_request():
    bundlepath = 'application/secure-connect-course-data.zip'
    clientId = 'URRrzRFMRvuBIZmLFumeqhvl'
    clientSecret = '++uM_E,5pH2kGnzZTqpYGU,E,GimsdCU5g_XtTckupaBmIkeMT9kaxAP82SgAr72t4w.I4zUsq.TU6.z4xihUYHgG4Y6AOiPjl-mRNk.6DxLYngZT025ZWF05+Hqo1l5'

    cloud_config= {
        'secure_connect_bundle': bundlepath
    }
    auth_provider = PlainTextAuthProvider(clientId, clientSecret)
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    session = cluster.connect()
    g.db_session = session 

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
                            'value': '740 M'
                        },
                        {
                            'title': 'Công ty',
                            'value': '50 M'
                        },
                        {
                            'title': 'Ngôn ngữ',
                            'value': '24'
                        }
                    ],
                    'website': 'https://www.linkedin.com/jobs'
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
                },
                {
                    'title': 'Dice',
                    'information':[
                        {
                            'title': 'Người dùng',
                            'value': '5.9 M'
                        },
                        {
                            'title': 'Người dùng/tháng',
                            'value': '1.7 M'
                        },
                        {
                            'title': 'Hồ sơ',
                            'value': '3 M'
                        }
                    ],
                    'website': 'https://www.dice.com/'
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
                            'value': '82+ M'
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
                            'value': '20+ M'
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
                            'value': '38+ M'
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
                    'value': 'Khoa học máy tính'
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
    keyspace = 'course_data'
    session= g.db_session
    selected_options = request.form.getlist('selected_options')

    query = f'select name, subject, enroll, programing_language, fee, framework, level, rating, link from {keyspace}.courses;'
    rs = session.execute(query)
    df = pd.DataFrame(list(rs))
    df['fee'] = df['fee'].round(2)
    df['rating'] = df['rating'].round(1)

    courses = pd.DataFrame([])
    
    if len(selected_options) != 0:
        courses = courseFilter(selected_options,df)

    top_course = getTopCourses(df)

    #get filter data
    filter_data = getCourseFilterData(df)

    return render_template('course-finder.html', courses = courses , top_course = top_course, selected_options = selected_options,filter_data = filter_data)

@app.route('/job-finder', methods=['GET', 'POST'])
def jobFinder():
    keyspace = 'job_data'
    session= g.db_session
    selected_options = request.form.getlist('selected_options')

    query = f'select title, industry, tool, programming_language, min_salary, max_salary, framework, link from {keyspace}.job_search;'
    rs = session.execute(query)
    df = pd.DataFrame(list(rs))

    jobs = pd.DataFrame([])
    
    if len(selected_options) != 0:
        jobs = jobFilter(selected_options,df)

    top_job = getTopJob(df)

    #get filter data
    filter_data = getJobFilterData(df)

    return render_template('job-finder.html', jobs = jobs , top_job = top_job, selected_options = selected_options,filter_data = filter_data)

@app.route('/course-visualization/<key>', methods=['GET', 'POST'])
def courseVisualization(key):
    session= g.db_session

    # selected_db = request.args.get('selected_db')
    # print('selected',selected_db)
    keyspace = key



    db_info = course_data_statistic(session, keyspace)

    fig1, fig1_dialog = course_graph1(session, keyspace)
    graph1JSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
    graph1_dialogJSON = json.dumps(fig1_dialog, cls=plotly.utils.PlotlyJSONEncoder)

    # Graph two
    fig2, fig2_dialog = course_graph2(session, keyspace)
    graph2JSON = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    graph2_dialogJSON = json.dumps(fig2_dialog, cls=plotly.utils.PlotlyJSONEncoder)

    # Graph three
    fig3, fig3_dialog = course_graph3(session, keyspace)
    graph3JSON = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
    graph3_dialogJSON = json.dumps(fig3_dialog, cls=plotly.utils.PlotlyJSONEncoder)

    fig4, fig4_dialog = course_graph4(session, keyspace)
    graph4JSON = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
    graph4_dialogJSON = json.dumps(fig4_dialog, cls=plotly.utils.PlotlyJSONEncoder)

    fig5, fig5_dialog = course_graph5(session, keyspace)
    graph5JSON = json.dumps(fig5, cls=plotly.utils.PlotlyJSONEncoder)
    graph5_dialogJSON = json.dumps(fig5_dialog, cls=plotly.utils.PlotlyJSONEncoder)

    fig6, fig6_dialog,listSubjects6  = course_graph6(session, keyspace)
    graph6JSON = json.dumps(fig6, cls=plotly.utils.PlotlyJSONEncoder)
    graph6_dialogJSON = json.dumps(fig6_dialog, cls=plotly.utils.PlotlyJSONEncoder)

    fig7, fig7_dialog,listSubjects7  = course_graph7(session, keyspace)
    graph7JSON = json.dumps(fig7, cls=plotly.utils.PlotlyJSONEncoder)
    graph7_dialogJSON = json.dumps(fig7_dialog, cls=plotly.utils.PlotlyJSONEncoder)


    fig8, fig8_dialog,listSubjects8  = course_graph8(session, keyspace)
    graph8JSON = json.dumps(fig8, cls=plotly.utils.PlotlyJSONEncoder)
    graph8_dialogJSON = json.dumps(fig8_dialog, cls=plotly.utils.PlotlyJSONEncoder)


    graphsData = [
        {
            'name':'Biểu đồ thống kê số lượng học viên theo lĩnh vực',
            'chartId':'chart1',
            'dialogId': 'dialog-chart1',
            'graphData': graph1JSON,
            'graphDialogData': graph1_dialogJSON,
            'haveFilter': False,
            'filter': []
        },
        {
            'name':'Biểu đồ thống kê số lượng khóa học theo lĩnh vực',
            'chartId':'chart2',
            'dialogId': 'dialog-chart2',
            'graphData': graph2JSON,
            'graphDialogData': graph2_dialogJSON,
            'haveFilter': False,
            'filter': []
        },
        {
            'name':'Biểu đồ thời gian học trung bình theo lĩnh vực và cấp độ',
            'chartId':'chart3',
            'dialogId': 'dialog-chart3',
            'graphData': graph3JSON,
            'graphDialogData': graph3_dialogJSON,
            'haveFilter': False,
            'filter': []
        },
        {
            'name':'Biểu đồ học phí trung bình theo lĩnh vực và cấp độ',
            'chartId':'chart4',
            'dialogId': 'dialog-chart4',
            'graphData': graph4JSON,
            'graphDialogData': graph4_dialogJSON,
            'haveFilter': False,
            'filter': []
        },
        {
            'name':'Biểu đồ thống kê mức độ phổ biến các công nghệ hiện nay',
            'chartId':'chart5',
            'dialogId': 'dialog-chart5',
            'graphData': graph5JSON,
            'graphDialogData': graph5_dialogJSON,
            'haveFilter': False,
            'filter': []
        },
        {
            'name':'Biểu đồ tương quan tỷ lệ ngôn ngữ lập trình theo lĩnh vực',
            'chartId':'chart6',
            'dialogId': 'dialog-chart6',
            'graphData': graph6JSON,
            'graphDialogData': graph6_dialogJSON,
            'haveFilter': True,
            'filter': listSubjects6
        },
        {
            'name':'Biểu đồ tương quan tỷ lệ khung chương trình theo lĩnh vực',
            'chartId':'chart7',
            'dialogId': 'dialog-chart7',
            'graphData': graph7JSON,
            'graphDialogData': graph7_dialogJSON,
            'haveFilter': True,
            'filter': listSubjects7
        },
        {
            'name':'Biểu đồ tương quan tỷ lệ công cụ trình theo lĩnh vực',
            'chartId':'chart8',
            'dialogId': 'dialog-chart8',
            'graphData': graph8JSON,
            'graphDialogData': graph8_dialogJSON,
            'haveFilter': True,
            'filter': listSubjects8
        },
    ]
    return render_template('course-visualization.html', graphsData=graphsData, db_info=db_info, selected_db=keyspace)

@app.route('/job-visualization/<key>' , methods=['GET', 'POST'])
def jobVisualization(key):
    session= g.db_session
    keyspace = key

    db_info = job_data_statistic(session, keyspace)

    fig1, fig1_dialog = job_graph1(session, keyspace)
    graph1JSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
    graph1_dialogJSON = json.dumps(fig1_dialog, cls=plotly.utils.PlotlyJSONEncoder)

    # Graph two
    fig2, fig2_dialog = job_graph2(session, keyspace)
    graph2JSON = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    graph2_dialogJSON = json.dumps(fig2_dialog, cls=plotly.utils.PlotlyJSONEncoder)

    # Graph three
    fig3, fig3_dialog,listSubjects3  = job_graph3(session, keyspace)
    graph3JSON = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
    graph3_dialogJSON = json.dumps(fig3_dialog, cls=plotly.utils.PlotlyJSONEncoder)

    fig4, fig4_dialog,listSubjects4  = job_graph4(session, keyspace)
    graph4JSON = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
    graph4_dialogJSON = json.dumps(fig4_dialog, cls=plotly.utils.PlotlyJSONEncoder)

    fig5, fig5_dialog,listSubjects5  = job_graph5(session, keyspace)
    graph5JSON = json.dumps(fig5, cls=plotly.utils.PlotlyJSONEncoder)
    graph5_dialogJSON = json.dumps(fig5_dialog, cls=plotly.utils.PlotlyJSONEncoder)


    fig6, fig6_dialog = job_graph6(session, keyspace)
    graph6JSON = json.dumps(fig6, cls=plotly.utils.PlotlyJSONEncoder)
    graph6_dialogJSON = json.dumps(fig6_dialog, cls=plotly.utils.PlotlyJSONEncoder)


    graphsData = [
        {
            'name':'Biểu đồ thống kê mức độ phổ biến của các lĩnh vực',
            'chartId':'chart1',
            'dialogId': 'dialog-chart1',
            'graphData': graph1JSON,
            'graphDialogData': graph1_dialogJSON,
            'haveFilter': False,
            'filter': []
        },
        {
            'name':'Biểu đồ phân bố mức lương theo lĩnh vực',
            'chartId':'chart2',
            'dialogId': 'dialog-chart2',
            'graphData': graph2JSON,
            'graphDialogData': graph2_dialogJSON,
            'haveFilter': False,
            'filter': []
        },

        {
            'name':'Biểu đồ tương quan tỷ lệ ngôn ngữ lập trình theo lĩnh vực',
            'chartId':'chart3',
            'dialogId': 'dialog-chart3',
            'graphData': graph3JSON,
            'graphDialogData': graph3_dialogJSON,
            'haveFilter': True,
            'filter': listSubjects3
        },
        {
            'name':'Biểu đồ tương quan tỷ lệ khung chương trình theo lĩnh vực',
            'chartId':'chart4',
            'dialogId': 'dialog-chart4',
            'graphData': graph4JSON,
            'graphDialogData': graph4_dialogJSON,
            'haveFilter': True,
            'filter': listSubjects4
        },
        {
            'name':'Biểu đồ tương quan tỷ lệ công cụ trình theo lĩnh vực',
            'chartId':'chart5',
            'dialogId': 'dialog-chart5',
            'graphData': graph5JSON,
            'graphDialogData': graph5_dialogJSON,
            'haveFilter': True,
            'filter': listSubjects5
        },
        {
            'name':'Biểu đồ thống kê mức độ phổ biến các công nghệ hiện nay',
            'chartId':'chart6',
            'dialogId': 'dialog-chart6',
            'graphData': graph6JSON,
            'graphDialogData': graph6_dialogJSON,
            'haveFilter': False,
            'filter': []
        },
    ]

    return render_template('job-visualization.html', graphsData=graphsData, db_info=db_info)


def getTopCourses(df):
    df_top = df.sort_values(by = 'enroll', ascending=False).head(10)
    return df_top

def courseFilter(options, df):
    subjects = []
    frameworks = []
    programing_languages = []
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
            programing_languages.append(value)
        if key.find('Level') != - 1:
            value = key.split(':')[1].strip().lower()
            levels.append(value)

    conditions = []
    if subjects:
        conditions.append(df['subject'].isin(subjects))
    if levels:
        conditions.append(df['level'].isin(levels))
    if programing_languages:
        programing_language_condition = df['programing_language'].apply(lambda x: any(language in x.split(', ') for language in programing_languages))
        conditions.append(programing_language_condition)
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

    return filtered_df.sort_values(by='enroll', ascending=False)

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
    languages = getNormalizedArray(df.programing_language.unique())

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


def course_data_statistic(session, keyspace):
    query = f'select subject, programing_language, tool, framework, link from {keyspace}.courses;'
    rs = session.execute(query)
    df = pd.DataFrame(list(rs))
    total_course = len(df)
    total_subject = df['subject'].nunique()
    total_framework = df['framework'].str.split(',').explode().nunique()
    total_tool_count = df['tool'].str.split(',').explode().nunique()
    total_language_count = df['programing_language'].str.split(',').explode().nunique()
    return [total_course,total_subject, total_language_count, total_tool_count, total_framework]

def job_data_statistic(session, keyspace):
    query = f'select industry, programing_language, tool, framework, link from {keyspace}.jobs;'
    rs = session.execute(query)
    df = pd.DataFrame(list(rs))
    total_course = len(df)
    total_industry = df['industry'].nunique()
    total_framework = df['framework'].str.split(',').explode().nunique()
    total_tool_count = df['tool'].str.split(',').explode().nunique()
    total_language_count = df['programing_language'].str.split(',').explode().nunique()
    return [total_course,total_industry, total_language_count, total_tool_count, total_framework]

def course_graph1(session, keyspace):
    query = f'select subject, total_enroll from {keyspace}.subject_course_enroll;'
    result = session.execute(query)
    df = pd.DataFrame(list(result))
    df.columns = ['Subject', 'Total Enrolls']
    fig = px.pie(df.head(10), names="Subject", values="Total Enrolls", height= 420, width= 420, color_discrete_sequence=px.colors.qualitative.Pastel1)
    fig.update_layout(showlegend=False,margin=dict(t=15, l=0))
    fig.update_traces(textposition='inside', textinfo='label + value')
    
    fig_dialog = px.pie(df, names="Subject", values="Total Enrolls", height=750, width= 1000, color_discrete_sequence=px.colors.qualitative.Pastel1)
    fig_dialog.update_traces(textposition='inside', textinfo='label+percent+value')
    return fig, fig_dialog

def course_graph2(session, keyspace):
    query = f'select subject, total_course from {keyspace}.subject_course_enroll;'
    result = session.execute(query)
    df = pd.DataFrame(list(result))
    df.columns = ['Subject', 'Total Courses']
    fig = px.pie(df.head(10), names="Subject", values="Total Courses",height= 420, width= 420, color_discrete_sequence=px.colors.qualitative.Pastel1)
    fig.update_layout(showlegend=False,margin=dict(t=15, l=0))
    fig.update_traces(textposition='inside', textinfo='label + value')

    fig_dialog = px.pie(df, names="Subject", values="Total Courses", height=750, width= 1000,color_discrete_sequence=px.colors.qualitative.Pastel1)
    fig_dialog.update_traces(textposition='inside', textinfo='label+percent+value')
    return fig, fig_dialog

def course_graph3(session, keyspace):
    query = f'select subject, level, time from {keyspace}.subject_level_time_fee;'
    result = session.execute(query)
    df = pd.DataFrame(list(result))
    df.columns = ['Subject', 'Level', 'Average Time']
    fig = px.bar(df.head(10), x='Subject', y='Average Time', color='Level', barmode='stack', height=410, width=375, color_discrete_sequence=px.colors.qualitative.Pastel1)
    fig.update_layout(margin=dict(t=5, l=0))
    fig.update_traces(texttemplate='%{y}', textposition='inside')

    fig_dialog = px.bar(df, x='Subject', y='Average Time', color='Level', barmode='stack', height=650, width=1000,color_discrete_sequence=px.colors.qualitative.Pastel1)
    fig_dialog.update_traces(texttemplate='%{y}', textposition='inside')
    
    return fig, fig_dialog

def course_graph4(session, keyspace):
    query = f'select subject, level, fee from {keyspace}.subject_level_time_fee;'
    result = session.execute(query)
    df = pd.DataFrame(list(result))
    df.columns = ['Subject', 'Level', 'Average Fee']
    fig = px.bar(df.head(10), x='Subject', y='Average Fee', color='Level', barmode='stack', height=410, width=375, color_discrete_sequence=px.colors.qualitative.Pastel1)
    fig.update_layout( margin=dict(t=5, l=0))
    fig.update_traces(texttemplate='%{y}', textposition='auto')
    fig_dialog = px.bar(df, x='Subject', y='Average Fee', color='Level', barmode='stack', height=650, width=1100,color_discrete_sequence=px.colors.qualitative.Pastel1)
    fig_dialog.update_traces(texttemplate='%{y}', textposition='inside')
    return fig, fig_dialog

def course_graph5(session, keyspace):
    query = f'select * from {keyspace}.top_tech;'
    result = session.execute(query)
    df = pd.DataFrame(list(result))
    df.columns = ['Technology Type', 'Technology Name','Total Courses']
    df_limited = df.groupby('Technology Type').apply(lambda x: x.nlargest(10, 'Total Courses')).reset_index(drop=True)
    fig = px.bar(df_limited.head(10), x='Technology Type', y='Total Courses', color='Technology Name', barmode='group', height=410, width=375, color_discrete_sequence=px.colors.qualitative.Pastel1)
    fig.update_layout(margin=dict(t=5, l=0))
    fig.update_traces(texttemplate='%{y}', textposition='auto')

    fig_dialog = px.bar(df_limited, x='Technology Type', y='Total Courses', color='Technology Name', barmode='group', height= 650, width =1100, color_discrete_sequence=px.colors.qualitative.Pastel1)
    fig_dialog.update_layout(xaxis_title='Technology Type', yaxis_title='Total Courses')
    fig_dialog.update_traces(texttemplate='%{y}', textposition='inside')
    return fig, fig_dialog

def course_graph6(session, keyspace):
    query = f'select subject,programming_language,total_course from {keyspace}.subject_language_course;'
    result = session.execute(query)
    df = pd.DataFrame(list(result))
    df.columns = ['Subject', 'Language', 'Total Courses']
    subjects_list = df['Subject'].unique().tolist()
    list_fig = []
    list_fig_dialog = []
    for subject in df['Subject'].unique().tolist():
        df_language = df[df['Subject'] == subject]
        fig = px.pie(df_language.head(10), names="Language", values="Total Courses", height= 420, width= 420,color_discrete_sequence=px.colors.qualitative.Pastel1)
        fig.update_layout(showlegend=False, margin=dict(t=15, l=0))
        fig.update_traces(textposition='inside', textinfo='label + value')
        list_fig.append(fig)

        fig_dialog = px.pie(df_language, names="Language", values="Total Courses", height=750, width= 1000,color_discrete_sequence=px.colors.qualitative.Pastel1)
        fig_dialog.update_traces(textposition='inside', textinfo='label+percent+value')
        list_fig_dialog.append(fig_dialog)


    return list_fig ,list_fig_dialog, list(enumerate(subjects_list))

def course_graph7(session, keyspace):
    query = f'select subject,framework,total_course from {keyspace}.subject_framework_course;'
    result = session.execute(query)
    df = pd.DataFrame(list(result))
    df.columns = ['Subject', 'Framework', 'Total Courses']
    subjects_list = df['Subject'].unique().tolist()
    list_fig = []
    list_fig_dialog = []
    for subject in df['Subject'].unique().tolist():
        df_language = df[df['Subject'] == subject]
        fig = px.pie(df_language.head(10), names="Framework", values="Total Courses", height= 420, width= 420,color_discrete_sequence=px.colors.qualitative.Pastel1)
        fig.update_layout(showlegend=False, margin=dict(t=15, l=0))
        fig.update_traces(textposition='inside', textinfo='label + value')
        list_fig.append(fig)

        fig_dialog = px.pie(df_language, names="Framework", values="Total Courses", height=750, width= 1000,color_discrete_sequence=px.colors.qualitative.Pastel1)
        fig_dialog.update_traces(textposition='inside', textinfo='label+percent+value')
        list_fig_dialog.append(fig_dialog)

    return list_fig ,list_fig_dialog, list(enumerate(subjects_list))

def course_graph8(session, keyspace):
    query = f'select subject,tool,total_course from {keyspace}.subject_tool_course;'
    result = session.execute(query)
    df = pd.DataFrame(list(result))
    df.columns = ['Subject', 'Tool', 'Total Courses']
    subjects_list = df['Subject'].unique().tolist()
    list_fig = []
    list_fig_dialog = []
    for subject in df['Subject'].unique().tolist():
        df_language = df[df['Subject'] == subject]
        fig = px.pie(df_language.head(10), names="Tool", values="Total Courses", height= 420, width= 420,color_discrete_sequence=px.colors.qualitative.Pastel2)
        fig.update_layout(showlegend=False, margin=dict(t=15, l=0))
        fig.update_traces(textposition='inside', textinfo='label + value')
        list_fig.append(fig)

        fig_dialog = px.pie(df_language, names="Tool", values="Total Courses", height=750, width= 1000,color_discrete_sequence=px.colors.qualitative.Pastel2)
        fig_dialog.update_traces(textposition='inside', textinfo='label+percent+value')
        list_fig_dialog.append(fig_dialog)

    return list_fig ,list_fig_dialog, list(enumerate(subjects_list))

def job_graph1(session, keyspace):
    query = f'select industry,total_job from {keyspace}.industry_job;'
    result = session.execute(query)
    df = pd.DataFrame(list(result))
    df.columns = ['Industry', 'Total Postings']

    fig = px.pie(df.head(10), names="Industry", values="Total Postings",height= 420, width= 420,color_discrete_sequence=px.colors.qualitative.Pastel2)
    fig.update_layout(showlegend=False, margin=dict(t=15, l=0))
    fig.update_traces(textposition='inside', textinfo='label + value')

    fig_dialog = px.pie(df, names="Industry", values="Total Postings", height=750, width= 1000,color_discrete_sequence=px.colors.qualitative.Pastel2)
    fig_dialog.update_traces(textposition='inside', textinfo='label+percent+value')
    return fig, fig_dialog

def job_graph2(session, keyspace):
    query = f'select industry,min_salary, max_salary from {keyspace}.industry_salary;'
    result = session.execute(query)
    df = pd.DataFrame(list(result))
    df.columns = ['Industry', 'Min Salary', 'Max Salary']
    fig = px.bar(df.head(10), x='Industry', y=['Min Salary', 'Max Salary'], barmode='group', height=410, width=375,color_discrete_sequence=px.colors.qualitative.Pastel2)
    fig.update_layout(margin=dict(t=5, l=0), yaxis_title='Salary')
    fig.update_traces(texttemplate='%{y}', textposition='inside')

    fig_dialog = px.bar(df, x='Industry', y=['Min Salary', 'Max Salary'], barmode='group', height=650, width =1000,color_discrete_sequence=px.colors.qualitative.Pastel2)
    fig_dialog.update_layout(
        xaxis_title='Industry',
        yaxis_title='Salary'
    )
    fig_dialog.update_traces(texttemplate='%{y}', textposition='inside')
    return fig, fig_dialog

def job_graph3(session, keyspace):
    query = f'select industry,programming_language,total_job from {keyspace}.industry_language_job;'
    result = session.execute(query)
    df = pd.DataFrame(list(result))
    df.columns = ['Industry', 'Programming Language', 'Total Postings']
    industries_list = df['Industry'].unique().tolist()
    list_fig = []
    list_fig_dialog = []
    for industry in industries_list:
        df_language = df[df['Industry'] == industry]
        fig = px.pie(df_language.head(10), names="Programming Language", values="Total Postings", height= 420, width= 420,color_discrete_sequence=px.colors.qualitative.Pastel2)
        fig.update_layout(showlegend=False, margin=dict(t=15, l=0))
        fig.update_traces(textposition='inside', textinfo='label + value')
        list_fig.append(fig)

        fig_dialog = px.pie(df_language, names="Programming Language", values="Total Postings", height=750, width= 1000,color_discrete_sequence=px.colors.qualitative.Pastel2)
        fig_dialog.update_traces(textposition='inside', textinfo='label+percent+value')
        list_fig_dialog.append(fig_dialog)

    return list_fig ,list_fig_dialog, list(enumerate(industries_list))

def job_graph4(session, keyspace):
    query = f'select industry,framework,total_job from {keyspace}.industry_framework_job;'
    result = session.execute(query)
    df = pd.DataFrame(list(result))
    df.columns = ['Industry', 'Framework', 'Total Postings']
    industries_list = df['Industry'].unique().tolist()
    list_fig = []
    list_fig_dialog = []
    for industry in industries_list:
        df_language = df[df['Industry'] == industry]
        fig = px.pie(df_language.head(10), names="Framework", values="Total Postings", height= 420, width= 420,color_discrete_sequence=px.colors.qualitative.Pastel2)
        fig.update_layout(showlegend=False, margin=dict(t=15, l=0))
        fig.update_traces(textposition='inside', textinfo='label + value')
        list_fig.append(fig)

        fig_dialog = px.pie(df_language, names="Framework", values="Total Postings", height=750, width= 1000,color_discrete_sequence=px.colors.qualitative.Pastel2)
        fig_dialog.update_traces(textposition='inside', textinfo='label+percent+value')
        list_fig_dialog.append(fig_dialog)

    return list_fig ,list_fig_dialog, list(enumerate(industries_list))

def job_graph5(session, keyspace):
    query = f'select industry,tool,total_job from {keyspace}.industry_tool_job;'
    result = session.execute(query)
    df = pd.DataFrame(list(result))
    df.columns = ['Industry', 'Tool', 'Total Postings']
    industries_list = df['Industry'].unique().tolist()
    list_fig = []
    list_fig_dialog = []
    for industry in industries_list:
        df_language = df[df['Industry'] == industry]
        fig = px.pie(df_language.head(10), names="Tool", values="Total Postings", height= 420, width= 420,color_discrete_sequence=px.colors.qualitative.Pastel2)
        fig.update_layout(showlegend=False, margin=dict(t=15, l=0))
        fig.update_traces(textposition='inside', textinfo='label + value')
        list_fig.append(fig)

        fig_dialog = px.pie(df_language, names="Tool", values="Total Postings", height=750, width= 1000,color_discrete_sequence=px.colors.qualitative.Pastel2)
        fig_dialog.update_traces(textposition='inside', textinfo='label+percent+value')
        list_fig_dialog.append(fig_dialog)

    return list_fig ,list_fig_dialog, list(enumerate(industries_list))

def job_graph6(session, keyspace):
    query = f'select tech_type,tech_name,total_job from {keyspace}.top_tech;'
    result = session.execute(query)
    df = pd.DataFrame(list(result))
    df.columns = ['Technology Type', 'Technology Name','Total Postings']
    df_limited = df.groupby('Technology Type').apply(lambda x: x.nlargest(10, 'Total Postings')).reset_index(drop=True)
    fig = px.bar(df_limited, x='Technology Type', y='Total Postings', color='Technology Name', barmode='group', height=410, width=375,color_discrete_sequence=px.colors.qualitative.Pastel2)
    fig.update_layout( margin=dict(t=5, l=0))
    fig.update_traces(texttemplate='%{y}', textposition='inside')

    fig_dialog = px.bar(df_limited, x='Technology Type', y='Total Postings', color='Technology Name', barmode='group', height=650, width =1000,color_discrete_sequence=px.colors.qualitative.Pastel2)
    fig_dialog.update_traces(texttemplate='%{y}', textposition='inside')
    fig_dialog.update_layout( xaxis_title='Technology Type', yaxis_title='Total Postings')
    return fig, fig_dialog