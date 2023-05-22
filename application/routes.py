from application import app
from flask import render_template
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


@app.route('/test')
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
                    {'title': 'Dữ liệu 2'}]),
            dict(label='Dữ liệu 3',
                method='update',
                args=[{'visible': [False, False, True, False, False]},
                    {'title': 'Dữ liệu 3'}]),
            dict(label='Dữ liệu 4',
                method='update',
                args=[{'visible': [False, False, False, True, False]},
                    {'title': 'Dữ liệu 4'}]),
            dict(label='Dữ liệu 5',
                method='update',
                args=[{'visible': [False, False, False, False, True]},
                    {'title': 'Dữ liệu 5'}])
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
    return render_template('course.html', graphJSON = graphJSON)

@app.route('/course')
def course():
    app.config['ACTIVE_TAB'] = 'course'
    # Graph One
    df = px.data.medals_wide()
    fig1 = px.bar(df, x="nation", y=["gold", "silver", "bronze"], title="Wide-Form Input")
    graph1JSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)

    # Graph two
    df = px.data.iris()
    fig2 = px.scatter_3d(df, x='sepal_length', y='sepal_width', z='petal_width',
              color='species',  title="Iris Dataset")
    graph2JSON = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)

    # Graph three
    df = px.data.gapminder().query("continent=='Oceania'")
    fig3 = px.line(df, x="year", y="lifeExp", color='country',  title="Life Expectancy")
    graph3JSON = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)

    #Graph four
    data_canada = px.data.gapminder().query("country == 'Canada'")
    fig4 = px.bar(data_canada, x='year', y='pop')
    graph4JSON = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)


    return render_template('course.html', graph1JSON=graph1JSON,  graph2JSON=graph2JSON, graph3JSON=graph3JSON, graph4JSON=graph4JSON)

@app.route('/job-posting')
def recruitment():
    app.config['ACTIVE_TAB'] = 'job-postings'
    # Graph One
    df = px.data.medals_wide()
    fig1 = px.bar(df, x="nation", y=["gold", "silver", "bronze"], title="Wide-Form Input")
    graph1JSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)

    # Graph two
    df = px.data.iris()
    fig2 = px.scatter_3d(df, x='sepal_length', y='sepal_width', z='petal_width',
              color='species',  title="Iris Dataset")
    graph2JSON = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)

    # Graph three
    df = px.data.gapminder().query("continent=='Oceania'")
    fig3 = px.line(df, x="year", y="lifeExp", color='country',  title="Life Expectancy")
    graph3JSON = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)

    #Graph four
    data_canada = px.data.gapminder().query("country == 'Canada'")
    fig4 = px.bar(data_canada, x='year', y='pop')
    graph4JSON = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)


    return render_template('job-posting.html', graph1JSON=graph1JSON,  graph2JSON=graph2JSON, graph3JSON=graph3JSON, graph4JSON=graph4JSON)

@app.route('/data')
def data():
    return render_template('data.html')