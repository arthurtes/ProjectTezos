import smartpy as sp

@sp.module
def main():
    class Poll(sp.Contract):
        def __init__(self, recipient, title, simpleAnswer, fieldList, anonymous):
            self.data.recipient = recipient # Recipient of all collected money
            self.data.title = title
            self.data.anonymous = anonymous # To allow anonymous voting
            self.data.simpleAnswer = simpleAnswer
            self.data.fieldList # A list of field from wich you can vote
               
        @sp.onchain_view()
        def getDisplay(self):
            """
                Display current vote state
            """
            sp.result(42)
            
            """assert sp.amount == self.data.price, "Wrong price"
           owner_share = sp.split_tokens(self.data.price, abs(100 - self.data.author_rate), 100)
           sp.send(self.data.owner, owner_share)
           self.data.price += sp.split_tokens(sp.amount, 10, 100)
           self.data.owner = sp.sender"""
    
        @sp.entrypoint
        def claim_author_rate(self):
            assert sp.sender == self.data.recipient, " not your money "
            sp.send(self.data.author, sp.balance)

@sp.add_test()
def test():
    scenario = sp.test_scenario("Test", main)
    alice = sp.test_account('Alice').address
    bob = sp.test_account('Bob').address
    eve = sp.test_account('Eve').address
    
    contract = main.Poll(eve, "Do you like Tezos", False, ["Yes", "No"], True)
    scenario += contract

    sp.trace(contract.display())










