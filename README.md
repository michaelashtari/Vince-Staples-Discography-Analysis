# Vince-Staples-Discography-Analysis
This repository contains all workfiles supporting my analytical exploration of Vince Staples' discography.

The numbered .ipynb files (Jupyter notebooks) contain all markdown and Python code related to the data collection, exploration, and modeling steps of the analysis, with the 'tracks.csv' file being the output of the data collection exercise (step 1 of 3), and input to the exploratory stage (step 2 of 3). After adequate examination of the dataset, I perform track segmentation by employing K-Means clustering to form pseudo-albums (step 3 of 3). At this stage, I further characterize each cluster by visualizing the distributions of their audio features. In this sense, the clustering step can be seen as an extension of the EDA performed in step 2.

All other non-ipynb files are supporting documents for the Vince Staples Album Analysis dashboard, which is currently being publicly hosted on the Heroku platform as a hobbyist app, and can be accessed here: https://polar-harbor-82279.herokuapp.com. The dashboard provides an analytical canvas to facilitate intra-album track comparisons, and was built using Plotly's web-application building framework, Dash; see 'album_track_analysis_dash.py' for details.

Thank you for taking the time to peruse this repo! Any comments or feedback/criticism are welcome.
