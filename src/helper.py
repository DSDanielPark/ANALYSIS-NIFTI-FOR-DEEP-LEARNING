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
    '''
    nifti path를 인풋으로 받아서, xyz spacing 및 z축 위치의 절반을 보여줍니다. xyz축으로 정렬되어있다고 가정합니다.
    '''
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



############
def get_mask_nii_path(nii_list, subject_numb, mask_word):
    '''
    this method used in method(get_matching_path_dict)
    
    args
    nii_list: globbed nii list(raw and mask)
    subject_numb: only for BIDS format file name must be has subject and modality
    mask_word: only for BIDS format, mask file include 'msk' or 'mask' word in file name
    '''

    mask_nii_path = None
    for nii_path in nii_list:
        if subject_numb in nii_path and mask_word in nii_path:
            mask_nii_path = nii_path

    return mask_nii_path



def get_matching_path_dict(nii_list, maskword): 
    '''
    args
    nii_list: BIDS 포맷으로 된 raw, mask 파일패스가 glob으로 담긴 리스트 1개
    maskword: 'msk' or 'mask'와 같이 파일명에 있는 mask 파일 표시단어
    '''
    matching_path_dict = dict()
    for nii_path in nii_list:

        if 'msk' not in nii_path:
            raw_nii = nii_path
            
            subject = nii_path.split('//')[-1].split('_')[0]

            mask_nii_path = get_mask_nii_path(nii_list, subject, maskword)

            matching_path_dict[raw_nii] = mask_nii_path

        else:
            pass
    
    return matching_path_dict