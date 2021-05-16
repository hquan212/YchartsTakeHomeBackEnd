# Robert Quan Ycharts Take Home

import copy
from Account import Account

class Recon:
    """
    This is the main Reconciliation class.
    Attributes:

    """
    def __init__(self, fileLocations=None):
        """
        The constructor for Recon class.
        Parameters:
        """
        self.reconInFileLocation = fileLocations
        self.reconOutFileLocation = './output/recon.out'
        self.AccountA = None
        self.AccountB = None
        self.positiveCashActions = ['SELL', 'DIVIDEND', 'DEPOSIT']
        self.negativeCashActions = ['BUY', 'FEE']
        self.initializeState()

    def __groupCommands(self, sequence, sep=""):
        """
        Method to read in commands from recon file and create command blocks.
        """
        group = []
        for element in sequence:
            if element == sep:
                yield group
                group = []
                continue
            group.append(element)
        yield group

    def initializeState(self):
        """
        Method to read in commands from recon file and create command blocks.
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
            self.unitReconcilliation()

    def initializeNewAccount(self, typeOfCommand):
        """
        Initializes a new Account Object with its own assets and cash allocation
        """
        newAccount = Account(typeOfCommand[0])
        for command in typeOfCommand[1:]:
            assetTicket, assetValue = command.split()
            newAccount.addAsset(assetTicket, assetValue)
        return newAccount


    def runTransactions(self, account, transactions):
        transactionId = transactions[0]
        for transaction in transactions[1:]:
            actionList  = transaction.split()
            assetTicket = actionList[0]
            commandType = actionList[1]
            assetAmount = actionList[2]
            cashAmount  = actionList[3]
            if commandType.upper() in self.positiveCashActions:
                account.positiveCashAction(assetTicket, assetAmount, cashAmount)
            elif commandType.upper() in self.negativeCashActions:
                account.negativeCashAction(assetTicket, assetAmount, cashAmount)
        account.setDate(account.getDate().split('-')[0] + "-ACT")  # section actual amount name after transactions

    def unitReconcilliation(self):
        """
            Run reconcilliation. AccountB from AccountA. Produce new account C to reconOut
        """
        self.AccountA.showInfo()
        self.AccountB.showInfo()

        sharesA = self.AccountA.getShares()
        sharesB = self.AccountB.getShares()
        allKeys = copy.deepcopy(sharesB)
        sharesC = {}
        allKeys.update(sharesA)
        
        for ticket in allKeys.keys():
            if ticket in sharesB and ticket in sharesA: 
                differenceAmount =sharesB[ticket] - sharesA[ticket]
                if int(differenceAmount) == 0:
                    continue
                sharesC[ticket] = sharesB[ticket] - sharesA[ticket]
            elif ticket in sharesB and ticket not in sharesA: 
                sharesC[ticket] = sharesB[ticket]
            elif ticket not in sharesB and ticket in sharesA: 
                sharesC[ticket] = -1 * sharesA[ticket]
            else:
                continue

        totalCash = self.AccountB.getCash() - self.AccountA.getCash()
        self.writeToReconOutFile(sharesC, totalCash)

    def writeToReconOutFile(self, sharesDict, totalCash):

        with open(self.reconOutFileLocation, 'w') as fp: 
            cashLine = 'Cash ' +  str(totalCash) + '\n'
            fp.write(cashLine)
            for ticket, amount in sharesDict.items():
                ticketLine = ticket + ' ' + str(amount) + '\n'
                fp.write(ticketLine)