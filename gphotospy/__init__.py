import logging

logging.basicConfig(
    level=logging.ERROR,
    filename='gphtospy.log',
    filemode='w',
    format='%(name)s - %(asctime)s - %(levelname)s - %(message)s')
