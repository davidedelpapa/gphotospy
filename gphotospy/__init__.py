import logging

logging.basicConfig(
    level=logging.ERROR,
    filename='app.log',
    filemode='w',
    format='%(name)s - %(asctime)s - %(levelname)s - %(message)s')
