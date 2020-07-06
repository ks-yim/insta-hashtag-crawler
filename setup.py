import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='insta-hashtag-crawler',
    version='0.0.4',
    author='K.S. Yim',
    author_email='point1304@gmail.com',
    description='A gevent-based simple instagram hashtag crawler',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/point1304/insta-hashtag-crawler',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'gevent>=1.4.0',
        'requests>=2.22.0',
    ],
    entry_points={
        'console_scripts': [
            'insta-crawl = insta_hashtag_crawler.command:crawl'
        ]
    }
)
