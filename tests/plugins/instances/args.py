import os

import pytest

from assessment_service.args import Parser


@pytest.fixture(scope="session")
def parser() -> Parser:
    db_user = os.environ.get("APP_DB_USER", "assessment_service")
    db_password = os.environ.get("APP_DB_PASSWORD", "assessment_service")
    db_name = os.environ.get("APP_DB_NAME", "assessment_service")
    db_host = os.environ.get("APP_DB_HOST", "localhost")
    db_port = os.environ.get("APP_DB_PORT", "5432")
    return Parser().parse_args(
        [
            f"--database-user={db_user}",
            f"--database-password={db_password}",
            f"--database-host={db_host}",
            f"--database-port={db_port}",
            f"--database-name={db_name}",
            "--app-host=127.0.0.1",
            "--app-port=8000",
            "--log-level=info",
            "--log-format=plain",
            "--debug=True",
            "--pool-size=4",
        ]
    )
