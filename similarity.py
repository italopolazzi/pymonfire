import math
from collections import Counter


def build_vector(dict1, dict2):
    d1 = Counter(set(Counter(dict1['positive'].keys())).union(set(dict1['neutral'])))
    d2 = Counter(set(Counter(dict2['positive'].keys())).union(set(dict2['neutral'])))
    
    all_items = set(d1).union(set(d2))
    print(all_items)
    
    v1 = [d1[k] for k in all_items]
    v2 = [d2[k] for k in all_items]
    
    return v1,v2


def cosim(v1, v2):
    dot_product = sum(n1 * n2 for n1, n2 in zip(v1,v2))
    
    magnitude1 = math.sqrt(sum(n ** 2 for n in v1))
    magnitude2 = math.sqrt(sum(n ** 2 for n in v2))
    
    return dot_product/(magnitude1*magnitude2)


def teste():
    propaganda = {
        'positive': {'subway': 1.00, 'sanduiche': 0.90, 'cookies ': 0.2, 'suco': 0.45, 'carne': 0.2},
        'neutral': {'lanche': 0.75, 'comida': 1, 'almoco': 0.75, 'restaurante': 0.5, 'fome': 0.30},
        'negative': {}
    }
    user = {
        'positive': {'pessoas': 1.00, 'hobbies': 0.39, 'comida': 0.13, 'starcraft 2': 0.12, 'subway': 0.46},
        'neutral': {'foto': 0.36, 'inspira': 0.07, 'amigos': 0.51, 'estilo': 0.08, 'trabalho': 0.63, 'modelo': 0.19,'grana': 0.16},
        'negative': {}
    }
    
    sim = Sililarity().calculate(propaganda, user)
    print(sim)


class Sililarity:
    def calculate(self, dict1, dict2):
        #l1 = l1.split()
        # #l2 = l2.split()
        
        v1, v2 = build_vector(dict1, dict2)
        sim = cosim(v1,v2)
        
        return sim
    
#teste()