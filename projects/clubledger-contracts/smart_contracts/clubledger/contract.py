from algopy import ARC4Contract, arc4, Global, Txn, Box


class Event(arc4.Struct):
    club: arc4.Address
    total_sponsor_funds: arc4.UInt64
    total_ticket_revenue: arc4.UInt64
    allocated_amount: arc4.UInt64
    spent_amount: arc4.UInt64
    status: arc4.String


class ClubLedger(ARC4Contract):

    # Global Admin
    admin = arc4.Global(arc4.Address)

    # -------------------------------------------------
    # CONTRACT CREATION
    # -------------------------------------------------

    @arc4.abimethod(create="require")
    def create(self):
        self.admin = Txn.sender

    # -------------------------------------------------
    # CREATE EVENT (Club Only)
    # -------------------------------------------------

    @arc4.abimethod
    def create_event(self, event_id: arc4.String):

        # Prevent zero address
        assert Txn.sender != Global.zero_address

        # Ensure event does not already exist
        assert not Box.exists(event_id.bytes)

        event = Event(
            club=Txn.sender,
            total_sponsor_funds=0,
            total_ticket_revenue=0,
            allocated_amount=0,
            spent_amount=0,
            status="ACTIVE"
        )

        Box.put(event_id.bytes, event.bytes)

    # -------------------------------------------------
    # RECORD SPONSOR CONTRIBUTION
    # -------------------------------------------------

    @arc4.abimethod
    def record_sponsor(self, event_id: arc4.String, amount: arc4.UInt64):

        assert Box.exists(event_id.bytes)

        event_bytes = Box.get(event_id.bytes)
        event = Event.from_bytes(event_bytes)

        # Only allow positive amounts
        assert amount > 0

        event.total_sponsor_funds += amount

        Box.put(event_id.bytes, event.bytes)

    # -------------------------------------------------
    # RECORD TICKET SALE
    # -------------------------------------------------

    @arc4.abimethod
    def record_ticket_sale(self, event_id: arc4.String, amount: arc4.UInt64):

        assert Box.exists(event_id.bytes)

        event_bytes = Box.get(event_id.bytes)
        event = Event.from_bytes(event_bytes)

        assert amount > 0

        event.total_ticket_revenue += amount

        Box.put(event_id.bytes, event.bytes)

    # -------------------------------------------------
    # ALLOCATE FUNDS (Admin Only)
    # -------------------------------------------------

    @arc4.abimethod
    def allocate_funds(self, event_id: arc4.String, amount: arc4.UInt64):

        assert Txn.sender == self.admin
        assert Box.exists(event_id.bytes)

        event_bytes = Box.get(event_id.bytes)
        event = Event.from_bytes(event_bytes)

        total_available = event.total_sponsor_funds + event.total_ticket_revenue

        # Cannot allocate more than available
        assert amount <= total_available

        event.allocated_amount = amount

        Box.put(event_id.bytes, event.bytes)

    # -------------------------------------------------
    # RECORD VENDOR PAYMENT (Admin Only)
    # -------------------------------------------------

    @arc4.abimethod
    def record_vendor_payment(self, event_id: arc4.String, amount: arc4.UInt64):

        assert Txn.sender == self.admin
        assert Box.exists(event_id.bytes)

        event_bytes = Box.get(event_id.bytes)
        event = Event.from_bytes(event_bytes)

        # Ensure allocated exists
        assert event.allocated_amount > 0

        # Prevent overspending
        assert event.spent_amount + amount <= event.allocated_amount

        event.spent_amount += amount

        # If fully spent, mark completed
        if event.spent_amount == event.allocated_amount:
            event.status = "COMPLETED"

        Box.put(event_id.bytes, event.bytes)

    # -------------------------------------------------
    # READ EVENT DETAILS
    # -------------------------------------------------

    @arc4.abimethod(readonly=True)
    def get_event(self, event_id: arc4.String) -> Event:

        assert Box.exists(event_id.bytes)

        event_bytes = Box.get(event_id.bytes)
        return Event.from_bytes(event_bytes)
