import features
import SvgParser
import numpy

import matplotlib.pyplot as plt


class DTW(object):

    def __init__(self, keyword):
        self.keyword = keyword
        self.keyword_features_vector = features.calculate_image_features(keyword)
        self.cost_fix_hv = numpy.sqrt(len(self.keyword_features_vector[0]) * 100 ** 2) / 3
        self.diagonal_margin = 50

    # Masis method to calculate the cost (probably better)
    def calculate_cost_and_matrix(self, compare_vector):
        compare_vector = features.calculate_image_features(compare_vector)
        max_i, max_j = len(self.keyword_features_vector), len(compare_vector)
        matrix = [[None] * (max_j) for i in range(max_i)]
        diagonal_factor = float(max_j) / float(max_i)

        for i in range(max_i):
            j_low = max(int((i * diagonal_factor) - self.diagonal_margin), 0)
            j_high = min(int((i * diagonal_factor) + self.diagonal_margin), max_j)
            for j in range(j_low, j_high):
                if i == 0 and j == 0:
                    matrix[i][j] = 0
                    continue

                lowest_cost = []
                if i - 1 >= 0 and j - 1 >= 0\
                        and not matrix[i - 1][j - 1] is None:  # cost that is defined by going diagonal
                    v1 = numpy.array(self.keyword_features_vector[i])
                    v2 = numpy.array(compare_vector[j])
                    lowest_cost.append(matrix[i - 1][j - 1] + numpy.linalg.norm(v1 - v2))
                if j - 1 >= 0 and not matrix[i][j - 1] is None:  # cost that is defined by going from left to right
                    lowest_cost.append(matrix[i][j - 1] + self.cost_fix_hv)
                if i - 1 >= 0 and not matrix[i - 1][j] is None:  # cost that is defined by going from top to bottom
                    lowest_cost.append(matrix[i - 1][j] + self.cost_fix_hv)

                matrix[i][j] = min(lowest_cost)
        return (matrix[max_i - 1][max_j - 1] / (self.cost_fix_hv * (max_i + max_j))), matrix

    # Pascis method to calculate the cost
    def calculate_cost_pasci(self, compare_vector):
        # v1 = i, v2 = j
        compare_vector = features.calculate_image_features(compare_vector)
        v1, v2 = self.__transform_features__(compare_vector), \
                 self.__transform_features__(self.keyword_features_vector)

        cost = []
        for i in range(min(len(v1), len(v2))):
            cost.append(self.calculate_cost_and_matrix_pasci(v1[i], v2[i])[0])
        return sum(cost), None

    def calculate_cost_and_matrix_pasci(self, v1, v2):
        max_i, max_j = len(v1) + 1, len(v2) + 1
        matrix = [[0] * max_j for i in range(max_i)]
        cost_fix_hv = (sum(v1) + sum(v2)) / (len(v1) + len(v2)) / 2

        if cost_fix_hv < 1:
            cost_fix_hv = 1

        for i in range(max_i):
            for j in range(max_j):
                if i == 0 and j == 0:
                    continue

                lowest_cost = []
                if i - 1 >= 0 and j - 1 >= 0:  # cost that is defined by going diagonal
                    lowest_cost.append(matrix[i - 1][j - 1] + abs(v1[i - 1] - v2[j - 1]))
                if j - 1 >= 0:  # cost that is defined by going from left to right
                    lowest_cost.append(matrix[i][j - 1] + cost_fix_hv)
                if i - 1 >= 0:  # cost that is defined by going from top to bottom
                    lowest_cost.append(matrix[i - 1][j] + cost_fix_hv)

                matrix[i][j] = min(lowest_cost)
        return matrix[max_i - 1][max_j - 1], matrix

    # Methods to visualise the DTW Vector
    @staticmethod
    def __transform_features__(features):
        feature_vector = []
        for i in range(len(features[0])):
            feature_vector.append([f[i] for f in features])
        return feature_vector

    @staticmethod
    def backtracking_path(matrix):
        noNones = lambda fn: lambda *args : fn(a for a in args if a is not None)

        i, j = len(matrix) - 1, len(matrix[0]) - 1
        path = [[j, i]]
        while i > 0 and j > 0:
            if i == 0:
                j -= 1
            elif j == 0:
                i -= 1
            else:

                if matrix[i - 1][j] == noNones(min)(matrix[i - 1][j - 1], matrix[i - 1][j], matrix[i][j - 1]):
                    i -= 1
                elif matrix[i][j - 1] == noNones(min)(matrix[i - 1][j - 1], matrix[i - 1][j], matrix[i][j - 1]):
                    j -= 1
                else:
                    i -= 1
                    j -= 1
            path.append([j, i])
        path.append([0, 0])
        return path

    # Define functions to visualize the results
    def plot_keyword_features(self):
        for feature in features:
            plt.plot(feature, 'r', label='')
            plt.legend()
        self.plt_output(plt, 'keyword_features')

    def plot_matrix_cost(self, matrix):
        for i in range(0, len(matrix)):
            for j in range(0, len(matrix[0])):
                if matrix[i][j] is None:
                    matrix[i][j] = numpy.nan

        path = self.backtracking_path(matrix)
        print path
        path_x, path_y = [point[0] for point in path], [point[1] for point in path]
        plt.imshow(matrix, interpolation='nearest', cmap='Reds', aspect=.5)
        plt.gca().invert_yaxis()
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.grid()
        plt.colorbar()
        plt.plot(path_x, path_y)
        self.plt_output(plt, 'matrix_cost')

    # Not working yet
    def plot_feature_mapping(self, v1, v2, matrix):
        plt.plot(v1, 'bo-', label='x')
        plt.plot(v2, 'g^-', label='y')
        plt.legend()
        path = self.backtracking_path(matrix)
        for [map_x, map_y] in path:
            plt.plot([map_x, map_y], [v1[map_x - 1], v2[map_y - 1]], 'r')
            print map_x, v1[map_x - 1], ":", map_y, v2[map_y - 1]

        self.plt_output(plt, 'feature_mapping')

    def plt_output(self, plt, name):
        plt.title(name)
        plt.show()                      # shows results in popup
        # plt.savefig(name + '.png')    # saves results in file system


# An example that takes the first word and searches in the images for the same word
# Pictures need to be already cropped.
if __name__ == "__main__":
    svg_parser = SvgParser.SvgParser("ground-truth/locations/", "images/", "task/train.txt", "task/valid.txt")

    # 2 words that are equal: (orders)
    # training_keyword = svg_parser.binarize("cropped/train/270_2_out.png", 0.5)
    # training_sample = svg_parser.binarize("cropped/train/270_16_out.png", 0.5)

    # 2 words hat are different:
    training_keyword = svg_parser.binarize("cropped/train/270_4_out.png", 0.5)
    training_sample = svg_parser.binarize("cropped/train/270_20_out.png", 0.5)

    dtw = DTW(training_keyword)
    result = dtw.calculate_cost_and_matrix(training_sample)
    print "cost: ", result[0]

    dtw.plot_matrix_cost(result[1])