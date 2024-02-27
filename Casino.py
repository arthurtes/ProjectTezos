import smartpy as sp

@sp.module
def main():   

    class Poll(sp.Contract):
        def __init__(self, title, fieldList):
            self.data.title = title
            self.data.fieldList = fieldList # A list of field from wich you can vote
            self.data.winners = sp.set()
            sp.cast(self.data.winners, sp.set[sp.address])

        @sp.entrypoint
        def vote(self, address, option):
            assert self.data.fieldList.contains(option), "Field not recognized"
            self.data.fieldList[option].add(address)
            
            

        @sp.entrypoint
        def result(self):
            lowestAddress = sp.set()
            lowestCount = 9999999999999999
            for key in self.data.fieldList.keys():
                if len(self.data.fieldList[key]) < lowestCount:
                    lowestCount = len(self.data.fieldList[key])
                    lowestAddress = self.data.fieldList[key]
            self.data.winners = lowestAddress


    class PollSet(sp.Contract):
        def __init__(self, title, start_time, end_time):
            self.data.author = sp.sender
            self.data.title = title
            self.data.players = sp.big_map()
            self.data.bets = []
            self.data.start_time = start_time
            self.data.end_time = end_time
            
        @sp.entrypoint
        def add_bet(self, question, answers):
            assert sp.now < self.data.end_time, "The time has ended"
            bet = sp.create_contract(Bet, None, sp.tez(0), sp.record(title=question, fieldList=answers, winners=sp.set()))
            self.data.bets.push(bet)
        
        @sp.entrypoint
        def participate(self):
            assert not (self.data.players.contains(sp.sender)), "you are already participating"
            assert sp.amount >= sp.tez(1), "you need to send at least 1 tez to participate"
            self.data.players[sp.sender] = 0

    
    
    @sp.effects(with_storage="read-only")
    def get_players():
        return self.data.players



@sp.add_test()
def test():
    scenario = sp.test_scenario("Test", main)
    alice = sp.test_account('Alice').address
    bob = sp.test_account('Bob').address
    eve = sp.test_account('Eve').address
    
    contract = main.Bet("Do you like Tezos", {"Yes": sp.set(), "No": sp.set()})
    scenario += contract

    contract.vote(sp.record(address = alice, option = "Maybe"), _valid = False, _exception = "Field not recognized")
    contract.vote(sp.record(address = alice, option = "Yes"))
    contract.vote(sp.record(address = bob, option = "No"))
    contract.vote(sp.record(address = alice, option = "No"))

    contract.result()
