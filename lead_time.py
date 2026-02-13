"""
Lead Times
"""

import math

def getMaxLeadTimeDays(leadTimes):
    return max(leadTimes)
    
def getAverageLeadTimeDays(leadTimes):
    return round(sum(leadTimes) / 10)
    
def getMaxLeadTimeMonths(leadTimes):
    maxDays = getMaxLeadTimeDays(leadTimes)
    return maxDays / 30.5

def getAverageLeadTimeMonths(leadTimes):
    averageDays = getAverageLeadTimeDays(leadTimes)
    return round(averageDays / 30.5, 2)

def getSDLeadTimesDays(leadTimes):
    average = getAverageLeadTimeDays(leadTimes)
    
    sum_squared_diff = sum([(lead - average) ** 2 for lead in leadTimes])
    
    variance = sum_squared_diff / 9
    
    sd = math.sqrt(variance)
    
    return sd
    
def getSDLeadTimesMonths(leadTimes):
    sd = getSDLeadTimesDays(leadTimes)
    
    m_sd = sd / 30.5
    
    return m_sd

def getSetLeadTimes(leadTimes):
    return set(leadTimes)

def getLeadTimes(delivery):
    lead = []
    
    for i in range(delivery):
        while True:
            try:
                time = int(input("Enter your lead time over delivery " + str(i + 1) + ": "))
                break
            except ValueError:
                print("Input must be an integer. Try Again.")
        lead.append(time)
    
    return lead
    
