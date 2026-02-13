"""
Output
"""

# output information
def printSKUnit(sales, sku, location):
    print("Stockkeeping Info for " + sku + " from " + location + "\n")
    
    print("Total Sales: " + str(sales.getTotal()))
    print("Average Monthly Sales: " + str(sales.getMeanRounded()))
    print("Average Daily Sales: " + str(sales.getMeanDailyRounded()))
    print("Demand Standard Deviation: " + str(sales.getSDFromTotalRounded()))
    
    print("\n")
    
    print("Average Lead Time in Days: " + str(sales.getAverageLeadTimeDays()))
    print("Average Lead Time in Months: " + str(sales.getAverageLeadTimeMonths()))
    print("Max Lead Time in Days: " + str(sales.getMaxLeadTimeDays()))
    print("Max Lead Time in Months: " + str(sales.getMaxLeadTimeMonthsRounded()))
    print("Lead Time Standard Deviation in Days: " + str(sales.getSDFromLeadTimeDaysRounded()))
    print("Lead Time Standard Deviation in Months: " + str(sales.getSDFromLeadTimeMonthsRounded()))
    print("Targetted Service Rate: " + str(sales.getTargetedServiceRate()) + "%")
    print("Z-Score: " + str(sales.getZScore()))
    
    print("\n")
    
    print("Safety Stock Quantity on Demand Only: " + str(sales.getSafetyStockRounded()))
    print("Reorder Point on Demand Only: " + str(sales.getReorderPoint()))
    
    print("Safety Stock Quantity on Lead Time: " + str(sales.getSafetyStockWithLeadTimeRounded()))
    print("Reorder Point on Lead Time: " + str(sales.getReorderPointWithLeadTime()))
    
    quantities = sales.getReorderQuantityNumDays()
    print("Reorder Quantity: " + str(sales.getReorderQuantity()))
    for quantity in quantities:
        print("Reorder Quantity for " + str(quantity) + " days: " + str(quantities[quantity]))
