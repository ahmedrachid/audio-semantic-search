from panns_inference import AudioTagging
from pedalboard.io import AudioFile
import streamlit as st
import torch
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from IPython.display import Audio as player
from audio_recorder_streamlit import audio_recorder
from scipy.io import wavfile
import io
import librosa

engine = create_engine('postgresql://gpadmin:Ahmed0409@34.163.202.105:5432/demo_gpdb')

def find_similar_audios(vector, limit):
    query = """SELECT name, artist, audio, genre
                FROM public.audio 
                 ORDER BY panns_embeddings <-> '{vector}'  LIMIT {limit};""".format(vector=vector, limit=limit)

    r=pd.read_sql_query(query, con = engine)
    r=r.to_dict(orient='records')

    return r

st.sidebar.image("gp_icon.png")

st.title("♫⋆Music Recommendation App ♫⋆")

# st.sidebar.header("About")
st.sidebar.markdown("""
    <div style="font-size: medium; font-style: italic">
    This is a  <b>Music Recommendation Application</b> leveraging <font color="green"> VMware Greenplum</font> as a Vector Database thanks to and <font color="blue"> pgvector extension </font> for AI-powered Search.<br><br><br>
    </div>
    """, unsafe_allow_html=True)

limit = st.sidebar.slider('Number of musics to recommend', 1, 10, 3)
mp3_or_audio = st.sidebar.radio(
        "MP3 or Recording 👉",
        options=["MP3", "Recording"],
    )
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
at = AudioTagging(checkpoint_path=None, device=device)

if mp3_or_audio == "MP3":
    st.markdown("Upload your favorite songs and get a list of recommendations from our database of music.")



    music_file = st.file_uploader(label="📀 Music file 🎸", )
    st.write("")

    if music_file:
        st.audio(music_file)
        with AudioFile(music_file) as f:
            a_song = f.read(f.frames)[0][None, :]
        clip, emb = at.inference(a_song)

        st.subheader('Audio Semantic Search', divider='rainbow')
        results = find_similar_audios(vector = list(emb[0]), limit = limit)
        for result in results:
            st.markdown(f"*Song*: {result['name']}")
            st.markdown(f"*Artist*: {result['artist']}")
            st.caption(f"Genre: {result['genre']}")
            st.audio(np.array(result['audio']), sample_rate=44100)
            st.divider()
            #st.audio(result.payload["urls"])

else:
    st.markdown("Record your favorite songs and get a list of recommendations from our database of music.")
    st.write("")
    audio_bytes = audio_recorder(text="",
                            recording_color="#e82c2c",
                            neutral_color="#243682",
                            icon_name="music",
                            icon_size="4x",
                                 )
    if audio_bytes:
        st.audio(audio_bytes, format="audio/wav")
        (audio, _) = librosa.core.load(io.BytesIO(audio_bytes), sr=44100, mono=True)
        audio = audio[None, :]  # (batch_size, segment_samples)
        clip, emb = at.inference(audio)

        st.subheader('Audio Semantic Search', divider='rainbow')
        results = find_similar_audios(vector = list(emb[0]), limit = limit)
        for result in results:
            st.markdown(f"*Song*: {result['name']}")
            st.markdown(f"*Artist*: {result['artist']}")
            st.caption(f"Genre: {result['genre']}")
            st.audio(np.array(result['audio']), sample_rate=44100)
            st.divider()