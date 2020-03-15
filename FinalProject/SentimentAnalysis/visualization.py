import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import plotly.express as px

external_stylesheets1 = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# lower counts 182 205 224
# lower hover 109 256 194
# external_stylesheets=external_stylesheets
app = dash.Dash(__name__)
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
                    {'label': 'Democrats', 'value': 'TheDemocrats'},
                    {'label': 'Republicans', 'value': 'GOP'}
                ],
                value='pulvereyes',
                style=({"textAlign": "center", "width": "50%", "left": 20, 'font-family': 'Open Sans'})
            )
        ],
            style=({"width": "49%", 'display': 'inline-block', 'border-radios': '10px'})),
        html.Div([
            dcc.Checklist(
                id="emotionCheckList",
                options=[
                    {'label': 'anger', 'value': 'anger'},
                    {'label': 'disgust', 'value': 'disgust'},
                    {'label': 'joy', 'value': 'joy'},
                    {'label': 'surprise', 'value': 'surprise'},
                    {'label': 'anticipation', 'value': 'anticipation'},
                    {'label': 'fear', 'value': 'fear'},
                    {'label': 'sadness', 'value': 'sadness'},
                    {'label': 'trust', 'value': 'trust'}
                ],
                value=['anger', 'fear', 'anticipation', 'surprise', 'joy', 'sadness', 'trust', 'disgust'],
                labelStyle={'display': 'inline-block'}
            )
        ],
            id='radioitems',
            style={'width': '49%', 'float': 'right', 'display': 'inline-block', 'border-radios': '8px',
                   'font-family': 'Open Sans', 'font-size': '14'})
    ],
        style={
            'borderBottom': 'thin lightgrey solid',
            'backgroundColor': 'rgb(205, 205, 205)',
            'border-radius': '10px',
            'border-color': 'rgb(170, 170, 170)',
            'border-width': '3px',
            'padding': '10px 5px',
            'right': '30px'
        }
    ),
    html.Div([
        html.Div([
            # html.H1("overview", style={"textAlign": "center"}),
            dcc.Graph(id='overview_vis')
        ]),
        html.Div([
            # html.H1("expand view", style={"textAlign": "center"}),
            dcc.Graph(id='expandview_vis')
        ])
        # html.Div([
        # html.H1("Mood view", style={"textAlign": "center"}),
        # dcc.Graph(id='moodview_vis')
        # ])
    ]),
    # left: scatter plot of words within the same time frame
    # right: set of tweets within the same time frame
    html.Div([
        html.Div([
            html.H5("VAD", style={"textAlign": "center"}),
            dcc.Graph(id='vad_vis')
        ], style={'width': '40%', 'display': 'inline-block', 'padding': '0 20'}),
        html.Div([
            html.H5("tweets", style={"textAlign": "center"}),
            dcc.Graph(id='tweets_vis')
        ], style={'display': 'inline-block', 'width': '59%'})
    ])
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
    # print(dg)
    fig.add_trace(go.Scatter(
        x=df['DateTime'],
        y=dg['Original Tweet'],
        fill='tozeroy',
        mode='none',
        name='Tweet Counts'))
    fig.update_layout(
        height=200,
        width=1363,
        margin=dict(l=20, r=20, t=20, b=20),
        showlegend=True,
        yaxis_range=(0, 10)
    )
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label="1m",
                         step="month",
                         stepmode="backward"),
                    dict(count=2,
                         label="2m",
                         step="month",
                         stepmode="backward"),
                    dict(count=6,
                         label="6m",
                         step="month",
                         stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    return fig


@app.callback(
    dash.dependencies.Output('expandview_vis', 'figure'),
    [dash.dependencies.Input('userDropDown', 'value'),
     dash.dependencies.Input('emotionCheckList', 'value')]
)
def update_expandview(user, emotion):
    # on top of valance?
    file = 'new_output_' + user + '.csv'
    df = pd.read_csv(file)
    df.sort_values(by=['DateTime'])
    # print(emotion)
    # height by the number of tweets of the day
    df['DateTime'] = pd.to_datetime(df['DateTime'])
    df.index = df['DateTime']
    dg = df.resample('D').count()
    # fig = go.Figure()
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    if 'sadness' in emotion:
        fig.add_trace(go.Scatter(
            x=df['DateTime'],
            y=df['sadness'],
            hovertext='sadness',
            hoverinfo='text',
            mode='lines',
            name='sadness',
            line=dict(width=0.2, color='rgb(127, 156, 200)'),
            stackgroup='one'
        ), secondary_y=False)
    if 'surprise' in emotion:
        fig.add_trace(go.Scatter(
            x=df['DateTime'],
            y=df['surprise'],
            hovertext='surprise',
            hoverinfo='text',
            mode='lines',
            name='surprise',
            line=dict(width=0.2, color='rgb(106, 164, 190)'),
            stackgroup='one'
        ), secondary_y=False)
    if 'fear' in emotion:
        fig.add_trace(go.Scatter(
            x=df['DateTime'],
            y=df['fear'],
            hovertext='fear',
            hoverinfo='text',
            mode='lines',
            name='fear',
            line=dict(width=0.2, color='rgb(134, 185, 126)'),
            stackgroup='one'
        ), secondary_y=False)
    if 'trust' in emotion:
        fig.add_trace(go.Scatter(
            x=df['DateTime'],
            y=df['trust'],
            hovertext='trust',
            hoverinfo='text',
            mode='lines',
            name='trust',
            line=dict(width=0.2, color='rgb(168, 200, 70)'),
            stackgroup='one'
        ), secondary_y=False)
    if 'joy' in emotion:
        fig.add_trace(go.Scatter(
            x=df['DateTime'],
            y=df['joy'],
            hovertext='joy',
            hoverinfo='text',
            mode='lines',
            name='joy',
            line=dict(width=0.2, color='rgb(240, 218, 106)'),
            stackgroup='one'
        ), secondary_y=False)
    if 'anticipation' in emotion:
        fig.add_trace(go.Scatter(
            x=df['DateTime'],
            y=df['anticipation'],
            hovertext='anticipation',
            hoverinfo='text',
            mode='lines',
            name='anticipation',
            line=dict(width=0.2, color='rgb(213, 159, 97)'),
            stackgroup='one'
        ), secondary_y=False)
    if 'anger' in emotion:
        fig.add_trace(go.Scatter(
            x=df['DateTime'],
            y=df['anger'],
            hovertext='anger',
            hoverinfo='text',
            mode='lines',
            name='anger',
            line=dict(width=0.2, color='rgb(226, 53, 88)'),
            stackgroup='one'
        ), secondary_y=False)
    if 'disgust' in emotion:
        fig.add_trace(go.Scatter(
            x=df['DateTime'],
            y=df['disgust'],
            hovertext='disgust',
            hoverinfo='text',
            mode='lines',
            name='disgust',
            line=dict(width=0.2, color='rgb(165, 50, 189)'),
            stackgroup='one'
        ), secondary_y=False)
    # print(dg)
    fig.add_trace(go.Scatter(
        x=df['DateTime'],
        y=dg['Original Tweet'],
        fill='tozeroy',
        mode='lines',
        name='Tweet Counts',
        line=dict(width=0.2, color='rgb(182, 105, 224)')
    ), secondary_y=True)
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=0, t=20, b=20),
        showlegend=True,
        yaxis_range=(-0.25, 1.25)
    )
    # add rannge slider
    # reference: https://plot.ly/python/range-slider/
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label="1m",
                         step="month",
                         stepmode="backward"),
                    dict(count=2,
                         label="2m",
                         step="month",
                         stepmode="backward"),
                    dict(count=6,
                         label="6m",
                         step="month",
                         stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    return fig


if __name__ == '__main__':
    app.run_server(debug=True, port=8800)
