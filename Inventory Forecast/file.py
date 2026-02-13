"""
File Writer
"""
def checker(sales, sku, location):
    check = input("Type 'yes' for saving information into file, type 'no' to not save information: ")
    while True:
        if check == "yes":
            fileWriter(sales, sku, location)
            break
        elif check == "no":
            break
        else:
            print("Invalid input. Try again. \n")

def fileWriter(sales, sku, location):
    filename = f"{sku}_{location}_sku_info.txt"
    
    with open(filename, 'w') as f:
        f.write("Stockkeeping Info for " + sku + " from " + location + "\n")
        f.write("Safety Stock Quantity on Demand Only: " + str(sales.getSafetyStockRounded()) + "\n")
        f.write("Reorder Point on Demand Only: " + str(sales.getReorderPoint()) + "\n")
        f.write("Safety Stock Quantity on Lead Time: " + str(sales.getSafetyStockWithLeadTimeRounded()) + "\n")
        f.write("Reorder Point on Lead Time: " + str(sales.getReorderPointWithLeadTime()) + "\n")
        f.write("Reorder Quantity: " + str(sales.getReorderQuantity()) + "\n")
        
        quantities = sales.getReorderQuantityNumDays()
        for quantity in quantities:
            f.write("Reorder Quantity for " + str(quantity) + " days: " + str(quantities[quantity]) + "\n")
    
    print(filename + " has been successfully created.")

