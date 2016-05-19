import numpy


def calculate_features(signatures):
    return [calculate_signature_feature(signature) for signature in signatures]


def calculate_signature_feature(signature):
    # this is a placeholder for some actual feature calculations. Calculate all features here and return them as a new signature object.
    # return [x[1] for x in signature.data]
    return [calculate_x_velocity(signature), calculate_y_velocity(signature)]


def calculate_x_velocity(signature):
    return numpy.diff([x[0] for x in signature.data])


def calculate_y_velocity(signature):
    return numpy.diff([x[1] for x in signature.data])
