import os
import nibabel as nib
import numpy as np

path1 = os.getcwd() + '/data/outputsTs_2d'
file_list1 = os.listdir(path1)
file_list_nii1 = [file for file in file_list1 if file.endswith(".nii.gz")]
#print(len(file_list_nii1))
#print ("file_list_py: {}".format(file_list_nii1))

path2 = os.getcwd() + '/data/outputsTs_3dfullres'
file_list2 = os.listdir(path2)
file_list_nii2 = [file for file in file_list2 if file.endswith(".nii.gz")]


img1_path = path1+"/"+file_list_nii1[0]
img1 = nib.load(img1_path) #nifti 파일에서 이미지 영역만 가져오기
img1_affine = img1.affine ########## img1 affine metrix 저장

numpy1 = np.array(img1.dataobj) #numpy 자료형으로 변경
img2_path = path2+"/"+file_list_nii2[0]
img2 = nib.load(img2_path)
img2_affine = img2.affine ########## img1 affine metrix 저장

print(f'diff affine_metrix between 2 nifti image: {img1_affine-img2_affine}')

numpy2 = np.array(img2.dataobj)

element_1 = np.unique(numpy1) #Inference 값이 0, 1로 구성되어 있는지 체크
element_2 = np.unique(numpy2) 

voxel1 = np.count_nonzero(numpy1) #segmented voxel 개수 확인
voxel2 = np.count_nonzero(numpy2) 

numpy3 = np.logical_or(numpy1, numpy2) #union
numpy3 = numpy3.astype(np.int8)
voxel3 = np.count_nonzero(numpy3) 

##########Pos
img = nib.Nifti1Image(numpy3, img1_affine)  # Save axis for data (just identity) ######### 이미지1 affine metrix로 플로팅함
img.header.get_xyzt_units()

path3= path1 = os.getcwd() + '/data'

img.to_filename(os.path.join(path3,'test4d.nii.gz'))  # Save as NiBabel file

print("check")