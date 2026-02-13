"""
Number of Deliveries
"""

def getDeliveries():
    while True:
        try:
            delivery = int(input("Enter number of deliveries: "))
            break
        except ValurError:
            print("Invalid input, try again.")
    
    return delivery
