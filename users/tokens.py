from django.contrib.auth.tokens import PasswordResetTokenGenerator as TokenGenerator


class PasswordResetTokenGenerator(TokenGenerator):
    def _make_hash_value(self, user, timestamp):
        hash = super()._make_hash_value(user, timestamp)
        return f"{hash}{user.is_active}_PASSWORD_RESET"


class ActivateAccountTokenGenerator(TokenGenerator):
    def _make_hash_value(self, user, timestamp):
        hash = super()._make_hash_value(user, timestamp)
        return f"{hash}{user.is_active}_ACTIVATE_ACCOUNT"


class EmployeeSetupTokenGenerator(TokenGenerator):
    def _make_hash_value(self, user, timestamp):
        hash = super()._make_hash_value(user, timestamp)
        return f"{hash}{user.is_active}_EMPLOYEE_SETUP"


activation_token = ActivateAccountTokenGenerator()
password_reset_token = PasswordResetTokenGenerator()
employee_setup_token = EmployeeSetupTokenGenerator()
