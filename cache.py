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


# build a cache memory with a doubly-linked list

# Linked-list node constructor 
class Node:
	def __init__(self, key):
		self.key = key
		self.data = fib(key)
		self.next = None
		self.prev = None

class LinkedList:
	def __init__(self):
		self.head = None
		self.tail = None


# print(llist.head) # memory space of Node(4)
# print(llist.head.data) # fibonacci value of 5
llist = LinkedList()

llist.head = Node(1) # {'key': 1, 'data': 1, 'next': None, 'prev': None}
current = llist.head
last = llist.tail

# llist.head.next = Node(2)


current.next = Node(2) #(llist.head.next = Node(2))

print(current.next) # <__main__.Node object at 0x1093f23c8>

previous = current
current = current.next #(current is Node 2)

# llist.head is now {'key': 1, 'data': 1, 'next': Node object at 0x1093f23c8, 'prev': None }
# llist.head.next is {'key': 2, 'data': 2, 'next': none, 'prev': None }
print(current.data) # 2 print(llist.head.next.data)

current.prev = previous # (1) llist.head.next.prev = llist.head
# list.head.next is now {'key': 2, 'data': 2, 'next': None, 'prev': Node object at 0x10932dbe0 }

print(llist.head.next.prev ) # Node(1) <__main__.Node object at 0x10932dbe0>


current.next = Node(3) #  llist.head.next.next = Node(3) which is {'key': 3, 'data': 3, 'next': None, 'prev': None}

print(llist.head.next.next.key, llist.head.next.next.data, llist.head.next.next.next, llist.head.next.next.prev, ) # 3 3 None None

previous = current
current = current.next #(current is Node 3)
current.prev = previous # llist.head.next.next.prev = llist.head.next {'key': 3, 'data': 3, 'next': None, 'prev': Node object at 0x1093f23c8}


print(current.prev ) #  Node(2) <__main__.Node object at 0x10932dbe0>

node = llist.head

while node.next:
	print(node.data)
	node = node.next
else:
	print(node.data)








# def chain(input):
	
# 	# if  not first time through
# 	if llist.head:


# 	# First time through (empty list)
# 	else:
# 		llist.head = Node(input)
# 		print('first time through')
# 		llist.tail = llist.head 


