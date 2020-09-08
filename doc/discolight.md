# Annotation Loaders


## FourCornersCSV

Loads annotations from a CSV file in the following format\.

image\_name, x\_min, y\_min, x\_max, y\_max, label

### Parameters


**annotations\_file** *(str)*, required<br/>
The path to the CSV file containing the annotations



**normalized** *(bool)* = True<br/>
whether the bounding box coordinates are stored in a normalized format







## PascalVOC

A Pascal VOC annotation loader\.

### Parameters


**annotations\_folder** *(str)*, required<br/>
The folder where the annotations are stored







## WidthHeightCSV

Loads annotations from a CSV file in the following format\.

image\_name, x\_min, y\_min, width, height, label

### Parameters


**annotations\_file** *(str)*, required<br/>
The path to the CSV file containing the annotations



**normalized** *(bool)* = True<br/>
whether the bounding box coordinates are stored in a normalized format







## YOLODarknet

A YOLO Darknet annotation loader\.

### Parameters


**annotations\_folder** *(str)*, required<br/>
The folder where the annotations are stored



**image\_ext** *(str)* = jpg<br/>
The file extension for loaded images








# Annotation Writers


## FourCornersCSV

Writes annotations to a CSV file in the following format\.

image\_name, x\_min, y\_min, x\_max, y\_max, label

### Parameters


**annotations\_file** *(str)*, required<br/>
The path to the CSV file to write the annotations to



**normalized** *(bool)* = True<br/>
whether the bounding box coordinates should be normalized before saving







## PascalVOC

A Pascal VOC annotation writer\.

### Parameters


**annotations\_folder** *(str)*, required<br/>
the directory to save annotation files to



**clean\_directory** *(bool)* = True<br/>
whether to forcibly ensure the output directory is empty



**database** *(str)* = <br/>
The name of the source database







## WidthHeightCSV

Writes annotations to a CSV file in the following format\.

image\_name, x\_min, y\_min, width, height, label

### Parameters


**annotations\_file** *(str)*, required<br/>
The path to the CSV file to write the annotations to



**normalized** *(bool)* = True<br/>
whether the bounding box coordinates should be normalized before saving







## YOLODarknet

A YOLO Darknet annotation writer\.

### Parameters


**annotations\_folder** *(str)*, required<br/>
the directory to save annotation files to



**clean\_directory** *(bool)* = True<br/>
whether to forcibly ensure the output directory is empty








# Image Loaders


## Directory

Load images from a directory in the filesystem\.

The image name from the AnnotationLoader will be used to fetch a file with
the same name in the given directory\.

### Parameters


**directory** *(str)*, required<br/>
The directory from which to load images








# Image Writers


## Directory

Writes images to a directory in the filesystem\.

Images will be saved to a file with the given name in the given directory\.

### Parameters


**clean\_directory** *(bool)* = True<br/>
whether to forcibly ensure the output directory is empty



**directory** *(str)*, required<br/>
the directory to save images to








# Augmentations


## ColorTemperature

Changes the color temperature of the input image\.

The class changes the color temperature to a value
between 1,000 and 40,000 Kelvins \(ie\. working as a
warming or cooling filter\)\.

This class has largely been adapted from @aleju/imgaug library's
augmenters\.ChangeColorTemperature\(\) function\. @aleju/imgaug
library can be found at <https://github\.com/aleju/imgaug/>

### Example
<table style="width: 100%">
<tr>
<td><b>Input Image</b></td>
<td><b>Augmented Image</b></td>
<td><b>Input Image<br/>(with Bounding Boxes)</b></td>
<td><b>Augmented Image<br/>(with Bounding Boxes)</b></td>
</tr>
<tr>
<td style="vertical-align: bottom">
<img src="images/ColorTemperature-input.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

<td style="vertical-align: bottom">
<img src="images/ColorTemperature.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

<td style="vertical-align: bottom">
<img src="images/ColorTemperature-input-bboxes.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

<td style="vertical-align: bottom">
<img src="images/ColorTemperature-bboxes.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

</tr>
</table>

### Parameters


**kelvin** *(int in range \[1000, 40000\])* = 3000<br/>
temperature value in to which temperature should be changed



**probs** *(float in range \[0\.0, 1\.0\])* = 1\.0<br/>
The probability that this augmentation will be applied









## GaussianNoise

Add gaussian noise to the given image\.

### Example
<table style="width: 100%">
<tr>
<td><b>Input Image</b></td>
<td><b>Augmented Image</b></td>
<td><b>Input Image<br/>(with Bounding Boxes)</b></td>
<td><b>Augmented Image<br/>(with Bounding Boxes)</b></td>
</tr>
<tr>
<td style="vertical-align: bottom">
<img src="images/GaussianNoise-input.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

<td style="vertical-align: bottom">
<img src="images/GaussianNoise.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

<td style="vertical-align: bottom">
<img src="images/GaussianNoise-input-bboxes.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

<td style="vertical-align: bottom">
<img src="images/GaussianNoise-bboxes.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

</tr>
</table>

### Parameters


**mean** *(float)* = 0<br/>




**probs** *(float in range \[0\.0, 1\.0\])* = 1\.0<br/>
The probability that this augmentation will be applied



**variance** *(float)* = 0\.01<br/>










## GrayScale

Return a grayscale version of the given image\.

### Example
<table style="width: 100%">
<tr>
<td><b>Input Image</b></td>
<td><b>Augmented Image</b></td>
<td><b>Input Image<br/>(with Bounding Boxes)</b></td>
<td><b>Augmented Image<br/>(with Bounding Boxes)</b></td>
</tr>
<tr>
<td style="vertical-align: bottom">
<img src="images/GrayScale-input.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

<td style="vertical-align: bottom">
<img src="images/GrayScale.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

<td style="vertical-align: bottom">
<img src="images/GrayScale-input-bboxes.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

<td style="vertical-align: bottom">
<img src="images/GrayScale-bboxes.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

</tr>
</table>

### Parameters


**probs** *(float in range \[0\.0, 1\.0\])* = 1\.0<br/>
The probability that this augmentation will be applied









## HorizontalFlip

Horizontally flips the given image\.

### Example
<table style="width: 100%">
<tr>
<td><b>Input Image</b></td>
<td><b>Augmented Image</b></td>
<td><b>Input Image<br/>(with Bounding Boxes)</b></td>
<td><b>Augmented Image<br/>(with Bounding Boxes)</b></td>
</tr>
<tr>
<td style="vertical-align: bottom">
<img src="images/HorizontalFlip-input.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

<td style="vertical-align: bottom">
<img src="images/HorizontalFlip.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

<td style="vertical-align: bottom">
<img src="images/HorizontalFlip-input-bboxes.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

<td style="vertical-align: bottom">
<img src="images/HorizontalFlip-bboxes.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

</tr>
</table>

### Parameters


**probs** *(float in range \[0\.0, 1\.0\])* = 1\.0<br/>
The probability that this augmentation will be applied









## ImageCompression

Apply a compression effect to the given image\.

This function is a lossy JPEG compression operation\.

### Example
<table style="width: 100%">
<tr>
<td><b>Input Image</b></td>
<td><b>Augmented Image</b></td>
<td><b>Input Image<br/>(with Bounding Boxes)</b></td>
<td><b>Augmented Image<br/>(with Bounding Boxes)</b></td>
</tr>
<tr>
<td style="vertical-align: bottom">
<img src="images/ImageCompression-input.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

<td style="vertical-align: bottom">
<img src="images/ImageCompression.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

<td style="vertical-align: bottom">
<img src="images/ImageCompression-input-bboxes.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

<td style="vertical-align: bottom">
<img src="images/ImageCompression-bboxes.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

</tr>
</table>

### Parameters


**probs** *(float in range \[0\.0, 1\.0\])* = 1\.0<br/>
The probability that this augmentation will be applied



**strength** *(int in range \[0, 100\])* = 1<br/>
Compression strength









## MotionBlur

Add motionblur to a given image\.

### Example
<table style="width: 100%">
<tr>
<td><b>Input Image</b></td>
<td><b>Augmented Image</b></td>
<td><b>Input Image<br/>(with Bounding Boxes)</b></td>
<td><b>Augmented Image<br/>(with Bounding Boxes)</b></td>
</tr>
<tr>
<td style="vertical-align: bottom">
<img src="images/MotionBlur-input.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

<td style="vertical-align: bottom">
<img src="images/MotionBlur.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

<td style="vertical-align: bottom">
<img src="images/MotionBlur-input-bboxes.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

<td style="vertical-align: bottom">
<img src="images/MotionBlur-bboxes.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

</tr>
</table>

### Parameters


**direction** *(DOWN \| UP \| RIGHT \| LEFT \| TOPRIGHT \| TOPLEFT \| BOTTOMLEFT \| BOTTOMRIGHT)* = DOWN<br/>
direction in which the blur is pointer towards



**kernel\_size** *(int in range \[0, Inf\])* = 10<br/>
Specify the kernel size, greater the size, the more the motion



**probs** *(float in range \[0\.0, 1\.0\])* = 1\.0<br/>
The probability that this augmentation will be applied





Sample image augmented with options:
```
kernel_size: 100
```





## RandomCrop

Randomly crops the given image\.

### Example
<table style="width: 100%">
<tr>
<td><b>Input Image</b></td>
<td><b>Augmented Image</b></td>
<td><b>Input Image<br/>(with Bounding Boxes)</b></td>
<td><b>Augmented Image<br/>(with Bounding Boxes)</b></td>
</tr>
<tr>
<td style="vertical-align: bottom">
<img src="images/RandomCrop-input.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

<td style="vertical-align: bottom">
<img src="images/RandomCrop.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

<td style="vertical-align: bottom">
<img src="images/RandomCrop-input-bboxes.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

<td style="vertical-align: bottom">
<img src="images/RandomCrop-bboxes.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

</tr>
</table>

### Parameters


**max\_height** *(float in range \[0, 1\])* = 0\.7<br/>
Maximum height of cropped area \(normalized\)



**max\_width** *(float in range \[0, 1\])* = 0\.7<br/>
Maximum width of cropped area \(normalized\)



**probs** *(float in range \[0\.0, 1\.0\])* = 1\.0<br/>
The probability that this augmentation will be applied





Sample image augmented with options:
```
max_height: 0.9
max_width: 0.9
```





## RandomEraser

Randomly erase a rectangular area in the given image\.

The erased area is replaced with random noise\.

### Example
<table style="width: 100%">
<tr>
<td><b>Input Image</b></td>
<td><b>Augmented Image</b></td>
<td><b>Input Image<br/>(with Bounding Boxes)</b></td>
<td><b>Augmented Image<br/>(with Bounding Boxes)</b></td>
</tr>
<tr>
<td style="vertical-align: bottom">
<img src="images/RandomEraser-input.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

<td style="vertical-align: bottom">
<img src="images/RandomEraser.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

<td style="vertical-align: bottom">
<img src="images/RandomEraser-input-bboxes.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

<td style="vertical-align: bottom">
<img src="images/RandomEraser-bboxes.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

</tr>
</table>

### Parameters


**probs** *(float in range \[0\.0, 1\.0\])* = 1\.0<br/>
The probability that this augmentation will be applied



**x\_range** *(range in \[0\.0, 1\.0\])* = \(0\.0, 1\.0\)<br/>
normalized x range for coordinates that may be erased



**y\_range** *(range in \[0\.0, 1\.0\])* = \(0\.0, 1\.0\)<br/>
normalized y range for coordinates that may be erased









## RandomHSV

Randomly shift the color space of the given image\.

### Example
<table style="width: 100%">
<tr>
<td><b>Input Image</b></td>
<td><b>Augmented Image</b></td>
<td><b>Input Image<br/>(with Bounding Boxes)</b></td>
<td><b>Augmented Image<br/>(with Bounding Boxes)</b></td>
</tr>
<tr>
<td style="vertical-align: bottom">
<img src="images/RandomHSV-input.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

<td style="vertical-align: bottom">
<img src="images/RandomHSV.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

<td style="vertical-align: bottom">
<img src="images/RandomHSV-input-bboxes.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

<td style="vertical-align: bottom">
<img src="images/RandomHSV-bboxes.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

</tr>
</table>

### Parameters


**brightness** *(range in \[\-Inf, Inf\])* = \(0\.0, 0\.0\)<br/>




**hue** *(range in \[\-Inf, Inf\])* = \(0\.0, 0\.0\)<br/>




**probs** *(float in range \[0\.0, 1\.0\])* = 1\.0<br/>
The probability that this augmentation will be applied



**saturation** *(range in \[\-Inf, Inf\])* = \(0\.0, 0\.0\)<br/>










## RandomRotate

Randomly rotate the given image\.

### Example
<table style="width: 100%">
<tr>
<td><b>Input Image</b></td>
<td><b>Augmented Image</b></td>
<td><b>Input Image<br/>(with Bounding Boxes)</b></td>
<td><b>Augmented Image<br/>(with Bounding Boxes)</b></td>
</tr>
<tr>
<td style="vertical-align: bottom">
<img src="images/RandomRotate-input.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

<td style="vertical-align: bottom">
<img src="images/RandomRotate.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

<td style="vertical-align: bottom">
<img src="images/RandomRotate-input-bboxes.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

<td style="vertical-align: bottom">
<img src="images/RandomRotate-bboxes.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

</tr>
</table>

### Parameters


**angle\_range** *(range in \[\-360\.0, 360\.0\])* = \(\-10\.0, 10\.0\)<br/>
The range from which the random angle will be chosen



**probs** *(float in range \[0\.0, 1\.0\])* = 1\.0<br/>
The probability that this augmentation will be applied









## Resize

Resize an image without preserving aspect ratio\.

### Example
<table style="width: 100%">
<tr>
<td><b>Input Image</b></td>
<td><b>Augmented Image</b></td>
<td><b>Input Image<br/>(with Bounding Boxes)</b></td>
<td><b>Augmented Image<br/>(with Bounding Boxes)</b></td>
</tr>
<tr>
<td style="vertical-align: bottom">
<img src="images/Resize-input.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

<td style="vertical-align: bottom">
<img src="images/Resize.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

<td style="vertical-align: bottom">
<img src="images/Resize-input-bboxes.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

<td style="vertical-align: bottom">
<img src="images/Resize-bboxes.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

</tr>
</table>

### Parameters


**height** *(int in range \[0, Inf\])* = 512<br/>
The height of the resized image



**interpolation** *(INTER\_NEAREST \| INTER\_LINEAR \| INTER\_AREA \| INTER\_CUBIC \| INTER\_LANCZOS4)* = INTER\_LINEAR<br/>
The interpolation type



**probs** *(float in range \[0\.0, 1\.0\])* = 1\.0<br/>
The probability that this augmentation will be applied



**width** *(int in range \[0, Inf\])* = 512<br/>
the width of the resized image









## ResizeMaintainAspectRatio

Resize an image while preserving aspect ratio\.

### Example
<table style="width: 100%">
<tr>
<td><b>Input Image</b></td>
<td><b>Augmented Image</b></td>
<td><b>Input Image<br/>(with Bounding Boxes)</b></td>
<td><b>Augmented Image<br/>(with Bounding Boxes)</b></td>
</tr>
<tr>
<td style="vertical-align: bottom">
<img src="images/ResizeMaintainAspectRatio-input.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

<td style="vertical-align: bottom">
<img src="images/ResizeMaintainAspectRatio.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

<td style="vertical-align: bottom">
<img src="images/ResizeMaintainAspectRatio-input-bboxes.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

<td style="vertical-align: bottom">
<img src="images/ResizeMaintainAspectRatio-bboxes.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

</tr>
</table>

### Parameters


**input\_dim** *(int in range \[0, Inf\])* = 512<br/>
The new length of the shortest dimension



**interpolation** *(INTER\_NEAREST \| INTER\_LINEAR \| INTER\_AREA \| INTER\_CUBIC \| INTER\_LANCZOS4)* = INTER\_LINEAR<br/>
The interpolation type



**probs** *(float in range \[0\.0, 1\.0\])* = 1\.0<br/>
The probability that this augmentation will be applied









## Rotate

Rotate the given image\.

### Example
<table style="width: 100%">
<tr>
<td><b>Input Image</b></td>
<td><b>Augmented Image</b></td>
<td><b>Input Image<br/>(with Bounding Boxes)</b></td>
<td><b>Augmented Image<br/>(with Bounding Boxes)</b></td>
</tr>
<tr>
<td style="vertical-align: bottom">
<img src="images/Rotate-input.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

<td style="vertical-align: bottom">
<img src="images/Rotate.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

<td style="vertical-align: bottom">
<img src="images/Rotate-input-bboxes.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

<td style="vertical-align: bottom">
<img src="images/Rotate-bboxes.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

</tr>
</table>

### Parameters


**angle** *(float)* = 5<br/>




**probs** *(float in range \[0\.0, 1\.0\])* = 1\.0<br/>
The probability that this augmentation will be applied









## SaltAndPepperNoise

Add salt and pepper or RGB noise to the given image\.

### Example
<table style="width: 100%">
<tr>
<td><b>Input Image</b></td>
<td><b>Augmented Image</b></td>
<td><b>Input Image<br/>(with Bounding Boxes)</b></td>
<td><b>Augmented Image<br/>(with Bounding Boxes)</b></td>
</tr>
<tr>
<td style="vertical-align: bottom">
<img src="images/SaltAndPepperNoise-input.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

<td style="vertical-align: bottom">
<img src="images/SaltAndPepperNoise.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

<td style="vertical-align: bottom">
<img src="images/SaltAndPepperNoise-input-bboxes.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

<td style="vertical-align: bottom">
<img src="images/SaltAndPepperNoise-bboxes.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

</tr>
</table>

### Parameters


**noise\_type** *(RGB \| SnP)* = RGB<br/>
The type of noise



**pepper** *(int in range \[0, 255\])* = 0<br/>
The color of the pepper



**probs** *(float in range \[0\.0, 1\.0\])* = 1\.0<br/>
The probability that this augmentation will be applied



**replace\_probs** *(float)* = 0\.1<br/>




**salt** *(int in range \[0, 255\])* = 255<br/>
The color of the salt









## Scale

Scale the given image\.

### Example
<table style="width: 100%">
<tr>
<td><b>Input Image</b></td>
<td><b>Augmented Image</b></td>
<td><b>Input Image<br/>(with Bounding Boxes)</b></td>
<td><b>Augmented Image<br/>(with Bounding Boxes)</b></td>
</tr>
<tr>
<td style="vertical-align: bottom">
<img src="images/Scale-input.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

<td style="vertical-align: bottom">
<img src="images/Scale.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

<td style="vertical-align: bottom">
<img src="images/Scale-input-bboxes.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

<td style="vertical-align: bottom">
<img src="images/Scale-bboxes.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

</tr>
</table>

### Parameters


**probs** *(float in range \[0\.0, 1\.0\])* = 1\.0<br/>
The probability that this augmentation will be applied



**scale\_x** *(float in range \[\-1\.0, Inf\])* = 0\.2<br/>




**scale\_y** *(float in range \[\-1\.0, Inf\])* = 0\.2<br/>










## Sepia

Returns a given image passed through the sepia filter\.

### Example
<table style="width: 100%">
<tr>
<td><b>Input Image</b></td>
<td><b>Augmented Image</b></td>
<td><b>Input Image<br/>(with Bounding Boxes)</b></td>
<td><b>Augmented Image<br/>(with Bounding Boxes)</b></td>
</tr>
<tr>
<td style="vertical-align: bottom">
<img src="images/Sepia-input.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

<td style="vertical-align: bottom">
<img src="images/Sepia.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

<td style="vertical-align: bottom">
<img src="images/Sepia-input-bboxes.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

<td style="vertical-align: bottom">
<img src="images/Sepia-bboxes.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

</tr>
</table>

### Parameters


**probs** *(float in range \[0\.0, 1\.0\])* = 1\.0<br/>
The probability that this augmentation will be applied









## Sequence

Perform a sequence of augmentations on the given image\.

### Example
<table style="width: 100%">
<tr>
<td><b>Input Image</b></td>
<td><b>Augmented Image</b></td>
<td><b>Input Image<br/>(with Bounding Boxes)</b></td>
<td><b>Augmented Image<br/>(with Bounding Boxes)</b></td>
</tr>
<tr>
<td style="vertical-align: bottom">
<img src="images/Sequence-input.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

<td style="vertical-align: bottom">
<img src="images/Sequence.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

<td style="vertical-align: bottom">
<img src="images/Sequence-input-bboxes.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

<td style="vertical-align: bottom">
<img src="images/Sequence-bboxes.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

</tr>
</table>

### Parameters


**augmentations** *(augmentation\_list)* = \[\]<br/>




**probs** *(float in range \[0\.0, 1\.0\])* = 1\.0<br/>
The probability that this augmentation will be applied





Sample image augmented with options:
```
augmentations:
- name: GrayScale
- name: Rotate
  options:
    angle: 35
- name: SaltAndPepperNoise
  options:
    noise_type: SnP
```





## Shear

Horizontally shear the given image\.

### Example
<table style="width: 100%">
<tr>
<td><b>Input Image</b></td>
<td><b>Augmented Image</b></td>
<td><b>Input Image<br/>(with Bounding Boxes)</b></td>
<td><b>Augmented Image<br/>(with Bounding Boxes)</b></td>
</tr>
<tr>
<td style="vertical-align: bottom">
<img src="images/Shear-input.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

<td style="vertical-align: bottom">
<img src="images/Shear.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

<td style="vertical-align: bottom">
<img src="images/Shear-input-bboxes.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

<td style="vertical-align: bottom">
<img src="images/Shear-bboxes.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

</tr>
</table>

### Parameters


**probs** *(float in range \[0\.0, 1\.0\])* = 1\.0<br/>
The probability that this augmentation will be applied



**shear\_factor** *(float)* = 0\.2<br/>










## Translate

Translate the given image\.

### Example
<table style="width: 100%">
<tr>
<td><b>Input Image</b></td>
<td><b>Augmented Image</b></td>
<td><b>Input Image<br/>(with Bounding Boxes)</b></td>
<td><b>Augmented Image<br/>(with Bounding Boxes)</b></td>
</tr>
<tr>
<td style="vertical-align: bottom">
<img src="images/Translate-input.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

<td style="vertical-align: bottom">
<img src="images/Translate.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

<td style="vertical-align: bottom">
<img src="images/Translate-input-bboxes.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

<td style="vertical-align: bottom">
<img src="images/Translate-bboxes.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

</tr>
</table>

### Parameters


**probs** *(float in range \[0\.0, 1\.0\])* = 1\.0<br/>
The probability that this augmentation will be applied



**translate\_x** *(float in range \[0\.0, 1\.0\])* = 0\.2<br/>




**translate\_y** *(float in range \[0\.0, 1\.0\])* = 0\.2<br/>










## VerticalFlip

Vertically flip the given image\.

### Example
<table style="width: 100%">
<tr>
<td><b>Input Image</b></td>
<td><b>Augmented Image</b></td>
<td><b>Input Image<br/>(with Bounding Boxes)</b></td>
<td><b>Augmented Image<br/>(with Bounding Boxes)</b></td>
</tr>
<tr>
<td style="vertical-align: bottom">
<img src="images/VerticalFlip-input.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

<td style="vertical-align: bottom">
<img src="images/VerticalFlip.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

<td style="vertical-align: bottom">
<img src="images/VerticalFlip-input-bboxes.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

<td style="vertical-align: bottom">
<img src="images/VerticalFlip-bboxes.jpg" width="235px" height="176px" style="display: block; width: 100%"/>
</td>

</tr>
</table>

### Parameters


**probs** *(float in range \[0\.0, 1\.0\])* = 1\.0<br/>
The probability that this augmentation will be applied








