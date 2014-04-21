from distutils.core import setup
    
setup(name='AMIE-process',
      version='0.1.0',
      description='AMIE processing tools',
      author='Tanghong Qiu',
      author_email='taqiu@indiana.edu',
      url='https://github.iu.edu/rmday/AMIE-processing',
      scripts=['bin/rac.py', 'bin/rpc.py'],
      packages=['amie'],
      package_dir={'':'lib'},
      data_files=[('/etc/amie-processing', ['conf/amie-processing.cfg']),],
)