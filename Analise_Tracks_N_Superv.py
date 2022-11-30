# Luciano Pinheiro Batista

# Aquisição de atributos das músicas para clusterização

from __future__ import print_function    # (at top of module)
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import numpy as np
import os

os.environ['SPOTIPY_CLIENT_ID'] = 'cdf39b5c3fe34a8ca659e21f96100b9f'
os.environ['SPOTIPY_CLIENT_SECRET'] = '497310228ce341bea13bff8c213f08f7'
os.environ['SPOTIPY_REDIRECT_URI'] = 'https://localhost:8888/callback'

generos =  {'Sad': 0,
            'Happy': 1,
            }

playlists = {}

def Pega_Playlists(sp):
    
    for genero in generos.keys():
        results = sp.search(genero, type='playlist', limit = 1)
        for result in results['playlists']['items']:
            playlists[result['id']] = generos[genero]

def Pega_Tracks(pl_id, sp):
    
    offset = 0
    Tracks = []

    while True:
        response = sp.playlist_items(pl_id,
                                 offset=offset,
                                 fields='items.track.id,total',
                                 additional_types=['track'])
    
        for i in range(len(response['items'])):
            Tracks.append(response['items'][i]['track']['id'])

        offset = offset + len(response['items'])

        print(offset)
        
        if len(response['items']) == 0 or offset >= 50:
            break 

        
    
    return Tracks

def Pega_Atributos(Track, sp):
    Analysis = sp.audio_analysis(Track)
    Duration = [Analysis['track']['duration']]
    Loudness = [Analysis['track']['loudness']]
    Tempo = [Analysis['track']['tempo']]
    Time_Signature = [Analysis['track']['time_signature']]
    Key = [Analysis['track']['key']]
    Mean_Tatum_Duration = np.sum([Tatum['duration'] for Tatum in Analysis['tatums']]) / len(Analysis['tatums'])
    Mean_Segment_Duration = np.sum([Segment['duration'] for Segment in Analysis['segments']]) / len(Analysis['segments'])
    Mean_Bar_Duration = np.sum([Bar['duration'] for Bar in Analysis['bars']]) / len(Analysis['bars'])
    Mean_Section_Duration = np.sum([Section['duration'] for Section in Analysis['sections']]) / len(Analysis['sections'])
    Mean_Beat_Duration = np.sum([Beat['duration'] for Beat in Analysis['beats']]) / len(Analysis['beats'])
    Mean_Timbre = np.sum([Segments['timbre'] for Segments in Analysis['segments']], axis=0) / len(Analysis['segments'])
    Mean_Pitches = np.sum([Segments['pitches'] for Segments in Analysis['segments']], axis=0) / len(Analysis['segments'])

    print("Track id:", Track)

    Atributos = np.concatenate((Duration,
                            Loudness,
                            Tempo,
                            Time_Signature,
                            Key,
                            Mean_Tatum_Duration,
                            Mean_Segment_Duration,
                            Mean_Bar_Duration,
                            Mean_Section_Duration,
                            Mean_Beat_Duration,
                            Mean_Timbre,
                            Mean_Pitches), axis = None)
        
    return Atributos

def Salva_Atributos(sp):
    Tracks = []
    Labels = []
    for playlist in playlists.keys():
        New_Tracks = Pega_Tracks(playlist, sp)
        Tracks += New_Tracks
        for Track in New_Tracks: 
            Labels.append(playlists[playlist])
    Atributos = [Pega_Atributos(Track, sp) for Track in Tracks]
    print(len(Atributos))
    print(len(Labels))
    np.savetxt("Atributos.csv", Atributos, delimiter=",")
    np.savetxt("Labels.csv", Labels, delimiter=",")

def main():
    client_credentials_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    Pega_Playlists(sp)
    print(playlists.keys())
    Salva_Atributos(sp)

if __name__ == '__main__':

    main()