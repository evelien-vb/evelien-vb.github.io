import pandas as pd
import numpy 
import json

import plotly as px
import plotly.graph_objects as go

def word_count_plot(results,word):
    df_word = results[word]['word_count']
    
    bg_color = 'rgb(0,0,0)'
    paper_color = 'rgb(0,0,0)'
    font_plot = 'Arial'
    font_size_plot = 20
    text_color = 'rgb(255,255,255)'

    fig = go.Figure(data=[go.Scatter(name = 'de Volkskrant',x=df_word['year'], y=df_word['De Volkskrant']),
                     go.Scatter(name = 'Trouw',x=df_word['year'], y=df_word['Trouw']),
                     go.Scatter(name = 'Algemeen Dagblad',x=df_word['year'], y=df_word['Algemeen dagblad']),
                     go.Scatter(name = 'de Telegraaf',x=df_word['year'], y=df_word['De Telegraaf'])])

    fig['layout']['xaxis'].update(title='jaar')
    fig['layout']['yaxis'].update(title='Aantal keer')
    fig.update_layout(title_text='Aantal keren dat '+word+ ' wordt genoemd in een artikel op de voorpagina')
    fig.update_layout(autosize=False,width=1200, height=600)
    fig.update_layout(font_family=font_plot,font_size=font_size_plot,plot_bgcolor=bg_color,paper_bgcolor=paper_color)
    fig.update_traces(line_width=5)
    fig.update_layout(hovermode='x unified')
    fig.update_layout(title_font_color=text_color)
    fig.update_xaxes(title_font_color=text_color,tickfont_color=text_color)
    fig.update_yaxes(title_font_color=text_color,tickfont_color=text_color)
    fig.update_layout(legend_font_color=text_color)
    
    graphJSON = json.dumps(fig, cls=px.utils.PlotlyJSONEncoder)
    
    return graphJSON


def plot_most_important_words(results,word):
    
    bg_color = 'rgb(0,0,0)'
    paper_color = 'rgb(0,0,0)'
    font_plot = 'Arial'
    font_size_plot = 20
    text_color = 'rgb(255,255,255)'
    
    df_miw = results[word]['most_important_words']
    year = results[word]['year_most_count']
    if type(df_miw)==pd.core.frame.DataFrame:
        fig = go.Figure(data=[
        go.Bar(name='Volkskrant', x=df_miw['word'], y=df_miw['De Volkskrant'],marker_color='rgb(81, 72, 250)'),
         go.Bar(name='Trouw', x=df_miw['word'], y=df_miw['Trouw'],marker_color='rgb(137, 72, 250)'),
        go.Bar(name='Algemeen Dagblad', x=df_miw['word'], y=df_miw['Algemeen dagblad'],marker_color='rgb(250, 72, 122)'),
        go.Bar(name='Telegraaf', x=df_miw['word'], y=df_miw['De Telegraaf'],marker_color='rgb(255, 0, 0)'),
        ])

        fig.update_yaxes(tickformat= '%')
        fig.update_layout(title_text='Woordgebruik in artikelen uit ' +  str(year) + ' waarin '+word +' genoemd wordt')
        fig['layout']['yaxis'].update(title='% van artikelen waar woorden in genoemd wordt')
        fig.update_layout(autosize=False,width=1200, height=600)
        fig.update_layout(font_family=font_plot,font_size=font_size_plot,plot_bgcolor=bg_color,paper_bgcolor=paper_color)
        fig.update_layout(title_font_color=text_color)
        fig.update_xaxes(title_font_color=text_color,tickfont_color=text_color)
        fig.update_yaxes(title_font_color=text_color,tickfont_color=text_color)
        fig.update_layout(legend_font_color=text_color)
        
        
        graphJSON = json.dumps(fig, cls=px.utils.PlotlyJSONEncoder)
        return graphJSON
        
    
    else:
        return ''

def get_ml_results_str(results,word):
    np_title_list = ['het algemeen dagblad','de telegraaf','de volkskrant','trouw']
    cm_test= results[word]['ml_results']['Test results']['cm']
   
    cm_test_norm = cm_test/ cm_test.astype(numpy.float).sum(axis=0)
    
    results_str = '<h1> Resulaten van de machine learning berekeningen: <h1>'
    for i,np_i in enumerate(np_title_list):

         
         recall_result = list(cm_test_norm[i][:])
         print(recall_result[0])
         recall_result_max = recall_result.copy()
         recall_result_max.pop(i)

         max_dif_class = max(recall_result_max)
         dif_np = np_title_list[recall_result.index(max_dif_class)]
         results_str = results_str + '<h1>' + str(round(recall_result[i]*100,2)) +'% van de artikelen uit '+ np_i + ' zijn correct geclassificeerd.'+str(round(max_dif_class*100,2)) + '% van de artikelen uit '+np_i + ' zijn geclassificeerd als ' + dif_np +'.<h1>'
         print(results_str)
    
    print(results_str)    
    return results_str

def get_ml_results_plot(results,word):
    bg_color = 'rgb(0,0,0)'
    paper_color = 'rgb(0,0,0)'
    font_plot = 'Arial'
    font_size_plot = 20
    text_color = 'rgb(255,255,255)'
    year = results[word]['year_most_count']
    np_title_list = ['het algemeen dagblad','de telegraaf','de volkskrant','trouw']
    
    cm_test= results[word]['ml_results']['Test results']['cm']
    cm_test_norm = cm_test/ cm_test.astype(numpy.float).sum(axis=0)
    df_cm_temp = pd.DataFrame(columns=np_title_list,index=np_title_list)

    
    for i,np_i in enumerate(np_title_list):
        for j,np_j in enumerate(np_title_list):
            df_cm_temp.iloc[j][np_i] = cm_test_norm[i][j]
            
    print(df_cm_temp)
    df_cm = pd.DataFrame(columns=np_title_list)
    print(df_cm_temp.loc['het algemeen dagblad'])
    df_cm.loc['de volkskrant']=df_cm_temp.loc['de volkskrant'].copy()
    df_cm.loc['trouw']=df_cm_temp.loc['trouw'].copy()
    df_cm.loc['het algemeen dagblad']=df_cm_temp.loc['het algemeen dagblad'].copy()
    df_cm.loc['de telegraaf']=df_cm_temp.loc['de telegraaf'].copy()

    np_title_list = ['Volkskrant','Trouw','Algemeen dagblad','Telegraaf']
    fig = go.Figure(data=[
       go.Bar(name='Volkskrant', x=np_title_list, y=df_cm['de volkskrant'],marker_color='rgb(81, 72, 250)'),
       go.Bar(name='Trouw', x=np_title_list, y=df_cm['trouw'],marker_color='rgb(137, 72, 250)'),
       go.Bar(name='Algemeen Dagblad', x=np_title_list, y=df_cm['het algemeen dagblad'],marker_color='rgb(250, 72, 122)'),
       go.Bar(name='Telegraaf', x=np_title_list, y=df_cm['de telegraaf'],marker_color='rgb(255, 0, 0)'),
        ])
    
    
    fig['layout']['xaxis'].update(title='Artikelen uit krant x')
    fig['layout']['yaxis'].update(title='% van artikelen geclassificeerd als krant y')
    fig.update_yaxes(tickformat= '%')
    fig.update_layout(autosize=False,width=1200, height=600)
    fig.update_layout(font_family=font_plot,font_size=font_size_plot,plot_bgcolor=bg_color,paper_bgcolor=paper_color)
    fig.update_layout(title_font_color=text_color)
    fig.update_xaxes(title_font_color=text_color,tickfont_color=text_color)
    fig.update_yaxes(title_font_color=text_color,tickfont_color=text_color)
    fig.update_layout(legend_font_color=text_color)
    fig.update_layout(title_text='Resultaten machine learning classificatie van artikelen uit het jaar ' +  str(year) + ' waarin '+ word +' genoemd wordt')     
    graphJSON = json.dumps(fig, cls=px.utils.PlotlyJSONEncoder)
    return graphJSON
            
 