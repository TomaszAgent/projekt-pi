n = int(input())
m = int(input())


class Contract:
    def __init__(self, first_name, last_name, contract_num):
        self.first_name = first_name
        self.last_name = last_name
        self.contract_num = contract_num
        self.next = None


class ContractList:
    def __init__(self):
        self.head = None
        self.tail = None

    def add_contract(self, first_name, last_name, contract_num):
        new_contract = Contract(first_name, last_name, contract_num)
        if self.head is None:
            self.head = new_contract
        else:
            self.tail.next = new_contract
        self.tail = new_contract

    def search_contract_num(self, last_name):
        current = self.head
        while current is not None:
            if current.last_name == last_name:
                return current.contract_num
            current = current.next
        return -1


contract_list = ContractList()

for i in range(n):
    first_name, last_name, contract_num = input().split()
    contract_list.add_contract(first_name, last_name, int(contract_num))

for i in range(m):
    last_name = input().strip()
    contract_num = contract_list.search_contract_num(last_name)
    print(contract_num)
