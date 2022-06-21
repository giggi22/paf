from setuptools import setup

setup(
    name = 'ttdplanner',
    version = '0.1.0',
    packages = ['ttdplanner']
    #install_requires = ["numpy","pandas","scipy"]
    entry_points = {
        'console_scripts': [
            'ttdplanner = ttdplanner.__main__',
            ]}
    )



