"""Utilities for manipulating image annotation bounding boxes."""
import numpy as np
import cv2


def draw_rect(img, bboxes, color=None, stroke=None):
    """Draw annotation bounding boxes on the image as red rectangles."""
    img = img.copy()
    bboxes = bboxes[:, :4]
    bboxes = bboxes.reshape(-1, 4)
    for bbox in bboxes:
        pt1, pt2 = (bbox[0], bbox[1]), (bbox[2], bbox[3])
        pt1 = int(pt1[0]), int(pt1[1])
        pt2 = int(pt2[0]), int(pt2[1])
        stroke = int(max(img.shape[:2]) / 200) if stroke is None else stroke
        img = cv2.rectangle(img.copy(), pt1, pt2, color, stroke)
    return img


def bbox_area(bbox):
    """Compute the area of the annotation bounding box."""
    return (bbox[:, 2] - bbox[:, 0]) * (bbox[:, 3] - bbox[:, 1])


def clip_box(bbox, clipping_box, alpha):
    """Clip the given bounding box."""
    # TODO: AR CANNOT BE ZERO.
    np.seterr(divide="ignore", invalid="ignore")
    area = bbox_area(bbox)
    x_min = np.maximum(bbox[:, 0], clipping_box[0]).reshape(-1, 1)
    y_min = np.maximum(bbox[:, 1], clipping_box[1]).reshape(-1, 1)
    x_max = np.minimum(bbox[:, 2], clipping_box[2]).reshape(-1, 1)
    y_max = np.minimum(bbox[:, 3], clipping_box[3]).reshape(-1, 1)

    bbox = np.hstack((x_min, y_min, x_max, y_max, bbox[:, 4:]))
    delta_area = (area - bbox_area(bbox)) / area
    mask = (delta_area < (1 - alpha)).astype(int)
    bbox = bbox[mask == 1, :]
    return bbox


def get_corners(bboxes):
    """Get the corners of an array of annotation bounding boxes."""
    width = (bboxes[:, 2] - bboxes[:, 0]).reshape(-1, 1)
    height = (bboxes[:, 3] - bboxes[:, 1]).reshape(-1, 1)

    x_top_left = bboxes[:, 0].reshape(-1, 1)
    y_top_left = bboxes[:, 1].reshape(-1, 1)

    x_top_right = x_top_left + width
    y_top_right = y_top_left

    x_btm_left = x_top_left
    y_btm_left = y_top_left + height

    x_btm_right = x_top_right
    y_btm_right = y_btm_left

    corners = np.hstack((
        x_top_left,
        y_top_left,
        x_top_right,
        y_top_right,
        x_btm_left,
        y_btm_left,
        x_btm_right,
        y_btm_right,
    ))
    return corners


def rotate_box(corners, angle, center_x, center_y, height, width):
    """Rotate a bounding box."""
    corners = corners.reshape(-1, 2)
    corners = np.hstack(
        (corners, np.ones((corners.shape[0], 1), dtype=type(corners[0][0]))))
    center_x, center_y = width // 2, height // 2
    transformation_matrix = cv2.getRotationMatrix2D(center=(center_x,
                                                            center_y),
                                                    angle=angle,
                                                    scale=1.0)
    sin_theta = np.abs(transformation_matrix[0][1])
    cos_theta = np.abs(transformation_matrix[0][0])
    new_width = int((width * cos_theta) + (height * sin_theta))
    new_height = int((width * sin_theta) + (height * cos_theta))
    translate_x = (new_width / 2) - center_x
    translate_y = (new_height / 2) - center_y
    transformation_matrix[0][2] = transformation_matrix[0][2] + translate_x
    transformation_matrix[1][2] = transformation_matrix[1][2] + translate_y
    rotated_bbox_coordinates = np.dot(transformation_matrix, corners.T).T
    rotated_bbox_coordinates = rotated_bbox_coordinates.reshape(-1, 8)
    return rotated_bbox_coordinates


def get_enclosing_box(corners):
    """Get the bounding box enclosing the given bounding boxes."""
    x_coords = corners[:, [0, 2, 4, 6]]
    y_coords = corners[:, [1, 3, 5, 7]]
    x_min = np.min(x_coords, 1).reshape(-1, 1)
    y_min = np.min(y_coords, 1).reshape(-1, 1)
    x_max = np.max(x_coords, 1).reshape(-1, 1)
    y_max = np.max(y_coords, 1).reshape(-1, 1)
    final = np.hstack((x_min, y_min, x_max, y_max, corners[:, 8:]))
    return final


def letterbox_image(img, input_dimension):
    """Resize the image to input_dimension, preserving aspect ratio."""
    input_dimension = (input_dimension, input_dimension)
    img_w, img_h = img.shape[1], img.shape[0]
    width, height = input_dimension
    new_w = int(img_w * min(width / img_w, height / img_h))
    new_h = int(img_h * min(width / img_w, height / img_h))
    resized_image = cv2.resize(img, (new_w, new_h))
    canvas = np.full((input_dimension[1], input_dimension[0], 3), 0)
    canvas[(height - new_h) // 2:(height - new_h) // 2 + new_h,
           (width - new_w) // 2:(width - new_w) // 2 +
           new_w, :, ] = resized_image
    return canvas
