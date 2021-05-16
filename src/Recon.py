# Robert Quan Ycharts Take Home

import copy
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
        self.initializeState()

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

    def initializeState(self):
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
            assetTicket, assetValue = command.split()
            newAccount.addAsset(assetTicket, assetValue)
        return newAccount

    def runTransactions(self, account, transactions):
        """
        Method to run every transaction command and update account. Will check for positive cash case or negative.
        """
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

    def unitReconciliation(self):
        """
            Run Unit Reconciliation. AccountB from AccountA. Produce new AccountC and write to recon.out file
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
        """
        Writes out to recon.out file.
        """
        with open(self.reconOutFileLocation, 'w') as fp: 
            cashLine = 'Cash ' +  str(totalCash) + '\n'
            fp.write(cashLine)
            for ticket, amount in sharesDict.items():
                ticketLine = ticket + ' ' + str(amount) + '\n'
                fp.write(ticketLine)