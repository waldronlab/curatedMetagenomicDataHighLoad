import setuptools

setuptools.setup(
    name='curatedMetagenomicsData',
    version='0.0.1',
    author='Francesco Beghini',
    author_email='francesco.beghini@unitn.it',
    url='https://github.com/waldronlab/curatedMetagenomicDataHighLoad',
    packages=setuptools.find_namespace_packages(),
    entry_points={
        'console_scripts': [
            'curatedMetagenomicsData_pipeline = curatedMetagenomicsDataPipeline.curatedMetagenomicData_pipeline:pipeline',
            'download_files = curatedMetagenomicsDataPipeline.utils:download_file'
        ]
    },
)