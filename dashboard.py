from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objs as go
import pandas as pd

df = pd.read_csv('dummy_data.csv')
df.Date=pd.to_datetime(df.Date)
# df_grouped_scheme_year = df.groupby(['Description of Scheme', 'year'])['Sanctioned Amount'].agg({
#     'Total Sanctioned Amount': 'sum',
#     'Mean Sanctioned Amount': 'mean',
#     'Max Sanctioned Amount': 'max'
# }).reset_index()


app =Dash(__name__,external_stylesheets=['assets/page.css'], suppress_callback_exceptions=True)

# graph 1 layout 
page_1_graph_1= html.Div([
    dcc.Dropdown(options=[{'label': i, 'value': i} for i in df.Class.unique()], value=['COMPS'], multi=True, id='dropdown-selection',
                 ),
                 dcc.Dropdown(
                    options=[
                        {'label': 'Bar Chart', 'value': 'bar'},
                     {'label': 'Pie Chart', 'value': 'pie'},
                     {'label': 'Treemap', 'value': 'treemap'},
                    #  {'label': 'Line', 'value': 'line'},
                     
                 ],
                 value='treemap',
                 id='dropdown-graph-type',
                 placeholder="Select graph type",
                 )
,

    dcc.Graph(id='graph-content')
    ],className='p1g1')

@callback(
    Output('graph-content', 'figure'),
    [Input('dropdown-selection', 'value'),
     Input('dropdown-graph-type', 'value'),
     ],
     
)
def update_graph(selected_class, graph_type):
    # Filter DataFrame based on the selected class value
    if(selected_class == []):
        return None

    grouped_class=df.groupby([df.Date.dt.year,'Class'])['Sanctioned Amount'].sum().reset_index()


    # print(df[df['Class'] == selected_class])
    dff = df[df['Class'] == selected_class[0]]

    x_val = dff.Date.dt.year.unique()
    y_val = dff.groupby(dff.Date.dt.year)['Sanctioned Amount'].sum().values



    if graph_type == 'bar':

        data=df[df['Class'].isin(selected_class)].pivot_table(index=df['Date'].dt.year, columns='Class', values='Sanctioned Amount', aggfunc='sum').reset_index().fillna(0)
        
        fig = px.bar(data, x='Date', y=selected_class, title='Sanctioned Amount vs Year', template='plotly_dark', barmode='group',
             )


        return fig

    # elif graph_type == 'line':

    #     data=df[df['Class'].isin(selected_class)].pivot_table(index=df['Date'].dt.year, columns='Class', values='Sanctioned Amount', aggfunc='sum').reset_index().fillna(0)

    #     fig = px.line(data, x='Date', y=selected_class, color='Class', title='Sanctioned Amount vs Year', template='plotly_dark', 
    #                   mode='lines+markers')

    #     return fig

    
    elif graph_type == 'pie':

        specs=[{"type": "pie"} for i in range(len(selected_class))]
        print(specs)
        fig = make_subplots(rows=1, cols=len(selected_class), subplot_titles=selected_class,print_grid=True,specs=[specs])
        
        for i, class_name in enumerate(selected_class, start=1):
            # Filter DataFrame based on the selected class value
            dff = df[df['Class'] == class_name]
            
            # Group by 'Class' and year extracted from 'Date', then sum 'Sanctioned Amount'
            grouped_data = dff.groupby(dff['Date'].dt.year)['Sanctioned Amount'].sum().reset_index()
            labels=grouped_data['Date']
            values=grouped_data['Sanctioned Amount']
            
            # Create a pie chart for the selected class
            trace = go.Pie(labels=labels, values=values, name=class_name)
            fig.add_trace(trace, row=1, col=i)
            
        fig.update_layout(height=400*len(selected_class), title_text="Sanctioned Amount by Year for Selected Classes",template='plotly_dark')
        return fig


    elif graph_type == 'treemap':
        dff['year']=dff['Date'].dt.year
        fig = px.treemap(dff, path=['year'], values='Sanctioned Amount', title='Sanctioned Amount by Scheme', template='plotly_dark')


    else:
        fig = None  
    
    return fig


page_1_graph_2 = html.Div([
    dcc.Dropdown(
        options=[
            {'label': 'All', 'value': 'all'}
        ] + [{'label': cls, 'value': cls} for cls in df['Class'].unique()],
        id='class-distribution-dropdown',
        value='all',  # Set default value to 'All'
        placeholder='Select a class'
    ),
   
    dcc.Dropdown(
        options=[
            {'label': 'All', 'value': 'all'}
        ] + [{'label': year, 'value': year} for year in sorted(df['year'].unique())],
        id='year-distribution-dropdown',
        value='all',  # Set default value to 'All'
        placeholder='Select a year'
    ),
    dcc.Graph(id='scheme-pie-chart')
], className='p1g1')

@app.callback(
    Output('scheme-pie-chart', 'figure'),
    [Input('class-distribution-dropdown', 'value'),
     Input('year-distribution-dropdown', 'value')]
)
def update_pie_chart(selected_class, selected_year):
    filtered_df = df.copy()

    if selected_class != 'all':
        filtered_df = filtered_df[filtered_df['Class'] == selected_class]
    if selected_year != 'all':
        filtered_df = filtered_df[filtered_df['year'] == selected_year]

    scheme_distribution = filtered_df['Description of Scheme'].value_counts()

    # Define custom color scheme
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

    pie_chart_figure = go.Figure(
        data=[go.Pie(
            labels=scheme_distribution.index,
            values=scheme_distribution.values,
            hole=0.5,  # Set the size of the hole in the middle of the pie chart
            marker=dict(colors=colors),
              # Set custom color scheme
            
        )]
    )

    title = 'Distribution of Students Based on Scheme'
    if selected_class != 'all':
        title += f' in Class {selected_class}'
    if selected_year != 'all':
        title += f' in Year {selected_year}'

    pie_chart_figure.update_layout(
        title=title,
        template='plotly_dark',
        margin=dict(l=20, r=20, t=80, b=20),  # Add padding to the top of the plot area
        height=400,  # Set the height of the pie chart
        width=800,  # Set the total width of the figure
        legend=dict(
            orientation="v",  # Set legend orientation to vertical
            x=1.05,  # Set the x position of the legend to be just right of the chart
            y=0.5,   # Set the y position of the legend to center vertically
            xanchor='left',  # Anchor legend horizontally to the left of the chart
            yanchor='middle'  # Anchor legend vertically at the middle of the chart
        )
    )

    return pie_chart_figure


page_1_graph_3=html.Div([
    dcc.Graph(id='average-sanctioned-amount-bar-plot')
],className='p1g1')

@app.callback(
    Output('average-sanctioned-amount-bar-plot', 'figure'),
    [Input('average-sanctioned-amount-bar-plot', 'id')]
)
def update_bar_plot(id):
    average_sanctioned_amount = df.groupby('Description of Scheme')['Sanctioned Amount'].mean().reset_index()
    bar_plot_figure = go.Figure(
        data=[go.Bar(
            x=average_sanctioned_amount['Description of Scheme'],
            y=average_sanctioned_amount['Sanctioned Amount'],
            marker_color='royalblue',  # Change bar color
            width=0.5  # Adjust bar width
        )]
    )
    bar_plot_figure.update_layout(
        title='Average Sanctioned Amount for Each Scheme',
        xaxis_title='Scheme',
        yaxis_title='Average Sanctioned Amount',
        template='plotly_dark'
    )

    bar_plot_figure.update_xaxes(tickangle=0, tickmode='array', automargin=True)


    return bar_plot_figure


page_1_graph_4=html.Div([
    dcc.Graph(id='sentiment-over-time-graph')
],className='p1g1')

@app.callback(
    Output('sentiment-over-time-graph', 'figure'),
    [Input('sentiment-over-time-graph', 'id')]
)
def update_sentiment_over_time_graph(id):
    sentiment_over_time = df.groupby(['year', 'month', 'sentiment_label']).size().reset_index(name='count')

    sentiment_over_time_fig = go.Figure()
    for sentiment in df['sentiment_label'].unique():
        temp = sentiment_over_time[sentiment_over_time['sentiment_label'] == sentiment]
        sentiment_over_time_fig.add_trace(go.Scatter(x=temp['year'].astype(str) + '-' + temp['month'].astype(str),
                                                    y=temp['count'],
                                                    mode='lines+markers',
                                                    name=sentiment))
        sentiment_over_time_fig.update_layout(title='Distribution of Sentiment Labels Over Time',
                                      xaxis_title='Date',
                                      yaxis_title='Count',
                                      template='plotly_dark')

    return sentiment_over_time_fig


page_1_graph_5=html.Div([

    dcc.Dropdown(
        id='class-dropdown-record-count',
        options=[{'label': 'All', 'value': 'all'} ]+[{'label': cls, 'value': cls} for cls in df['Class'].unique()],
        value=df['Class'].unique()[0],
        placeholder='Select a class'
    ),
    dcc.Dropdown(
        id='scheme-dropdown-record-count',
        options=[{'label': scheme, 'value': scheme} for scheme in df['Description of Scheme'].unique()],
        value=df['Description of Scheme'].unique()[0],
        placeholder='Select a scheme'
    ),

    html.Div([

    #dcc.Graph(id='monthly-count-graph'),
    dcc.Graph(id='yearly-count-graph'),

    ],id='record-count-graph')
    ],className='p1g1')

@app.callback(
    [#Output('monthly-count-graph', 'figure'),
     Output('yearly-count-graph', 'figure')],
    [Input('class-dropdown-record-count', 'value'),
     Input('scheme-dropdown-record-count', 'value')]
)

def update_record_count_graphs(selected_class, selected_scheme):

    if(selected_class == 'all'):
        class_data = df
    else  :
        class_data = df[df['Class'] == selected_class]
    
    scheme_data = class_data[class_data['Description of Scheme'] == selected_scheme]
    monthly_count = scheme_data.groupby('month').size().reset_index(name='count')
    yearly_count = scheme_data.groupby('year').size().reset_index(name='count')

    yearly_count_fig = go.Figure(
        data=[go.Bar(
            x=yearly_count['year'],
            y=yearly_count['count'],
            marker_color='royalblue'
        )]
    )
    yearly_count_fig.update_layout(
        title='Yearly Record Count for Selected Class and Scheme',
        xaxis_title='Year',
        yaxis_title='Record Count',
        template='plotly_dark'
    )

    return (yearly_count_fig,)  

page_1_graph_6 = html.Div([
    dcc.Dropdown(
        id='scheme-dropdown',
        options=[{'label': 'All', 'value': 'all'}]+[{'label': scheme, 'value': scheme} for scheme in df['Description of Scheme'].unique()],
        value=df['Description of Scheme'].unique()[0],
        placeholder='Select a Scheme'
    ),

    dcc.Dropdown(
        id='scheme-aggregation-dropdown',  # Corrected ID
        options=[{'label': option, 'value': option} for option in ['mean', 'sum']],
        value='sum',
        placeholder='Select an Aggregation Option'
    ),

    dcc.Graph(id='scheme-amount-graph')
],className='p1g1')

@app.callback(
    Output('scheme-amount-graph', 'figure'),
    [Input('scheme-dropdown', 'value'),
     Input('scheme-aggregation-dropdown', 'value')]  # Corrected ID
)
def update_graph(selected_scheme, selected_aggregation):

    if(selected_scheme == 'all'):
        filtered_df = df
    else  :  
        filtered_df = df[df['Description of Scheme'] == selected_scheme]

    aggregated_value = filtered_df.groupby('year')['Sanctioned Amount'].agg(str(selected_aggregation))

    fig = px.bar(x=aggregated_value.index, y=aggregated_value.values,
                 title=f'{selected_aggregation.capitalize()} Sanctioned Amount for {selected_scheme}',
                 labels={'x': 'Year', 'y': f'{selected_aggregation.capitalize()} Sanctioned Amount (INR)'},
                 color=aggregated_value.index,template='plotly_dark',color_discrete_sequence=['#7FD4C1'])
    return fig


page_1_graph_7 = html.Div([
    dcc.Dropdown(
        id='trend-sanctioned-amount-scheme-dropdown',
        options=[{'label': scheme, 'value': scheme} for scheme in df['Description of Scheme'].unique()],
        value=df['Description of Scheme'].unique()[0],  # Set default value to the first scheme
        placeholder='Select a Scheme'
    ),

    dcc.Graph(id='trend-sanctioned-amount-per-scheme-graph-container')
],id='trend-sanctioned-amount-scheme-container')

@app.callback(
    Output('trend-sanctioned-amount-per-scheme-graph-container', 'figure'),
    [Input('trend-sanctioned-amount-scheme-dropdown', 'value')]
)

def generate_trend_sanctioned_amount_per_scheme_graph(selected_scheme):
    trend_sanctioned_amount_per_scheme = df.groupby(['Description of Scheme', 'year', 'month'])[
        'Sanctioned Amount'].sum().reset_index().copy()
    
    trend_sanctioned_amount_per_scheme_fig = go.Figure()
    for scheme in trend_sanctioned_amount_per_scheme['Description of Scheme'].unique():
        if scheme == selected_scheme:
            temp = trend_sanctioned_amount_per_scheme[
                trend_sanctioned_amount_per_scheme['Description of Scheme'] == scheme].copy()  # Make a copy here
            temp['year'] = temp['year'].astype(str)
            temp['month'] = temp['month'].astype(str)
            trend_sanctioned_amount_per_scheme_fig.add_trace(go.Scatter(x=temp['year'] + '-' + temp['month'],
                                                                         y=temp['Sanctioned Amount'],
                                                                         mode='lines+markers',
                                                                         name=scheme))
    trend_sanctioned_amount_per_scheme_fig.update_layout(
        title='Trend of Sanctioned Amounts Over Time for Scheme: ' + selected_scheme,
        xaxis_title='Date',
        yaxis_title='Sanctioned Amount',
        template='plotly_dark')
    return trend_sanctioned_amount_per_scheme_fig


page_1_graph_8=html.Div([
    dcc.Dropdown(
        id='sentiment-scheme-dropdown',
        options=[{'label': scheme, 'value': scheme} for scheme in df['Description of Scheme'].unique()],
        value=df['Description of Scheme'].unique()[0],
        placeholder='Select a Scheme'
    ),
    dcc.Graph(id='sentiment-scheme-graph')
],className='p1g1' )

# Define the callback to update the graph
@app.callback(
    Output('sentiment-scheme-graph', 'figure'),
    [Input('sentiment-scheme-dropdown', 'value')]
)

def update_graph(selected_scheme):
    filtered_data = df[df['Description of Scheme'] == selected_scheme]

    grouped_data=filtered_data.groupby(['year','sentiment_label'])['Record No.'].size().reset_index(name='count')

    sentiment_over_time_fig = go.Figure()

    # Loop through each unique sentiment label
    for sentiment in filtered_data['sentiment_label'].unique():
        # Filter the grouped data for the current sentiment label
        temp = grouped_data[grouped_data['sentiment_label'] == sentiment]
        
        # Add a trace for the current sentiment label
        sentiment_over_time_fig.add_trace(go.Scatter(x=temp['year'].astype(str),
                                                     y=temp['count'],
                                                     mode='lines+markers',
                                                     name=sentiment))

    # Update layout
    sentiment_over_time_fig.update_layout(title=f'Distribution of Sentiment Labels Over Time for Scheme: {selected_scheme}',
                                           xaxis_title='Year',
                                           yaxis_title='Count',
                                           template='plotly_dark')

    
    return sentiment_over_time_fig



app.layout = html.Div([

    # col-1 => sidebar

    # html.Div([
    #     html.H1(children='Welcome To DashBoard', style={'textAlign':'center'})
    # ],style={'width': '100%', 
    #         'position': 'relative',
    #         'flex':'1',
    #         'background-color':'#4c25c1',
    #         'min-height':'100%'
    #          },
    #          id='col-1'
    #          ),
    
    #  col-2 => content

    html.Div([
    html.H1(children=[
    html.Span('EmpowerED', style={'color': 'limegreen'}),
    ' Analytics'
], style={'textAlign': 'center', 'color': 'white', 'margin': '10px', 'padding': '5px'}),

    # page 1
    html.Div(   
            [page_1_graph_1,page_1_graph_2,page_1_graph_6,page_1_graph_8,page_1_graph_5,page_1_graph_3,page_1_graph_4],
            id="page-1"
            ),

    # page 2
    html.Div(   
            [page_1_graph_7],
            id="page-2"
            ),



    # page 3

    ],id='col-2',style={'width': '100%','flex':'4'})
    
], style={'width': '100%', 'position': 'relative','display':'flex'},id="body")

if __name__ == '__main__':
    print("app is running on :" f'http://127.0.0.1:8050/')
    app.run(debug=False)