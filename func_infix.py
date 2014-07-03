""" Enables several functional tools for programming in an infix style.

TODO: Contact author (maybe)
pull the thing and edit it
push this to my own repository
tests

>>> 'mys' |dup(len)| (lambda x: x.id * x.len) |pipe| it[0:20]
'mysmysmysm'

"""

import operator
from collections import namedtuple

class It(object):
	""" Shortcut for writing lambdas.
>>> it = It()
>>> (lambda x: x[0])('lol') == it[0]('lol')
True
>>> (lambda s: s.upper())('lol') == it.upper('lol')
True
>>> it*it(5) == 25
True
	"""
	def __getattr__(self, v):
		return lambda y: getattr(y, v if v != self else y)
	def __getitem__(self, v):
		return lambda y: y[v if v != self else y]
		
it = It()

# Who ever came up with this is awesome
class Infix(object): 
	'Allows you to build custom infix functions'
	def __init__(self, function):
		self.function = function
	def __ror__(self, other):
		return Infix(lambda x: self.function(other, x))
	def __or__(self, other):
		return self.function(other)

def Zipw():
	""" zipWith/Matrix style operations
>>> zipw = Zipw()
>>> [1, 2, 3] |zipw.add| [1,1,1]
[2, 3, 4]
	"""	

	class _Zipw():
		pass
		for op in dir(operator):
			if '__' in op:
				continue
			newop = getattr(operator, op)
			zipw.__dict__[op] = Infix(lambda La, Lb, op=op: [newop(a, b) for a, b in zip(La, Lb)])

		# def __getattribute__(self, attr):
		# op = getattr(operator, attr)
		# self.__dict__[attr] = Infix(lambda La, Lb, op=op: \
			# [newop(a, b) for a, b in zip(La, Lb)])
		# return self.__dict__[attr]

zipw = Zipw()
		
# (_1, _2, _3, _4, _5) = tuple(('partial', i) for i in range(5))

# Used for partial application when using |pipe|
__ = object()
class PipeError(Exception): pass

@Infix
def pipe(x, arg):
	""" Allows you to pipe any arbitrary function; supports partial application when called with tuples.
>>> 'lol' |pipe| len |pipe| range
[0, 1, 2]
>>> 5 |pipe| (tuple, (__, 2))
(5, 2)
	"""
	global __
	if hasattr(arg, '__call__'):
		return arg(x)

	f, args = arg[0], arg[1:]
	
	#for nopx in [i for i in range(len(args)) if i[0] == 'partial']
	#	args.insert(nopx, xtup[nopx])
		
	#if len(nops) > 1:
	#	raise PipeError("Cannot have more than one __")
	#elif len(nops) == 0:
	#	return f(*(args)+(x,))
	#else:
	#args.insert(nops[0], x)
	__ = x
	f(*args)

	return __
	
id = lambda x: x

# TODO: maybe flattening
def dup(*sp):
	""" Allows you to split the pipe, use it[n] or it.len to get a certain value from the pipe.
>>> 'what a world'.split() |dup(len)| list
(['what', 'a', 'world'], 3)

>>> 'what a world'.split() |dup(len)| it[1]
3

>>> 'war love war'.split() |dup(id, len, set)| lambda x: [x.len, x.id, x.set]
(3, ['war', 'love', 'war'], set(['love', 'war']))
	"""
	if len(sp) == 1:
		tup = namedtuple('dup', ['id', sp.__name__])
		return Infix(lambda x, f: tup(f(x), sp(f(x))))
	else:
		tup = namedtuple('dup', (g.__name__ for g in sp))
		return Infix(lambda x, f: tup(g(f(x)) for g in sp))
		
if __name__ == '__main__':
    import doctest
    doctest.testmod()