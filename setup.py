from setuptools import setup, find_packages

# Print the packages detected by find_packages()
print(find_packages())

# Read the contents of README.md for long description
with open('./talklocal/README.md', 'r') as fh:
    long_description = fh.read()

# Read the requirements from requirements.txt
with open('requirements.txt', 'r') as req_file:
    requirements = req_file.read().splitlines()

# The package data to be included
package_data = {
    'talklocal': ['subtitle/.keep'],  # .keep file to retain an empty folder
}

# Setup configuration
setup(
    name='talklocal',
    version='1.0.0',
    author='Wrick Talukdar',
    author_email='wrick.talukdar@gmail.com',
    license="MIT License",
    description='Real-time transcription, multilingual translation, and subtitling',
    long_description=long_description,
    long_description_content_type='text/markdown',  # Long description format
    url='https://github.com/iamwrick/app_talklocal.git',
    packages=find_packages(),  # Automatically find packages in the project
    package_data=package_data,  # Include package data such as the subtitle/.keep file
    install_requires=requirements,  # Dependencies from requirements.txt
    classifiers=[
        'Programming Language :: Python :: 3',
        # Add more classifiers if needed
    ],
    python_requires='>=3.6',  # Specify the minimum Python version supported
)
