from setuptools import setup, find_packages
name = 'datextractor'
version='0.0.1'
package_dir = {name: name}
setup(
  name=name,
  version=version,
  license='MIT',
  install_requires=['egenix-mx-base']
  package_dir=package_dir
)