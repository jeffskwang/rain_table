from setuptools import setup
import re


# borrowed from Agile Scientific bruges tools
verstr = 'unknown'
VERSIONFILE = "rain_table/_version.py"
with open(VERSIONFILE, "r") as f:
    verstrline = f.read().strip()
    pattern = re.compile(r"__version__ = ['\"](.*)['\"]")
    mo = pattern.search(verstrline)
if mo:
    verstr = mo.group(1)
    print("Version "+verstr)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))


setup(
    name='rain_table',
    version=verstr,
    author='Jeffrey Kwang and Andrew J. Moodie',
    author_email='amoodie@rice.edu',
    packages=['rain_table'],
    url='https://github.com/sededu/rain_table',
    license='LICENSE.txt',
    description='educational activity for teaching how water is routed through a drainage basin',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    python_requires='>=3',
    install_requires=[
        'scipy',
        'numpy',
        'matplotlib',
        'shapely'],
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Education',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Science/Research',
        'Topic :: Education'],
    project_urls={
        'Bug Reports': 'https://github.com/sededu/rain_table/issues',
        'Source': 'https://github.com/sededu/rain_table',
    },
)
