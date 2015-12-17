from setuptools import setup, find_packages

version = '1.0'

setup(name='pareto.portlet.twittertimeline',
      version=version,
      description="Twitter timeline portlet for Plone",
      long_description=(open("README.rst").read() + "\n" +
                        open("CHANGES.rst").read()),
      # Get more strings from
      # https://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
          "Framework :: Plone",
          "Framework :: Plone :: 4.3",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.7",
          ],
      keywords='diazo theme',
      author='Pareto and Zest',
      author_email='info@zestsoftware.nl',
      url='http://www.zeelandia.com/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['pareto', 'pareto.portlet'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
