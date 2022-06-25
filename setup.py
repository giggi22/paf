from setuptools import setup

setup(
    name='paf',
    version='0.1.0',
    packages=['paf'],
    install_requires=["numpy", "pandas", "scipy", "matplotlib", "numexpr", "uncertainties"],
    entry_points={
        'console_scripts': [
            'ttdplanner = ttdplanner.__main__',
        ]}
)
