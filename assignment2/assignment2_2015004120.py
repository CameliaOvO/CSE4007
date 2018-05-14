
def cosine_similarity(a, b):
    return sum([x * y for x, y in zip(a, b)]) / ((sum([x ** 2 for x in a]) ** 0.5) * (sum([x ** 2 for x in b]) ** 0.5))


def euclidean_similarity(x, y):
    return sum([(xk - yk) ** 2 for xk, yk in zip(x, y)]) ** 0.5


def find_max(c1, c2, sim):
    return max([sim(p1, p2) for p1 in c1 for p2 in c2])


def get_vectors():
    result = []
    with open("WordEmbedding.txt", 'r') as f:
        for word, vector in zip(*[f] * 2):
            result.append((word.strip(), list(map(float, vector.split(",")))))
    return result

word_vector = get_vectors()

print(cosine_similarity(word_vector[3][1], word_vector[0][1]))
