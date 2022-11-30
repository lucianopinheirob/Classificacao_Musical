# Luciano Pinheiro Batista

# Aquisição de atributos das músicas para teste da rede MLP.

from __future__ import print_function
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import numpy as np
import os

os.environ['SPOTIPY_CLIENT_ID'] = 'cdf39b5c3fe34a8ca659e21f96100b9f'
os.environ['SPOTIPY_CLIENT_SECRET'] = '497310228ce341bea13bff8c213f08f7'
os.environ['SPOTIPY_REDIRECT_URI'] = 'https://localhost:8888/callback'

Albums = {'7aNclGRxTysfh6z0d8671k': (0, 'Techno'),
          '2mBbV0Ad6B4ydHMZlzAY7S': (1, 'Reggae'),
          '4fN80AnER7ua5DH8U1A7k9': (2, 'Samba'),
          '6ggO3YVhyonYuFWUPBRyIv': (3, 'Punk'),
          '2Lq2qX3hYhiuPckC8Flj21': (4, 'Metal'),
          '3RePY8Fh1liHgQQ2X8CjYH': (5, 'Classical')}


def Pega_Tracks(album_id, sp):
    
    Tracks = []
    Album_Tracks = sp.album_tracks(album_id, limit=50, offset=0, market=None)
    
    for Album_Track in Album_Tracks['items']:
        Tracks.append(Album_Track['id'])
    
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

def Salva_Atributos(Album_id, sp):
    Tracks = Pega_Tracks(Album_id, sp)
    Atributos = [Pega_Atributos(Track, sp) for Track in Tracks]
    Labels = len(Tracks)*[Albums[Album_id][0]]
    np.savetxt(f"Teste_{Albums[Album_id][1]}.csv", Atributos, delimiter=",")
    np.savetxt(f"Labels_{Albums[Album_id][1]}.csv", Labels, delimiter=",")
    
def main():
    client_credentials_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    for Album_id in Albums.keys():
        Salva_Atributos(Album_id, sp)

if __name__ == '__main__':
    main()

## Nome dos Álbums selecionados:

#Clássica Nocturne Vol. 1 '3RePY8Fh1liHgQQ2X8CjYH'
#Metal Master of Puppets '2Lq2qX3hYhiuPckC8Flj21'
#Punk Never Mind The Bollocks '6ggO3YVhyonYuFWUPBRyIv'
#Samba Cartola (1976) '7x7UYZtatkx5fnqBOhmx1b'
#Reggae Exodus '2mBbV0Ad6B4ydHMZlzAY7S'
#Eletronica Selected Ambients Works 85-92 '7aNclGRxTysfh6z0d8671k'