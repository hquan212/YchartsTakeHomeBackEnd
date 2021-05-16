# Robert Quan Ycharts Take Home


class Account:
    """
        Class Account:
            Object that can store a running cash balance, dictionary collection of assets under 
            portolio and unique date name.
    """
    def __init__(self, date=None):
        self.__date = date 
        self.__shares = {} 
        self.__cash = 0 
    
    def getShares(self):
        return self.__shares
    
    def getCash(self):
        return self.__cash

    def setDate(self, date):
        self.__date = date 

    def getDate(self):
        return self.__date

    def addAsset(self, ticket, amount):
        """
            Method to add a new asset to this account. Will 
        """
        amount = float(amount)
        if ticket.lower() == 'cash':
            self.addCashAmount(amount)
            return
        if ticket in self.__shares:
            self.__shares[ticket] += amount
        else:
            self.__shares[ticket] = amount

    def addCashAmount(self, cashAmount):
        self.__cash += float(cashAmount)

    def removeCashAmount(self, cashAmount):
        self.__cash -= float(cashAmount)

    def positiveCashAction(self, ticket, assetAmount, cashAmount):
        """
            If the overall cash balance increases, use this method to update Account object.
            Keywords: Sell, Dividend, Deposit
        """
        if ticket.lower() == 'cash':
            self.addCashAmount(cashAmount)
            return
        if not ticket in self.__shares:  # short sell
            self.addAsset(ticket, -1*assetAmount)
        self.__shares[ticket] -= float(assetAmount)
        self.clearEmptyAssets(ticket)
        self.__cash += float(cashAmount)
        return 

    def negativeCashAction(self, ticket, assetAmount, cashAmount):
        """
            If the overall cash balance decreases, use this method to update Account object.
            Keywords: Buy, Fee
        """
        if ticket.lower() == 'cash':
            self.removeCashAmount(cashAmount)
            return
        if not ticket in self.__shares:
            self.addAsset(ticket, assetAmount)
        else:
            self.__shares[ticket] += float(assetAmount)
        self.clearEmptyAssets(ticket)
        self.__cash -= float(cashAmount)
        return 
    
    def clearEmptyAssets(self, ticket):
        """
            Removes an empty asset from the shares list.
        """
        if self.__shares[ticket] == 0:
            del self.__shares[ticket]

    def showInfo(self):
        print("-======================", self.__date,"==========================================")
        print('self.__shares')
        print(self.__shares)
        print() 
        print('Cash on Hand:')
        print(self.__cash)
        print("-================================================================\n\n")
        return