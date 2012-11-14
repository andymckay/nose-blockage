from setuptools import setup


setup(
    name='nose-blockage',
    version='0.1.1',
    description='Raise errors when communicating outside of tests',
    long_description=open('README.rst').read(),
    author='Andy McKay',
    author_email='andym@mozilla.com',
    license='BSD',
    install_requires=['nose'],
    packages=['blockage'],
    url='https://github.com/andymckay/nose-blockage',
    entry_points={
        'nose.plugins.0.10': [
            'blockage = blockage:NoseBlockage'
        ]
    },
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Framework :: Django'
    ]
)
