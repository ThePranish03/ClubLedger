from collections.abc import Iterator
import pytest
from algopy_testing import AlgopyTestContext, algopy_testing_context
from smart_contracts.clubledger.contract import ClubLedger


@pytest.fixture()
def context() -> Iterator[AlgopyTestContext]:
    with algopy_testing_context() as ctx:
        yield ctx


def test_create_event(context: AlgopyTestContext) -> None:
    contract = ClubLedger()

    event_id = context.any.string(length=10)

    # simulate create
    contract.create()

    contract.create_event(event_id)

    event = contract.get_event(event_id)

    assert event.total_sponsor_funds == 0
    assert event.total_ticket_revenue == 0
    assert event.allocated_amount == 0
    assert event.spent_amount == 0
    assert event.status == "ACTIVE"


def test_sponsor_and_ticket(context: AlgopyTestContext) -> None:
    contract = ClubLedger()
    contract.create()

    event_id = context.any.string(length=10)

    contract.create_event(event_id)
    contract.record_sponsor(event_id, 100)
    contract.record_ticket_sale(event_id, 50)

    event = contract.get_event(event_id)

    assert event.total_sponsor_funds == 100
    assert event.total_ticket_revenue == 50


def test_allocation_and_vendor_payment(context: AlgopyTestContext) -> None:
    contract = ClubLedger()
    contract.create()

    event_id = context.any.string(length=10)

    contract.create_event(event_id)
    contract.record_sponsor(event_id, 200)
    contract.record_ticket_sale(event_id, 100)

    # allocate 250 (<= 300)
    contract.allocate_funds(event_id, 250)

    event = contract.get_event(event_id)
    assert event.allocated_amount == 250

    # pay vendor
    contract.record_vendor_payment(event_id, 200)
    event = contract.get_event(event_id)
    assert event.spent_amount == 200

    # pay remaining
    contract.record_vendor_payment(event_id, 50)
    event = contract.get_event(event_id)

    assert event.spent_amount == 250
    assert event.status == "COMPLETED"
