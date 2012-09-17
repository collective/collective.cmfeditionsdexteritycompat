from setuptools import setup, find_packages
import os

version = '0.1b8'

setup(name='collective.cmfeditionsdexteritycompat',
      version=version,
      description='Makes `Products.CMFEditions`_ works with `Dexterity` content types.',
      long_description=open(os.path.join("collective", "cmfeditionsdexteritycompat", "README.txt")).read() \
        + '\n\n'
        + open(os.path.join("docs", "HISTORY.txt")).read(),
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
            'Products.CMFPlone',
            'Products.CMFEditions',
            'Products.CMFDiffTool',            
            
        ]
      },
      
      entry_points="""      
      [z3c.autoinclude.plugin]
      target = plone
      """,      
)
