class Implication:
    def __init__(self,p,c):
        self.premise = p.copy()
        self.consequent = c.copy()
        pass
    def __str__(self):
        return str(self.premise)+'->'+str(self.consequent)
    def __repr__(self):
        return str(self.premise)+'->'+str(self.consequent)
    def print_for_context(self, cont):
        old_values = range(0, len(cont))
        p_new = list(map(dict(zip(old_values, cont)).get, self.premise))
        c_new = list(map(dict(zip(old_values, cont)).get, self.consequent))
        return str(p_new)+'->'+str(c_new)
    
    def Galois(X,context,t):
        if len(X)==0:
            if t=='ObjectsToAttributes': return set(range(0, context[1][1]))
            if t=='AttributesToObjects': return set(range(0, context[1][0]))
        if t=='ObjectsToAttributes':
            context_temp=[context[0][x] for x in list(X)]
        if t=='AttributesToObjects':
            transposed=list(zip(*context[0]))
            context_temp=[transposed[x] for x in list(X)]
        at=[sum(i) for i in zip(*context_temp)]
        attributes=set()
        for i in range(0,len(at)):
            if at[i]==len(X):   
                attributes.update(set([i]))
        return attributes
    
    def example_to_column_nums(example):
        new = [i for i in range(0, len(example)) if example[i]==1]
        return new