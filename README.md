# Waymo Open Dataset
Tools to download Waymo Open Dataset and extract point clouds and labels from the downloaded data samples.  
# Installation
First, install gsutil, tool to access Google Cloud Storage from the command line.
Follow the installation instruction in [here](https://cloud.google.com/storage/docs/gsutil_install).

Next, install conda, package and environment management system for python. Follow the installation instructions [here](https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html). 

Finally, install the library through conda:
```
conda env update -f env/environment.yml --prune
```
# How to use
To download Waymo Open Dataset and extract tf records from the downloaded archives:
```
python download_and_extract_waymo_data_archives.py --output-dir --split --max-archive-files
```
To extract point clouds and labels from the tf records
```
python extract_point_clouds_and_labels.py --input-dir --output-dir
```