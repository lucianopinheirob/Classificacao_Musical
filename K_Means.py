
# Luciano Pinheiro Batista

# Plota o gráfico de Silhouette Score por número de clusters. 

import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.decomposition import PCA
from sklearn.preprocessing import normalize
from sklearn.metrics import silhouette_score




def K_Means_Cluster(Atributos, k):
    
    K_Means = KMeans(n_clusters=k)
    K_Means.fit(Atributos)
    Clusters = K_Means.fit_predict(Atributos)
    if (k == 2):
        Cluster_0 = Clusters[0:190]
        Cluster_1 = Clusters[190:389]
        taxa1 = np.sum(np.equal(Cluster_0, 0)) / len(Cluster_0)
        taxa2 = np.sum(np.equal(Cluster_1, 1)) / len(Cluster_1)
        print(taxa1)
        print(taxa2)
        print(Clusters)
    
    return silhouette_score(Atributos, Clusters)

def Plot(Silhouette_Scores, Ks):
    fig, ax = plt.subplots()
    ax.scatter(Ks, Silhouette_Scores)
    ax.set_xlabel('Número de Clusters')
    ax.set_ylabel('Silhouette Scores')
    ax.set_xticks(Ks)
    plt.show()

def main():
    
    Atributos = np.genfromtxt('Atributos.csv', delimiter=',')
    Atributos = normalize(Atributos, norm='max', axis=1)
    
    Ks = [2, 3, 4, 5, 6, 7, 8]
    Silhouette_Scores = [K_Means_Cluster(Atributos, k) for k in Ks]
    
    Plot(Silhouette_Scores, Ks)


if __name__ == '__main__':
    main()

