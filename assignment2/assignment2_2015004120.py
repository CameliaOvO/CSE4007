import time


def complete_link_clustering(sim):
    level, clusters = [], [[x] for x in range(len(vectors))]
    proximity_matrix = [[find_least_sim(clusters[i], clusters[j], sim) for j in range(len(clusters)) if i > j] for i in range(len(clusters))][1:]
    while len(clusters) > 1:
        least_sim = sim[2](enumerate([(i.index(sim[2](i)), sim[2](i)) for i in proximity_matrix]), key=lambda x: x[1][1])
        r, s = clusters[least_sim[0]+1], clusters[least_sim[1][0]]
        level.append([find_least_sim(r, s, sim), r, s])
        clusters.remove(r), clusters.remove(s), clusters.append(r+s)
        del proximity_matrix[least_sim[0]]
        if least_sim[1][0] > 0:
            del proximity_matrix[least_sim[1][0]-1]
        i = 0
        while i < len(proximity_matrix):
            if len(proximity_matrix[i]) > least_sim[0]+1:
                del proximity_matrix[i][least_sim[0]+1]
            if len(proximity_matrix[i]) > least_sim[1][0]:
                del proximity_matrix[i][least_sim[1][0]]
            if len(proximity_matrix[i]) == 0:
                proximity_matrix.remove(proximity_matrix[i])
            else:
                i += 1
        proximity_matrix.append([find_least_sim(r+s, clusters[t], sim) for t in range(len(clusters)-1)])
    return level


def cosine_similarity(a, b):
    return sum([x * y for x, y in zip(a, b)]) / ((sum([x ** 2 for x in a]) ** 0.5) * (sum([x ** 2 for x in b]) ** 0.5))


def euclidean_similarity(x, y):
    return sum([(xk - yk) ** 2 for xk, yk in zip(x, y)]) ** 0.5


def find_least_sim(c1, c2, sim):
    return sim[1]([sim[0](vectors[p1], vectors[p2]) for p1 in c1 for p2 in c2])


def get_words_vectors():
    word_list, vector_list = [], []
    with open("WordEmbedding.txt", 'r') as f:
        for word, vector in zip(*[f] * 2):
            word_list.append(word.strip())
            vector_list.append(list(map(float, vector.split(","))))
    return word_list, vector_list

arguments = ['c', 0.8, 'entropy']

similarity_measure = arguments[0]
similarity_threshold = arguments[1]
evaluation_method = arguments[2]

words, vectors = get_words_vectors()
start = time.clock()
cosine_sim = (cosine_similarity, min, max)
euclidean_sim = (euclidean_similarity, max, min)

# make cluster tree
level_cluster = complete_link_clustering(euclidean_sim)


print('execution time : ', time.clock() - start)
