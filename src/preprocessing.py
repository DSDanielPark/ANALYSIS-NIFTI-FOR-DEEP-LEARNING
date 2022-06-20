import numpy as np
import glob
import pandas as pd
import nibabel as nib
import monai


# monai cropforeground vs nonzero3darray



def if_minus_return_0(value):
    
    if np.sign(value) == -1:
        value = 0
    else:
        value
        
    return value

def makenonzero3darray(nifti_file_path: str, save_path: str, margin: int) -> None:
    
    file_name = nifti_file_path.split('\\')[-1].rstrip('nii.gz')
    
    nii = nib.load(nifti_file_path)
    nii_array = nii.get_fdata()
    original_affine = nii.affine
    print(nii.shape)
    
    non_zeros = np.nonzero(nii_array>3)

    x_min = non_zeros[0].min()
    x_max = non_zeros[0].max()

    y_min = non_zeros[1].min()
    y_max = non_zeros[1].max()

    z_min = non_zeros[2].min()
    z_max = non_zeros[2].max()
    
    
    
    clip_x_min = if_minus_return_0(x_min-margin)
    clip_x_max = if_minus_return_0(x_max+margin)
    
    clip_y_min = if_minus_return_0(y_min-margin)
    clip_y_max = if_minus_return_0(y_max-margin)
    
    clip_z_min = if_minus_return_0(z_min-margin)
    clip_z_max = if_minus_return_0(z_max-margin)
    
    
    
    nonzero3darray = nii_array[clip_x_min:clip_x_max, clip_y_min:clip_y_max, clip_z_min:clip_z_max]
    print(nonzero3darray.shape)
    
    img = nib.Nifti1Image(nonzero3darray, original_affine) 
    img.to_filename(f'{save_path}/{file_name}.nii.gz')
    
    return nonzero3darray



def threshold_at_two(x):
    # threshold at 2
    return x > 2


def monai_cropforeground(nifit_file_path:str, save_path: str):
    
    file_name = nifit_file_path.split('\\')[-1].rstrip('.nii.gz')

    img = nib.load(nifit_file_path)
    img_array = img.get_fdata()
    original_affine = img.affine
    cropper = monai.transforms.CropForeground(select_fn=threshold_at_two, margin=2)
    cropped_img = cropper(img_array)

    img = nib.Nifti1Image(cropped_img, original_affine) 
    img.to_filename(f'{save_path}/{file_name}.nii.gz')
