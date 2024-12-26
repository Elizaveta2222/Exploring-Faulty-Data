import pandas as pd
from Implication import Implication
from ExpFaultyData_5 import ExpFaultyData

def main():
    context_df = pd.read_csv('example.csv',sep=';')
    context_K = [context_df.values.tolist(),context_df.shape]
    context_df_expert = pd.read_csv('example_expert.csv',sep=';')
    context_expert = [context_df_expert.values.tolist(),context_df_expert.shape]
    # Достоверность
    c = 0.5

    M=list(range(0,context_K[1][1]))
    Th_c_K = {Implication({0}, {3}), #hair -> milk
              Implication({0}, {4}), #hair -> predator
              Implication({0}, {5}), #hair -> breathes
            #   Implication({0}, {6}), #hair -> mammal
              Implication({1}, {2}), #feathers -> eggs
              Implication({1}, {4}), #feathers -> predator
              Implication({1}, {5}), #feathers -> breathes
            #   Implication({1}, {8}), #feathers -> bird
              Implication({2}, {4}), #eggs -> predator
            #   Implication({2}, {7}), #eggs -> fish
              Implication({3}, {0}), #milk -> hair
              Implication({3}, {4}), #milk -> predator
              Implication({3}, {5}), #milk -> breathes
            #   Implication({3}, {0}), #milk -> mammal
              Implication({4}, {0}), #predator -> hair
              Implication({4}, {2}), #predator -> eggs
              Implication({4}, {3}), #predator -> milk
              Implication({4}, {5}), #predator -> breathes
            #   Implication({4}, {6}), #predator -> mammal
              Implication({5}, {0}), #breathes -> hair
              Implication({5}, {3}), #breathes -> milk
              Implication({5}, {4}), #breathes -> predator
            #   Implication({5}, {6}), #breathes -> mammal
            #   Implication({6}, {0}), #mammal -> hair
            #   Implication({6}, {3}), #mammal -> milk
            #   Implication({6}, {4}), #mammal -> predator
            #   Implication({6}, {5}), #mammal -> breathes
            #   Implication({7}, {2}), #fish -> eggs
            #   Implication({7}, {4}), #fish -> predator
            #   Implication({8}, {1}), #bird -> feathers
            #   Implication({8}, {2}), #bird -> eggs
            #   Implication({8}, {4}), #bird -> predator
            #   Implication({8}, {5}), #bird -> breathes
              }
    K = {Implication({1}, {2})}

    exploration = ExpFaultyData.ExploringFaultyData(K, Th_c_K, M, context_K, context_expert, context_df, c)

if  __name__ == "__main__":
    main()
