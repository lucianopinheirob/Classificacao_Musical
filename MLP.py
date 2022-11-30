# Luciano Pinheiro Batista

# Acurácia da rede MLP, Matriz de Confusão, e Desempenho da rede junto aos álbums selecionados. 

import numpy as np
from sklearn.preprocessing import normalize
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from Analise_Tracks_Superv_Testes import Albums

def Multilayer(X_Train, Y_Train):
    
    MLP = MLPClassifier(hidden_layer_sizes = (100, 100),
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
    print(confusion_matrix(Y_Test, Preds))
    print(accuracy_score(Y_Test, Preds))

def Predictions_Albums(MLP, Atributos_Album_Teste, Labels_Album_Teste):

    Preds = MLP.predict(Atributos_Album_Teste)
    for Label, Pred in zip(Labels_Album_Teste, Preds):
        print(Label, Pred)

def main():
    
    try:
        Atributos = np.genfromtxt('Atributos.csv', delimiter=',')
        Labels = np.genfromtxt('Labels.csv', delimiter=',')
        
    except:
        print("Aquisição dos dados de treinamento ainda não foi realizada!")
        return None
    
    Atributos = normalize(Atributos, norm='max', axis=1)
    X_Train, X_Test, Y_Train, Y_Test = train_test_split(Atributos, Labels, test_size=0.33, random_state=None)
    MLP = Multilayer(X_Train, Y_Train)
    Predictions(MLP, X_Test, Y_Test)
    
    for Value in Albums.values():
        try:
            Atributos_Album_Teste = np.genfromtxt(f'Teste_{Value[1]}.csv', delimiter=',')
            Labels_Album_Teste = np.genfromtxt(f'Labels_{Value[1]}.csv', delimiter=',')
            Atributos_Album_Teste = normalize(Atributos_Album_Teste, norm='max', axis=1)
        except:
            print("Aquisição dos dados de teste ainda não foi realizada!")
            return

        Predictions_Albums(MLP, Atributos_Album_Teste, Labels_Album_Teste)


if __name__ == '__main__':
    main()

