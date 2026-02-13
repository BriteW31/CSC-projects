import CSC_reorder_point_safety_quantity_UPDATED as csc
import months as m
import lead_time as lead
import zscore as z
import delivery as d
import output as out
import file as f

# user input function
def getSKUnit():
    print("Enter monthly HFX SKU sales here: \n")
    
    location = input("Location: ")
    sku = input("Item SKU: ")
    jan = m.getJan()
    feb = m.getFeb()
    mar = m.getMar()
    apr = m.getApr()
    may = m.getMay()
    jun = m.getJun()
    jul = m.getJul()
    aug = m.getAug()
    sep = m.getSep()
    octo = m.getOct()
    nov = m.getNov()
    dec = m.getDec()
    srv = m.getSRV()
    
    print("\n")
    
    delivery = d.getDeliveries()
    
    print("\n")
    
    leadTimes = lead.getLeadTimes(delivery)
    
    print("\n")
    
    rate = z.getRate()
    
    print("\n")
    
    sales = csc.CSC(jan, feb, mar, apr, may, jun, jul, aug, sep, octo, nov, dec, srv, rate, leadTimes)
    out.printSKUnit(sales, sku, location)
    
    print("\n")
    
    f.checker(sales, sku, location)
    

# calling function
while (True):
    loop_str = input("Type 'yes' for SKUnits, type 'no' to quit: ")
    
    if (loop_str == 'no'):
        break
    elif (loop_str == 'yes'):
        getSKUnit()
        print("\n\n")
    else:
        print("Invalid input. Try again. \n")

