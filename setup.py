import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'controller_2024b'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name), glob('launch/*.launch.xml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='d-robo',
    maintainer_email='sarukiti1891@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'controller_2024b_A = controller_2024b.controller_2024b_A:main',
            'controller_2024b_B = controller_2024b.controller_2024b_B:main',
            'controller_2024b_C = controller_2024b.controller_2024b_C:main',
            'controller_2024b_2_4 = controller_2024b.controller_2024b_2_4:main'
        ],
    },
)
