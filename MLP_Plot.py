# Luciano Pinheiro Batista

# Plota o gráfico de Acurácia por número de neurônios. 

import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import normalize
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from Analise_Tracks_Superv_Testes import Albums

def Multilayer(X_Train, Y_Train, neuronio):
    
    MLP = MLPClassifier(hidden_layer_sizes = (neuronio, neuronio),
                        max_iter = 500,
                        tol = 0.001,
                        learning_rate_init = .01,
                        solver = "sgd",
                        activation = "tanh",
                        learning_rate = "constant",
                        verbose = 1
                        )

    MLP.fit(X_Train, Y_Train) 

    return MLP

def Predictions(MLP, X_Test, Y_Test):

    Preds = MLP.predict(X_Test)
    return accuracy_score(Y_Test, Preds)

def Plot(Neuronios, Accs):
    fig, ax = plt.subplots()
    ax.scatter(Neuronios, Accs)
    ax.set_xlabel('Número de Neurônios')
    ax.set_ylabel('Acurácia')
    ax.set_xticks(Neuronios)
    plt.show()

def main():
    try:
        Atributos = np.genfromtxt('Atributos.csv', delimiter=',')
        Labels = np.genfromtxt('Labels.csv', delimiter=',')
    except:
        print("Aquisição dos dados de treinamento ainda não foi realizada!")
        return None
    
    Atributos = normalize(Atributos, norm='max', axis=1)
    X_Train, X_Test, Y_Train, Y_Test = train_test_split(Atributos, Labels, test_size=0.33, random_state=None)
    
    Neuronios = np.arange(2, 25, 2)
    Accs = []

    for Neuronio in Neuronios:
        MLP = Multilayer(X_Train, Y_Train, Neuronio)
        Accs.append(Predictions(MLP, X_Test, Y_Test))

    Plot(Neuronios, Accs)
    
if __name__ == '__main__':
    main()

