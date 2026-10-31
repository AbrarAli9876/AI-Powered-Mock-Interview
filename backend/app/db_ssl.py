
import os


def get_database_connect_args() -> dict:
    """
    Return MySQL SSL connection arguments.

    Local development:
        Uses the existing connection behaviour.

    Production:
        Uses the Aiven CA certificate with
        certificate and hostname verification.
    """

    ca_path = os.getenv("MYSQL_SSL_CA")

    if not ca_path:
        return {}

    if not os.path.isfile(ca_path):
        raise FileNotFoundError(
            f"MySQL CA certificate was not found: {ca_path}"
        )

    return {
        "ssl_ca": ca_path,
        "ssl_verify_cert": True,
        "ssl_verify_identity": True,
    }
