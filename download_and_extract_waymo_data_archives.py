import os
import argparse

from common_utils import create_folder


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="output_dir")
    parser.add_argument("--split", choices=["training", "validation"], default="training")
    parser.add_argument("--max-archive-files", default=5, type=int)
    args = parser.parse_args()

    output_dir, max_archive_files, split = args.output_dir, args.max_archive_files, args.split
    url_template = "gs://waymo_open_dataset_v_1_4_1/archived_files/{split}/{split}_%04d.tar".format(split=split)
    create_folder(output_dir)

    for archive_id in range(0, max_archive_files):
        flag = os.system("gsutil cp " + url_template % archive_id + " " + output_dir)
        assert flag == 0, "Failed to download segment %d. Make sure gsutil is installed" % archive_id
        os.system("cd %s; tar xf %s_%04d.tar" % (output_dir, split, archive_id))


if __name__ == "__main__":
    main()
