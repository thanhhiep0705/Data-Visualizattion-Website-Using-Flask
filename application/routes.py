import os
from application import app
from flask import render_template, url_for
import pandas as pd
import json
import plotly
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

app.config['ACTIVE_TAB'] = '/'

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

@app.route('/course-finder')
def courseSearch():
    # csv_url = url_for('static', filename='Course.csv')
    # df = pd.read_csv(csv_url)
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the file path for the CSV file
    csv_path = os.path.join(current_dir, 'static', 'Course.csv')

    # Load the CSV file into a DataFrame
    df = pd.read_csv(csv_path, encoding='latin1')
    course = df.head(5)
    top_course = df.head(5)

    return render_template('course-finder.html', course = course , top_course = top_course)

@app.route('/job-finder')
def jobSearch():
    # csv_url = url_for('static', filename='Course.csv')
    # df = pd.read_csv(csv_url)
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

    graphsList = [
        {
            'name':'Chart 1',
            'chartId':'chart1',
            'dialogId': 'dialog-chart1'
        },
        {
            'name':'Chart 2',
            'chartId':'chart2',
            'dialogId': 'dialog-chart2'
        },
        {
            'name':'Chart 3',
            'chartId':'chart3',
            'dialogId': 'dialog-chart3'
        },
        {
            'name':'Chart 4',
            'chartId':'chart4',
            'dialogId': 'dialog-chart4'
        },
    ]

    return render_template('course-visualization.html', graph1JSON=graph1JSON,  graph2JSON=graph2JSON, graph3JSON=graph3JSON, graph4JSON=graph4JSON, graphsList = graphsList)

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

    graphsList = [
        {
            'name':'Chart 1',
            'chartId':'chart1',
            'dialogId': 'dialog-chart1'
        },
        {
            'name':'Chart 2',
            'chartId':'chart2',
            'dialogId': 'dialog-chart2'
        },
        {
            'name':'Chart 3',
            'chartId':'chart3',
            'dialogId': 'dialog-chart3'
        },
        {
            'name':'Chart 4',
            'chartId':'chart4',
            'dialogId': 'dialog-chart4'
        },
    ]

    return render_template('job-visualization.html', graph1JSON=graph1JSON,  graph2JSON=graph2JSON, graph3JSON=graph3JSON, graph4JSON=graph4JSON, graphsList = graphsList)
