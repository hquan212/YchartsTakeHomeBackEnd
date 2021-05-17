# Robert Quan Ycharts Take Home

from Account import Account

class Recon:
    """
        Class Recon
            It will read in the instruction set from recon.in and
            it will create two Account objects and update accordingly
            and perform updates based on transactions instructions.
    """
    def __init__(self, fileLocations=None):
        self.reconInFileLocation = fileLocations
        self.reconOutFileLocation = './output/recon.out'
        self.AccountA = None
        self.AccountB = None
        self.positiveCashActions = ['SELL', 'DIVIDEND', 'DEPOSIT']
        self.negativeCashActions = ['BUY', 'FEE']

    def __groupCommands(self, sequence, sep=""):
        """
        Private method to create command blocks.
        """
        group = []
        for element in sequence:
            if element == sep:
                yield group
                group = []
                continue
            group.append(element)
        yield group

    def setup(self):
        """
        Method to read in commands from recon file.
        Will execute the run command to update Accounts.
        """
        commandBlocks = []
        with open(self.reconInFileLocation) as fp:
            completeComands = [line.strip() for line in fp.readlines()]
            for block in self.__groupCommands(completeComands):
                commandBlocks.append(block)
        self.runBlockCommands(commandBlocks)

    def runBlockCommands(self, commandBlocksList = []):
        """
        Method to run each command block. Creates respective accounts and runs Transactions
        """
        self.AccountA = self.initializeNewAccount(commandBlocksList[0])
        self.runTransactions(self.AccountA, commandBlocksList[1])
        self.AccountB = self.initializeNewAccount(commandBlocksList[2])
        if self.AccountA and self.AccountB:
            self.unitReconciliation()
        else:
            print("Missing account two reconcile. Please check input file.")

    def initializeNewAccount(self, typeOfCommand):
        """
        Initializes a new Account Object with its own assets and cash allocation
        """
        newAccount = Account(typeOfCommand[0])
        for command in typeOfCommand[1:]:
            symbol, assetValue = command.split()
            newAccount.addAsset(symbol, assetValue)
        return newAccount

    def runTransactions(self, account, transactions):
        """
        Method to run every transaction command and update account. Will check for positive cash case or negative.
        """
        transactionId = transactions[0]
        for transaction in transactions[1:]:
            actionList  = transaction.split()
            symbol = actionList[0]
            transactionCode = actionList[1]
            shareAmount = actionList[2]
            totalValue  = actionList[3]
            if transactionCode.upper() in self.positiveCashActions:
                account.positiveCashAction(symbol, shareAmount, totalValue)
            elif transactionCode.upper() in self.negativeCashActions:
                account.negativeCashAction(symbol, shareAmount, totalValue)
        account.setDate("D1-ACT")  # section actual amount name after transactions

    def unitReconciliation(self):
        """
            Run Unit Reconciliation. AccountB from AccountA. Produce new AccountC and write to recon.out file
        """
        self.AccountA.showInfo()
        self.AccountB.showInfo()

        sharesA = self.AccountA.getShares()
        sharesB = self.AccountB.getShares()
        allTickets = set(sharesB).union(set(sharesA))
        sharesC = {}

        for ticket in allTickets:
            if ticket in sharesB and ticket in sharesA: 
                differenceAmount = sharesB[ticket] - sharesA[ticket]
                if int(differenceAmount) == 0:
                    continue
                sharesC[ticket] = differenceAmount
            elif ticket in sharesB and ticket not in sharesA: 
                sharesC[ticket] = sharesB[ticket]
            elif ticket not in sharesB and ticket in sharesA: 
                sharesC[ticket] = -1 * sharesA[ticket]
            else:
                continue

        totalCash = self.AccountB.getCash() - self.AccountA.getCash()
        self.writeToReconOutFile(sharesC, totalCash)

    def writeToReconOutFile(self, sharesDict, totalCash):
        """
        Writes out to recon.out file.
        """
        print("-====================== Unit Reconciliation ==========================================")

        with open(self.reconOutFileLocation, 'w') as fp: 
            cashLine = 'Cash ' +  str(totalCash) + '\n'
            print(cashLine)
            fp.write(cashLine)
            for ticket, amount in sharesDict.items():
                ticketLine = ticket + ' ' + str(amount) + '\n'
                print(ticketLine)
                fp.write(ticketLine)