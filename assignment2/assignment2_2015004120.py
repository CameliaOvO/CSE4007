def complete_link_clustering(sim):
    level, clusters = [], [[x] for x in range(len(vectors))]
    proximity_matrix = [[find_least_sim(clusters[i], clusters[j], sim) for j in range(len(clusters)) if i > j] for i in range(len(clusters))][1:]
    while len(clusters) > 1:
        least_sim = sim[2](enumerate([(i.index(sim[2](i)), sim[2](i)) for i in proximity_matrix]), key=lambda x: x[1][1])
        r, s = clusters[least_sim[0]+1], clusters[least_sim[1][0]]
        level.append([find_least_sim(r, s, sim), r + s])
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


def normalize(level):
    max_val = max(level, key=lambda x: x[0])[0]
    min_val = min(level, key=lambda x: x[0])[0]
    for l in level:
        l[0] = 1 - ((l[0] - min_val) / (max_val - min_val))
    return level

cosine_sim = (cosine_similarity, min, max)
euclidean_sim = (euclidean_similarity, max, min)


arguments = ['c', 0.2, 'entropy']

similarity_measure = cosine_sim if arguments[0] == 'c' else euclidean_sim
similarity_threshold = arguments[1]
evaluation_method = arguments[2]

words, vectors = get_words_vectors()

# make cluster tree
level_cluster = complete_link_clustering(similarity_measure)[::-1]

if similarity_measure == euclidean_sim:
    level_cluster = normalize(level_cluster)

import bisect

cluster_idx = 0
cluster_num = [0 for x in range(len(vectors))]
limit = bisect.bisect_left([x[0] for x in level_cluster], similarity_threshold)
level_cluster = level_cluster[limit:]

for level in level_cluster:
    cluster_idx += 1
    flag = False
    for c in level[1]:
        if cluster_num[c] == 0:
            flag = True
            cluster_num[c] = cluster_idx
    if not flag:
        cluster_idx -= 1

for i in range(len(cluster_num)):
    if cluster_num[i] == 0:
        cluster_idx += 1
        cluster_num[i] = cluster_idx

# write on file

write_word, write_vector = [], []
with open("WordEmbedding.txt", 'r') as rf:
    for word, vector in zip(*[rf] * 2):
        write_word.append(word.strip())
        write_vector.append(vector.strip())

print(len(write_word), len(write_vector), len(cluster_num))

with open("WordClustering.txt", 'w') as wf:
    for word, vector, cluster in zip(write_word, write_vector, cluster_num):
        wf.write(word + "\n")
        wf.write(vector + "\n")
        wf.write(str(cluster) + "\n")

# calculate entropy

with open("WordTopic.txt", 'r') as f:
    whole = [x.strip().lower() for x in f.readlines()]

word_topic = []
topic = []
for word in whole:
    if (not word.isalnum()) and topic != []:
        word_topic.append(topic)
        topic = []
    if word.isalnum():
        topic.append(word)
word_topic.append(topic)

word_class = []
for word in words:
    for cls in word_topic:
        if word in cls:
            word_class.append(word_topic.index(cls))
            break

from collections import Counter

clustered = [[] for x in range(cluster_idx)]
for i in range(len(cluster_num)):
    clustered[cluster_num[i] - 1].append(word_class[i])

counter_clustered = [[x[1] for x in Counter(clusters).items()] for clusters in clustered]

from math import log2

cluster_entropy = [sum([-(x / sum(lis)) * log2(x / sum(lis)) for x in lis]) for lis in counter_clustered]
cluster_size = [len(cluster) / len(clustered) for cluster in clustered]

entropy = sum([x * y for x, y in zip(cluster_size, cluster_entropy)])


# calculate silhouette


# calculate davies boulden


# calculate dunn index