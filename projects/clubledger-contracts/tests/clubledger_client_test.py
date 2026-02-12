import algokit_utils
import pytest
from algokit_utils import (
    AlgoAmount,
    AlgorandClient,
    SigningAccount,
)

from smart_contracts.artifacts.clubledger.clubledger_client import (
    ClubledgerClient,
    ClubledgerFactory,
)


@pytest.fixture()
def deployer(algorand_client: AlgorandClient) -> SigningAccount:
    account = algorand_client.account.from_environment("DEPLOYER")
    algorand_client.account.ensure_funded_from_environment(
        account_to_fund=account.address,
        min_spending_balance=AlgoAmount.from_algo(10),
    )
    return account


@pytest.fixture()
def clubledger_client(
    algorand_client: AlgorandClient, deployer: SigningAccount
) -> ClubledgerClient:
    factory = algorand_client.client.get_typed_app_factory(
        ClubledgerFactory,
        default_sender=deployer.address,
    )

    client, _ = factory.deploy(
        on_schema_break=algokit_utils.OnSchemaBreak.AppendApp,
        on_update=algokit_utils.OnUpdate.AppendApp,
    )

    return client


def test_full_event_flow(clubledger_client: ClubledgerClient) -> None:

    event_id = "event1"

    # create event
    clubledger_client.send.create_event(args=(event_id,))

    # sponsor funds
    clubledger_client.send.record_sponsor(args=(event_id, 500))

    # ticket sales
    clubledger_client.send.record_ticket_sale(args=(event_id, 200))

    # allocate funds
    clubledger_client.send.allocate_funds(args=(event_id, 600))

    # vendor payment
    clubledger_client.send.record_vendor_payment(args=(event_id, 600))

    result = clubledger_client.send.get_event(args=(event_id,))

    event = result.abi_return

    assert event.total_sponsor_funds == 500
    assert event.total_ticket_revenue == 200
    assert event.allocated_amount == 600
    assert event.spent_amount == 600
    assert event.status == "COMPLETED"
