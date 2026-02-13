
'''
Goal: create the safety quantity, and reorder point for any item for CSC
Additional Goals: update the program periodically for SKUnits information for the future --> Microsoft Tasks
'''
import math
import lead_time as lead
import zscore as z

class CSC:
    def __init__(self, jan, feb, mar, apr, may, jun, jul, aug, sep, octo, nov, dec, srv, rate, leadTimes):
        self.jan = jan
        self.feb = feb
        self.mar = mar
        self.apr = apr
        self.may = may
        self.jun = jun
        self.jul = jul
        self.aug = aug
        self.sep = sep
        self.octo = octo
        self.nov = nov
        self.dec = dec
        self.srv = srv
        self.rate = rate
        self.leadTimes = leadTimes
    
    def getAverageLeadTimeDays(self):
        return lead.getAverageLeadTimeDays(self.leadTimes)
    
    def getMaxLeadTimeDays(self):
        return lead.getMaxLeadTimeDays(self.leadTimes)
    
    def getAverageLeadTimeMonths(self):
        return lead.getAverageLeadTimeMonths(self.leadTimes)
    
    def getMaxLeadTimeMonths(self):
        return lead.getMaxLeadTimeMonths(self.leadTimes)
    
    def getMaxLeadTimeMonthsRounded(self):
        return round(self.getMaxLeadTimeMonths())
    
    def getSDFromLeadTimeDays(self):
        return lead.getSDLeadTimesDays(self.leadTimes)
    
    def getSDFromLeadTimeDaysRounded(self):
        return round(self.getSDFromLeadTimeDays(), 2)
    
    def getSDFromLeadTimeMonths(self):
        return lead.getSDLeadTimesMonths(self.leadTimes)
    
    def getSDFromLeadTimeMonthsRounded(self):
        return round(self.getSDFromLeadTimeMonths(), 2)
    
    def getNumberOfDeliveries(self):
        return 10
    
    def getTargetedServiceRate(self):
        return self.rate
    
    def getZScore(self):
        return z.getZScore(self.rate)
    
    def getTotal(self):
        total = (self.jan + self.feb + self.mar 
                 + self.apr + self.may + self.jun 
                 + self.jul + self.aug + self.sep + self.octo 
                 + self.nov + self.dec + self.srv)
        return total
    
    def getMean(self):
        mean = self.getTotal() / 12
        
        return mean
    
    def getMeanRounded(self):
        rounded = round(self.getMean())
        
        return rounded
    
    def getMeanDaily(self):
        mean = self.getTotal() / 365
        
        return mean
    
    def getMeanDailyRounded(self):
        rounded = round(self.getMeanDaily(), 1)
        
        return rounded
    
    def getSDFromTotal(self):
        mean = self.getMean()
        
        sum_squared_diff = ((self.jan - mean)**2 + (self.feb - mean)**2 
        + (self.mar - mean)**2 + (self.apr - mean)**2 + (self.may - mean)**2 
        + (self.jun - mean)**2 + (self.jul - mean)**2 + (self.aug - mean)**2 
        + (self.sep - mean)**2 + (self.octo - mean)**2 + (self.nov - mean)**2 
        + (self.dec - mean)**2)
        
        variance = sum_squared_diff / 11
        
        sd = math.sqrt(variance)
        
        return sd
    
    def getSDFromTotalRounded(self):
        return round(self.getSDFromTotal(), 1)
    
    def getSafetyStock(self):
        safety = self.getZScore() * self.getSDFromTotal() * math.sqrt(self.getAverageLeadTimeMonths())
        
        return safety
    
    def getSafetyStockRounded(self):
        return round(self.getSafetyStock())
    
    def getSafetyStockWithLeadTime(self):
        safety = self.getZScore() * math.sqrt((self.getAverageLeadTimeMonths() * (self.getSDFromTotal() ** 2))
                                                + (self.getMean() * self.getSDFromLeadTimeMonths()) ** 2)
        
        return safety
    
    def getSafetyStockWithLeadTimeRounded(self):
        return round(self.getSafetyStockWithLeadTime())
    
    def getReorderPoint(self):
        reorder = self.getSafetyStock() + self.getMean() * self.getAverageLeadTimeMonths()
        
        rounded = math.floor(reorder)
        
        return rounded
    
    def getReorderPointWithLeadTime(self):
        reorder = self.getSafetyStockWithLeadTime() + self.getMeanDaily() * self.getAverageLeadTimeDays()
        
        rounded = math.floor(reorder)
        
        return rounded
    
    def getReorderQuantity(self):
        daily = self.getMeanDaily()
        
        reorder_quantity = daily * 365 - self.getReorderPointWithLeadTime()
        
        rounded = round(reorder_quantity) + 1
        
        return rounded
    
    def getReorderQuantityNumDays(self):
        # rework this
        reorder = self.getReorderQuantity()
        
        quantity = {}
        lead_time_set = set(self.leadTimes)
        
        for lead in lead_time_set:
            lead_time_reorder = reorder * (lead / 365.25)
            rounded = round(lead_time_reorder)
            quantity[lead] = rounded
        
        sorted_quantity = dict(sorted(quantity.items()))
        
        return sorted_quantity
    


    
