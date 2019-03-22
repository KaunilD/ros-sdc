import random
import numpy as np
import math
def run_ransac(
    data, max_iterations,
    ransac_threshold, ransac_consensus,

    ref_vector = None, ref_threshold = 0.4,
    sample_size=3, stop_at_goal=True, random_seed=None
):

    best_ic = 0
    best_model = None
    inliers = None
    if ref_vector is not None:
        denom = np.sum(np.power(ref_vector, 2))
        ref_vector = ref_vector/(np.sqrt(denom))

    for i in range(max_iterations):
        s = np.random.choice(data.shape[0], sample_size)
        m = fit_plane(data[s])

        is_valid = True

        if ref_vector is not None:
            is_valid = check_perpendicular_plane(m, ref_vector, ref_threshold)

        if is_valid:
            distances = evaluate_model(m, data)
            inliers = distances < ransac_threshold
            ic = np.sum(inliers)
            if ic > best_ic:
                best_ic = ic
                best_model = m
                if ic > ransac_consensus and stop_at_goal:
                    break

    print('took iterations:', i+1, 'best model:', best_model, 'explains:', best_ic)
    return best_model, best_ic, inliers


# plane equation: ax + by + cz + d = 0;
def fit_plane(xyzs):
    v1, v2 = xyzs[2] - xyzs[0], xyzs[1] - xyzs[0]

    normal = np.cross(v1, v2)
    a, b, c = normal

    # todo, if denom<eps
    denom = np.sum(np.power(normal, 2))
    normal = normal/np.sqrt(denom)
    d = np.dot(-xyzs[0], normal.T)

    return np.asarray([normal[0], normal[1], normal[2], d])


def check_model(model):
    return model.size == 4 & np.all(np.isfinite(model))


def check_perpendicular_plane(model, normal_axis, threshold):
    valid = check_model(model)
    if True:
        a = min(1, max(-1, np.dot(normal_axis, model[0:3])))
        angle = abs(math.acos(a))
        angle = min(angle, math.pi - angle)
        valid = angle < threshold

    return valid


def evaluate_model(model, points):
    distances = abs(np.dot(points, model[0:3]) + model[3])
    return distances
