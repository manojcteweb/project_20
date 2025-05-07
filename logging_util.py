import logging

class LoggingUtil:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # Set up logging to a file
        logging.basicConfig(filename='application.log', level=logging.INFO,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    def log_activity(self, activity_type, user_id, message):
        """
        Logs various activities for audit purposes.

        :param activity_type: Type of activity (e.g., 'credit_check', 'document_verification')
        :param user_id: ID of the user associated with the activity
        :param message: Detailed message about the activity
        """
        log_message = f"Activity Type: {activity_type}, User ID: {user_id}, Message: {message}"
        self.logger.info(log_message)
