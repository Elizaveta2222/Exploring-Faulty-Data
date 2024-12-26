# import pandas as pd
import copy

from Implication import Implication

class ExpFaultyData:
    def ClosureOnImp(A,L):
        Li=L.copy()
        while True:
            stable=True   
            Lj=Li.copy()
            for i in Lj:
                if (i.premise.issubset(A)):
                    A.update(i.consequent)
                    stable=False
                    Li.difference_update(set([i]))
            if stable==True:
                break
        return A

    def ClosureOnContext(A,context):
        A = Implication.Galois(A,context,'AttributesToObjects')
        A = Implication.Galois(A,context,'ObjectsToAttributes')
        return A
    
    def SmallestSet (A,M,Ki,context_KLi):
        for m in list(reversed(M)):
            if m in A:
                A.difference_update(set([m]))
            else:           
                A_temp=A.copy()
                A_temp.update(set([m]))
                B=ExpFaultyData.ClosureOnImp(A_temp,Ki)
                B_diff=B.copy()
                B_diff.difference_update(A)  
                B_L=B.copy()
                if all(i>=m for i in B_diff) and (B != ExpFaultyData.ClosureOnContext(B_L, context_KLi)):
                    return B
        return -1
    
    def FindConfidence(imp, context):
        galois_PC = Implication.Galois(set.union(imp.premise, imp.consequent), context, 'AttributesToObjects')
        galois_C = Implication.Galois(imp.premise, context, 'AttributesToObjects')
        return len(galois_PC)/len(galois_C)
        
    def SmallestIntent (P, M, context_KLi, context_Li, Ki, context_K, l, c):
        for m in list(reversed(M)):
            if m in P:
                P.difference_update(set([m]))
            else:
                P_temp=copy.deepcopy(P)
                P_temp.update(set([m]))
                B=ExpFaultyData.ClosureOnContext(P_temp,context_KLi)
                B_diff=copy.deepcopy(B)
                B_diff.difference_update(P)  

                B_L=copy.deepcopy(B)
                if (context_Li[0] == []):
                    B_L = set()
                else:
                    ExpFaultyData.ClosureOnContext(B_L, context_Li)

                B_K = copy.deepcopy(B)
                ExpFaultyData.ClosureOnImp(B_K, Ki)

                B_L_K_diff = B_L.difference(B_K)

                exist = False

                for m in B_L_K_diff:
                    if ExpFaultyData.FindConfidence(Implication(B, {m}), context_K) >= c :
                        l == m
                        exist = True
                        break

                if all(i>=m for i in B_diff) and exist:
                    return B
        return -1
    
    def expert_p(imp, context, M):
        AI =  Implication.Galois(imp.premise, context, 'AttributesToObjects')
        BI = Implication.Galois(imp.consequent, context, 'AttributesToObjects')
        # Является ли AI подмножеством BI
        if (AI.issubset(BI)) :
            return False
        else :
            AI.difference_update(BI)
            return context[0][AI.pop()]
        
    def DeleteFalseImplications(L, C) :
        ex = Implication.example_to_column_nums(C)
        L_updated = L.copy()
        for i in L :
            if not (not i.premise.issubset(ex) or i.consequent.issubset(ex)) :
                L_updated.remove(i)
        return L_updated
    
    def LecticalComparison(P1, P2):
        i = 0
        P1 = list(P1)
        P2 = list(P2)
        l_P1 = len(P1)
        l_P2 = len(P2)
        if (l_P1 > l_P2):
            max = l_P2
        else:
            max = l_P1
        while (max > i+1 and P1[i] == P2[i]):
            i = i+1

        if (P1[i] < P2[i]):
            return True
        if (P1[i] > P2[i]):
            return False
        
        if (l_P1 < l_P2):
            return True
        else:
            return False


    
    def ExploringFaultyData(K, Th_c_K, M, context_K, context_expert, context_df, c):
        print('Значение M - ' + str(M))
        print('Значение K - ' + str(K))
        print('Значение Th_c_K - ' + str(Th_c_K))
        # i
        i = 0
        Pi = ExpFaultyData.ClosureOnImp(set(), K)
        print('Значение Pi - ' + str(Pi))
        Ki = K
        Li = Th_c_K
        colums = len(M)
        rows = 0
        context_Li = [[],(rows,colums)]
        print('Контекст Li - ' + str(context_Li))

        while (True):
            # ii
            context_KLi = copy.deepcopy(context_K)
            for c in context_Li[0]:
                context_KLi[0].append(c)
            m = -1
            Pi_1 = ExpFaultyData.SmallestIntent(Pi, M, context_KLi, context_Li, Ki, context_K, m, c)
            Pi_2 = ExpFaultyData.SmallestSet(Pi, M, Ki, context_KLi)

            print('Pi_1 - ' + str(Pi_1))
            print('Pi_2 - ' + str(Pi_2))

            if Pi_1==-1 and Pi_2==-1:
                break
            if Pi_1==-1:
                Pi = Pi_2
            else:
                if Pi_2==-1:
                    Pi = Pi_1
                else:
                    if (ExpFaultyData.LecticalComparison(Pi_1, Pi_2)):
                        Pi = Pi_1
                    else:
                        Pi = Pi_2
            
            # Выбор Q
            if (Pi == Pi_1):
                Qi = Pi_1.add(m)
            else:
                Qi = ExpFaultyData.ClosureOnContext(Pi_2, context_KLi)
            print('P_i - ' + str(Pi))
            print('Выбранное Q - ' + str(Qi))

            # Инициализация импликации
            imp = Implication(Pi, Qi)
            print('Есть ли контрпример для ' + imp.print_for_context(context_df.columns))
            # Запрос к эксперту
            counterexample = ExpFaultyData.expert_p(imp, context_expert, M)
            print(counterexample)

            # iv - v
            if (counterexample) :
                # Удаление импликаций, противоречащих контрпримеру
                Li = ExpFaultyData.DeleteFalseImplications(Li, counterexample)
                # Добавлен контрпример
                context_Li[0].append(counterexample)
                rows = rows + 1
                context_Li[1] = (rows,colums)
                print('Контекст Li - ' + str(context_Li))
                print('Значение Li - ' + str(Li))
            else :
                Ki.add(imp)
                print(Ki)
            # vi
            i = i+1
        print(Ki)
        print(Li)
    
