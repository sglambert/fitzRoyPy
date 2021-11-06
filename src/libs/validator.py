class AbortError(Exception):
    """
    Raised when validation outcome is Abort.
    """


class FailError(Exception):
    """
    Raise when validation outcome is Fail.
    """


class Validator:
    """
    Used for performing data validations.
    """

    def __init__(self, logger, db, validations):
        self.logger = logger
        self.db = db
        self.validations = self.get_validations(validations)

    def get_validations(self, vals):
        """
        Dynamically import validations.
        This allows us to decide when we want to run certain validations.
        """
        # Store all validations in /sql directory in file validations_sql.py
        validations_module = 'validations_sql'
        validations = validations_module.__dict__.get(vals)
        self.validations = validations
        return self.validations

    def validation_enabled(self):
        """
        Check what validations in validations_sql.py are enabled
        (Any validation that is not 'OFF' is enabled)
        """
        enabled_validations = []
        for vals in self.validations:
            if vals.get('Validation Setting') == 'OFF':
                self.logger.info("Validation {} not enabled".format(vals.get('Validation NAme')))
                continue
            else:
                enabled_validations.append(vals)
        return enabled_validations

    def validate_sql(self):
        """
        Records the result of the validation query
        """
        # Get all validations that are enabled in validations_sql.py
        all_validations = self.validation_enabled()

        validation_outcomes = []
        failed_validations = []
        with self.db as db:
            for validations in all_validations:
                # Execute the validation query
                self.logger.info("Validating {}".format(validations.get('Validation Name')))
                validation_query_result = db.select_all(validations.get('Validation Query'))

                # Any results returned indicate an unexpected validation outcome
                if validation_query_result:
                    # Add all unexpected validations to failed_validations
                    failed_validations.append(validations)

                    # Add all unexpected validation outcomes to validation_outcomes
                    validation_outcomes.append(validation_query_result)

        # Pass all failed validations and validation outcomes to validation_outcome()
        # to handle processing. Validations may have different outcomes based on validation severity.
        self.validation_outcome(failed_validations, validation_outcomes)

    def validation_outcome(self, failed_validations, outcome):
        """
        IF validations return an unexpected result they will be passed
        to this method. failed_validations is a list of dictionaries with all the
        unexpected validations. Outcome is a list of lists with dictionaries
        having the validation query results.
        """
        validation_failures = []
        validation_skips = []

        for validation in failed_validations:
            if validation.get('Validation Setting') == 'ABORT':
                self.logger.error("AbortError: Failed critical validation check, "
                                  "Validation {} returned {}".format(
                                  validation.get('Validation Name'), outcome))
                raise AbortError("Failed validation check")

            elif validation.get("Validation Setting") == 'FAIL':
                validation_failures.append(validation)
            elif validation.get("Validation Setting") == 'SKIP':
                validation_skips.append(validation)

        if validation_failures:
            self.logger.error(FailError("{} validation failures on validations {}. Validation returned: {}"
                                        .format(len(validation_failures),
                                        [v.get('Validation Name') for v in validation_failures], outcome)))
            raise FailError

        if validation_skips:
            self.logger.info("{} validation skipped on validations {}. Validation returned: {}".format(
                len(validation_skips), [v.get('Validation Name') for v in validation_skips], outcome))
