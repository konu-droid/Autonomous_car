from setuptools import setup

package_name = 'arduino_serial'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='autonomous-car',
    maintainer_email='autonomous-car@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'Arduino_Serial = arduino_serial.accel:main',
            'Pot_Serial = arduino_serial.pot_data:main',
            'pots2 = arduino_serial.pot2:main'
        ],
    },
)
