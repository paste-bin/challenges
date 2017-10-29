So I've got ./exp.py which is my exploit wrapper around heapofun

I can get admin with a booking at seat ';4'

When I change a booking I can overflow the name and change the data structures in the heap

I've been able to make the pointer to the string point at other things in the heap and I can leak
the address of the heap and where things are stored.

I can make the next and prev pointers point to the .plt entry for puts and something else.
This means that when I refund the booking it will write the address of the something else 
to puts's plt entry but it also writes to this something else's spot in memory which is stoping
me from making puts do whatever I want.

I'm pretty stuck so any help is really appreciated!
Cheers
pasteBin - Jordan

