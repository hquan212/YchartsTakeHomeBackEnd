# Robert Quan Ycharts Take Home

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
        self.reconFileLocation = fileLocations
        self.initializeState()

    def initializeState(self):
          with open(self.reconFileLocation) as fp:
            for line in fp:
              print(line)