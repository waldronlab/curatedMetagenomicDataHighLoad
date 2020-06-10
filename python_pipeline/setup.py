import setuptools

setuptools.setup(
    name='curatedmetagenomicspipeline',
    version='0.0.1',
    author='Francesco Beghini',
    author_email='francesco.beghini@unitn.it',
    url='https://github.com/waldronlab/curatedmetagenomics',
    packages=setuptools.find_namespace_packages(),
    entry_points={
        'console_scripts': [
            'cmd_pipeline = curatedMetagenomicsDataPipeline.curatedMetagenomicData_pipeline:pipeline',
            'cmd_utilities_cli = curatedMetagenomicsDataPipeline.cli:cmd_cli'
        ]
    },
    long_description_content_type='text/markdown',
    long_description=open('README.md').read()
)