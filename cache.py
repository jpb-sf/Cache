import time
import sys

# Program is using a doubly linked-list to cache for fast insertion/deletion
# Then ut uses a backup dictionary that maps values for fast lookup.
# Lookup will alsio require sort afterwards, and sort and lookup are slow in a linked-list. 
# Best of both worlds using doubly-linked list, and backing it up mapping dictionary


# fibonacci function
def fib(n):

	if n == 0 or n == 1:
		return 1
	else:
		return fib(n - 1) + fib(n - 2)

# testing time to run function
start = time.time()
# print([fib(x) for x in range(32)])
#print(fib(89))
end = time.time()
elapsed = end - start
print(elapsed)

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


# Build a doubly linked-list!
llist = LinkedList()
backup = Map()
count = 0

# Function adds new node to a linked list
def addLink(key):

	# If list doesn't exit
	if llist.head == None:
		# Set head to Node class (becomes first node)
		llist.head = Node(key)
		# Point tail to head, as head pointer value becomes tail after a second node is added
		llist.tail = llist.head
		
		# Back it for fast lookup(map to dict)
		backup.add(key, Node(key).data)
		return llist
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

		# Back it for fast lookup(map to dict)
		backup.add(key, Node(key).data)

		return llist

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

# function is called from readCache, 'reads'/ returns value from hashmap dict, if exists in cache
def returnCache(key):
	if key in backup.dict:
		print(backup.dict[key])
		return backup.dict[key]
	else:
		print("cache miss backup")
		# Kick the value back to the user before the program adds the new value to the cache
		print(fib(key))
		return fib(key)

# Function returns cache value from hashmap backup, then updates doubly-linked list by moving node to front. 
def readCache(key):

	# return value to user from the map backup cache if value exists, if not cached, calculate and return to user.
	# Then continue adding new value to cache
	returnCache(key)

	# If the backup hashmap is full and value is not already cached, delete last node in linked-list, and key/value in backup
	if len(backup.dict) >= 5 and not key in backup.dict:
		print('delete')
		delLink()

	current = llist.head
	# Loop through doubly linked-list beginning with llink.head to move it to front of cache
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
				
				# Move current Node to head of list
				current.next = llist.head
				# Point current head previous to current
				llist.head.prev = current
				# Reset llist.head to point to key
				llist.head = current

				return "updated"
			else:
				return "Node at front"

		current = current.next
	addLink(key)
	return "cache miss linked-list"

readCache(1) # cache miss backup, return '1', cache miss linked-list
readCache(2)
readCache(3)
print(llist.head.key) # 3
print(llist.tail.key) # 1
readCache(10)
readCache(4) #Length is still 4 until AFTER the function finishes, then it becomes 5. The next call will delete the sixth value
print('the tail is ' + str(llist.tail.key)) # 1
print(backup.dict) # {1: 1, 2: 2, 3: 3, 10: 89, 4: 5}
readCache(5) # 8, delete tail
print(llist.head.key) # 5
print(llist.tail.key) # 2
print(backup.dict) # {1: 1, 2: 2, 3: 3, 10: 89, 4: 5}
print('the tail is ' + str(llist.tail.key)) # 2
readCache(12) 
print(backup.dict) # {2: 2, 3: 3, 10: 89, 4: 5, 12: 233}

readCache(8) 
print(backup.dict) # {3: 3, 10: 89, 4: 5, 12: 233, 8: 34}


print(llist.head.key) # head is 8	
print(llist.head.next.key) # next is 12

print(llist.tail.key) # tail is 10
readCache(10)
print(llist.head.key) # head is 10
print(llist.head.next.key) # next is 8

print(llist.tail.key) # key is still 10!








