# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 20GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import warnings
warnings.filterwarnings('ignore')
emp_eng = pd.read_csv('/kaggle/input/employeedataset/employee_engagement_survey_data.csv')
emp_eng.head()
emp_eng.shape
def data_description(dataframe):
    description = pd.DataFrame({'Columns':dataframe.columns,
                                'Dtype' : [dataframe[i].dtype for i in dataframe.columns],
                                'Nunique Values': [dataframe[i].nunique() for i in dataframe.columns],
                                'Null Values': [dataframe[i].isna().sum() for i in dataframe.columns]})
    return description

data_description(emp_eng)
training = pd.read_csv('/kaggle/input/employeedataset/training_and_development_data.csv')
training.head()
training.shape
data_description(training)
combine = pd.merge(emp_eng,training,on=['Employee ID'])
combine.head()
combine['Survey Date'] = pd.to_datetime(combine['Survey Date'])
combine['Training Date'] = pd.to_datetime(combine['Training Date'])
cat_cols = [col for col in combine.columns if combine[col].dtype == 'O' if col not in ['Location','Trainer']]
num_cols = combine.select_dtypes([np.number]).columns.to_list()
num_cols.remove('Employee ID')
def plots(data,col):
    
    fig = make_subplots(rows = 1, cols=2,subplot_titles=['Distribution of '+ col,'Distribution of '+ col])
    
    fig.add_traces(go.Histogram(x = data[col],name=str(col), 
                                xbins=dict(start=data[col].min(),end=data[col].max()),
                                marker=dict(color='#D7BDE2'),
                                marker_line_width=1,
                                marker_line_color="#BB8FCE"),1,1)
    
    fig.add_traces(go.Box(y = data[col],name=str(col),marker=dict(color='#D7BDE2'),
                          marker_line_width=1,marker_line_color="#BB8FCE"),1,2)
    
    fig.update_layout(paper_bgcolor='#F5EEF8', plot_bgcolor = '#F5EEF8',
                      template='plotly_white',
                      xaxis=dict(showgrid=False),
                      yaxis=dict(showgrid=False),
                      showlegend=False,
                      bargap=0.15)
    
    fig.show()
for i in num_cols:
    plots(combine,i)
plot_rows=1
plot_cols=3
fig = make_subplots(rows=plot_rows, cols=plot_cols,specs = [[{'type':'domain'},{'type':'domain'},{'type':'domain'}]],
                   subplot_titles=['Training Program','Training Type','Training Outcome'])

# add traces
x = 0
for i in range(1, plot_rows + 1):
    for j in range(1, plot_cols + 1):
        fig.add_trace(go.Pie(labels = combine[cat_cols[x]].value_counts().keys(),
                             values = combine[cat_cols[x]].value_counts().values,
                             name = str(combine[cat_cols].columns[x]),
                             textinfo='label+percent',
                             marker = dict(colors = px.colors.qualitative.Pastel1)),
                     row=i,
                     col=j)

        x=x+1
        
fig.update_traces(showlegend=False, hole = 0.6)

fig.update_layout(paper_bgcolor='#F5EEF8', plot_bgcolor = '#F5EEF8',title='Employee Training ',
                  annotations=[dict(text='Training Program', x=0.14, y=0.5, font_size=12, showarrow=False,font_color='grey'),
                              dict(text='Training Type', x=0.50, y=0.5, font_size=12, showarrow=False,font_color='grey'),
                              dict(text='Training Outcome', x=0.84, y=0.5, font_size=12, showarrow=False,font_color='grey')])
fig.show()
program = combine.groupby('Training Program Name')['Engagement Score','Satisfaction Score','Work-Life Balance Score'].mean()

fig = px.scatter(program,x=program.index,y=program.columns,
                 color_discrete_sequence=['#7FB3D5','#F7DC6F','#E59866'])

fig.update_traces(marker={'size': 12})
fig.update_layout(paper_bgcolor='#F5EEF8', plot_bgcolor = '#F5EEF8',
                  title='Training Program VS Average Scores')
fig.show()
outcome = combine.groupby('Training Outcome')['Engagement Score','Satisfaction Score','Work-Life Balance Score'].mean()
fig = px.scatter(outcome,x=outcome.index,y=outcome.columns,
                 color_discrete_sequence=['#7FB3D5','#F7DC6F','#E59866'])

fig.update_traces(marker={'size': 12})
fig.update_layout(paper_bgcolor='#F5EEF8', plot_bgcolor = '#F5EEF8',
                  title='Training Program VS Average Scores')
fig.show()
type_score = combine.groupby('Training Type')['Engagement Score','Satisfaction Score','Work-Life Balance Score'].mean()

fig = px.scatter(type_score,x=type_score.index,y=type_score.columns,
                 color_discrete_sequence=['#7FB3D5','#F7DC6F','#E59866'],)
fig.update_traces(marker={'size': 12})

fig.update_layout(paper_bgcolor='#F5EEF8', plot_bgcolor = '#F5EEF8',
                  title='Training Program VS Average Scores',)
fig.show()
fig = make_subplots(rows=1,cols=1, subplot_titles=['Training Cost VS Training Program '])

traces0 = (px.bar( x =combine['Training Program Name'],y=combine['Training Cost'],
                        color=combine['Training Program Name'],
                        color_discrete_map = {'Customer Service':'#9B59B6','Leadership Development':'#1F618D',
                                              'Technical Skills':'#138D75','Communication Skills':'#F1C40F',
                                              'Project Management':'#CA6F1E'})).data
for trace in traces0:
          fig.add_trace(trace,row=1,col=1)

        
fig.update_layout(paper_bgcolor='#F5EEF8', plot_bgcolor = '#F5EEF8')
fig.show()
internal = pd.DataFrame(combine[combine['Training Type'] == 'Internal']['Training Program Name'].value_counts())
external = pd.DataFrame(combine[combine['Training Type'] == 'External']['Training Program Name'].value_counts())
fig = make_subplots(rows = 1,cols=2,specs=[[{'type':'domain'},{'type':'domain'}]])

fig.add_trace(go.Pie(labels = internal.index,
                     values = internal['Training Program Name']),1,1)

fig.add_trace(go.Pie(labels =external.index,
                     values = external['Training Program Name']),1,2)

fig.update_traces(hole=0.6,marker = dict(colors = px.colors.qualitative.Pastel1))
fig.update_layout(paper_bgcolor='#F5EEF8', plot_bgcolor = '#F5EEF8',title='Employee Training ',
                  annotations=[dict(text='Training Type ', x=0.14, y=0.5, font_size=12, showarrow=False,font_color='grey'),
                              dict(text='Internal', x=0.50, y=0.5, font_size=12, showarrow=False,font_color='grey'),
                              dict(text='External', x=0.84, y=0.5, font_size=12, showarrow=False,font_color='grey')])
fig.show()
duration = pd.DataFrame(combine.groupby('Training Duration(Days)')['Training Program Name'].value_counts().reset_index(name='count'))
#duration = pd.DataFrame(combine.groupby('Training Duration(Days)')['Training Program Name'].value_counts())
fig = make_subplots(rows=1,cols=1, subplot_titles=['Training Cost VS Training Program '])

traces1 = (px.bar( x = duration['Training Duration(Days)'],
                   y = duration['count'],
                   color = duration['Training Program Name'],
                   color_discrete_map = {'Customer Service':'#9B59B6','Leadership Development':'#1F618D',
                                              'Technical Skills':'#138D75','Communication Skills':'#F1C40F',
                                              'Project Management':'#CA6F1E'})).data
for trace in traces1:
          fig.add_trace(trace,row=1,col=1)

        
fig.update_layout(paper_bgcolor='#F5EEF8', plot_bgcolor = '#F5EEF8')
fig.show()
''' Plot a Shifted Correlation Matrix '''
# Diagonal correlation is always unity & less relevant, shifted variant shows only relevant cases
def corrMat(df,id=False):
    
    corr_mat = df.corr().round(2)
    f, ax = plt.subplots(figsize=(10,5))
    mask = np.triu(np.ones_like(corr_mat, dtype=np.bool))
    mask = mask[1:,:-1]
    corr = corr_mat.iloc[1:,:-1].copy()
    sns.heatmap(corr,mask=mask,vmin=-0.3,vmax=0.3,center=0, 
                cmap='RdPu_r',square=False,lw=2,annot=True,cbar=False)
#     bottom, top = ax.get_ylim() 
#     ax.set_ylim(bottom + 0.5, top - 0.5) 
    ax.set_title('Shifted Linear Correlation Matrix')
corrMat(combine)

