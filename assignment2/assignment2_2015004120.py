from bisect import bisect_left
from collections import Counter
from math import log2


def complete_link_clustering(sim_name):
    sim = cosine_similarity if sim_name == 'c' else euclidean_distance
    most = min if sim == euclidean_distance else max
    levels, clusters = [], [[x] for x in range(num_of_words)]
    prox_mat = [[sim(vectors[i], vectors[j]) for j in range(num_of_words) if i > j] for i in range(num_of_words)][1:]
    while len(clusters) > 1:
        most_sim = most(enumerate([(i.index(most(i)), most(i)) for i in prox_mat]), key=lambda x: x[1][1])
        r, s = clusters[most_sim[0] + 1], clusters[most_sim[1][0]]
        levels.append([find_least_sim(r, s, sim), r + s])
        clusters.remove(r), clusters.remove(s), clusters.append(r + s)
        del prox_mat[most_sim[0]]
        if most_sim[1][0] > 0:
            del prox_mat[most_sim[1][0] - 1]
        it = 0
        while it < len(prox_mat):
            if len(prox_mat[it]) > most_sim[0] + 1:
                del prox_mat[it][most_sim[0] + 1]
            if len(prox_mat[it]) > most_sim[1][0]:
                del prox_mat[it][most_sim[1][0]]
            if len(prox_mat[it]) == 0:
                prox_mat.remove(prox_mat[it])
            else:
                it += 1
        prox_mat.append([find_least_sim(r + s, clusters[t], sim) for t in range(len(clusters) - 1)])
    return levels


def cosine_similarity(a, b):
    return sum([x * y for x, y in zip(a, b)]) / ((sum([x ** 2 for x in a]) ** 0.5) * (sum([x ** 2 for x in b]) ** 0.5))


def euclidean_distance(x, y):
    return sum([(xk - yk) ** 2 for xk, yk in zip(x, y)]) ** 0.5


def find_least_sim(c1, c2, sim):
    least = max if sim == euclidean_distance else min
    return least([sim(vectors[p1], vectors[p2]) for p1 in c1 for p2 in c2])


def normalize(level):
    max_val = max(level, key=lambda x: x[0])[0]
    min_val = min(level, key=lambda x: x[0])[0]
    for l in level:
        l[0] = 1 - ((l[0] - min_val) / (max_val - min_val))
    return level


def get_words_vectors():
    word_list, vector_list = [], []
    with open("WordEmbedding.txt", 'r') as f:
        for word, vector in zip(*[f] * 2):
            word_list.append(word.strip())
            vector_list.append(list(map(float, vector.split(","))))
    return word_list, vector_list, len(vector_list)


def divide_cluster(levels, threshold):
    cluster_idx, cluster_num = 0, [0 for _ in range(num_of_words)]
    limit = bisect_left([x[0] for x in levels], threshold)
    levels = levels[limit:]
    for level in levels:
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
    return cluster_idx, cluster_num


def write_on_file(result):
    write_word, write_vector = [], []
    with open("WordEmbedding.txt", 'r') as rf:
        for word, vector in zip(*[rf] * 2):
            write_word.append(word.strip())
            write_vector.append(vector.strip())
    with open("WordClustering.txt", 'w') as wf:
        for word, vector, cluster in zip(write_word, write_vector, result):
            wf.write(word + "\n" + vector + "\n" + str(cluster) + "\n")


def get_word_class():
    with open("WordTopic.txt", 'r') as f:
        whole = [x.strip().lower() for x in f.readlines()]
    word_topic, topic, word_cls = [], [], []
    for word in whole:
        if (not word.isalnum()) and topic != []:
            word_topic.append(topic)
            topic = []
        if word.isalnum():
            topic.append(word)
    word_topic.append(topic)
    for word in words:
        for cls in word_topic:
            if word in cls:
                word_cls.append(word_topic.index(cls))
                break
    return word_cls


def entropy_measure(n_clusters, c_list, word_cls):
    clustered = [[] for _ in range(n_clusters)]
    for i in range(len(c_list)):
        clustered[c_list[i] - 1].append(word_cls[i])
    counter_clustered = [[x[1] for x in Counter(clusters).items()] for clusters in clustered]

    cluster_entropy = [sum([-(x / sum(lis)) * log2(x / sum(lis)) for x in lis]) for lis in counter_clustered]
    cluster_size = [len(cluster) / len(clustered) for cluster in clustered]
    weighted_sum = sum([x * y for x, y in zip(cluster_size, cluster_entropy)])
    return weighted_sum


def silhouette_measure(n_clusters, c_list):
    silhouette_list = []
    dist_mat = [[euclidean_distance(x, y) for x in vectors] for y in vectors]
    clustered_idx = [[] for _ in range(n_clusters)]
    for i in range(len(c_list)):
        clustered_idx[c_list[i] - 1].append(i)

    for i in range(num_of_words):
        inner_cluster_idx = c_list[i] - 1
        if len(clustered_idx[inner_cluster_idx]) == 1:
            silhouette_list.append(0)
        else:
            c_i = clustered_idx[inner_cluster_idx]
            a_i = sum([dist_mat[i][cx] for cx in c_i if cx != i]) / (len(c_i) - 1)
            b_i = min([sum(dist_mat[i][cx] for cx in c) / len(c) for c in clustered_idx if c != c_i])
            silhouette_coef = (b_i - a_i) / max([a_i, b_i])
            silhouette_list.append(silhouette_coef)

    sil_measure = sum(silhouette_list) / len(silhouette_list)
    return sil_measure


argument = ['c', 0.4]
words, vectors, num_of_words = get_words_vectors()
word_class = get_word_class()

level_cluster = complete_link_clustering(argument[0])[::-1]
num_of_clusters, clustered_list = divide_cluster(level_cluster, argument[1])
write_on_file(clustered_list)

print('cosine similarity' if argument[0] == 'c' else 'euclidean distance')
print("divided into", num_of_clusters, "clusters with threshold ", argument[1])
print("entropy : \t", entropy_measure(num_of_clusters, clustered_list, word_class))
print("silhouette : \t", silhouette_measure(num_of_clusters, clustered_list))
