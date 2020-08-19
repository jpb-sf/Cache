import time
import sys
import csv
import shutil


# Mock Cache LRU program is using a doubly linked-list to cache for fast insertion/deletion
# Then it uses a dictionary to 'hash map' values for fast lookup.
# Lookup will also require sorting afterwards, and sort and lookup are slow in a linked-list. 
# Best of both worlds using doubly-linked list, and backing it up with hash map


# fibonacci function
def fib(n):
	if n == 0:
		return "zero"
	if n == 1:
		return 0
	if n == 2 or n == 3:
		return 1
	else:
		return fib(n - 1) + fib(n - 2)


# Node class (constructor) 
class Node:
	def __init__(self, key, val=False):
		self.key = key
		if val:
			self.data = val
		else:
			self.data = fib(key)
		self.next = None
		self.prev = None

# LinkedList class (constructor)
class LinkedList:
	def __init__(self):
		self.head = None
		self.tail = None


# No function to add to Hash Table: 
#backup.update({key: val})

# The addLink function has double usage. First it adds the new nodes to linked-list from user entries. 
# Second, it  is utilized in loadCache function to rebuild the linked-list during a new session or 
# (program is closed and reopened)
def addLink(key, val):
	# If program cache is empty
	if llist.head == None:
		# Set head to Node class (becomes first node)
		llist.head = Node(key, val)
		# Point tail to head, as head pointer value becomes tail after a second node is added
		llist.tail = llist.head
	else:
		# Create new node
		new = Node(key, val)
		# Point new node 'next' to llist.head
		new.next = llist.head

		# Set tail 'prev' if not set
		if not llist.tail.prev:
			llist.tail.prev = new

		# Point head of list 'prev' to new node
		llist.head.prev = new 
		# Reset llist.head to point to the new node
		llist.head = new

# If key value already exists, function 'moves' node to , and pointers(next, prev) in Linked List accordingly
def linkSwap(key):

	current = llist.head
	# If list isn't empty, Loop through doubly linked-list checking to see if key already exists
	while current:
		# If the current.key matches the key
		if current.key == key:
			
			# If the key is not the first node
			if current.prev:
				# If the key is not the last node (Node removes itself)
				if current.next:
					
					# Point the previous node's next to current node's next value
					current.prev.next = current.next
					# Point the next node's prev to the current nodes' nev
					current.next.prev = current.prev

				# If the key is the last node, set the second last node's next to none
				else:
					current.prev.next = None
					# Set linked list tail to the traversing 'current' value's prev
					llist.tail = current.prev
				
				# Move new Node's next to head of list
				current.next = llist.head
				# Point current head prev to current (new) Node
				llist.head.prev = current
				# Reset llist.head to point to new Node 'current'
				llist.head = current

			# Node value exists, swap in order of the linked-list nodes was made
			return True

		# updates value for the while loop
		current = current.next
	# Node value does not already exist
	return False


# Function removes least-recently-used node from linked-list, and least-recently-used key/value pair from hash map
# It returns the key of llist.tail
def delLRU():
	# Set the second to last node by referencing the linked-list tail's previous
	deleteKeyValue = llist.tail.key
	
	# delete from hashmap backup
	del backup[deleteKeyValue]
	
	# Put the secondToLast.next to point to None
	llist.tail.prev.next = None
	# Reset the tail value 
	llist.tail = llist.tail.prev

	print('del LRU')

	return deleteKeyValue


# Load the program cache into both the hash map, and the doubly-linked list from the cache (fib.csv)
def loadCache():
	fieldnames = ['key', 'val']
	try:
		with open('fib.csv', 'r+') as fibCsv:
			csvReader = csv.DictReader(fibCsv)
			fibCsv.seek(0, 2)
			# If cache is not empty, load it
			if not fibCsv.tell() == 0:
		
				fibCsv.seek(0)
				print('csv is not empty')
				for line in csvReader:
					# Load hashmap
					backup.update({int(line['key']): int(line['val'])})
					# Load doubly linked-list
					addLink(int(line['key']), int(line['val']))

				print('Load cache')
				print(llist.head.key)		
				print(llist.tail.key)		
				print('backup is ' + str(backup))
					
	except Exception as e:
		print(e)
	

# Function adds new value as a new node to a linked list; a key/value pair in the hash map and the csv file
def updateCache(key, val):

	fieldnames = ['key', 'val']
	
	try:
		with open('fib.csv', 'a+', newline="") as fibW:
			# csvReader = csv.DictReader(fibR)
			csvWriter = csv.DictWriter(fibW, fieldnames=fieldnames)
			# Search to see if file is empty
			fibW.seek(0,2)
			# If file is empty
			if fibW.tell() == 0:
				fibW.seek(0)
				csvWriter.writeheader()
			csvWriter.writerow({'key': key, 'val': val})
	except Exception as e:
		print(e)

def removeCache(deleteKeyValue):

	fieldnames = ['key', 'val']
	
	try:
		with open('fib.csv', 'r') as fibR, open('fib.csv', 'a+', newline="") as fibW, \
		open('temp.csv', 'a+', newline="") as tempW:
			csvReader = csv.DictReader(fibR, fieldnames=fieldnames)
			csvWriter = csv.DictWriter(fibW, fieldnames=fieldnames)
			tempWriter = csv.DictWriter(tempW, fieldnames=fieldnames)
			print('csv is full')
			print('deleteKeyValue is ' + str(deleteKeyValue))
			# Reset csv cursor to delete tag
			# fibCsv.seek(0)
			# For ever line in csv if the key is NOT matching, write the line
			for line in csvReader:
				if not line['key'] == str(deleteKeyValue):
					tempWriter.writerow(line) 
			# shutil.move('content of source','to destination')
			shutil.move('temp.csv','fib.csv')
	except Exception as e:
		print(e)
		
def clearCache():
	try:
		# WOW big learn. To clear a whole csv, make a new file, and save it over the old one
		with open('fib.csv', 'r') as csvOld, open('new.csv', 'w', newline='') as csvNew:
			csvReader = csv.DictReader(csvOld)
			csvOld.seek(0, 2)
			# If cache is empty, there is nothing to delete and copy over, function stops.
			if not csvOld.tell() == 0:
				# shutil.move('content of source','to destination')
				shutil.move('new.csv','fib.csv')

				# Check if backup has been loaded yett
				if backup:
					# Empty hash-map
					backup.clear()

				# Check if llist has been loaded yet
				if llist.head:
					# Delete nodes in linked list
					trav = llist.head.next
					# While trav is not None
					while not trav:
						
						# Delete previous node
						if trav.prev:
							del trav.prev
						# If last node, delete
						else:
							del trav
						
						# Traverse to next node
						try:
							trav = trav.next
						except Exception as e:
							pass

					# Reset head tail values
					llist.head = None
					llist.tail = None
				
				result = "Cache is cleared"
				return result
			
			else:
				result = "Cache is already cleared"
				return result

	except Exception as e:
		print(e)

	
# function is called from readCache, 'reads'/ returns value from hashmap dict, if exists in cache
def returnCache(state, key):
	
	if state:

		return backup[key]
	else:
		val = fib(key)
		return val

	# cacheManager function returns cache value to user from hashmap backup, IF it exists.
# If it doesn't exist, it calculates value, returns, and saves it to program data structures,
# and the cache (csv file)
def cacheManager(key):
	
	deleteKeyValue = False
	# Check if key is in the program's uploaded cache hash table 'backup' which is make for quick lookup
	if key in backup:
		
		# Call returnCache function which sends value to user
		start = time.time()
		val = returnCache(True, key)
		end = time.time()
		elapsed = "{:.8f}".format(end - start)
		print('Return to user: Position ' + str(key) + ' is: ' + str(backup[key]))
		print('Time taken for cached value: ' + elapsed)

	# If the key is not uploaded into program cache hashmap
	if key not in backup:
		print("cache miss backup")
		
		# Kick the value back to the user before the program adds the new value to the cache
		# Call returnCache function which sends value to user
		start = time.time()
		val = returnCache(False, key)
		end = time.time()
		elapsed = "{:.8f}".format(end - start)
		print('Return to user: Position ' + str(key) + ' is: ' + str(val))
		print('Time taken for uncached value: ' + elapsed)

 	 # Then continue adding new value to the program's cache data structures, and csv.
	
	# capacity of cache is not full (False) until we check 
	capacity = False
	# If the backup hashmap is full and value is not already cached, delete last node in linked-list, and the key/value in backup
	if len(backup) >= 5 and not key in backup:
		# Cache capacity is Full (True)
		capacity = True
		print('Cache is full')
		
		# Delete value from program's memory (backup and linked-list)
		deleteKeyValue = delLRU()
		
		# Remove LRU value from cache
		removeCache(deleteKeyValue)

	# Finally, if key value does not exist in program memory already, add the new key value pair
	# to the linked-list (addLink()), and hash-table (backup), and then to the cache (updateCache())
	if not linkSwap(key):
		addLink(key, val)
		backup.update({key: val})
		updateCache(key, val) 
	print('new llist.head.key is ' + str(llist.head.key))
	print('new llist.tail.key is ' + str(llist.tail.key))
	print(backup)
	
#================================================================

# Switch representing first time entry is submitted by user after program is opened
first = True
# Greeting only when program first runs
greeting = True
# Switch for open/close value of program
program = True

while program:

	# If program just opened, initiate data structures
	if first:
		global llist
		llist = LinkedList()
		global backup 
		backup = {}
		# Greet users with menu options that can inputed
	if greeting == True:
		print(f'(For menu options, enter "m") \n\nHi User,')

	# Prompt user for a number
	print(f'what Fibonacci value would you like? \nEnter position number: ')
	
	# Receive input
	entry = input()
	greeting = False
	
	# If user chooses to close program, set vswitch to False
	if entry == 'n' or entry == 'N':
		program = False
		print('Program closed')
	
	# If program is still true
	elif program:
		
		if entry == "m" or entry == "M":
			print(f'Menu: \nEnter "c" to clear all cache. \nEnter "e" to exit program.\n' )

		elif entry == "e" or entry == "E":
			print('Program exited')
			sys.exit()
		
		elif entry == "c" or entry == "C":
			print("Are you sure you want to delete your cache? ('y' or 'n')")
			clear = False
			while not clear:
				confirm = input()
				if confirm == 'y' or confirm == 'Y':
					print(clearCache())
					clear = True

				elif confirm == 'n' or confirm == 'N':
					print('Cache is NOT cleared')
					clear = True
				
				elif not confirm == 'n' or not confirm =='N':
					print('To clear cache please confirm with a "y" for yes, or "n" to NOT clear cache')
			
		else:
			# Try to set value to an int
			try:
				entry = int(entry)
			
			# If you can't, # value is not all numberical characters, prompt for number
			except Exception as e:
				print('Please enter only a number value of 1 or greater.')

			# value is not an int, get node	
			if isinstance(entry, int):
				
				# If input is the very first input submitted after program is opened,
				if first == True:
					print("let's load cache")
					first = False
					# Load the cache values from csv into the program's linked-list, and hash map backup
					loadCache()
				
				# if entry is valid, read it
				cacheManager(entry)






