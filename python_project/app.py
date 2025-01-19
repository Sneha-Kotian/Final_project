from flask import Flask, render_template, request, jsonify
import pandas as pd
import random

app = Flask(__name__)

df = pd.read_csv(r'C:\Users\SNEHA\python_project\python_project\data.csv')

genres = df.columns[18:].tolist()  

@app.route('/')
def home():
    songs = df['song_name'].sort_values().unique().tolist()
    genres = df.columns[18:].tolist()  
    return render_template('index.html', songs=songs, genres=genres)

@app.route('/recommend', methods=['POST'])
def recommend():
    
    song_name = request.form['song_name']
    genre = request.form['genre']
    top_n = int(request.form['top_n'])

    print(f"Received song_name: {song_name}, genre: {genre}, top_n: {top_n}")  

    filtered_df = df[df['song_name'].str.contains(song_name, case=False, na=False)]  

    if genre != 'All':
        filtered_df = filtered_df[filtered_df[genre] > 0.5]  

    recommendations_count = min(top_n, len(filtered_df))
    print(f"Filtered data count: {len(filtered_df)}")  
    
    recommendations = filtered_df[['song_name', 'artist_name', 'spotify_track_link', 'thumbnail_link']].sample(n=recommendations_count)
   
    recommendations_list = recommendations.to_dict(orient='records')

    return jsonify(recommendations_list)

if __name__ == '__main__':
    app.run(debug=True)
