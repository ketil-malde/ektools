from setuptools import setup

setup(name='ektools',
      version='0.1',
      description='Utilities to read and process Simrad RAW files',
      url='http://github.com/ketil-malde/ektools',
      author='Ketil Malde',
      author_email='ketil@malde.org',
      license='MIT',
      packages=['ektools'],
      scripts=['tools/eklist'],
#      install_requires=[pynmea2],
      zip_safe=False)
