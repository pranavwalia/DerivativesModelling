import math
import random
import numpy

##Simple Monte Carlo Pricing Class for Vanilla Call Option
class SimpleMCPricer():
    def __init__(self, expiry, strike, spot, vol, r, paths):
        #The sigma value on the left side of the exponent
        self.variance = vol**2 * expiry
        #The sigma value on the right side of the e exponent
        self.root_Variance = math.sqrt(self.variance)
        #Corresponds to the (-1/2 * sigma^2)
        self.itoCorr = -0.5*self.variance
        ##Corresponds to S0e^(rT - 1/2 sigma^2T)
        self.movedSpot = spot*math.exp(r*expiry + self.itoCorr)
        self.runningSum = 0
        ##Simulate for all paths
        for i in range(0,paths):
            thisGauss = numpy.random.normal()
            ##Our rootVariance already has been multiplied by the expiry
            thisSpot = self.movedSpot*math.exp(self.root_Variance*thisGauss)
            #Determine payoff of this specific path
            thisPayoff = thisSpot - strike
            #Value of option is zero is our price is less than the strike
            thisPayoff = thisPayoff if thisPayoff > 0 else 0
            self.runningSum+=thisPayoff
        
        self.mean = self.runningSum/paths
        self.mean*= math.exp(-r * expiry)
    
    def getMean(self):
        return round(self.mean,2)
    
if __name__ == '__main__':
    model = SimpleMCPricer(2,32,30,.1,0.03,1000000)
    print("Price",model.getMean())

