import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='insta_hashtag_crawler',
    version='0.0.1',
    author='Gyeongsu Yim',
    author_email='point1304@gmail.com',
    description='A gevent-based simple instagram hashtag crawler',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/pypa/smpleproject',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'insta-crawl = insta_crawler.command:crawl'
        ]
    }
)
