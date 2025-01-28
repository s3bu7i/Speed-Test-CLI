from setuptools import setup, find_packages

setup(
    name='speed-test-tool',
    version='1.0.1',
    description='A simple CLI tool for downloading files with progress tracking',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='s3bu7i',
    author_email='sabuhi.gasimzada@gmail.com',
    url='https://github.com/yourusername/file-downloading-tool',
    packages=find_packages(),
    install_requires=[
        'requests',  # Add any other dependencies here
        'tqdm',
    ],
    entry_points={
        'console_scripts': [
            'file-download=file_downloading_tool.cli:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
