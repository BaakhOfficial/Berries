from setuptools import find_packages, setup

setup(
    name='berrylib',
    packages=find_packages(),
    version='0.0.4',
    description='Wildberries api requests library',
    install_requires=['requests', 'pandas'],
    author='Nikolai Baakh',
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests'
)