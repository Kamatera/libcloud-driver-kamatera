from setuptools import setup, find_packages


with open("README.md", "r") as f:
    long_description = f.read()


setup(
    name="libcloud_driver_kamatera",
    version="0.0.0",
    packages=find_packages(exclude=['tests',]),
    install_requires=["apache-libcloud>=2.8.2"],
    description='Apache Libcloud driver for managing Kamatera compute resources',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Kamatera',
    url='https://github.com/Kamatera/libcloud-driver-kamatera',
    license='MIT',
)
