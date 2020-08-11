# Annotation Loaders

## FourCornersCSV

Loads annotations from a CSV file in the following format\.

image_name, x_min, y_min, x_max, y_max, label

### Parameters

**annotations_file** _(str)_, required<br/>
The path to the CSV file containing the annotations

**normalized** _(bool)_ = True<br/>
whether the bounding box coordinates are stored in a normalized format

## WidthHeightCSV

Loads annotations from a CSV file in the following format\.

image_name, x_min, y_min, width, height, label

### Parameters

**annotations_file** _(str)_, required<br/>
The path to the CSV file containing the annotations

**normalized** _(bool)_ = True<br/>
whether the bounding box coordinates are stored in a normalized format

# Annotation Writers

## FourCornersCSV

Writes annotations to a CSV file in the following format\.

image_name, x_min, y_min, x_max, y_max, label

### Parameters

**annotations_file** _(str)_, required<br/>
The path to the CSV file to write the annotations to

**normalized** _(bool)_ = True<br/>
whether the bounding box coordinates should be normalized before saving

## WidthHeightCSV

Writes annotations to a CSV file in the following format\.

image_name, x_min, y_min, width, height, label

### Parameters

**annotations_file** _(str)_, required<br/>
The path to the CSV file to write the annotations to

**normalized** _(bool)_ = True<br/>
whether the bounding box coordinates should be normalized before saving

# Image Loaders

## Directory

Load images from a directory in the filesystem\.

The image name from the AnnotationLoader will be used to fetch a file with
the same name in the given directory\.

### Parameters

**directory** _(str)_, required<br/>
The directory from which to load images

# Image Writers

## Directory

Writes images to a directory in the filesystem\.

Images will be saved to a file with the given name in the given directory\.

### Parameters

**clean_directory** _(bool)_ = True<br/>
whether to forcibly ensure the output directory is empty

**directory** _(str)_, required<br/>
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

**kelvin** _(int in range \[1000, 40000\])_ = 3000<br/>
temperature value in to which temperature should be changed

**probs** _(float in range \[0\.0, 1\.0\])_ = 1\.0<br/>
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

**mean** _(float)_ = 0<br/>

**probs** _(float in range \[0\.0, 1\.0\])_ = 1\.0<br/>
The probability that this augmentation will be applied

**variance** _(float)_ = 0\.01<br/>

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

**probs** _(float in range \[0\.0, 1\.0\])_ = 1\.0<br/>
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

**probs** _(float in range \[0\.0, 1\.0\])_ = 1\.0<br/>
The probability that this augmentation will be applied

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

**max_height** _(float in range \[0, 1\])_ = 0\.7<br/>
Maximum height of cropped area \(normalized\)

**max_width** _(float in range \[0, 1\])_ = 0\.7<br/>
Maximum width of cropped area \(normalized\)

**probs** _(float in range \[0\.0, 1\.0\])_ = 1\.0<br/>
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

**probs** _(float in range \[0\.0, 1\.0\])_ = 1\.0<br/>
The probability that this augmentation will be applied

**x_range** _(range in \[0\.0, 1\.0\])_ = \(0\.0, 1\.0\)<br/>
normalized x range for coordinates that may be erased

**y_range** _(range in \[0\.0, 1\.0\])_ = \(0\.0, 1\.0\)<br/>
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

**brightness** _(range in \[\-Inf, Inf\])_ = \(0\.0, 0\.0\)<br/>

**hue** _(range in \[\-Inf, Inf\])_ = \(0\.0, 0\.0\)<br/>

**probs** _(float in range \[0\.0, 1\.0\])_ = 1\.0<br/>
The probability that this augmentation will be applied

**saturation** _(range in \[\-Inf, Inf\])_ = \(0\.0, 0\.0\)<br/>

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

**angle_range** _(range in \[\-360\.0, 360\.0\])_ = \(\-10\.0, 10\.0\)<br/>
The range from which the random angle will be chosen

**probs** _(float in range \[0\.0, 1\.0\])_ = 1\.0<br/>
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

**angle** _(float)_ = 5<br/>

**probs** _(float in range \[0\.0, 1\.0\])_ = 1\.0<br/>
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

**noise_type** _(RGB \| SnP)_ = RGB<br/>
The type of noise

**pepper** _(int in range \[0, 255\])_ = 0<br/>
The color of the pepper

**probs** _(float in range \[0\.0, 1\.0\])_ = 1\.0<br/>
The probability that this augmentation will be applied

**replace_probs** _(float)_ = 0\.1<br/>

**salt** _(int in range \[0, 255\])_ = 255<br/>
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

**probs** _(float in range \[0\.0, 1\.0\])_ = 1\.0<br/>
The probability that this augmentation will be applied

**scale_x** _(float in range \[\-1\.0, Inf\])_ = 0\.2<br/>

**scale_y** _(float in range \[\-1\.0, Inf\])_ = 0\.2<br/>

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

**probs** _(float in range \[0\.0, 1\.0\])_ = 1\.0<br/>
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

**augmentations** _(augmentation_list)_ = \[\]<br/>

**probs** _(float in range \[0\.0, 1\.0\])_ = 1\.0<br/>
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

**probs** _(float in range \[0\.0, 1\.0\])_ = 1\.0<br/>
The probability that this augmentation will be applied

**shear_factor** _(float)_ = 0\.2<br/>

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

**probs** _(float in range \[0\.0, 1\.0\])_ = 1\.0<br/>
The probability that this augmentation will be applied

**translate_x** _(float in range \[0\.0, 1\.0\])_ = 0\.2<br/>

**translate_y** _(float in range \[0\.0, 1\.0\])_ = 0\.2<br/>

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

**probs** _(float in range \[0\.0, 1\.0\])_ = 1\.0<br/>
The probability that this augmentation will be applied
