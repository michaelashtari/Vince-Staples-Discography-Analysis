#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 30 12:52:11 2022

@author: michaelashtari
"""
import pandas as pd
import numpy as np
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Read in the tracks dataset, containing all tracks from the artist

tracks_df = pd.read_csv('tracks.csv', index_col = 'Unnamed: 0')

# Define a list of all normalized columns in the dataset (numerical columns that range between 0 and 1)

tracks_df_floats = tracks_df.select_dtypes('float64')
normalized_columns = tracks_df_floats.loc[:,((tracks_df_floats >= 0) & (tracks_df_floats <= 1)).any()].columns.to_list()

# Add an option for all columns, specifically for the dropdown widget

normalized_columns_dropdown = list(normalized_columns)
normalized_columns_dropdown.insert(0, 'All')

# Create a dictionary containing definitions of all audio features
feature_definitions = {
    'danceability' : ['Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity.', ' A value of 0.0 is least danceable and 1.0 is most danceable.'],
    'energy' : ['Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity.', 'Typically, energetic tracks feel fast, loud, and noisy. ', 'For example, death metal has high energy, while a Bach prelude scores low on the scale. ', 'Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy.'],
    'speechiness' : ['Speechiness detects the presence of spoken words in a track. ','The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value. ', 'Values above 0.66 describe tracks that are probably made entirely of spoken words. ','Values between 0.33 and 0.66 describe tracks that may contain both music and speech, either in sections or layered, including such cases as rap music. ','Values below 0.33 most likely represent music and other non-speech-like tracks.'],
    'acousticness' : ['Acousticness is a confidence measure from 0.0 to 1.0 of whether the track is acoustic. ','1.0 represents high confidence the track is acoustic.'],
    'instrumentalness' : ['Instrumentalness predicts whether a track contains no vocals. ','"Ooh" and "aah" sounds are treated as instrumental in this context. ','Rap or spoken word tracks are clearly "vocal". ','The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. ','Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0.'],
    'liveness' : ['Liveness detects the presence of an audience in the recording.','Higher liveness values represent an increased probability that the track was performed live. ','A value above 0.8 provides strong likelihood that the track is live.'],
    'valence' : ['Valence is a measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. ','Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry).']
    }

# Create a dash application

app = dash.Dash(__name__)
server = app.server

# Create the app layout

app.layout = html.Div(children=[html.H1('Vince Staples Album Analysis',
                                        style = {'textAlign' : 'center',
                                                 'fontSize' : '40'
                                                 }
                                        ),
                                
                                html.Label('Select an album for track-level breakdown',
                                           style = {'font-weight' : 'bold'}
                                           ),
                                
                                dcc.Dropdown(options = [album for album in tracks_df['album'].unique()[::-1]],
                                             value = 'Hell Can Wait',
                                             id = 'album_selection_dropdown'
                                             ),
                                html.Div(id = 'album_title_cover'),
                                
                                html.Br(),
                                
                                html.Div(dcc.Graph(id = 'track_popularity_barchart'),
                                         style = {'width' : 1000, 'margin' : 'auto'}
                                         ),
                                
                                html.Br(),
                                
                                html.Br(),
                                
                                html.Label('Select an audio feature to filter the heatmap. A definition is generated below the plot for reference',
                                           style = {'font-weight' : 'bold'}
                                           ),
                                
                                dcc.Dropdown(options = normalized_columns_dropdown,
                                             value = 'All',
                                             id = 'audio_feature_dropdown'),
                                html.Br(),
                                
                                html.Div(children = [
                                    dcc.Graph(id = 'album_heatmap', style = {'display' : 'inline-block'}),
                                    dcc.Graph(id = 'tempo_duration_lines', style = {'display' : 'inline-block'})
            
                                    ]),
                                
                                html.Div(id = 'audio_feature_definition',
                                         style = {'width' : 550})
                                
                                
    ],
    style = {'font-family' : 'Calibri'}
    )


# Create callback function that takes the selected album and audio feature(s) and returns a heatmap

@app.callback(Output(component_id = 'album_heatmap', component_property = 'figure'),
              Input(component_id = 'album_selection_dropdown', component_property = 'value'),
              Input(component_id = 'audio_feature_dropdown', component_property = 'value')
              )

def get_heatmap(album, audio_feature):
    # Filter dataframe to selected album
    album_tracks = tracks_df[tracks_df['album'] == album]
    album_tracks.set_index(keys = 'track_name', drop = True, inplace = True)
    
    if audio_feature == 'All':
        album_tracks = album_tracks.loc[:, normalized_columns]
        heatmap_fig = px.imshow(album_tracks, zmin = 0, zmax = 1, color_continuous_scale = ['white', 'teal'])
        heatmap_fig.update_layout(dict(autosize = True, xaxis = go.layout.XAxis(tickangle = 45)))
    else:
        album_tracks = pd.DataFrame(album_tracks.loc[:, audio_feature])
        heatmap_fig = px.imshow(album_tracks, color_continuous_scale = ['white', 'teal'])
        heatmap_fig.update_layout(dict(plot_bgcolor = 'white'))
        heatmap_fig.update_xaxes(dict(tickangle = 0))
        heatmap_fig.update_layout(dict(autosize = True))
    
    heatmap_fig.update_layout(dict(title = 'Track-level Audio Feature Heatmap', title_x = 0.5, xaxis_title = 'Audio Feature', yaxis_title = 'Track Name', width = 550, height = 550))
    
    return heatmap_fig

@app.callback(Output(component_id = 'audio_feature_definition', component_property = 'children'),
              Input(component_id = 'audio_feature_dropdown', component_property = 'value')
              )
def get_heatmap_caption(audio_feature):
    caption = []
    
    if audio_feature == 'All':
        return html.Br()
    else:
        for sentence in feature_definitions[audio_feature]: 
            caption_sentence = html.Div(children = [
                html.P(children = sentence,
                       style = {'textAlign' : 'left',
                                'fontSize' : 14}
                       ),
                html.P(children = '',style = {'margin' : 0, 'textIndent' : 3}),
                ]
            )
            
            caption.append(caption_sentence)
        
        # Create a header preluding the definition
        
        caption_header = html.H4(children = 'Definition',
                                 style = {'font-weight' : 'bold',
                                          'fontSize' : 16,
                                          'textAlign' : 'center'
                                          }
                                 )
        caption.insert(0, caption_header)
        
        return caption
    
# Create callback function that takes the selected album and produces a plot with curves for tempo/duration of tracks within the album
    
@app.callback(Output(component_id = 'tempo_duration_lines', component_property = 'figure'),
              Input(component_id = 'album_selection_dropdown', component_property = 'value')
              )
def get_tempo_duration_plot(album):
    #Filter dataframe to selected album
    album_tracks = tracks_df[tracks_df['album'] == album]
    album_tracks.set_index(keys = 'track_name', drop = False, inplace = True)
    album_tracks['track_duration_m'] = album_tracks['track_duration_s']/60
    
    tempo_duration_plot = make_subplots(specs = [[{'secondary_y' : True}]])
    
    tempo_duration_plot.add_trace(
        go.Scatter(x = album_tracks['track_name'], y = album_tracks['tempo'], name = 'Tempo', mode = 'lines'),
        secondary_y = False
        )
    
    tempo_duration_plot.add_trace(
        go.Scatter(x = album_tracks['track_name'], y = album_tracks['track_duration_m'], name = 'Duration', mode = 'lines'),
        secondary_y = True
        )
   
    tempo_duration_plot.layout.title = dict(text = 'Track-level Tempo and Duration', x = 0.5)
    tempo_duration_plot.layout.legend = dict(orientation = 'h', borderwidth = 0.1, y = 1.02, xanchor = 'left', yanchor = 'bottom', bordercolor = 'white')
    tempo_duration_plot.layout.xaxis.title = 'Track Name'
    tempo_duration_plot.layout.xaxis.tickangle = 45
    tempo_duration_plot.layout.yaxis.title = 'Tempo (BPM)'
    tempo_duration_plot.layout.yaxis2.title = 'Track Duration (min)'
    tempo_duration_plot.update_layout(dict(width = 850, height = 550))
    

   # tempo_duration_plot.update_layout(dict(title = 'Track Tempo and Duration Trajectory'), title_x = 0.5, xaxis_title = 'Track Name', yaxis_title = 'Tempo')
    
    return tempo_duration_plot


# Create callback function that takes the selected album and displays the album name (as a header) and the album cover
    
@app.callback(Output(component_id = 'album_title_cover', component_property = 'children'),
              Input(component_id = 'album_selection_dropdown', component_property = 'value')
              )
def get_album_header_and_cover(album):
    album_cover_url = tracks_df[tracks_df['album'] == album].iloc[0]['album_cover_url_large']
    album_release_date = tracks_df[tracks_df['album'] == album].iloc[0]['album_release_date']
    fig = go.Figure()
    fig.add_layout_image(dict(source = album_cover_url))
    div = html.Div(children = [html.H2(children = album,
                                       style = {'textAlign' : 'center'}
                                       ),
                               html.Div(children = [
                                   html.Strong(children = 'Released: '),
                                   html.Span(children = album_release_date + '\n')
                                   ],
                                   style = {'textAlign' : 'center'}
                                ),
                               
                               html.Img(src = album_cover_url)
                               ],
                   style = {'textAlign' : 'center'}
                   )
                               
    return div
    

# Create callback function that takes the selected album and produces a bar chart of constituent tracks' popularity
    
@app.callback(Output(component_id = 'track_popularity_barchart', component_property = 'figure'),
              Input(component_id = 'album_selection_dropdown', component_property = 'value')
              )
def get_pop_barchart(album):
    #Filter dataframe to selected album
    album_tracks = tracks_df[tracks_df['album'] == album]
    album_tracks.set_index(keys = 'track_name', drop = True, inplace = True)
    
    pop_barchart_fig = px.bar(album_tracks, y = 'track_popularity')
    pop_barchart_fig.update_layout(dict(title = 'Track Popularity'), title_x = 0.5, xaxis_title = 'Track Name', yaxis_title = 'Popularity Score (out of 100)')
    pop_barchart_fig.update_traces(dict(marker_color = 'teal'))
    
    return pop_barchart_fig
    



# Run the app
if __name__ == '__main__':
    app.run_server()
