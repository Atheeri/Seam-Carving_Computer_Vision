# Seam-Carving_Computer_Vision

# Introduction 
Most of digital images are viewed in different devices with a variety of resolutions. the shift of multiple device make the resolution of viewing images difficult because they usually are resized to shape limited space.Resizing an image’s height and width can cause distortion if not using an effective algorithm. One such algorithm is seam carving which allows for resizing by still maintaining the important features of an image.This allows you to make carvings of the image but keep the most important features of the image during the resizing process. The purpose of seam carving algorithm is image retargeting, which is the issue in images displaying without deformation on media of various sizes such as cell phones, or projection screens. In this paper we will introduce multiple applications of seam craving algorithm, and discuss in deep the method about it.In addition, we will also shows a new energy criterion for improving the visual quality of retargeted images and videos. The original seam carving operator focuses on deleting seams with the least amount of energy while ignoring the energy put into the photos and video by applying the operator. To combat this, the new criterion for reducing seams will be to look forward. This method is referred as forward energy it predicts which pixels would be nearest after removing a seam and uses that data to suggest the optimum seam to eliminate. This is in contrast to the traditional approach’s backward energy.

# Requirements: 				
1.	Implementation of the base algorithm from the paper for reducing image’s height and width.
2.	Ability to increase an image’s height and width
3.	Implementation of forward energy from the followup paper.
4.	Adding one novel energy adjustment (i.e., face detection, object detection, etc). 

# Source Code Files: 

●	seam_carving_parts_1_and_2.py
●	seam_carving_parts_3_and_4.py


File 1: seam_carving_parts_1_and_2.py

The code for parts 1 and 2. This script is using python3. A sample run of this file would look like:

python3 seam_carving_parts_1_and_2.py input_image output_image increase/decrease numbersOfHorizontalSeams numbersOfVerticalSeams
 
# Here are some sample commands that one can use, you can copy these commands and use them in tux with the attached images:

python3 seam_carving_parts_1_and_2.py pasta.jpg newpasta.png decrease 20 20
python3 seam_carving_parts_1_and_2.py Small_scream.png output1.png increase 10 10
python3 seam_carving_parts_1_and_2.py frog.jpg newfrog.jpg increase 5 5
python3 seam_carving_parts_1_and_2.py Small_scream.png smaller_scream.jpg decrease 10 10

