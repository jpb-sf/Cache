import time
import sys
import csv
import shutil

"""
Mock Ccche LRU program uses a doubly linked-list to cache for fast insertion/deletion,
along with keeping track of 'LRU order.' The program also uses a dictionary to 'hash map' key/vals
for the fast lookup of values. As lookup is slow in a linked-list, and insertion/deletion 
is slower in a hashmap, the program uses best of both worlds; a linked-list, and hash-map 
for a smooth LRU cache. 
"""

# fibonacci function (helper function to illustray LRU times)
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

# No function to add to Hash Table: (backup.update({key: val}))

# The add_link() first adds the new nodes to linked-list from user entries. 
# Second, it  is utilized in load_cache function to rebuild the linked-list during a new session, 
# or  if program is closed and reopened
def add_link(key, val):
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

# If key value already exists, function 'moves' node, and pointers(next, prev) in Linked List accordingly
def link_swap(key):

	current = llist.head
	# If list isn't empty, Loop through doubly linked-list checking to see if key already exists
	while current:
		# If the current.key matches the key
		if current.key == key:
			
			# If the key is not the first node, (if it is, function returns true, exits)
			if current.prev:
				# If the key is not the last node (Node removes itself)
				if current.next:
					
					# Point the previous node's next to current node's next value
					current.prev.next = current.next
					# Point the next node's prev to the current nodes' nev
					current.next.prev = current.prev

				# If the key is the last node,
				else:
					# Set the second last node's next to none
					current.prev.next = None
					# Set linked list tail to the 'current' value's prev (second to last)
					llist.tail = current.prev
				
				# Move new Node 'current's' next pointer to the llist.head (current head becomes the second node in the LL)
				current.next = llist.head
				# Point current head prev to the current Node (connection finished)
				llist.head.prev = current
				# Reset llist.head to point to the new Node 'current'
				llist.head = current

			# Node value exists, swap in order of the linked-list nodes was made
			return True

		# updates value for the while loop
		current = current.next
	# Node value does not already exist
	return False


# Function removes least-recently-used node from linked-list, and least-recently-used key/value pair from hash map
# It returns the key of llist.tail
def del_LRU():
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


# Load the program's 'cache' into both its hash map, and doubly-linked list from the db (fib.csv)
def load_cache():
	fieldnames = ['key', 'val']
	try:
		with open('fib.csv', 'r+') as fibCsv:
			csvReader = csv.DictReader(fibCsv)
			fibCsv.seek(0, 2)
			# If cache is not empty, load it
			if not fibCsv.tell() == 0:
		
				fibCsv.seek(0)
				for line in csvReader:
					# Load hashmap
					backup.update({int(line['key']): int(line['val'])})
					# Load doubly linked-list
					add_link(int(line['key']), int(line['val']))

				print('Load cache')
				print(llist.head.key)		
				print(llist.tail.key)		
				print('backup is ' + str(backup))
					
	except Exception as e:
		print(e)
	

# Function adds new value as a new node to a linked list; a key/value pair in the hash map and the csv file
def update_cache(key, val):

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

def remove_cache(deleteKeyValue):

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
		
def clear_cache():
	try:
		#Clear the whole csv, by making a new file, and saving it over the old one
		with open('fib.csv', 'r') as csvOld, open('new.csv', 'w', newline='') as csvNew:
			csvReader = csv.DictReader(csvOld)
			csvOld.seek(0, 2)
			# If cache is empty, there is nothing to delete and copy over, function stops.
			if not csvOld.tell() == 0:
				# shutil.move('content of source','to destination')
				shutil.move('new.csv','fib.csv')

				# Check if backup has been loaded yet
				if backup:
					# Empty hash map
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

	
# Function is called from readCache, 'reads'/ returns value from hashmap dict, if exists in cache
def return_cache(state, key):
	
	if state:

		return backup[key]
	else:
		val = fib(key)
		return val

# cache_manager() function returns cache value to user from hashmap backup, IF it exists.
# If it doesn't exist, it calculates value, returns, and saves it to program data structures,
# and the cache (csv file)
def cache_manager(key):
	
	deleteKeyValue = False
	# Check if key is in the program's uploaded cache hash table 'backup' which is make for quick lookup
	if key in backup:
		
		# Call return_cache function which sends value to user
		start = time.time()
		val = return_cache(True, key)
		end = time.time()
		elapsed = "{:.8f}".format(end - start)
		print('Return to user: Position ' + str(key) + ' is: ' + str(backup[key]))
		print('Time taken for cached value: ' + elapsed)

	# If the key is not uploaded into program cache hashmap
	if key not in backup:
		print("cache miss backup")
		
		# Kick the value back to the user before the program adds the new value to the cache
		# Call return_cache function which sends value to user
		start = time.time()
		val = return_cache(False, key)
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
		deleteKeyValue = del_LRU()
		
		# Remove LRU value from cache
		remove_cache(deleteKeyValue)

	# Finally, if key value does not exist in program memory already, add the new key value pair
	# to the linked-list (add_link()), and hash-table (backup), and then to the cache (update_cache())
	if not link_swap(key):
		add_link(key, val)
		backup.update({key: val})
		update_cache(key, val) 
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
	
	
	# If program is still true
	if program:
		
		if entry == "m" or entry == "M":
			print(f'Menu: \nEnter "c" to clear all cache. \nEnter "e" to exit program.\n' )

		elif entry == "e" or entry == "E":
			print('Program exited')
			program = False
			sys.exit()
		
		elif entry == "c" or entry == "C":
			print("Are you sure you want to delete your cache? ('y' or 'n')")
			clear = False
			while not clear:
				confirm = input()
				if confirm == 'y' or confirm == 'Y':
					print(clear_cache())
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
			
			# If you can't, # value is not all numerical characters, prompt for number
			except Exception as e:
				print('Please enter only a number value of 1 or greater.')

			# if entry is int
			if isinstance(entry, int):
				
				# If input is the very first input submitted after program is opened,
				if first == True:
					first = False
					# Load the cache values from csv db into the program's linked-list, and hash map 
					load_cache()
				
				# if entry is valid, itread 
				cache_manager(entry)






