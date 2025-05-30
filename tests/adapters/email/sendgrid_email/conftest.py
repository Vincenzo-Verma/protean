import pytest

from tests.shared import initialize_domain


@pytest.fixture(autouse=True)
def test_domain():
    domain = initialize_domain(name="Sendgrid Email Tests", root_path=__file__)

    with domain.domain_context():
        yield domain
