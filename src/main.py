# Robert Quan Ycharts Take Home

from Recon import Recon
import sys 

if __name__ == "__main__":

    if len(sys.argv) > 1: 
        reconInLocation = sys.argv[1]
    else:
        print("Please include filepath for recon.in file as comand line argument!")
        raise SystemExit
    
    recon = Recon(reconInLocation)
    recon.setup()
