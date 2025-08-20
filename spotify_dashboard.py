import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
import numpy as np
from datetime import datetime, timedelta
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Spotify Story",
    page_icon="images/spotify.ico",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for dark masculine styling
st.markdown("""
<style>
    body, .stApp {
        background-color: #0e1117;
        color: #e0e0e0;
    }
    
    .main-header {
        font-size: 3.8rem;
        font-weight: 800;
        background: linear-gradient(45deg, #1DB954, #1ed760);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        letter-spacing: -1px;
    }
    
    .subtitle {
        font-size: 1.3rem;
        color: #FFFFFF;
        text-align: center;
        margin-bottom: 2rem;
        font-style: italic;
        font-weight: 300;
    }
    
    .metric-container {
        background: linear-gradient(135deg, #121212 0%, #1c1c1c 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.6);
        margin-bottom: 1rem;
        border: 1px solid #2a2a2a;
        transition: transform 0.3s ease;
    }
    
    .metric-container:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.8);
    }
    
    .metric-container h3 {
        font-size: 2.2rem;
        margin-bottom: 0.2rem;
        font-weight: 700;
    }
    
    .metric-container p {
        font-size: 1rem;
        color: #8c8c8c;
        margin-bottom: 0;
    }
    
    .story-section {
        background: rgba(25, 25, 35, 0.7);
        padding: 1.8rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        border-left: 4px solid #1DB954;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
    }
    
    .story-section h2 {
        font-size: 1.8rem;
        margin-bottom: 1rem;
        color: #ffffff;
        border-bottom: 1px solid #2a2a2a;
        padding-bottom: 0.5rem;
    }
    
    .insight-box {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        margin: 1.5rem 0;
        border: 1px solid #2a2a2a;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.5);
    }
    
    .insight-box h3 {
        font-size: 1.6rem;
        margin-bottom: 1rem;
        color: #1DB954;
        border-bottom: 1px solid #2a2a2a;
        padding-bottom: 0.5rem;
    }
    
    .insight-box ul {
        padding-left: 1.5rem;
        margin-bottom: 0;
    }
    
    .insight-box li {
        margin-bottom: 0.8rem;
        font-size: 1.1rem;
    }
    
    .genre-tag {
        background: linear-gradient(45deg, #1DB954, #1ed760);
        color: #0e1117;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        margin: 0.3rem;
        display: inline-block;
        font-size: 0.9rem;
        font-weight: 600;
    }
    
    .mood-indicator {
        padding: 1.2rem 0.5rem;
        border-radius: 10px;
        margin: 0.5rem;
        text-align: center;
        font-weight: bold;
        background: #1a1a1a;
        border: 1px solid #2a2a2a;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.3);
    }
    
    .mood-indicator h4 {
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
        color: #ffffff;
    }
    
    .mood-indicator p {
        font-size: 1.1rem;
        margin-bottom: 0;
        color: #8c8c8c;
    }
    
    .stMetric > div > div > div > div {
        color: #1DB954;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff;
        font-weight: 600;
    }
    
    p {
        color: #b0b0b0;
    }
    
    .st-bb, .st-at {
        background-color: #1a1a1a !important;
    }
    
    .st-bc, .st-bd {
        color: #ffffff !important;
    }
    
    .stFileUploader > div > div {
        background: #121212 !important;
        border: 1px solid #2a2a2a !important;
        color: #e0e0e0 !important;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        background: #121212;
        border-bottom: 1px solid #2a2a2a;
    }
    
    .stTabs [aria-selected="true"] {
        background: #1a1a1a !important;
        color: #1DB954 !important;
        font-weight: 600 !important;
        border-bottom: 2px solid #1DB954 !important;
    }
    
    .stTabs [aria-selected="false"] {
        color: #8c8c8c !important;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_sample_data():
    """Generate sample data for demonstration"""
    np.random.seed(42)
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='min')
    
    # Sample artists and tracks
    artists = ['The Beatles', 'Taylor Swift', 'Drake', 'Billie Eilish', 'Ed Sheeran', 
               'Ariana Grande', 'Post Malone', 'Olivia Rodrigo', 'Bad Bunny', 'The Weeknd',
               'Dua Lipa', 'Harry Styles', 'Coldplay', 'Imagine Dragons', 'Adele']
    
    tracks = {
    'The Beatles': ['Hey Jude', 'Come Together', 'Let It Be', 'Here Comes the Sun'],
    'Taylor Swift': ['Anti-Hero', 'Shake It Off', 'Blank Space', 'Love Story'],
    'Drake': ['God\'s Plan', 'In My Feelings', 'Hotline Bling', 'Started From the Bottom'],
    'Billie Eilish': ['bad guy', 'Happier Than Ever', 'Therefore I Am', 'Ocean Eyes'],
    'Ed Sheeran': ['Shape of You', 'Perfect', 'Thinking Out Loud', 'Bad Habits'],
    'Ariana Grande': ['thank u, next', '7 rings', 'positions', 'Break Free'],
    'Post Malone': ['Circles', 'Sunflower', 'Rockstar', 'Congratulations'],
    'Olivia Rodrigo': ['drivers license', 'good 4 u', 'vampire', 'deja vu'],
    'Bad Bunny': ['Tití Me Preguntó', 'Me Porto Bonito', 'Un Verano Sin Ti', 'Yo Perreo Sola'],
    'The Weeknd': ['Blinding Lights', 'Can\'t Feel My Face', 'Starboy', 'The Hills'],
    'Dua Lipa': ['Levitating', 'Don\'t Start Now', 'Physical', 'New Rules'],
    'Harry Styles': ['As It Was', 'Watermelon Sugar', 'Adore You', 'Golden'],
    'Coldplay': ['Yellow', 'Viva La Vida', 'Fix You', 'The Scientist'],
    'Imagine Dragons': ['Believer', 'Radioactive', 'Thunder', 'Demons'],
    'Adele': ['Someone Like You', 'Hello', 'Rolling in the Deep', 'Easy On Me']
}
    
    # Expand tracks for all artists
    for artist in artists:
        if artist not in tracks:
            tracks[artist] = [f'{artist} Song {i+1}' for i in range(4)]
    
    platforms = ['Desktop', 'Mobile', 'Web Player']
    
    data = []
    for _ in range(50000):  # Generate 50k records
        date = pd.Timestamp(np.random.choice(dates))
        artist = np.random.choice(artists, p=[0.15, 0.12, 0.10, 0.08, 0.07, 0.06, 0.05, 0.05, 0.05, 0.05, 0.04, 0.04, 0.04, 0.04, 0.06])
        track = np.random.choice(tracks[artist])
        platform = np.random.choice(platforms, p=[0.4, 0.45, 0.15])
        
        # More realistic listening patterns
        hour_weight = 1.0
        if 6 <= date.hour <= 9:  # Morning commute
            hour_weight = 1.5
        elif 17 <= date.hour <= 20:  # Evening commute
            hour_weight = 2.0
        elif 21 <= date.hour <= 23:  # Evening relaxation
            hour_weight = 1.8
        elif 0 <= date.hour <= 2:  # Late night
            hour_weight = 0.3
        
        if np.random.random() < hour_weight * 0.1:  # Skip some entries based on hour weight
            ms_played = np.random.normal(180000, 60000)  # ~3 minutes average
            ms_played = max(5000, min(300000, ms_played))  # Clamp between 5s and 5min
            
            skipped = ms_played < 30000 or np.random.random() < 0.15  # Skip if <30s or random
            
            data.append({
                'ts': date,
                'username': 'user123',
                'platform': platform,
                'ms_played': int(ms_played),
                'conn_country': 'US',
                'ip_addr_decrypted': '192.168.1.1',
                'user_agent_decrypted': 'Spotify/1.0',
                'master_metadata_track_name': track,
                'master_metadata_album_artist_name': artist,
                'master_metadata_album_album_name': f'{artist} Album',
                'episode_name': None,
                'episode_show_name': None,
                'spotify_episode_uri': None,
                'reason_start': np.random.choice(['trackdone', 'fwdbtn', 'playbtn']),
                'reason_end': np.random.choice(['trackdone', 'fwdbtn', 'backbtn', 'logout']),
                'shuffle': np.random.choice([True, False]),
                'skipped': skipped,
                'offline': False,
                'offline_timestamp': None,
                'incognito_mode': False
            })
    
    return pd.DataFrame(data)

def preprocess_data(df):
    """Preprocess the dataframe"""
    # Handle different column name variations
    if 'master_metadata_track_name' in df.columns:
        df['track_name'] = df['master_metadata_track_name']
    elif 'trackName' in df.columns:
        df['track_name'] = df['trackName']
    
    if 'master_metadata_album_artist_name' in df.columns:
        df['artist_name'] = df['master_metadata_album_artist_name']
    elif 'artistName' in df.columns:
        df['artist_name'] = df['artistName']
    
    if 'msPlayed' in df.columns:
        df['ms_played'] = df['msPlayed']
    
    # Convert timestamp
    if 'endTime' in df.columns:
        df['ts'] = pd.to_datetime(df['endTime'])
    else:
        df['ts'] = pd.to_datetime(df['ts'])
    
    # Add time-based columns
    df['date'] = df['ts'].dt.date
    df['hour'] = df['ts'].dt.hour
    df['month'] = df['ts'].dt.month
    df['weekday'] = df['ts'].dt.day_name()
    df['minutes_played'] = df['ms_played'] / 60000
    
    # Add skipped column if not present
    if 'skipped' not in df.columns:
        df['skipped'] = df['ms_played'] < 30000  # Less than 30 seconds considered skipped
    
    # Add platform column if not present
    if 'platform' not in df.columns:
        df['platform'] = 'Unknown'
    
    # Clean data
    df = df.dropna(subset=['track_name', 'artist_name'])
    df = df[df['ms_played'] > 0]
    
    return df

def generate_insights(df):
    """Generate personalized insights"""
    insights = []
    
    # Total listening time insight
    total_hours = df['minutes_played'].sum() / 60
    if total_hours > 1000:
        insights.append(f"🎧 You've listened to {total_hours:.0f} hours of music - that's equivalent to {total_hours/8:.0f} full workdays!")
    elif total_hours > 500:
        insights.append(f"🎵 With {total_hours:.0f} hours of listening, music is clearly a big part of your life!")
    
    # Top artist insight
    top_artist = df.groupby('artist_name')['minutes_played'].sum().idxmax()
    top_artist_hours = df.groupby('artist_name')['minutes_played'].sum().max() / 60
    insights.append(f"🌟 {top_artist} is your musical soulmate with {top_artist_hours:.0f} hours of listening time!")
    
    # Time pattern insight
    peak_hour = df.groupby('hour')['track_name'].count().idxmax()
    if 6 <= peak_hour <= 9:
        insights.append("☀️ You're a morning music lover - starting your day with the perfect soundtrack!")
    elif 17 <= peak_hour <= 20:
        insights.append("🌅 Evening is your prime music time - perfect for unwinding after a long day!")
    elif 21 <= peak_hour <= 23:
        insights.append("🌙 You're a night owl who finds comfort in late-night melodies!")
    
    # Skip rate insight
    skip_rate = (df['skipped'].sum() / len(df)) * 100
    if skip_rate < 15:
        insights.append("🎯 You're a patient listener with a low skip rate - you give songs a real chance!")
    elif skip_rate > 30:
        insights.append("⚡ You know what you want! Your high skip rate shows you're decisive about your music taste.")
    
    # Discovery insight
    unique_artists = df['artist_name'].nunique()
    if unique_artists > 200:
        insights.append(f"🌍 You're a musical explorer with {unique_artists} different artists in your library!")
    
    return insights

def create_mood_analysis(df):
    """Create a simple mood analysis based on listening patterns"""
    # This is a simplified version - in reality you'd use audio features from Spotify API
    mood_patterns = {
        'Energetic Morning': df[(df['hour'] >= 6) & (df['hour'] <= 9)]['track_name'].count(),
        'Focus Mode': df[(df['hour'] >= 10) & (df['hour'] <= 16)]['track_name'].count(),
        'Chill Evening': df[(df['hour'] >= 17) & (df['hour'] <= 20)]['track_name'].count(),
        'Late Night Vibes': df[(df['hour'] >= 21) | (df['hour'] <= 2)]['track_name'].count(),
    }
    
    return mood_patterns

# Main dashboard
def main():
     # Set Plotly dark theme
    pio.templates.default = "plotly_dark"
    
    # Header
    st.markdown('<h1 class="main-header"> Your Spotify Story</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">A journey through your musical universe</p>', unsafe_allow_html=True)
    
    # Data upload section at the top
    st.markdown("### 📊 Upload Your Spotify Data")
    uploaded_file = st.file_uploader("Choose your Spotify Extended Streaming History CSV file", type=['csv'])
    
    # Load data
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            df = preprocess_data(df)
            st.success("✅ Your data loaded successfully!")
        except Exception as e:
            st.error(f"Error loading file: {str(e)}")
            st.info("Using sample data for demonstration...")
            df = load_sample_data()
            df = preprocess_data(df)
    else:
        st.info("👆 Upload your Spotify data above, or explore with our sample data!")
        df = load_sample_data()
        df = preprocess_data(df)
    
    # Key metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    total_tracks = len(df)
    total_hours = df['minutes_played'].sum() / 60
    unique_artists = df['artist_name'].nunique()
    unique_tracks = df['track_name'].nunique()
    skip_rate = (df['skipped'].sum() / len(df)) * 100 if 'skipped' in df.columns else 0
    
    with col1:
        st.markdown(f"""
        <div class="metric-container">
            <h3>{total_tracks:,}</h3>
            <p>Tracks Played</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-container">
            <h3>{total_hours:.0f}h</h3>
            <p>Hours Listened</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-container">
            <h3>{unique_artists}</h3>
            <p>Artists Explored</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-container">
            <h3>{unique_tracks:,}</h3>
            <p>Unique Songs</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
        <div class="metric-container">
            <h3>{skip_rate:.1f}%</h3>
            <p>Skip Rate</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Mood Analysis Section
    st.markdown("""
    <div class="story-section">
        <h2>🎭 Your Musical Moods</h2>
        <p>Different times call for different vibes. Here's how your mood shifts throughout the day.</p>
    </div>
    """, unsafe_allow_html=True)
    
    mood_data = create_mood_analysis(df)
    col1, col2, col3, col4 = st.columns(4)
    
    mood_colors = ['#1a1a1a', '#1a1a1a', '#1a1a1a', '#1a1a1a']
    mood_borders = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4']
    for i, (mood, count) in enumerate(mood_data.items()):
        with [col1, col2, col3, col4][i]:
            st.markdown(f"""
            <div class="mood-indicator" style="border-top: 4px solid {mood_borders[i]};">
                <h4>{mood.upper()}</h4>
                <p>{count} Tracks</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Story Section 1: Musical Journey Over Time
    st.markdown("""
    <div class="story-section">
        <h2>📈 Your Musical Journey</h2>
        <p>Let's explore how your music taste evolved throughout the year. Notice the peaks and valleys - 
        they tell a story of your moods, seasons, and life moments.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Listening activity over time
    daily_activity = df.groupby('date').agg({
        'track_name': 'count',
        'minutes_played': 'sum'
    }).reset_index()
    daily_activity.columns = ['date', 'tracks_played', 'minutes_played']
    
    fig_timeline = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Daily Tracks Played', 'Daily Minutes Listened'),
        vertical_spacing=0.1
    )
    
    fig_timeline.add_trace(
        go.Scatter(
            x=daily_activity['date'],
            y=daily_activity['tracks_played'],
            mode='lines',
            fill='tonexty',
            name='Tracks',
            line=dict(color='#1DB954', width=2),
            fillcolor='rgba(29, 185, 84, 0.3)'
        ),
        row=1, col=1
    )
    
    fig_timeline.add_trace(
        go.Scatter(
            x=daily_activity['date'],
            y=daily_activity['minutes_played'],
            mode='lines',
            fill='tonexty',
            name='Minutes',
            line=dict(color='#1ed760', width=2),
            fillcolor='rgba(30, 215, 96, 0.3)'
        ),
        row=2, col=1
    )
    
    fig_timeline.update_layout(
        height=500,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    
    st.plotly_chart(fig_timeline, use_container_width=True)
    
    # Story Section 2: Your Musical DNA
    st.markdown("""
    <div class="story-section">
        <h2>🧬 Your Musical DNA</h2>
        <p>Every listener has a unique musical fingerprint. Here's yours - the artists and songs 
        that define your sonic identity.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top artists
        top_artists = df.groupby('artist_name')['minutes_played'].sum().sort_values(ascending=False).head(10)
        
        fig_artists = px.bar(
            x=top_artists.values,
            y=top_artists.index,
            orientation='h',
            title="🎤 Your Top Artists by Listening Time",
            color=top_artists.values,
            color_continuous_scale='Viridis'
        )
        
        fig_artists.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            coloraxis_showscale=False,
            height=400,
            yaxis={'categoryorder': 'total ascending'}
        )
        
        st.plotly_chart(fig_artists, use_container_width=True)
    
    with col2:
        # Top tracks
        top_tracks = df.groupby(['track_name', 'artist_name'])['minutes_played'].sum().sort_values(ascending=False).head(10)
        track_labels = [f"{track} - {artist}" for (track, artist) in top_tracks.index]
        
        fig_tracks = go.Figure(data=[
            go.Bar(
                y=track_labels,
                x=top_tracks.values,
                orientation='h',
                marker=dict(
                    color=top_tracks.values,
                    colorscale='Plasma'
                )
            )
        ])
        
        fig_tracks.update_layout(
            title="🎵 Your Most Played Tracks",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=400,
            yaxis={'categoryorder': 'total ascending'}
        )
        
        st.plotly_chart(fig_tracks, use_container_width=True)
    
    # Story Section 3: When Music Moves You
    st.markdown("""
    <div class="story-section">
        <h2>⏰ When Music Moves You</h2>
        <p>Music has its moments. Some songs are for morning coffee, others for late-night contemplation. 
        Let's discover your listening patterns.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Hourly listening pattern
        hourly_pattern = df.groupby('hour')['track_name'].count()
        
        fig_hourly = go.Figure()
        
        fig_hourly.add_trace(go.Scatterpolar(
            r=hourly_pattern.values,
            theta=[f"{h:02d}:00" for h in hourly_pattern.index],
            fill='toself',
            fillcolor='rgba(29, 185, 84, 0.3)',
            line=dict(color='#1DB954', width=2),
            name='Listening Activity'
        ))
        
        fig_hourly.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, max(hourly_pattern.values)]),
                bgcolor="rgba(0,0,0,0)"
            ),
            title="🕐 Your 24-Hour Listening Clock",
            font=dict(color='white'),
            paper_bgcolor='rgba(0,0,0,0)',
            height=400
        )
        
        st.plotly_chart(fig_hourly, use_container_width=True)
    
    with col2:
        # Weekly pattern
        weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekly_pattern = df.groupby('weekday')['track_name'].count().reindex(weekday_order)
        
        fig_weekly = px.line_polar(
            r=weekly_pattern.values,
            theta=weekly_pattern.index,
            line_close=True,
            title="📅 Your Weekly Rhythm"
        )
        
        fig_weekly.update_traces(
            fill='toself',
            fillcolor='rgba(30, 215, 96, 0.3)',
            line=dict(color='#1ed760', width=3)
        )
        
        fig_weekly.update_layout(
            polar=dict(bgcolor="rgba(0,0,0,0)"),
            font=dict(color='white'),
            paper_bgcolor='rgba(0,0,0,0)',
            height=400
        )
        
        st.plotly_chart(fig_weekly, use_container_width=True)
    
    # Story Section 4: The Skip Chronicles
    if 'skipped' in df.columns:
        st.markdown("""
        <div class="story-section">
            <h2>⏭️ The Skip Chronicles</h2>
            <p>Not every song captures us immediately. Your skipping behavior reveals as much about your taste 
            as your favorite tracks do.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Skip rate by artist (for artists with at least 10 plays)
            skip_by_artist = df.groupby('artist_name').agg({
                'skipped': ['mean', 'count']
            }).reset_index()
            skip_by_artist.columns = ['artist_name', 'skip_rate', 'play_count']
            skip_by_artist = skip_by_artist[skip_by_artist['play_count'] >= 10]
            skip_by_artist = skip_by_artist.sort_values('skip_rate').head(10)
            
            fig_skip = px.bar(
                skip_by_artist,
                x='skip_rate',
                y='artist_name',
                orientation='h',
                title="🎯 Artists You Never Skip",
                color='skip_rate',
                color_continuous_scale='tealgrn'
            )
            
            fig_skip.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                coloraxis_showscale=False,
                height=400,
                yaxis={'categoryorder': 'total ascending'}
            )
            
            st.plotly_chart(fig_skip, use_container_width=True)
        
        with col2:
            # Listening completion by hour
            completion_by_hour = df.groupby('hour').agg({
                'skipped': lambda x: 1 - x.mean()
            }).reset_index()
            
            fig_completion = px.bar(
                completion_by_hour,
                x='hour',
                y='skipped',
                title="🎧 Attention Span Throughout the Day",
                color='skipped',
                color_continuous_scale='Viridis'
            )
            
            fig_completion.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                coloraxis_showscale=False,
                height=400,
                xaxis_title="Hour of Day",
                yaxis_title="Completion Rate"
            )
            
            st.plotly_chart(fig_completion, use_container_width=True)
    
    # Story Section 5: Platform Preferences
    if 'platform' in df.columns and df['platform'].nunique() > 1:
        st.markdown("""
        <div class="story-section">
            <h2>📱 Your Digital Music Journey</h2>
            <p>From your phone to your desktop, each platform tells a different part of your musical story.</p>
        </div>
        """, unsafe_allow_html=True)
        
        platform_stats = df.groupby('platform').agg({
            'track_name': 'count',
            'minutes_played': 'sum',
            'skipped': 'mean' if 'skipped' in df.columns else lambda x: 0
        }).reset_index()
        
        fig_platforms = make_subplots(
            rows=1, cols=3,
            subplot_titles=('Tracks Played', 'Minutes Listened', 'Skip Rate'),
            specs=[[{"type": "pie"}, {"type": "pie"}, {"type": "pie"}]]
        )
        
        fig_platforms.add_trace(
            go.Pie(
                labels=platform_stats['platform'],
                values=platform_stats['track_name'],
                name="Tracks"
            ),
            row=1, col=1
        )
        
        fig_platforms.add_trace(
            go.Pie(
                labels=platform_stats['platform'],
                values=platform_stats['minutes_played'],
                name="Minutes"
            ),
            row=1, col=2
        )
        
        if 'skipped' in df.columns:
            fig_platforms.add_trace(
                go.Pie(
                    labels=platform_stats['platform'],
                    values=platform_stats['skipped'],
                    name="Skip Rate"
                ),
                row=1, col=3
            )
        
        fig_platforms.update_traces(
            hole=0.4,
            hoverinfo="label+percent+name",
            textinfo="label+percent"
        )
        
        fig_platforms.update_layout(
            height=400,
            font=dict(color='white'),
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False
        )
        
        st.plotly_chart(fig_platforms, use_container_width=True)
    
    # Monthly listening trends
    st.markdown("""
    <div class="story-section">
        <h2>📅 Seasonal Soundtrack</h2>
        <p>Your music taste changes with the seasons. See how your listening habits flow throughout the year.</p>
    </div>
    """, unsafe_allow_html=True)
    
    monthly_stats = df.groupby('month').agg({
        'track_name': 'count',
        'minutes_played': 'sum',
        'artist_name': 'nunique'
    }).reset_index()
    
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    monthly_stats['month_name'] = [month_names[i-1] for i in monthly_stats['month']]
    
    fig_monthly = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Monthly Listening Activity', 'Artist Discovery by Month')
    )
    
    fig_monthly.add_trace(
        go.Scatter(
            x=monthly_stats['month_name'],
            y=monthly_stats['minutes_played'],
            mode='lines+markers',
            name='Minutes',
            line=dict(color='#1DB954', width=3),
            marker=dict(size=8)
        ),
        row=1, col=1
    )
    
    fig_monthly.add_trace(
        go.Bar(
            x=monthly_stats['month_name'],
            y=monthly_stats['artist_name'],
            name='Unique Artists',
            marker_color='#1ed760'
        ),
        row=1, col=2
    )
    
    fig_monthly.update_layout(
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        showlegend=False
    )
    
    st.plotly_chart(fig_monthly, use_container_width=True)
    
    # Listening streaks and habits
    st.markdown("""
    <div class="story-section">
        <h2>🔥 Your Listening Streaks</h2>
        <p>Consistency tells a story. Here are your most dedicated listening periods and habits.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Calculate listening streaks
    df_sorted = df.sort_values('ts')
    df_sorted['date'] = pd.to_datetime(df_sorted['date'])
    daily_listening = df_sorted.groupby('date')['track_name'].count().reset_index()
    daily_listening = daily_listening.sort_values('date')
    
    # Find longest streak
    daily_listening['prev_date'] = daily_listening['date'].shift(1)
    daily_listening['days_diff'] = (daily_listening['date'] - daily_listening['prev_date']).dt.days
    daily_listening['is_consecutive'] = daily_listening['days_diff'] == 1
    
    streaks = []
    current_streak = 1
    for i, row in daily_listening.iterrows():
        if row['is_consecutive']:
            current_streak += 1
        else:
            if current_streak > 1:
                streaks.append(current_streak)
            current_streak = 1
    if current_streak > 1:
        streaks.append(current_streak)
    
    longest_streak = max(streaks) if streaks else 1
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-container">
            <h3>{longest_streak}</h3>
            <p>Longest Streak (days)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        avg_daily_tracks = df.groupby('date')['track_name'].count().mean()
        st.markdown(f"""
        <div class="metric-container">
            <h3>{avg_daily_tracks:.0f}</h3>
            <p>Avg Daily Tracks</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        most_active_day = df.groupby('date')['track_name'].count().idxmax()
        most_active_count = df.groupby('date')['track_name'].count().max()
        st.markdown(f"""
        <div class="metric-container">
            <h3>{most_active_count}</h3>
            <p>Best Day ({most_active_day})</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Top songs by different time periods
    st.markdown("""
    <div class="story-section">
        <h2>🎯 Your Anthems Through Time</h2>
        <p>Some songs define moments, others define months. Here are your top tracks across different time periods.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for different time periods
    tab1, tab2, tab3, tab4 = st.tabs(["🌅 Morning Hits", "🏢 Workday Favorites", "🌆 Evening Chill", "🌙 Night Vibes"])
    
    with tab1:
        morning_tracks = df[(df['hour'] >= 6) & (df['hour'] <= 11)]
        if not morning_tracks.empty:
            morning_top = morning_tracks.groupby(['track_name', 'artist_name'])['track_name'].count().sort_values(ascending=False).head(10)
            morning_df = pd.DataFrame({
                'Track': [f"{track} - {artist}" for (track, artist) in morning_top.index],
                'Plays': morning_top.values
            })
            
            fig_morning = px.bar(morning_df, x='Plays', y='Track', orientation='h',
                               title="Your Morning Soundtrack", color='Plays',
                               color_continuous_scale='sunsetdark')
            fig_morning.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                coloraxis_showscale=False,
                yaxis={'categoryorder': 'total ascending'}
            )
            st.plotly_chart(fig_morning, use_container_width=True)
        else:
            st.info("No morning listening data available.")
    
    with tab2:
        work_tracks = df[(df['hour'] >= 9) & (df['hour'] <= 17)]
        if not work_tracks.empty:
            work_top = work_tracks.groupby(['track_name', 'artist_name'])['track_name'].count().sort_values(ascending=False).head(10)
            work_df = pd.DataFrame({
                'Track': [f"{track} - {artist}" for (track, artist) in work_top.index],
                'Plays': work_top.values
            })
            
            fig_work = px.bar(work_df, x='Plays', y='Track', orientation='h',
                            title="Your Focus & Flow Playlist", color='Plays',
                            color_continuous_scale='viridis')
            fig_work.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                coloraxis_showscale=False,
                yaxis={'categoryorder': 'total ascending'}
            )
            st.plotly_chart(fig_work, use_container_width=True)
        else:
            st.info("No workday listening data available.")
    
    with tab3:
        evening_tracks = df[(df['hour'] >= 17) & (df['hour'] <= 21)]
        if not evening_tracks.empty:
            evening_top = evening_tracks.groupby(['track_name', 'artist_name'])['track_name'].count().sort_values(ascending=False).head(10)
            evening_df = pd.DataFrame({
                'Track': [f"{track} - {artist}" for (track, artist) in evening_top.index],
                'Plays': evening_top.values
            })
            
            fig_evening = px.bar(evening_df, x='Plays', y='Track', orientation='h',
                               title="Your Evening Wind-Down", color='Plays',
                               color_continuous_scale='sunset')
            fig_evening.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                coloraxis_showscale=False,
                yaxis={'categoryorder': 'total ascending'}
            )
            st.plotly_chart(fig_evening, use_container_width=True)
        else:
            st.info("No evening listening data available.")
    
    with tab4:
        night_tracks = df[(df['hour'] >= 22) | (df['hour'] <= 5)]
        if not night_tracks.empty:
            night_top = night_tracks.groupby(['track_name', 'artist_name'])['track_name'].count().sort_values(ascending=False).head(10)
            night_df = pd.DataFrame({
                'Track': [f"{track} - {artist}" for (track, artist) in night_top.index],
                'Plays': night_top.values
            })
            
            fig_night = px.bar(night_df, x='Plays', y='Track', orientation='h',
                             title="Your Late Night Sessions", color='Plays',
                             color_continuous_scale='blues')
            fig_night.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                coloraxis_showscale=False,
                yaxis={'categoryorder': 'total ascending'}
            )
            st.plotly_chart(fig_night, use_container_width=True)
        else:
            st.info("No late night listening data available.")
    
    # Artist loyalty analysis
    st.markdown("""
    <div class="story-section">
        <h2>💖 Artist Loyalty Index</h2>
        <p>Some artists capture your heart for a moment, others for a lifetime. Here's your loyalty breakdown.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Calculate artist loyalty metrics
    artist_stats = df.groupby('artist_name').agg({
        'track_name': ['count', 'nunique'],
        'minutes_played': 'sum',
        'date': lambda x: (x.max() - x.min()).days + 1  # listening span
    }).reset_index()
    
    artist_stats.columns = ['artist_name', 'total_plays', 'unique_tracks', 'total_minutes', 'listening_span']
    artist_stats['avg_plays_per_track'] = artist_stats['total_plays'] / artist_stats['unique_tracks']
    artist_stats['loyalty_score'] = (artist_stats['total_minutes'] * artist_stats['listening_span']) / 1000
    
    # Filter for artists with significant listening
    significant_artists = artist_stats[artist_stats['total_plays'] >= 10].sort_values('loyalty_score', ascending=False).head(15)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_loyalty = px.scatter(
            significant_artists,
            x='listening_span',
            y='total_minutes',
            size='unique_tracks',
            color='loyalty_score',
            hover_data=['artist_name'],
            title="Artist Loyalty: Span vs Time",
            color_continuous_scale='Plasma'
        )
        
        fig_loyalty.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis_title="Days Listening Span",
            yaxis_title="Total Minutes"
        )
        
        st.plotly_chart(fig_loyalty, use_container_width=True)
    
    with col2:
        # Top loyal artists
        loyal_artists = significant_artists.head(10)
        
        fig_loyal_bar = px.bar(
            loyal_artists,
            x='loyalty_score',
            y='artist_name',
            orientation='h',
            title="🏆 Your Most Loyal Artist Relationships",
            color='loyalty_score',
            color_continuous_scale='Reds'
        )
        
        fig_loyal_bar.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            coloraxis_showscale=False,
            yaxis={'categoryorder': 'total ascending'}
        )
        
        st.plotly_chart(fig_loyal_bar, use_container_width=True)
    
    # Generate and display insights
    insights = generate_insights(df)
    
    if insights:
        st.markdown(f"""
        <div class="insight-box">
            <h3>🎯 Your Personalized Musical Insights</h3>
            <ul>
                {"".join([f"<li>{insight}</li>" for insight in insights])}
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Summary statistics
    st.markdown("---")
    st.markdown("### 📊 Quick Stats Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_session = df.groupby('date')['minutes_played'].sum().mean()
        st.metric("Avg Daily Session", f"{avg_session:.0f} min")
    
    with col2:
        most_played_artist = df['artist_name'].mode().iloc[0] if not df['artist_name'].mode().empty else "N/A"
        st.metric("Most Frequent Artist", most_played_artist)
    
    with col3:
        weekend_vs_weekday = df[df['weekday'].isin(['Saturday', 'Sunday'])]['minutes_played'].sum() / df['minutes_played'].sum()
        st.metric("Weekend Listening %", f"{weekend_vs_weekday*100:.1f}%")
    
    with col4:
        peak_month = df.groupby('month')['minutes_played'].sum().idxmax()
        month_names = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun',
                      7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}
        st.metric("Peak Month", month_names.get(peak_month, "N/A"))
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-style: italic; margin-top: 2rem;">
        <p>Made for Alejandro Acosta with kaggle datasets</p>
        <p>Your data stays private and is processed locally</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()