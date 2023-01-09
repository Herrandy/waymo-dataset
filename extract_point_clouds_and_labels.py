import argparse
import os
import glob
import json

import numpy as np
import tensorflow as tf
from waymo_open_dataset.dataset_pb2 import Frame
from waymo_open_dataset import label_pb2
from waymo_open_dataset.utils import frame_utils


def create_folder(folder_dir):
    if not os.path.exists(folder_dir):
        os.makedirs(folder_dir)


def save_pc(filename, pc):
    with open(filename, "wb") as f:
        pc.tofile(f)


def save_labels(filename, labels):
    labels_arr = []
    for label in labels:
        labels_arr.append(waymo_label_to_dict(label))

    with open(filename, "w") as f:
        json.dump(labels_arr, f)


def waymo_label_to_dict(label):

    if label.type == label_pb2.Label.Type.TYPE_VEHICLE:
        label_type = "vehicle"
    elif label.type == label_pb2.Label.Type.TYPE_PEDESTRIAN:
        label_type = "pedestrian"
    elif label.type == label_pb2.Label.Type.TYPE_SIGN:
        label_type = "sign"
    elif label.type == label_pb2.Label.Type.TYPE_CYCLIST:
        label_type = "cyclist"
    else:
        raise TypeError(f"Unknown label type {label.type}")

    label_dict = {
        "position": [label.box.center_x, label.box.center_y, label.box.center_z],
        "extent": [label.box.width, label.box.length, label.box.height],
        "rotation": [0.0, 0.0, label.box.heading],
        "num_lidar_points_in_box": label.num_lidar_points_in_box,
        "label_type": label_type,
    }
    return label_dict


def pc_from_range_image(frame):
    def _range_image_to_pc(ri_index):
        pc, _ = frame_utils.convert_range_image_to_point_cloud(
            frame, range_images, camera_projections, range_image_top_pose, ri_index=ri_index, keep_polar_features=True
        )
        return pc

    parsed_frame = frame_utils.parse_range_image_and_camera_projection(frame)
    range_images, camera_projections, _, range_image_top_pose = parsed_frame
    frame.lasers.sort(key=lambda laser: laser.name)
    return _range_image_to_pc(0), _range_image_to_pc(1)


def process_data(data):
    frame = Frame()
    frame.ParseFromString(bytearray(data.numpy()))
    pc_return_1, pc_return_2 = pc_from_range_image(frame)
    all_points = np.concatenate(pc_return_1 + pc_return_2, axis=0)
    labels = frame.laser_labels
    return all_points, labels


def process_records(input_dir, output_dir):
    records = glob.glob(os.path.join(input_dir, "*.tfrecord"))
    print(f"Found {len(records)} tf record(s)")

    output_pc_dir = os.path.join(output_dir, "pcs")
    output_label_dir = os.path.join(output_dir, "labels")
    create_folder(output_pc_dir)
    create_folder(output_label_dir)

    for record in records:
        print(f"Processing record {record}")
        data_set = tf.data.TFRecordDataset(record, compression_type="")
        for idx, data in enumerate(data_set):
            print(f"Frame index: {idx}")
            pc, labels = process_data(data)

            pc_filename = os.path.join(output_pc_dir, str(idx).zfill(5) + ".bin")
            labels_filename = os.path.join(output_label_dir, str(idx).zfill(5) + ".json")
            save_pc(pc_filename, pc)
            save_labels(labels_filename, labels)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create video from the dataset")
    parser.add_argument("-i", "--input-dir", default="/media/antti/Sensible4_2TB/datasets/waymo_dataset")
    parser.add_argument("-o", "--output-dir", default="output")
    args = parser.parse_args()
    process_records(args.input_dir, args.output_dir)
