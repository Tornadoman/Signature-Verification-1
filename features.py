import numpy


def calculate_features(signatures):
    return [calculate_signature_feature(signature) for signature in signatures]


def calculate_signature_feature(signature):
    signature.set_features([x_coordinates(signature), y_coordinates(signature), calculate_x_velocity(signature),
                            calculate_y_velocity(signature), pressure(signature)])
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
