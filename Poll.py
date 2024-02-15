import smartpy as sp

@sp.module
def main():
    def updateDisplay(self):
            self.data.toDisplay = ""
            self.data.toDisplay += self.data.title + "\n\n"
            for elt in self.data.fieldList.keys():
                self.data.toDisplay += self.data.fieldList[elt]
                self.data.toDisplay += (self.data.fieldList[elt]*100) / self.totalVote + "\n"
                
    class Poll(sp.Contract):
        def __init__(self, author, title, simpleAnswer, fieldList):
            self.data.author = author
            self.data.title = title
            self.data.simpleAnswer = simpleAnswer
            self.data.fieldList = fieldList # A list of field from wich you can vote
            self.data.totalVote = 0
            self.data.totalPeople = 0
            self.data.toDisplay = ""
            
            updateDisplay(self)

        @sp.entrypoint
        def vote(self, *field):
            assert sp.amount >= sp.tez(1), "Not enough"
            assert len(field) != 1 and self.data.simpleAnswer == True, "Only one answer is possible"

            if len(field) > 0:
                self.data.totalPeople += 1

            for opt in field:
                assert self.data.fieldList.keys().contains(opt), "Field not recognized"
                self.data.fieldList[opt] += 1
                self.data.totalVote += 1

            updateDisplay(self)
            
    
        @sp.entrypoint
        def claim_author_rate(self):
            assert sp.sender == self.data.author, " not your money "
            sp.send(self.data.author, sp.balance)

@sp.add_test()
def test():
    scenario = sp.test_scenario("Test", main)
    alice = sp.test_account('Alice').address
    bob = sp.test_account('Bob').address
    eve = sp.test_account('Eve').address
    
    contract = main.Poll(eve, "Do you like Tezos", False, ["Yes", "No"])
    scenario += contract

    sp.trace(contract.display())


























