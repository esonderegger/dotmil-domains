from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()

requirements = [
    'requests>=2.7',
    'beautifulsoup4>=4.3',
]


setup(name='dotmil_domains',
      version='0.0.1',
      description='An incomplete listing of .mil domains',
      url='https://github.com/esonderegger/dotmil-domains',
      author='Evan Sonderegger',
      author_email='evan@rpy.xyz',
      license='MIT',
      packages=['dotmil_domains'],
      install_requires=requirements,
      entry_points={
          'console_scripts': [
              'dotmil_domains = dotmil_domains.__main__:main'
          ]
      },
      zip_safe=False)
