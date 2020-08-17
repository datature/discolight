import setuptools

with open("longdescription.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="discolight",
    version="0.1.0",
    author="Hongnan Gao, Ian Duncan, Keechin Goh",
    author_email="discolight@datature.io",
    description="Flashy, ravey and state-of-the-art image augmentations to "
    "boost the performance of deep convolutional neural networks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/datature/discolight",
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    package_data={
        'discolight.doc_templates': ['*.md'],
        'discolight.doc_templates.augmentations': ['*.yml']
    },
    python_requires='>=3.6, <3.9',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Visualization"
    ],
    install_requires=[
        'yamale>=3.0.1', 'numpy>=1.19.0', 'opencv-python>=4.3.0.36',
        'scikit-image>=0.17.2', 'Pillow>=7.2.0', 'Jinja2>=2.11.2',
        'tqdm>=4.47.0'
    ],
    entry_points={'console_scripts': [
        'discolight=discolight.run:main',
    ]})
