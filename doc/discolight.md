# Annotation Loaders


## FourCornersCSV

Loads annotations from a CSV file in the following format\.

image\_name, x\_min, y\_min, x\_max, y\_max, label

### Parameters


**annotations\_file** *(str)*, required<br/>
The path to the CSV file containing the annotations



**normalized** *(bool)* = True<br/>
whether the bounding box coordinates are stored in a normalized format







## WidthHeightCSV

Loads annotations from a CSV file in the following format\.

image\_name, x\_min, y\_min, width, height, label

### Parameters


**annotations\_file** *(str)*, required<br/>
The path to the CSV file containing the annotations



**normalized** *(bool)* = True<br/>
whether the bounding box coordinates are stored in a normalized format








# Annotation Writers


## FourCornersCSV

Writes annotations to a CSV file in the following format\.

image\_name, x\_min, y\_min, x\_max, y\_max, label

### Parameters


**annotations\_file** *(str)*, required<br/>
The path to the CSV file to write the annotations to



**normalized** *(bool)* = True<br/>
whether the bounding box coordinates should be normalized before saving







## WidthHeightCSV

Writes annotations to a CSV file in the following format\.

image\_name, x\_min, y\_min, width, height, label

### Parameters


**annotations\_file** *(str)*, required<br/>
The path to the CSV file to write the annotations to



**normalized** *(bool)* = True<br/>
whether the bounding box coordinates should be normalized before saving








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


## GaussianNoise

Add gaussian noise to the given image\.

### Example
<table style="width: 100%">
<tr>
<td style="vertical-align: bottom">
<img src="images/GaussianNoise-input.jpg" style="display: block; width: 100%"/>
<br/>
Input Image
</td>

<td style="vertical-align: bottom">
<img src="images/GaussianNoise.jpg" style="display: block; width: 100%"/>
<br/>
Augmented Image
</td>

<td style="vertical-align: bottom">
<img src="images/GaussianNoise-input-bboxes.jpg" style="display: block; width: 100%"/>
<br/>
Input Image (with Bounding Boxes)
</td>

<td style="vertical-align: bottom">
<img src="images/GaussianNoise-bboxes.jpg" style="display: block; width: 100%"/>
<br/>
Augmented Image (with Bounding Boxes)
</td>

</tr>
</table>

### Parameters


**mean** *(float)* = 0<br/>




**probs** *(float)* = 1\.0<br/>
The probability that this augmentation will be applied


* must be between 0 and 1


**variance** *(float)* = 0\.01<br/>








## GrayScale

Return a grayscale version of the given image\.

### Example
<table style="width: 100%">
<tr>
<td style="vertical-align: bottom">
<img src="images/GrayScale-input.jpg" style="display: block; width: 100%"/>
<br/>
Input Image
</td>

<td style="vertical-align: bottom">
<img src="images/GrayScale.jpg" style="display: block; width: 100%"/>
<br/>
Augmented Image
</td>

<td style="vertical-align: bottom">
<img src="images/GrayScale-input-bboxes.jpg" style="display: block; width: 100%"/>
<br/>
Input Image (with Bounding Boxes)
</td>

<td style="vertical-align: bottom">
<img src="images/GrayScale-bboxes.jpg" style="display: block; width: 100%"/>
<br/>
Augmented Image (with Bounding Boxes)
</td>

</tr>
</table>

### Parameters


**probs** *(float)* = 1\.0<br/>
The probability that this augmentation will be applied


* must be between 0 and 1






## HorizontalFlip

Horizontally flips the given image\.

### Example
<table style="width: 100%">
<tr>
<td style="vertical-align: bottom">
<img src="images/HorizontalFlip-input.jpg" style="display: block; width: 100%"/>
<br/>
Input Image
</td>

<td style="vertical-align: bottom">
<img src="images/HorizontalFlip.jpg" style="display: block; width: 100%"/>
<br/>
Augmented Image
</td>

<td style="vertical-align: bottom">
<img src="images/HorizontalFlip-input-bboxes.jpg" style="display: block; width: 100%"/>
<br/>
Input Image (with Bounding Boxes)
</td>

<td style="vertical-align: bottom">
<img src="images/HorizontalFlip-bboxes.jpg" style="display: block; width: 100%"/>
<br/>
Augmented Image (with Bounding Boxes)
</td>

</tr>
</table>

### Parameters


**probs** *(float)* = 1\.0<br/>
The probability that this augmentation will be applied


* must be between 0 and 1






## RandomEraser

Randomly erase a rectangular area in the given image\.

The erased area is replaced with random noise\.

### Example
<table style="width: 100%">
<tr>
<td style="vertical-align: bottom">
<img src="images/RandomEraser-input.jpg" style="display: block; width: 100%"/>
<br/>
Input Image
</td>

<td style="vertical-align: bottom">
<img src="images/RandomEraser.jpg" style="display: block; width: 100%"/>
<br/>
Augmented Image
</td>

<td style="vertical-align: bottom">
<img src="images/RandomEraser-input-bboxes.jpg" style="display: block; width: 100%"/>
<br/>
Input Image (with Bounding Boxes)
</td>

<td style="vertical-align: bottom">
<img src="images/RandomEraser-bboxes.jpg" style="display: block; width: 100%"/>
<br/>
Augmented Image (with Bounding Boxes)
</td>

</tr>
</table>

### Parameters


**probs** *(float)* = 1\.0<br/>
The probability that this augmentation will be applied


* must be between 0 and 1


**x\_max** *(float)* = \-1<br/>




**x\_min** *(float)* = 0<br/>




**y\_max** *(float)* = \-1<br/>




**y\_min** *(float)* = 0<br/>








## RandomHSV

Randomly shift the color space of the given image\.

### Example
<table style="width: 100%">
<tr>
<td style="vertical-align: bottom">
<img src="images/RandomHSV-input.jpg" style="display: block; width: 100%"/>
<br/>
Input Image
</td>

<td style="vertical-align: bottom">
<img src="images/RandomHSV.jpg" style="display: block; width: 100%"/>
<br/>
Augmented Image
</td>

<td style="vertical-align: bottom">
<img src="images/RandomHSV-input-bboxes.jpg" style="display: block; width: 100%"/>
<br/>
Input Image (with Bounding Boxes)
</td>

<td style="vertical-align: bottom">
<img src="images/RandomHSV-bboxes.jpg" style="display: block; width: 100%"/>
<br/>
Augmented Image (with Bounding Boxes)
</td>

</tr>
</table>

### Parameters


**brightness** *(tuple)* = \(0, 0\)<br/>




**hue** *(tuple)* = \(0, 0\)<br/>




**probs** *(float)* = 1\.0<br/>
The probability that this augmentation will be applied


* must be between 0 and 1


**saturation** *(tuple)* = \(0, 0\)<br/>








## RandomRotate

Randomly rotate the given image\.

### Example
<table style="width: 100%">
<tr>
<td style="vertical-align: bottom">
<img src="images/RandomRotate-input.jpg" style="display: block; width: 100%"/>
<br/>
Input Image
</td>

<td style="vertical-align: bottom">
<img src="images/RandomRotate.jpg" style="display: block; width: 100%"/>
<br/>
Augmented Image
</td>

<td style="vertical-align: bottom">
<img src="images/RandomRotate-input-bboxes.jpg" style="display: block; width: 100%"/>
<br/>
Input Image (with Bounding Boxes)
</td>

<td style="vertical-align: bottom">
<img src="images/RandomRotate-bboxes.jpg" style="display: block; width: 100%"/>
<br/>
Augmented Image (with Bounding Boxes)
</td>

</tr>
</table>

### Parameters


**max\_angle** *(float)* = 10<br/>



* min\_angle must be less than max\_angle


**min\_angle** *(float)* = \-10<br/>



* must be less than max\_angle


**probs** *(float)* = 1\.0<br/>
The probability that this augmentation will be applied


* must be between 0 and 1






## Rotate

Rotate the given image\.

### Example
<table style="width: 100%">
<tr>
<td style="vertical-align: bottom">
<img src="images/Rotate-input.jpg" style="display: block; width: 100%"/>
<br/>
Input Image
</td>

<td style="vertical-align: bottom">
<img src="images/Rotate.jpg" style="display: block; width: 100%"/>
<br/>
Augmented Image
</td>

<td style="vertical-align: bottom">
<img src="images/Rotate-input-bboxes.jpg" style="display: block; width: 100%"/>
<br/>
Input Image (with Bounding Boxes)
</td>

<td style="vertical-align: bottom">
<img src="images/Rotate-bboxes.jpg" style="display: block; width: 100%"/>
<br/>
Augmented Image (with Bounding Boxes)
</td>

</tr>
</table>

### Parameters


**angle** *(float)* = 5<br/>




**probs** *(float)* = 1\.0<br/>
The probability that this augmentation will be applied


* must be between 0 and 1






## SaltAndPepperNoise

Add salt and pepper or RGB noise to the given image\.

### Example
<table style="width: 100%">
<tr>
<td style="vertical-align: bottom">
<img src="images/SaltAndPepperNoise-input.jpg" style="display: block; width: 100%"/>
<br/>
Input Image
</td>

<td style="vertical-align: bottom">
<img src="images/SaltAndPepperNoise.jpg" style="display: block; width: 100%"/>
<br/>
Augmented Image
</td>

<td style="vertical-align: bottom">
<img src="images/SaltAndPepperNoise-input-bboxes.jpg" style="display: block; width: 100%"/>
<br/>
Input Image (with Bounding Boxes)
</td>

<td style="vertical-align: bottom">
<img src="images/SaltAndPepperNoise-bboxes.jpg" style="display: block; width: 100%"/>
<br/>
Augmented Image (with Bounding Boxes)
</td>

</tr>
</table>

### Parameters


**noise\_type** *(str)* = RGB<br/>
The type of noise \(RGB or SnP\)


* must be RGB or SnP


**pepper** *(int)* = 0<br/>
The color of the pepper


* must be between 0 and 255


**probs** *(float)* = 1\.0<br/>
The probability that this augmentation will be applied


* must be between 0 and 1


**replace\_probs** *(float)* = 0\.1<br/>




**salt** *(int)* = 255<br/>
The color of the salt


* must be between 0 and 255






## Scale

Scale the given image\.

### Example
<table style="width: 100%">
<tr>
<td style="vertical-align: bottom">
<img src="images/Scale-input.jpg" style="display: block; width: 100%"/>
<br/>
Input Image
</td>

<td style="vertical-align: bottom">
<img src="images/Scale.jpg" style="display: block; width: 100%"/>
<br/>
Augmented Image
</td>

<td style="vertical-align: bottom">
<img src="images/Scale-input-bboxes.jpg" style="display: block; width: 100%"/>
<br/>
Input Image (with Bounding Boxes)
</td>

<td style="vertical-align: bottom">
<img src="images/Scale-bboxes.jpg" style="display: block; width: 100%"/>
<br/>
Augmented Image (with Bounding Boxes)
</td>

</tr>
</table>

### Parameters


**probs** *(float)* = 1\.0<br/>
The probability that this augmentation will be applied


* must be between 0 and 1


**scale\_x** *(float)* = 0\.2<br/>



* cannot be less than \-1


**scale\_y** *(float)* = 0\.2<br/>



* cannot be less than \-1






## Sepia

Returns a given image passed through the sepia filter\.

### Example
<table style="width: 100%">
<tr>
<td style="vertical-align: bottom">
<img src="images/Sepia-input.jpg" style="display: block; width: 100%"/>
<br/>
Input Image
</td>

<td style="vertical-align: bottom">
<img src="images/Sepia.jpg" style="display: block; width: 100%"/>
<br/>
Augmented Image
</td>

<td style="vertical-align: bottom">
<img src="images/Sepia-input-bboxes.jpg" style="display: block; width: 100%"/>
<br/>
Input Image (with Bounding Boxes)
</td>

<td style="vertical-align: bottom">
<img src="images/Sepia-bboxes.jpg" style="display: block; width: 100%"/>
<br/>
Augmented Image (with Bounding Boxes)
</td>

</tr>
</table>

### Parameters


**probs** *(float)* = 1\.0<br/>
The probability that this augmentation will be applied


* must be between 0 and 1






## Sequence

Perform a sequence of augmentations on the given image\.

### Example
<table style="width: 100%">
<tr>
<td style="vertical-align: bottom">
<img src="images/Sequence-input.jpg" style="display: block; width: 100%"/>
<br/>
Input Image
</td>

<td style="vertical-align: bottom">
<img src="images/Sequence.jpg" style="display: block; width: 100%"/>
<br/>
Augmented Image
</td>

<td style="vertical-align: bottom">
<img src="images/Sequence-input-bboxes.jpg" style="display: block; width: 100%"/>
<br/>
Input Image (with Bounding Boxes)
</td>

<td style="vertical-align: bottom">
<img src="images/Sequence-bboxes.jpg" style="display: block; width: 100%"/>
<br/>
Augmented Image (with Bounding Boxes)
</td>

</tr>
</table>

### Parameters


**augmentations** *(augmentation\_list)* = \[\]<br/>




**probs** *(float)* = 1\.0<br/>
The probability that this augmentation will be applied


* must be between 0 and 1






## Shear

Horizontally shear the given image\.

### Example
<table style="width: 100%">
<tr>
<td style="vertical-align: bottom">
<img src="images/Shear-input.jpg" style="display: block; width: 100%"/>
<br/>
Input Image
</td>

<td style="vertical-align: bottom">
<img src="images/Shear.jpg" style="display: block; width: 100%"/>
<br/>
Augmented Image
</td>

<td style="vertical-align: bottom">
<img src="images/Shear-input-bboxes.jpg" style="display: block; width: 100%"/>
<br/>
Input Image (with Bounding Boxes)
</td>

<td style="vertical-align: bottom">
<img src="images/Shear-bboxes.jpg" style="display: block; width: 100%"/>
<br/>
Augmented Image (with Bounding Boxes)
</td>

</tr>
</table>

### Parameters


**probs** *(float)* = 1\.0<br/>
The probability that this augmentation will be applied


* must be between 0 and 1


**shear\_factor** *(float)* = 0\.2<br/>








## Translate

Translate the given image\.

### Example
<table style="width: 100%">
<tr>
<td style="vertical-align: bottom">
<img src="images/Translate-input.jpg" style="display: block; width: 100%"/>
<br/>
Input Image
</td>

<td style="vertical-align: bottom">
<img src="images/Translate.jpg" style="display: block; width: 100%"/>
<br/>
Augmented Image
</td>

<td style="vertical-align: bottom">
<img src="images/Translate-input-bboxes.jpg" style="display: block; width: 100%"/>
<br/>
Input Image (with Bounding Boxes)
</td>

<td style="vertical-align: bottom">
<img src="images/Translate-bboxes.jpg" style="display: block; width: 100%"/>
<br/>
Augmented Image (with Bounding Boxes)
</td>

</tr>
</table>

### Parameters


**probs** *(float)* = 1\.0<br/>
The probability that this augmentation will be applied


* must be between 0 and 1


**translate\_x** *(float)* = 0\.2<br/>



* must be between 0 and 1


**translate\_y** *(float)* = 0\.2<br/>



* must be between 0 and 1






## VerticalFlip

Vertically flip the given image\.

### Example
<table style="width: 100%">
<tr>
<td style="vertical-align: bottom">
<img src="images/VerticalFlip-input.jpg" style="display: block; width: 100%"/>
<br/>
Input Image
</td>

<td style="vertical-align: bottom">
<img src="images/VerticalFlip.jpg" style="display: block; width: 100%"/>
<br/>
Augmented Image
</td>

<td style="vertical-align: bottom">
<img src="images/VerticalFlip-input-bboxes.jpg" style="display: block; width: 100%"/>
<br/>
Input Image (with Bounding Boxes)
</td>

<td style="vertical-align: bottom">
<img src="images/VerticalFlip-bboxes.jpg" style="display: block; width: 100%"/>
<br/>
Augmented Image (with Bounding Boxes)
</td>

</tr>
</table>

### Parameters


**probs** *(float)* = 1\.0<br/>
The probability that this augmentation will be applied


* must be between 0 and 1





