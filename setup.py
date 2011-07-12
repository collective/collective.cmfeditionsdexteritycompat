from setuptools import setup, find_packages
import os

version = '0.0.1dev'

setup(name='collective.cmfeditionsdexteritycompat',
      version=version,
      description='',
      long_description=open("README.txt").read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Rafael Oliveira',
      author_email='rafaelbco@gmail.com',
      url='http://',
      license="''",
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'setuptools',
        'five.grok',
        'z3c.autoinclude'
      ],
      
      extras_require = {
        'test': [
            'plone.app.testing',
            'plone.app.dexterity',
            'plone.app.versioningbehavior',
            'Plone',
            'Products.CMFEditions',
            'Products.CMFDiffTool',            
            
        ]
      },
      
      entry_points="""      
      [z3c.autoinclude.plugin]
      target = plone
      """,      
)
