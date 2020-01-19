import time
import sys
import csv
import shutil

# conn = sqlite3.connect('cache.db')
# print("opened db successfully")
# cursor = conn.cursor()


# Mock Cache LRU program is using a doubly linked-list to cache for fast insertion/deletion
# Then it uses a backup dictionary that maps values for fast lookup.
# Lookup will also require sort afterwards, and sort and lookup are slow in a linked-list. 
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


# testing time to run function
start = time.time()
# print([fib(x) for x in range(32)])
#print(fib(89))
end = time.time()
elapsed = end - start


# Node class (constructor) 
class Node:
	def __init__(self, key):
		self.key = key
		self.data = fib(key)
		self.next = None
		self.prev = None

# LinkedList class (constructor)
class LinkedList:
	def __init__(self):
		self.head = None
		self.tail = None

# Dict backup for fast lookup for cache
class Map:
	def __init__(self):
		self.dict = dict()

	def add(self, key, val):
		self.dict[key] = val

	def get(self, key):
		return self.dict[key]


# Function adds new value as a new node to a linked list; a key/value pair in the hash map and the csv file
def backUp(key, val):

	fieldnames = ['key', 'val']
	try:
		with open('fib.csv', 'a+', newline="") as fibCsv:
			csvWriter = csv.DictWriter(fibCsv, fieldnames=fieldnames)
			# Search to see if file is empty
			fibCsv.seek(0,2)
			# If file is empty
			if fibCsv.tell() == 0:
				fibCsv.seek(0)
				csvWriter.writeheader()
			csvWriter.writerow({'key': key, 'val': val})
	except Exception as e:
		print(e)

def addHash(key):
	val = int(fib(key))
	
	# Back it for fast lookup(map to dict)
	backup.dict.update({key: val})
	backUp(int(key), val)

# Function has double usage, first it adds the new nodes to linked-list from user entries when program is open, 
# and also is utilized in loadCache function to rebuild the linked-list during a new session
def addLink(key):

	if llist.head == None:
		# Set head to Node class (becomes first node)
		llist.head = Node(key)
		# Point tail to head, as head pointer value becomes tail after a second node is added
		llist.tail = llist.head
	else:
		# Create new node
		new = Node(key)
		# Point new node 'next' to llist.head
		new.next = llist.head

		# Set tail 'prev' if not set
		if not llist.tail.prev:
			llist.tail.prev = new

		# Point head of list 'prev' to new node
		llist.head.prev = new 
		# Reset llist.head to point to the new node
		llist.head = new


# function removes last node
def delLink():
	# Set the second to last node by referencing the linked-list tail's previous
	secondToLast = llist.tail.prev
	
	# delete from backup
	del backup.dict[llist.tail.key]
	
	# Delete that node
	del secondToLast.next

	# Put the secondToLast.next to point to None
	secondToLast.next = None
	# Reset the tail value 
	llist.tail = secondToLast

	return llist


# Load the cache into both the hash map, and the doubly-linked list from the db (fib.csv)
def loadCache():
	try:
		with open('fib.csv', 'r') as fibCsv:
			csvReader = csv.DictReader(fibCsv)
			fibCsv.seek(0, 2)
			# If db is empty, there is nothing to load, function stops.
			if fibCsv.tell() == 0:
				pass
			# Else if the csv is not empty, load it
			else:
				fibCsv.seek(0)
				print('csv is not empty')
				for line in csvReader:
					# Load hashmap
					backup.dict.update({int(line['key']): int(line['val'])})
					# Load doubly linked-list
					addLink(int(line['key']))
		
		print('check1')		
		print(backup.dict)
		print('check2')		
	
	except Exception as e:
		print(e)
	
# function is called from readCache, 'reads'/ returns value from hashmap dict, if exists in cache
def returnCache(key):
	
	if key in backup.dict:
		print('Position ' + str(key) + ' is: ' + str(backup.dict[key]))
		return backup.dict[key]
	else:
		print("cache miss backup")
		# Kick the value back to the user before the program adds the new value to the cache
		print('Position ' + str(key) + ' is: ' + str(fib(key)))
		return fib(key)

# Function returns cache value to user from hashmap backup, then checks to see if key exists in liknked-list; 
# if it exists, updates doubly-linked list by moving node to front.
# If Node key does not exist in the linked-list, calls addLink function in order to add Node 
def readCache(key):

	# return value to user from the map backup cache if value exists, if not cached, calculate and return to user.
	# Then continue adding new value to the program's cache data structures, and then the csv
	returnCache(key)

	# If the backup hashmap is full and value is not already cached, delete last node in linked-list, and key/value in backup
	if len(backup.dict) >= 5 and not key in backup.dict:
		print('delete')
		delLink()

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
				
				# Move new Node's next to head of list
				current.next = llist.head
				# Point current head prev to current (new) Node
				llist.head.prev = current
				# Reset llist.head to point to new Node 'current'
				llist.head = current

				return "updated"
			else:
				return "Node at front"

		current = current.next
	addLink(key)
	addHash(key)
	return "cache miss linked-list"


def delCache():
	try:
		# WOW big learn. To clear a whole csv, make a new file, and save it over the old one
		with open('fib.csv', 'r') as csvOld, open('new.csv', 'w', newline='') as csvNew:
			csvReader = csv.DictReader(csvOld)
			csvOld.seek(0, 2)
			# If db is empty, there is nothing to load, function stops.
			if not csvOld.tell() == 0:
				# shutil.move('content of source','to destination')
				shutil.move('new.csv','fib.csv')
				llist = LinkedList()
				backup = Map()
			else:
				print('Cache is alread empty')
				
	except Exception as e:
		print(e)

first = True

# Greet users with menu options that can inputed
print(f'(For menu options, enter "m") \n\nHi User,')
program = True
while(program):

	# Prompt user for a number
	print(f'what Fibonacci value would you like? \nEnter position number: ')
	# Receive input
	entry = input()

	# If user chooses to close program, set vswitch to False
	if entry == 'n' or entry == 'N':
		program = False
		print('Program closed')
	
	# If program is still true
	elif program:
		
		if entry == "m" or entry == "M":
			print(f'Menu: \n Enter "n" to close program. \n Enter "s" to see status of cache values. \n' +
			' Enter "d" to delete all cache \n' )
		
		elif entry == "d" or entry == "D":
			print("Are you sure you want to delete your cache? ('y' or 'n')")
			delCache()
		
		else:
			# Try to set value to an int
			try:
				entry = int(entry)
			
			# If you can't, # value is not all numberical characters, prompt for number
			except Exception as e:
				print('Please enter only a number value of 1 or greater.')

			# value is not an int, get node	
			if isinstance(entry, int):
				
				# If first user input after program is opened, set data structures
				if first == True:
					global llist
					llist = LinkedList()
					global backup 
					backup = Map()
					first = False
					print('no problems here')
					# Load the cache values from csv into the program's linked-list, and hash map backup
					loadCache()
				
				# If this is not the first user input
				else:
					print('not first input')
				
				readCache(entry)
	







# print(llist.head)
# readCache(1) # cache miss backup, return '1', cache miss linked-list

# readCache(2)
# readCache(3)
# print(llist.head.key) # 3
# print(llist.tail.key) # 1
# readCache(10)
# readCache(4) #Length is still 4 until AFTER the function finishes, then it becomes 5. The next call will delete the sixth value
# print('the tail is ' + str(llist.tail.key)) # 1
# print(backup.dict) # {1: 1, 2: 2, 3: 3, 10: 89, 4: 5}
# readCache(5) # 8, delete tail
# print(llist.head.key) # 5
# print(llist.tail.key) # 2
# print(backup.dict) # {1: 1, 2: 2, 3: 3, 10: 89, 4: 5}
# print('the tail is ' + str(llist.tail.key)) # 2
# readCache(12) 
# print(backup.dict) # {2: 2, 3: 3, 10: 89, 4: 5, 12: 233}

# readCache(8) 
# print(backup.dict) # {3: 3, 10: 89, 4: 5, 12: 233, 8: 34}


# print(llist.head.key) # head is 8	
# print(llist.head.next.key) # next is 12

# print(llist.tail.key) # tail is 10
# readCache(10)
# print(llist.head.key) # head is 10
# print(llist.head.next.key) # next is 8

# print(llist.tail.key) # key is still 10!








