import matplotlib.pyplot as plt
import numpy

import Parser
import features
from config import enrollment_path
from config import verification_gt_path
from config import verification_path


class DTW(object):
    def __init__(self, signature):
        self.signature = signature
        self.cost_fix_hv = numpy.sqrt(len(self.signature.data[0]) * 100 ** 2) / 3
        self.diagonal_margin = 50

    def calculate_cost_and_matrix(self, compare_signature):
        max_i, max_j = len(self.signature.data[0]), len(compare_signature.data[0])
        matrix = [[None] * max_j for i in range(max_i)]
        diagonal_factor = float(max_j) / float(max_i)

        for i in range(max_i):
            j_low = max(int((i * diagonal_factor) - self.diagonal_margin), 0)
            j_high = min(int((i * diagonal_factor) + self.diagonal_margin), max_j)
            for j in range(j_low, j_high):
                if i == 0 and j == 0:
                    matrix[i][j] = 0
                    continue

                lowest_cost = []
                if i - 1 >= 0 and j - 1 >= 0 \
                        and not matrix[i - 1][j - 1] is None:  # cost that is defined by going diagonal
                    v1 = numpy.array(self.signature.data[i])
                    v2 = numpy.array(compare_signature.data[j])
                    lowest_cost.append(matrix[i - 1][j - 1] + numpy.linalg.norm(v1 - v2))
                if j - 1 >= 0 and not matrix[i][j - 1] is None:  # cost that is defined by going from left to right
                    lowest_cost.append(matrix[i][j - 1] + self.cost_fix_hv)
                if i - 1 >= 0 and not matrix[i - 1][j] is None:  # cost that is defined by going from top to bottom
                    lowest_cost.append(matrix[i - 1][j] + self.cost_fix_hv)

                matrix[i][j] = min(lowest_cost)
        return matrix[max_i - 1][max_j - 1] / (self.cost_fix_hv * (max_i + max_j))

    # Methods to visualise the DTW Vector
    @staticmethod
    def __transform_features__(features):
        feature_vector = []
        for i in range(len(features[0])):
            feature_vector.append([f[i] for f in features])
        return feature_vector

    @staticmethod
    def backtracking_path(matrix):
        no_nones = lambda fn: lambda *args: fn(a for a in args if a is not None)

        i, j = len(matrix) - 1, len(matrix[0]) - 1
        path = [[j, i]]
        while i > 0 and j > 0:
            if i == 0:
                j -= 1
            elif j == 0:
                i -= 1
            else:

                if matrix[i - 1][j] == no_nones(min)(matrix[i - 1][j - 1], matrix[i - 1][j], matrix[i][j - 1]):
                    i -= 1
                elif matrix[i][j - 1] == no_nones(min)(matrix[i - 1][j - 1], matrix[i - 1][j], matrix[i][j - 1]):
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
        print (path)
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
            print (map_x, v1[map_x - 1], ":", map_y, v2[map_y - 1])

        self.plt_output(plt, 'feature_mapping')

    @staticmethod
    def plt_output(plt, name):
        plt.title(name)
        plt.show()  # shows results in popup
        # plt.savefig(name + '.png')    # saves results in file system


def sort_by_name(signature):
    return signature.filename


# An example that takes the first word and searches in the images for the same word
# Pictures need to be already cropped.
if __name__ == "__main__":
    enrollment = sorted(features.calculate_features(Parser.parse_files_in_directory(enrollment_path)), key=sort_by_name)
    verification = sorted(features.calculate_features(Parser.parse_files_in_directory(verification_path)),
                          key=sort_by_name)
    verification_gt = Parser.parse_validation_file(verification_gt_path)

    dtw = DTW(verification[0])
    result = dtw.calculate_cost_and_matrix(verification[1])
    print "cost: ", result[0]

    dtw.plot_matrix_cost(result[1])
