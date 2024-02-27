import smartpy as sp

@sp.module
def main():                
    class Bet(sp.Contract):
        def __init__(self, title, fieldList):
            self.data.title = title
            self.data.fieldList = fieldList # A list of field from wich you can vote
            self.data.toDisplay = ""
            self.data.winners = []
            sp.cast(self.data.winners, sp.list[sp.address])

        @sp.entrypoint
        def vote(self, option, address):
            assert self.data.fieldList.contains(option), "Field not recognized"
            self.data.fieldList[option].push(address)

        @sp.entrypoint
        def result(self):
            lowestAddress = []
            lowestCount = 9999999999999999
            for key in self.data.fieldList.keys():
                if len(self.data.fieldList[key]) > lowestCount:
                    lowestCount = len(self.data.fieldList[key])
                    lowestAddress = self.data.fieldList[key]
            self.data.winners = lowestAddress

@sp.add_test()
def test():
    scenario = sp.test_scenario("Test", main)
    alice = sp.test_account('Alice').address
    bob = sp.test_account('Bob').address
    eve = sp.test_account('Eve').address
    
    contract = main.Bet("Do you like Tezos", {"Yes": [], "No": []})
    scenario += contract


























