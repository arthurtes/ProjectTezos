import smartpy as sp

@sp.module
def main():
    class Poll(sp.Contract):
        def __init__(self, anonymous = False):
            self.data.anonymous = anonymous
            
               
        @sp.entrypoint
        def buy(self):
           assert sp.amount == self.data.price, "Wrong price"
           owner_share = sp.split_tokens(self.data.price, abs(100 - self.data.author_rate), 100)
           sp.send(self.data.owner, owner_share)
           self.data.price += sp.split_tokens(sp.amount, 10, 100)
           self.data.owner = sp.sender
    
        @sp.entrypoint
        def claim_author_rate(self):
            assert sp.sender == self.data.author, " not your money "
            sp.send(self.data.author, sp.balance)

@sp.add_test()
def test():
    scenario = sp.test_scenario("Test", main)
    alice = sp.test_account('Alice').address
    bob = sp.test_account('Bob').address
    
    nft = main.NftForSale(bob, sp.record(name= "NFT Name", desc = "NFT desc"), sp.tez(100), 5, bob)
    contract = main.NFTWrapper(alice)
    scenario += nft
    scenario += contract

    contract.buy_nft(nft.address, _sender = alice, _valid = False, _exception = "Wrong price")