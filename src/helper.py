import os
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt

def recursive_find_all_files(top_folder_path:str, file_format:str) -> list:
    gathered_file_pathes = []

    for (root, directories, files) in os.walk(top_folder_path):
        for file in files:
            if file_format in file:
                file_path = os.path.join(root, file)
                gathered_file_pathes.append(file_path)

    return gathered_file_pathes


def niishow(nifti_file_path: str) -> np.array:
    nii = nib.load(nifti_file_path)
    nii_array = nii.get_fdata()
    print(nii_array.shape)

    try:
        #x,y,z가 아닐 수도 있으나, 단순 eda용으로 시각화
        x,y,z = nii_array.shape
        plt.imshow(nii_array[:,:,z/2])
    except Exception as e:
        print(e)
        pass

    sx, sy, sz = nii.header.get_zooms()
    volume_unit = sx * sy * sz
    print(f'sx=={sx}, sy=={sy}, sz=={sz}, volume_unit_of_nii=={volume_unit}')

    return nii_array
