import time


import time


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

# Function adds new node to a linked list
def addLink(key):

	# If list doesn't exit
	if llist.head == None:
		# Set head to Node class (becomes first node)
		llist.head = Node(key)
		# Point tail to head, as head pointer value becomes tail after a second node is added
		llist.tail = llist.head
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
	# Delete that node
	del secondToLast.next
	# Put the secondToLast.next to point to None
	secondToLast.next = None
	# Reset the tail value 
	llist.tail = secondToLast
	return llist

		

# Read llist, if there is match move the key to the front of the list
def readCache(key):
	current = llist.head
	# Loop through doubly linked-list beginning with llink.head
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
			# If the key matches	
			return llist

		current = current.next
	
	return "cache miss"

addLink(1)
addLink(2)
addLink(3)

print(llist.tail.data) # 1
delLink()
print(llist.tail.data) # 2
addLink(4)

print(backup.dict)
print(llist.head.key) # 4

print(readCache(10)) # Cache miss
print(readCache(2).head.key) # 2

print(llist.head.data) # 2!