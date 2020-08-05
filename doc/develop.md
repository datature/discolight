# Developing Discolight

This document contains information about how to add additional augmentations
to Discolight.

## Setting up Local Development

If you would like to add your own image augmentations to Discolight,
you need to set up the repository for local development. We recommend
you create a virtual environment to install the required dependencies:

	       $ virtualenv --python=`which python3` venv/
	       $ source venv/bin/activate
	(venv) $ pip install -r requirements.txt

You can then invoke the command line utilities using the provided shell
scripts:

	(venv) $ ./discolight.sh generate ... (for discolight ...)
	
	(venv) $ ./discolight-doc.sh (for discolight-doc)

## Running Tests and Code Quality Checks

Once you have set up the repository for local development, you can run
the tests and code quality checks with the provided shell scripts:

	(venv) $ ./test.sh
	(venv) $ ./lint.sh
	
Unit tests will fail if code coverage falls below 90%.

You can also run the unit tests on Python 3.6, 3.7, and 3.8 using
Tox. To do this, you first need to install these version of Python on
your system. On Ubuntu, you can add the `deadsnakes` PPA and install
packages for each of these Python versions:

	$ sudo add-apt-repository ppa:deadsnakes/ppa
	$ sudo apt-get update
	$ sudo apt-get install python3.6 python3.7 python3.8 python3-distutils
	
Once you have installed the required versions of Python, run Tox:

	(venv) $ tox

## Adding a New Augmentation

Create a new Python file for your augmentation in
`src/discolight/augmentations`
(e.g. `src/discolight/augmentations/myaugmentation.py`). If your
augmentation will transform the image colors and shape, you should
extend the `Augmentation` class:

	import numpy as np
	import cv2
	from discolight.params.params import Params
	from .augmentation.types import Augmentation
	from .decorators.accepts_probs import accepts_probs
	
	@accepts_probs
	class MyAugmentation(Augmentation):
		"""Augmentation description"""

Your class constructor can take in zero or more parameters which are used to
configure how your augmentation operates:
		
		def __init__(self, param1, param2, ...):
			super().__init__()
			
			self.param1 = param1
			self.param2 = param2
			...

The parameters accepted by your augmentation must be described in a static
`params` method that returns a `Params` object. Start by constructing an
empty `Params` object, and then call the `add` method to describe all of
your augmentation parameters. The `add` method takes the following keyword
arguments:

> `name`
>
> The name of the parameter

> `description`
>
> A description of the parameter

> `data_type`
>
> The type of the parameter (more on this below).

> `default`
>
> A default value for the parameter

> `required=False`
>
> Whether the parameter must be specified. All augmentation parameters should
> _not_ be required - you should instead choose a sane default value that
> gives reasonable results.

Below is an example `params` method:
		
		@staticmethod
		def params():
			return Params.add("param1", "param1 description", int, 1).add
				"param2", "param2 description", float, 2.0)

The data type can be a Python built-in type like `float`, `int`, or `str`, or
one of the following that you can import from `.augmentation.types`:

> `BoundedNumber(number_type, minimum=None, maximum=None)`
>
> Ensures that the input value has `number_type` (i.e., `int` or
> `float` - type coercion will be used on input values if necessary),
> and is in the range [minimum, maximum]. If `minimum` is `None` then
> there is no lower bound, and if `maximum` is `None` then there is no
> upper bound.

> `NumericalRange(minimum=None, maximum=None)`
>
> Ensures that the input value is a numerical range expressed as a 2-tuple
> (lists of length 2 are accepted as input and converted to 2-tuples). The
> range specified must be inside the interval [minimum, maximum].
> If `minimum` is `None` then there is no lower bound, and if `maximum` is
> `None` then there is no upper bound.

You can also use an `Enum` object as the data type. To do this, construct an
`Enum` class where all of the enumeration values are strings:

	from enum import Enum
	
	class MyEnum(Enum):
		MYOPTION1 = "MYOPTION1"
		MYOPTION2 = "MYOPTION2"
		...

Then specify `MyEnum` as the data type parameter in `add`. When your
augmentation is constructed, the enumerated parameter will take a string,
and the augmentation factory function will check that it is one of your
enumeration options.

Note that wrapping your augmentation with the
`accepts_probs` decorator adds an additional `probs` parameter so that
your augmentation can be randomly applied with the probability
specified in `probs`. The parameters for your augmentation are passed
to the constructor.

Finally, you must implement the `augment` method to actually perform the
augmentation:
	    
		def augment(self, img, bboxes):
			
			...
			
			return img, bboxes

The `img` is an OpenCV image in `HxWxC` format, and `bboxes`
is a `n x 5` numpy array describing the annotations for the given
image, where `n` is the number of annotations. The format of the
columns is as follows:

	0: min_x
	1: max_x
	2: min_y
	3: max_y
	4: label

Your `augment` method should returned the augmented image and
annotations as a tuple.

**Important:** If your augmentation uses random number generators
_other_ than those provided by the built-in `random` module, you must
seed them with a value from `random.random()` so that your
augmentation function can be deterministic if `random.seed()` is
called (e.g., when snapshot tests are run).

**Important**: If your augmentation relies on 3rd party libraries
beyond those already installed with Discolight (e.g., numpy and
OpenCV), don't forget to add your additional dependency to `setup.py`
under `install_requires`.

If your augmenation only modifies the image color information and
leaves the original annotations intact, then you should extend the
`ColorAugmentation` class instead, which requires you to implement
an `augment_img` method returning only the augmented image.

	import numpy as np
	import cv2
	from discolight.params.params import Params
	from .augmentation.types import ColorAugmentation
	from .decorators.accepts_probs import accepts_probs
	
	@accepts_probs
	class MyAugmentation(ColorAugmentation):
		"""Augmentation description"""
		
		def __init__(self, param1, param2, ...):
			super().__init__()
			
			self.param1 = param1
			self.param2 = param2
			...
		
		@staticmethod
		def params():
			return Params.add("param1", "param1 description", int, 1).add
				"param2", "param2 description", float, 2.0)
	    
		def augment_img(self, img, bboxes):
			
			...
			
			# This time, return only the image
			return img

### Testing

Once you have added or updated your new augmentation, you need to
rebuild the snapshot library used for testing:

	(venv) $ ./test.sh --update-snapshots

If the default parameters are not ideal for snapshot testing, you can
change them.  Create a new file called `fixtures/MyAugmentation.yml`,
and enter the settings as follows:
	
	options:
		param1: 1
		param2: 2.5
		...

Once you have updated the snapshot set,  run the unit tests again to verify 
that your updated snapshots are working.

You are encouraged to add additional unit tests beyond the built-in
snapshot tests. Discolight uses PyTest, which loads tests in the
`tests/` directory from files prefixed with `test_`. To create
additional tests for your new augmentation, create the file
`test_MyAugmentation.py` under `tests/augmentations`. Use the provided
`sample_image` test fixture to get access to a sample image and
annotations to run your augmentation.

	import pytest
	import numpy as np
	
	from discolight.annotations import (annotations_to_numpy_array)
	from discolight.augmentations.myaugmentation import MyAugmentation
	
	@pytest.mark.usefixtures("sample_image")
	def test_my_augmentation_...(sample_image):
		
		img, annotations = sample_image
		
		bboxes = annotations_to_numpy_array(annotations)
		
	    # Parameters must be named here
		augmentation = MyAugmentation(param1=1.0)
		
		aug_img, aug_bboxes = augmentation.augment(img.copy(), bboxes.copy())
		
		... some assertions here ...
