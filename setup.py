from setuptools import setup

requirements = [
    # package requirements go here
]

setup(
    name='tipdetect',
    version='0.1',
    description="Find tips for a neuronal skeleton",
    author="Stephen Plaza",
    author_email='plazas@janelia.hhmi.org',
    url='https://github.com/janelia-flyem/tipdetect',
    packages=['tipdetect'],
    entry_points={
        'console_scripts': [
            'tipdetect=tipdetect.tipdetect:main'
        ]
    },
    install_requires=requirements,
    keywords='tip detect',
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ]
)
