from setuptools import setup

setup(
    name='plafi',
    version='0.1.0',
    packages=['plafi'],
    install_requires=["numpy", "pandas", "scipy", "matplotlib", "numexpr", "uncertainties", "tabulate"],
    entry_points={
        'console_scripts': [
            'plafi = plafi.__main__:main',
        ]}
)
