from setuptools import setup, find_packages

setup(
    name='speed-test-tool',            # The name of your package
    version='0.1.0',                   # The version of your package
    description='A simple CLI tool to test internet speed using speedtest-cli',
    long_description=open('README.md').read(),  # Read from the README file
    long_description_content_type='text/markdown',
    author='theos',
    author_email='sabuhi.gasimzada@gmail.com',
    # URL of the GitHub repository
    url='https://github.com/s3bu7i/Speed-Test-CLI',
    packages=find_packages(),         # Automatically find all packages
    install_requires=[
        'speedtest-cli',              # List of dependencies
        'rich',
    ],
    entry_points={
        'console_scripts': [
            # Make the main function callable as a CLI
            'speed-test=speed_test_tool.main:main',
        ],
    },
    classifiers=[  # Classifiers are used to categorize the package on PyPI
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Specify the Python version compatibility
)
