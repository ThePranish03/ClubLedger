from algopy import ARC4Contract, arc4, UInt64, GlobalState

class Clubledger(ARC4Contract):

    def __init__(self) -> None:
        # ✅ Correct: Define inside __init__ with 'self.'
        self.total_funds = GlobalState(UInt64(0)) 

    @arc4.abimethod
    def add_funds(self, amount: UInt64) -> UInt64:
        self.total_funds.value += amount
        return self.total_funds.value

    @arc4.abimethod
    def sponsor_fund(self, amount: UInt64) -> None:
        self.total_funds.value = self.total_funds.value + amount

    @arc4.abimethod
    def transfer_to_club(self, amount: UInt64) -> None:
        assert self.total_funds.value >= amount
        self.total_funds.value = self.total_funds.value - amount

    @arc4.abimethod
    def get_total_funds(self) -> UInt64:
        return self.total_funds.value


