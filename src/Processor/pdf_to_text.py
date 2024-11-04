import logging
import os

levels = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}


def createLog(module):

    logger = logging.getLogger(module)

    if 'LOG_LEVEL' in os.environ:
        checkLevel = os.environ['LOG_LEVEL'].lower()
    else:
        checkLevel = 'warning'

    consoleLog = logging.StreamHandler()

    if checkLevel in levels:
        logger.setLevel(levels[checkLevel])
        consoleLog.setLevel(levels[checkLevel])
    else:
        logger.setLevel(levels['warning'])
        consoleLog.setLevel(levels['warning'])

    formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s: %(message)s')  # noqa: E501
    consoleLog.setFormatter(formatter)

    logger.addHandler(consoleLog)
    return logger


logger = createLog('handler')


def lambda_handler(event, context):
    """The central handler function called when the Lambda function is invoked.

    Arguments:
        event {dict} -- Dictionary containing contents of the event that
        invoked the function, primarily the payload of data to be processed.
        context {LambdaContext} -- An object containing metadata describing
        the event source and client details.

    Returns:
        [string|dict] -- An output object that does not impact the effect of
        the function but which is reflected in CloudWatch
    """
    logger.info('Starting Lambda Execution')

    logger.debug(event)

    # Method to be invoked goes heresrc/pdf_to_s3.py
    logger.info('Successfully invoked lambda')

    # This return will be reflected in the CloudWatch logs
    # but doesn't actually do anything
    return 'Hello, World'