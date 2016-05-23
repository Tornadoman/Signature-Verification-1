import numpy


def calculate_features(signatures):
    return [calculate_signature_feature(signature) for signature in signatures]


def calculate_signature_feature(signature):
    #return signature
    feature_functions = (x_coordinates, y_coordinates, calculate_x_velocity, calculate_y_velocity, pressure)
    signature.data = zip(*[feature_function(signature) for feature_function in feature_functions])
    return signature


def calculate_x_velocity(signature):
    return numpy.diff([x[0] for x in signature.data])



def calculate_y_velocity(signature):
    return numpy.diff([x[1] for x in signature.data])


def x_coordinates(signature):
    return [x[0] for x in signature.data]


def y_coordinates(signature):
    return [x[1] for x in signature.data]


def pressure(signature):
    return [x[2] for x in signature.data]
