import random
import unittest

## Name : Isabella Valice
## People you worked with : Isabella Valice, Orli Forster, Margeaux Fortin
## Github URL :



### Customer Class
class Customer:

	# Constructor
	def __init__(self, name, money = 50):
		self.name = name
		self.money = money

	# Deposits money_top_add into customers account.
	def deposit_money(self, money_to_add):
		self.money += money_to_add

	# Pays the MedicineExpress driver	
	def make_payment(self, driver, amount):
		self.money = self.money - amount
		driver.receive_payment(amount)
				
		
	# Orders medicine from the pharmacy to be delivered by the driver,
	# assuming certain conditions are met.	
	def order_medicine(self, driver, pharmacy, drug_name, quantity):
		if not(driver.know_pharmacy(pharmacy)):
			print("Sorry, this service doesn't deliver from that pharmacy. Please try a different pharmacy!")
		elif self.money < driver.estimated_cost(pharmacy):
			print("Don't have enough money for that :( Please add more money to your account!")
		elif not(pharmacy.has_medicine(drug_name, quantity)):
			print("Our pharmacy has run out of " + drug_name + " :( Please try a different pharmacy!")
		else:
			bill = driver.place_order(pharmacy, drug_name, quantity)
			self.make_payment(driver, bill)
			self.take_medicine()

	# Takes the delivered medicine and prints out a message to indicate this.		
	def take_medicine(self):
		print("I am starting to feel better!")

	def __str__(self):
		return "Hello! My name is " + self.name + ". I have $" + str(self.money) + " and I need to order some medicine."

### Medicine Express Driver Class
class Driver:

	# Constructor. 
	def __init__(self, name, money = 500, pharmacies = [], delivery_fee = 5):
		self.name = name
		self.money = money
		self.pharmacies = pharmacies[:] # makes a copy of the list
		self.delivery_fee = delivery_fee

	# Adds a pharmacy to driver's known list of pharmacys	
	def add_pharmacy(self, new_pharmacy):
		self.pharmacies.append(new_pharmacy)

	# Receives payment from customer, and adds the money to the driver's account. 
	def receive_payment(self, money):
		self.money += money	

	# Returns the estimated cost of a delivery, namely the cost of the medicine
	# plus the driver's own delivery fee.	
	def estimated_cost(self, pharmacy, quantity):
		return ((pharmacy.cost * quantity) + self.delivery_fee)

	# Places an order at the pharmacy.
	# The delivery driver pays the pharmacy the cost.
	# The pharmacy processes the order
	# Function returns cost of the medicine + delivery fee.
	def place_order(self, pharmacy, drug_name, quantity):
		self.money = self.money - (pharmacy.cost * quantity)
		pharmacy.process_order(drug_name, quantity)
		return self.estimated_cost(pharmacy, quantity)

	# Returns boolean value letting customer know if this driver can deliver from that pharmacy or not.	
	def know_pharmacy(self, pharmacy):
		return pharmacy in self.pharmacies

	# string function.	
	def __str__(self):
		return "Hello, my name is " + self.name + " I am a Medicine Express driver, who has saved up $" + str(self.money) + ". I charge $" + str(self.delivery_fee) + " and I can deliver from " + str(len(self.pharmacies)) + " pharmacys."


### Create Pharmacy class here

class Pharmacy:
	def __init__(self, name, inventory, cost = 10, money = 500):
		self.name = name
		self.inventory = inventory
		self.cost = cost
		self.money = money
	
	def process_order(self, drug_name, quantity):
		if drug_name in self.inventory:
			self.inventory[drug_name] = self.inventory.get(drug_name, 0) - quantity
			self.money = self.money + quantity * self.cost

	def has_medicine(self, drug_name, quantity):
		if self.inventory[drug_name] >= quantity:
			return True
		return False

	def stock_up(self, drug_name, quantity):
		self.inventory[drug_name] = self.inventory.get(drug_name, 0) + quantity
	def __str__(self):
		return "Hello, we are " + self.name + ". These are the drugs that we currently have in stock" +self.inventory + 
		". We charge $" + self.cost + " per pill. We have $" + self.money + " in total."

class TestAllMethods(unittest.TestCase):

	def setUp(self):
		inventory = {"Vicodin":10, "Aderrall":30}
		self.c1 = Customer("Sulayman")
		self.c2 = Customer("Morgan", 150)
		self.p1 = Pharmacy("CVS", inventory, cost = 15)
		self.p2 = Pharmacy("Walgreens", inventory, cost = 12)
		self.p3 = Pharmacy("Meijer", inventory)
		self.d1 = Driver("Josephine")
		self.d2 = Driver("Joao", delivery_fee = 7, pharmacies = [self.p1, self.p2])

	## Check to see whether constructors work
	def test_customer_constructor(self):
		self.assertEqual(self.c1.name, "Sulayman")
		self.assertEqual(self.c2.name, "Morgan")
		self.assertEqual(self.c1.money, 50)
		self.assertEqual(self.c2.money, 150)

	## Check to see whether constructors work
	def test_driver_constructor(self):
		self.assertEqual(self.d1.name, "Josephine") 
		self.assertEqual(self.d1.delivery_fee, 5)
		self.assertEqual(self.d2.delivery_fee, 7)
		self.assertEqual(self.d1.pharmacies, [])
		self.assertEqual(len(self.d2.pharmacies), 2)

	## Check to see whether constructors work
	def test_pharmacy_constructor(self):
		self.assertEqual(self.p1.name, "CVS")
		self.assertEqual(self.p1.inventory, {"Vicodin":10, "Aderrall":30})
		self.assertEqual(self.p1.money, 500)
		self.assertEqual(self.p2.cost, 12)

	# Check that pharmacy can stock up properly.
	def test_stocking_medicine(self):
		inventory = {"Vicodin":10}
		p4 = Pharmacy("Miscellaneous Pharmacy", inventory)
		
		# Testing whether pharmacy can stock up on medicine	
		self.assertEqual(p4.inventory,{"Vicodin":10} )
		p4.stock_up("Vicodin", 10)
		p4.stock_up("Xanax", 20)
		self.assertEqual(p4.inventory, {"Vicodin": 20, "Xanax": 20})

	def test_make_payment(self):
		# Check to see how much money there is prior to a payment
		previous_money_customer = self.c2.money
		previous_money_driver = self.d2.money

		# Make the payment
		self.c2.make_payment(self.d2, 30)

		# See if money has changed hands
		self.assertEqual(self.c2.money, previous_money_customer - 30)
		self.assertEqual(self.d2.money, previous_money_driver + 30)


	# Check to see that MedicineExpress driver can manage pharmacies properly
	# (i.e., that add_restaurant and know_pharmacy work)
	def test_adding_and_knowing_pharmacy(self):
		d3 = Driver("Felix", delivery_fee = 7, pharmacies = [self.p1, self.p2])
		self.assertTrue(d3.know_pharmacy(self.p1))
		self.assertFalse(d3.know_pharmacy(self.p3))
		d3.add_pharmacy(self.p3)
		self.assertTrue(d3.know_pharmacy(self.p3))
		self.assertEqual(len(d3.pharmacies), 3)


	# Test that estimated cost works properly.
	def test_estimated_cost(self):
		self.assertEqual(self.d1.estimated_cost(self.p1, 5), 80)
		self.assertEqual(self.d2.estimated_cost(self.p2, 6), 79)


	# Check that pharmacy can properly see when it is empty
	def test_has_medicine(self):		

		# Test to see if has_medicine returns True when a pharmacy has medicine left
		self.assertEqual(self.p1.has_medicine("Vicodin", 5), True)
		# Test to see if has_medicine returns True when a pharmacy has 
		# just a little bit of medicine left (i.e., medicine_left == 1)
		self.assertEqual(self.p2.has_medicine("Vicodin", 9), True)
		# Test to see if has_medicine returns False when a pharmacy has no drugs left
		self.assertEqual(self.p1.has_medicine("Aderrall", 34), False)

	# Test order medicine
	def test_order_medicine(self):
		# test if customer doesn't have enough money to order

		# test if the pharmacy doesn't have medicine left in stock

		# check if the delivery drive can deliver from that pharmacy
		pass


def main():
	inventory1 = {"Advil": 20, "Aleeve": 120}
	inventory2 = {"Claritin":8 "Penicillin": 15}
	cust1 = Customer("Jane", 150)
	cust2 = Customer("Alex", 30)
	pharm1 = Pharmacy("CVS", inventory1, 12, 919)
	pharm2 = Pharmacy("Walgreens", inventory2, 10, 109)
	driver1 = Driver("Bill", 650, [pharm1, pharm2], 4)
	driver2 = Driver("Linda", 50, [pharm1, pharm2], 6)
	cust1.order_medicine(driver1, pharm1, "Claritin", 5)
	cust2.order_medicine(driver2, pharm2, "Aleeve", 3)

	

if __name__ == "__main__":
	main()
	print("\n")
	unittest.main(verbosity = 2)