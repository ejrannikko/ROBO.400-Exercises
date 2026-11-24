from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'turtlebot3_controller'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),

        # Install trajectory CSV files
        (os.path.join('share', package_name, 'trajectories'),
        glob('trajectories/*.csv')),

    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='miko',
    maintainer_email='miko.pollari@tuni.fi',
    description='Movement controller for turtlebot3 gazebo simulation. Exercise 3 of Tampere University course ROBO.400',
    license='Apache License 2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'turtlebot3_controller = turtlebot3_controller.turtlebot3_controller:main'
        ],
    },
)
