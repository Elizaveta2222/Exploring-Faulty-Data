import unittest
import pandas as pd
import copy
from ExpFaultyData_5 import ExpFaultyData, Implication

class TestExpFaultyData(unittest.TestCase):

    def setUp(self):
        self.context_df = pd.read_csv('example.csv',sep=';')
        self.context_K = [self.context_df.values.tolist(),self.context_df.shape]
        context_df_expert = pd.read_csv('example_expert.csv',sep=';')
        self.context_expert = [context_df_expert.values.tolist(),context_df_expert.shape]
        self.context_L = [[[0, 0, 0, 1, 1, 1]],(1,6)]

        context_KLi = copy.deepcopy(self.context_K)
        for c in self.context_L[0]:
            context_KLi[0].append(c)
        self.context_KLi = copy.deepcopy(context_KLi)

        self.c = 0.5
        self.M=list(range(0,self.context_K[1][1]))
        self.Th_c_K = {Implication({0}, {3}), #hair -> milk
              Implication({0}, {4}), #hair -> predator
              Implication({0}, {5}), #hair -> breathes
              Implication({1}, {2}), #feathers -> eggs
              Implication({1}, {4}), #feathers -> predator
              Implication({1}, {5}), #feathers -> breathes
              Implication({2}, {4}), #eggs -> predator
              Implication({3}, {0}), #milk -> hair
              Implication({3}, {4}), #milk -> predator
              Implication({3}, {5}), #milk -> breathes
              Implication({4}, {0}), #predator -> hair
              Implication({4}, {2}), #predator -> eggs
              Implication({4}, {3}), #predator -> milk
              Implication({4}, {5}), #predator -> breathes
              Implication({5}, {0}), #breathes -> hair
              Implication({5}, {3}), #breathes -> milk
              Implication({5}, {4}), #breathes -> predator
              }
        self.K = {Implication({0}, {3})}

#------------------------------------------------------------------------------

    def test_expert_p_valid(self):
        imp = Implication({0}, {3}) #hair -> milk
        expert_p = ExpFaultyData.expert_p(imp, self.context_K, self.M)
        self.assertEqual(expert_p, False)
    
    def test_expert_p_invalid(self):
        imp = Implication({0}, {2, 3, 4, 5})
        expert_p = ExpFaultyData.expert_p(imp, self.context_K, self.M)
        self.assertEqual(len(expert_p), len(self.M))

# #------------------------------------------------------------------------------

    def test_ClosureOnImp_empty(self):
        A = set()
        closureOnImp = ExpFaultyData.ClosureOnImp(A, self.Th_c_K)
        self.assertEqual(closureOnImp, set())

    def test_ClosureOnImp_notempty(self):
        A = {5} # breathes
        closureOnImp = ExpFaultyData.ClosureOnImp(A, self.Th_c_K)
        self.assertEqual(closureOnImp, {0, 2, 3, 4, 5})

# #------------------------------------------------------------------------------

    def test_ClosureOnContext_empty(self):
        A = set()
        closureOnContext = ExpFaultyData.ClosureOnContext(A, self.context_K)
        self.assertEqual(closureOnContext, set())

    def test_ClosureOnContext_notempty(self):
        A = {5} # breathes
        closureOnContext = ExpFaultyData.ClosureOnContext(A, self.context_K)
        self.assertEqual(closureOnContext, A)

    def test_ClosureOnContext_notempty_notfull(self):
        A = {3} # milk
        closureOnContext = ExpFaultyData.ClosureOnContext(A, self.context_K)
        self.assertEqual(closureOnContext, {0, 3, 5}) # hair, milk, breathes

# #------------------------------------------------------------------------------

    def test_SmallestSet_empty(self):
        A = set() # milk
        smallestSet = ExpFaultyData.SmallestSet(A, self.M, self.K, self.context_K)
        self.assertEqual(smallestSet, {3}) # milk 

    def test_SmallestSet_notempty(self):
        A = {3} # milk
        smallestSet = ExpFaultyData.SmallestSet(A, self.M, self.K, self.context_K)
        self.assertEqual(smallestSet, {3, 5}) # milk, breathes

    def test_SmallestSet_notempty_notexist(self):
        A = {0, 1, 2, 3, 4, 5}
        smallestSet = ExpFaultyData.SmallestSet(A, self.M, self.K, self.context_K)
        self.assertEqual(smallestSet, -1) 

# #------------------------------------------------------------------------------

    def test_FindConfidence_notzero(self):
        imp = Implication({5},{0})
        findConfidence = ExpFaultyData.FindConfidence(imp, self.context_K)
        self.assertEqual(findConfidence, 0.75) 

    def test_FindConfidence_zero(self):
        imp = Implication({0},{2})
        findConfidence = ExpFaultyData.FindConfidence(imp, self.context_K)
        self.assertEqual(findConfidence, 0) 

#------------------------------------------------------------------------------

    def test_SmallestIntent_empty(self):
        A = set() # milk
        l = -1
        smallestIntent = ExpFaultyData.SmallestIntent(A, self.M, self.context_KLi, self.context_L, self.K, self.context_K, l, self.c)
        self.assertEqual(smallestIntent, {5}) # milk 

    def test_SmallestIntent_notempty(self):
        A = {5} # milk
        l = -1
        smallestIntent = ExpFaultyData.SmallestIntent(A, self.M, self.context_KLi, self.context_L, self.K, self.context_K, l, self.c)
        self.assertEqual(smallestIntent, {4}) # milk 

#------------------------------------------------------------------------------

    def test_DeleteFalseImplications_conter(self):
        C = [0, 0, 1, 0, 0, 0]
        L = {Implication({1}, {4}), Implication({5}, {2, 3, 4}), Implication({2}, {4}), Implication({4}, {2})}
        diff = {Implication({2}, {4})}
        deleteFalseImplications = ExpFaultyData.DeleteFalseImplications(L, C)
        self.assertEqual(str(L.difference(deleteFalseImplications)), str(diff))

    def test_DeleteFalseImplications_notconter(self):
        C = [1, 0, 0, 0, 0, 0]
        L = {Implication({5}, {2, 3, 4}), Implication({2}, {4}), Implication({4}, {2}), Implication({1}, {4})}
        deleteFalseImplications = ExpFaultyData.DeleteFalseImplications(L, C)
        self.assertEqual(str(L.difference(deleteFalseImplications)), str(set()))

#------------------------------------------------------------------------------

    def test_LecticalComparison_eq(self):
        P1 = {0, 1, 2}
        P2 = {0, 1, 2}
        lecticalComparison = ExpFaultyData.LecticalComparison(P1, P2)
        self.assertEqual(lecticalComparison, False)

    def test_LecticalComparison_eqlen(self):
        P1 = {0, 1, 2}
        P2 = {0, 1, 3}
        lecticalComparison = ExpFaultyData.LecticalComparison(P1, P2)
        self.assertEqual(lecticalComparison, True)

    def test_LecticalComparison_diflen_eq(self):
        P1 = {0, 1, 2}
        P2 = {0, 1}
        lecticalComparison = ExpFaultyData.LecticalComparison(P1, P2)
        self.assertEqual(lecticalComparison, False)

    
    def test_LecticalComparison_diflen(self):
        P1 = {0, 1, 2}
        P2 = {0, 2}
        lecticalComparison = ExpFaultyData.LecticalComparison(P1, P2)
        self.assertEqual(lecticalComparison, True)
#------------------------------------------------------------------------------
 
    
if __name__ == "__main__":
    unittest.main()
