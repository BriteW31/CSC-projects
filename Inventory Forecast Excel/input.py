import CSC_reorder_point_safety_quantity_UPDATED as csc
import months as m
import lead_time as lead
import zscore as z
import delivery as d
import output as out
import file as f
import excel as e

# user input function
def getSKUnit():
    
    location = input("Location: ")
    sku = input("Item SKU: ")    
    source = input("Type 'excel' to load latest forecast, or press anything else for manual input: ")
    sales_data = {}
    
    if source == "excel":
        
        
        filename = input("Enter Excel filename (press Enter to get default: Sales_Excel.xlsx): ")
        if filename == "":
            filename = "Sales_Excel.xlsx"
                    
        loaded_data = e.get_forecast_data(sku, location, filename)
                
        if loaded_data:
            sales_data['jan'] = int(loaded_data.get('jan', 0))
            sales_data['feb'] = int(loaded_data.get('feb', 0))
            sales_data['mar'] = int(loaded_data.get('mar', 0))
            sales_data['apr'] = int(loaded_data.get('apr', 0))
            sales_data['may'] = int(loaded_data.get('may', 0))
            sales_data['jun'] = int(loaded_data.get('jun', 0))
            sales_data['jul'] = int(loaded_data.get('jul', 0))
            sales_data['aug'] = int(loaded_data.get('aug', 0))
            sales_data['sep'] = int(loaded_data.get('sep', 0))
            sales_data['octo'] = int(loaded_data.get('oct', 0))
            if 'octo' not in loaded_data and 'oct' in loaded_data:
                sales_data['octo'] = int(loaded_data['oct'])
            sales_data['nov'] = int(loaded_data.get('nov', 0))
            sales_data['dec'] = int(loaded_data.get('dec', 0))
            sales_data['srv'] = int(loaded_data.get('srv', 0))
        else:
            print("Switching to manual input due to error.\n")
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
    
    else:
        print("Enter monthly SKU sales here: \n")
        
        sales_data['jan'] = m.getJan()
        sales_data['feb'] = m.getFeb()
        sales_data['mar'] = m.getMar()
        sales_data['apr'] = m.getApr()
        sales_data['may'] = m.getMay()
        sales_data['jun'] = m.getJun()
        sales_data['jul'] = m.getJul()
        sales_data['aug'] = m.getAug()
        sales_data['sep'] = m.getSep()
        sales_data['octo'] = m.getOct()
        sales_data['nov'] = m.getNov()
        sales_data['dec'] = m.getDec()
        sales_data['srv'] = m.getSRV()
    
    print("\n")
    
    delivery = d.getDeliveries()
    
    print("\n")
    
    leadTimes = lead.getLeadTimes(delivery)
    
    print("\n")
    
    rate = z.getRate()
    
    print("\n")
    
    sales = csc.CSC(sales_data['jan'], sales_data['feb'], sales_data['mar'], 
                    sales_data['apr'], sales_data['may'], sales_data['jun'], 
                    sales_data['jul'], sales_data['aug'], sales_data['sep'], 
                    sales_data['octo'], sales_data['nov'], sales_data['dec'], 
                    sales_data['srv'], rate, leadTimes)
    
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

