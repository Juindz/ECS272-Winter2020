import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import plotly.express as px

external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]
# upper overview 91 143 186

# value=dict(rgb=dict(r=255, g=0, b=0, a=0))
# anger 234 118 142
# surprise 124 190 209
# anticipation 242 268 103
# trust 184 216 121
# fear 140 215 159
# joy 250 224 119
# surprise 126 190 207
# disgust 171 142 192

# lower counts 182 205 224
# lower hover 109 256 194
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([
    html.H1("PEARL by Zijun Deng and Nuoshi Li", style={"textAlign": "center"}),
    html.Div([
        html.Div([
            # bar with selections, id and set of emotions
            dcc.Dropdown(
                id="userDropDown",
                options=[
                    {'label': '14874721', 'value': 'pulvereyes'},
                    {'label': '14396017', 'value': 'wkulhanek'},
                    {'label': 'Compare tweets from two parties', 'value': 'politics'}
                ],
                value='pulvereyes',
                style=({"textAlign": "center", "width": "50%", "left": 20})
            )
        ]),
        html.Div([
            dcc.Checklist(
                id="emotionCheckList",
                options=[
                    {'label': 'Anger', 'value': 'anger'},
                    {'label': 'Disgust', 'value': 'disgust'},
                    {'label': 'Joy', 'value': 'joy'},
                    {'label': 'Surprise', 'value': 'surprise'},
                    {'label': 'Anticipation', 'value': 'anticipation'},
                    {'label': 'Fear', 'value': 'fear'},
                    {'label': 'Sadness', 'value': 'sadness'},
                    {'label': 'Trust', 'value': 'trust'}
                ],
                value=['anger', 'fear', 'anticipation', 'surprise', 'joy', 'sadness', 'trust', 'disgust'],
                labelStyle={'display': 'inline-block', "right": 50, "font": 50}
            )
        ])
    ]),
    html.Div([
        html.Div([
            #html.H1("overview", style={"textAlign": "center"}),
            dcc.Graph(id='overview_vis',
                      style={'height': 300})
        ]),
        html.Div([
            #html.H1("expand view", style={"textAlign": "center"}),
            dcc.Graph(id='expandview_vis', style={'height': 400}),
        ]),
        html.Div([
            #html.H1("Mood view", style={"textAlign": "center"}),
            dcc.Graph(id='moodview_vis', style={'height': 400}),
        ])
    ]),
    # left: scatter plot of words within the same time frame
    # right: set of tweets within the same time frame
    html.Div([
        html.Div([
            html.H1("VAD", style={"textAlign": "center"}),
            dcc.Graph(id='vad_vis')
        ], className="six columns"),
        html.Div([
            html.H1("tweets", style={"textAlign": "center"}),
            dcc.Graph(id='tweets_vis')
        ], className="six columns")
    ], className="row")
])


@app.callback(
    dash.dependencies.Output('overview_vis', 'figure'),
    [dash.dependencies.Input('userDropDown', 'value')]
)
def update_overview(user):
    file = 'new_output_' + user + '.csv'
    # area = the amount of tweets
    df = pd.read_csv(file)
    df.sort_values(by=['DateTime'])
    # height by the number of tweets of the day
    fig = go.Figure()
    df['DateTime'] = pd.to_datetime(df['DateTime'])
    df.index = df['DateTime']
    dg = df.resample('D').count()
    #print(dg)
    fig.add_trace(go.Scatter(x=df['DateTime'], y=dg['Original Tweet'], fill='tozeroy', mode='none'))
    fig.update_layout(
        showlegend=True,
        yaxis_range=(0, 10)
    )
    return fig


@app.callback(
    dash.dependencies.Output('expandview_vis', 'figure'),
    [dash.dependencies.Input('userDropDown', 'value')]
)
def update_expandview(user):
    # on top of valance?
    file = 'new_output_' + user + '.csv'
    df = pd.read_csv(file)
    df.sort_values(by=['DateTime'])
    emotions = []
    # color based on colum name
    # x = datetime
    # y = 8 emotion columns
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['DateTime'],
        y=df['sadness'],
        hovertext='sadness',
        hoverinfo='text',
        mode='lines',
        name='sadness',
        line=dict(width=0.5, color='rgb(234, 118, 142)'),
        stackgroup='one'
    ))
    fig.add_trace(go.Scatter(
        x=df['DateTime'],
        y=df['surprise'],
        hovertext='surprise',
        hoverinfo='text',
        mode='lines',
        name='surprise',
        line=dict(width=0.5, color='rgb(140, 215, 159)'),
        stackgroup='one'
    ))
    fig.add_trace(go.Scatter(
        x=df['DateTime'],
        y=df['fear'],
        hovertext='fear',
        hoverinfo='text',
        mode='lines',
        name='fear',
        line=dict(width=0.5, color='rgb(242, 268, 103)'),
        stackgroup='one'
    ))
    fig.add_trace(go.Scatter(
        x=df['DateTime'],
        y=df['trust'],
        hovertext='trust',
        hoverinfo='text',
        mode='lines',
        name='trust',
        line=dict(width=0.5, color='rgb(124, 190, 209)'),
        stackgroup='one'
    ))
    fig.add_trace(go.Scatter(
        x=df['DateTime'],
        y=df['joy'],
        hovertext='joy',
        hoverinfo='text',
        mode='lines',
        name='joy',
        line=dict(width=0.5, color='rgb(250, 224, 119)'),
        stackgroup='one'
    ))
    fig.add_trace(go.Scatter(
        x=df['DateTime'],
        y=df['anticipation'],
        hovertext='anticipation',
        hoverinfo='text',
        mode='lines',
        name='anticipation',
        line=dict(width=0.5, color='rgb(184, 247, 212)'),
        stackgroup='one'
    ))
    fig.add_trace(go.Scatter(
        x=df['DateTime'],
        y=df['anger'],
        hovertext='anger',
        hoverinfo='text',
        mode='lines',
        name='anger',
        line=dict(width=0.5, color='rgb(184, 216, 121)'),
        stackgroup='one'
    ))
    fig.add_trace(go.Scatter(
        x=df['DateTime'],
        y=df['disgust'],
        hovertext='disgust',
        hoverinfo='text',
        mode='lines',
        name='disgust',
        line=dict(width=0.5, color='rgb(171, 142, 192)'),
        stackgroup='one'
    ))
    fig.update_layout(
        showlegend=True,
        yaxis_range=(-0.5, 1.5))
    return fig



@app.callback(
    dash.dependencies.Output('moodview_vis', 'figure'),
    [dash.dependencies.Input('userDropDown', 'value')]
)
def update_moodview(user):
    # area = the amount of tweets
    file = 'new_output_' + user + '.csv'
    df = pd.read_csv(file)
    df.sort_values(by=['DateTime'])
    # height by the number of tweets of the day
    fig = go.Figure()
    df['DateTime'] = pd.to_datetime(df['DateTime'])
    df.index = df['DateTime']
    fig.add_trace(go.Scatter(x=df['DateTime'], y=df['keyword_counts'], fill='tozeroy', mode='none'))
    fig.update_layout(
        showlegend=True,
        yaxis_range=(0, 10)
    )
    return fig


if __name__ == '__main__':
    app.run_server(debug=True, port=8800)
