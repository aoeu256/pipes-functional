""" Enables several functional tools for programming in an infix style.

TODO: Contact author (maybe)
pull the thing and edit it
push this to my own repository
PEP proposal for pipes?
Better examples for dup?
>>> 'mys' |dup(len)| (lambda x: x.id * x.len) |pipe| it[0:4]
'mysm'

"""

import operator
from collections import namedtuple
from functools import wraps

class ItError(Exception): pass

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
		if not hasattr(self, v):
			return lambda y: getattr(y, v if v != self else y)
		elif hasattr(operator, v):
			newop = getattr(operator, v)
			return Infix(lambda La, Lb, op=v: [newop(a, b) for a, b in zip(La, Lb)])
		else:
			raise ItError("Only support getitem, getattr, and operators.")
	def __getitem__(self, v):		
		return lambda y: y[v if v != self else y]
	def __abs__(self, x):
		if x is self:
			return lambda y: operator.abs(y, y)
		return lambda y: operator.abs(y, x)
	def __add__(self, x):
		if x is self:
			return lambda y: operator.add(y, y)
		return lambda y: operator.add(y, x)
	def __and__(self, x):
		if x is self:
			return lambda y: operator.and_(y, y)
		return lambda y: operator.and_(y, x)
	def __concat__(self, x):
		if x is self:
			return lambda y: operator.concat(y, y)
		return lambda y: operator.concat(y, x)
	def __contains__(self, x):
		if x is self:
			return lambda y: operator.contains(y, y)
		return lambda y: operator.contains(y, x)
	def __delitem__(self, x):
		if x is self:
			return lambda y: operator.delitem(y, y)
		return lambda y: operator.delitem(y, x)
	def __delslice__(self, x):
		if x is self:
			return lambda y: operator.delslice(y, y)
		return lambda y: operator.delslice(y, x)
	def __div__(self, x):
		if x is self:
			return lambda y: operator.div(y, y)
		return lambda y: operator.div(y, x)
	def __doc__(self, x):
		if x is self:
			return lambda y: operator.doc(y, y)
		return lambda y: operator.doc(y, x)
	def __eq__(self, x):
		if x is self:
			return lambda y: operator.eq(y, y)
		return lambda y: operator.eq(y, x)
	def __floordiv__(self, x):
		if x is self:
			return lambda y: operator.floordiv(y, y)
		return lambda y: operator.floordiv(y, x)
	def __ge__(self, x):
		if x is self:
			return lambda y: operator.ge(y, y)
		return lambda y: operator.ge(y, x)
	def __getitem__(self, x):
		if x is self:
			return lambda y: operator.getitem(y, y)
		return lambda y: operator.getitem(y, x)
	def __getslice__(self, x, z):		
		if x is self:
			return lambda y: operator.getslice(y, y, z)		
		return lambda y: operator.getslice(y, x, z)
	def __gt__(self, x):
		if x is self:
			return lambda y: operator.gt(y, y)
		return lambda y: operator.gt(y, x)
	def __iadd__(self, x):
		if x is self:
			return lambda y: operator.iadd(y, y)
		return lambda y: operator.iadd(y, x)
	def __iand__(self, x):
		if x is self:
			return lambda y: operator.iand(y, y)
		return lambda y: operator.iand(y, x)
	def __iconcat__(self, x):
		if x is self:
			return lambda y: operator.iconcat(y, y)
		return lambda y: operator.iconcat(y, x)
	def __idiv__(self, x):
		if x is self:
			return lambda y: operator.idiv(y, y)
		return lambda y: operator.idiv(y, x)
	def __ifloordiv__(self, x):
		if x is self:
			return lambda y: operator.ifloordiv(y, y)
		return lambda y: operator.ifloordiv(y, x)
	def __ilshift__(self, x):
		if x is self:
			return lambda y: operator.ilshift(y, y)
		return lambda y: operator.ilshift(y, x)
	def __imod__(self, x):
		if x is self:
			return lambda y: operator.imod(y, y)
		return lambda y: operator.imod(y, x)
	def __imul__(self, x):
		if x is self:
			return lambda y: operator.imul(y, y)
		return lambda y: operator.imul(y, x)
	def __index__(self, x):
		if x is self:
			return lambda y: operator.index(y, y)
		return lambda y: operator.index(y, x)
	def __inv__(self, x):
		if x is self:
			return lambda y: operator.inv(y, y)
		return lambda y: operator.inv(y, x)
	def __invert__(self, x):
		if x is self:
			return lambda y: operator.invert(y, y)
		return lambda y: operator.invert(y, x)
	def __ior__(self, x):
		if x is self:
			return lambda y: operator.ior(y, y)
		return lambda y: operator.ior(y, x)
	def __ipow__(self, x):
		if x is self:
			return lambda y: operator.ipow(y, y)
		return lambda y: operator.ipow(y, x)
	def __irepeat__(self, x):
		if x is self:
			return lambda y: operator.irepeat(y, y)
		return lambda y: operator.irepeat(y, x)
	def __irshift__(self, x):
		if x is self:
			return lambda y: operator.irshift(y, y)
		return lambda y: operator.irshift(y, x)
	def __isub__(self, x):
		if x is self:
			return lambda y: operator.isub(y, y)
		return lambda y: operator.isub(y, x)
	def __itruediv__(self, x):
		if x is self:
			return lambda y: operator.itruediv(y, y)
		return lambda y: operator.itruediv(y, x)
	def __ixor__(self, x):
		if x is self:
			return lambda y: operator.ixor(y, y)
		return lambda y: operator.ixor(y, x)
	def __le__(self, x):
		if x is self:
			return lambda y: operator.le(y, y)
		return lambda y: operator.le(y, x)
	def __lshift__(self, x):
		if x is self:
			return lambda y: operator.lshift(y, y)
		return lambda y: operator.lshift(y, x)
	def __lt__(self, x):
		if x is self:
			return lambda y: operator.lt(y, y)
		return lambda y: operator.lt(y, x)
	def __mod__(self, x):
		if x is self:
			return lambda y: operator.mod(y, y)
		return lambda y: operator.mod(y, x)
	def __mul__(self, x):
		if x is self:
			return lambda y: operator.mul(y, y)
		return lambda y: operator.mul(y, x)
	def __ne__(self, x):
		if x is self:
			return lambda y: operator.ne(y, y)
		return lambda y: operator.ne(y, x)
	def __neg__(self, x):
		if x is self:
			return lambda y: operator.neg(y, y)
		return lambda y: operator.neg(y, x)
	def __not__(self):
		return lambda y: operator.not_(y)
	def __or__(self, x):
		if x is self:
			return lambda y: operator.or_(y, y)
		return lambda y: operator.or_(y, x)
	def __package__(self, x):
		if x is self:
			return lambda y: operator.package(y, y)
		return lambda y: operator.package(y, x)
	def __pos__(self, x):
		if x is self:
			return lambda y: operator.pos(y, y)
		return lambda y: operator.pos(y, x)
	def __pow__(self, x):
		if x is self:
			return lambda y: operator.pow(y, y)
		return lambda y: operator.pow(y, x)
	def __repeat__(self, x):
		if x is self:
			return lambda y: operator.repeat(y, y)
		return lambda y: operator.repeat(y, x)
	def __rshift__(self, x):
		if x is self:
			return lambda y: operator.rshift(y, y)
		return lambda y: operator.rshift(y, x)
	def __sub__(self, x):
		if x is self:
			return lambda y: operator.sub(y, y)
		return lambda y: operator.sub(y, x)
	def __truediv__(self, x):
		if x is self:
			return lambda y: operator.truediv(y, y)
		return lambda y: operator.truediv(y, x)
	def __xor__(self, x):
		if x is self:
			return lambda y: operator.xor(y, y)
		return lambda y: operator.xor(y, x)

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

class Zipw(object):
	""" zipWith/Matrix style operations
>>> zipw = Zipw()
>>> [1, 2, 3] |zipw.add| [1,1,1]
[2, 3, 4]
	"""	
	def __init__(self):
		for op in dir(operator):
			if '__' in op:
				continue
			newop = getattr(operator, op)
			setattr(self, op, Infix(lambda La, Lb, op=newop: [op(a, b) for a, b in zip(La, Lb)]))
zipw = Zipw()
		
# (_1, _2, _3, _4, _5) = tuple(('partial', i) for i in range(5))

# Used for partial application when using |pipe|
class PartialArg(object):
	'Holds data'
	def __getindex__(self, v):
		return {'__gn__': v}
	def __getitem__(self, k):
		return {'__gn__': k}
	def __getattr__(self, k):
		return {'__gn__': k}
__ = PartialArg()

class PipeError(Exception): pass

from StringIO import StringIO
class Log:
	log = StringIO()
	enableLogging = True
	previous = None

def PipeLogger(f):
	if Log.enableLogging:
		def func(x, arg):		
			res = f(x, arg)
			nl = '\n' if Log.previous is not x else ''
			Log.log.write(nl+str(x)+'|'+str(res))

			Log.previous = res
			return res
		return func
	else:
		return f

@Infix 
@PipeLogger
def pipe(x, arg):
	""" 
Allows you to write f(g(x) as x |pipe| f |pipe| g.
For multi-argument functions, use "S-Expression" form, and mark where 
each variable gets  __ i.e: ('map', it+1, __)

>>> 'lol' |pipe| len |pipe| range
[0, 1, 2]

>>> 'lol' |pipe| enumerate |pipe| (map, lambda a: (a[1], a[0])) |pipe| list
[('l', 0)]

>>> 5 |pipe| (list, __, 2))
(5, 2)
	"""
	global __	
	try:
		return arg(x)
	except TypeError:
		f, args = arg[0], arg[1:]
		xtup = x if '__len__' in x else tuple(x)
		args = [xtup[i['__gn__']] if '__gn__' in i else i for i in args]

		return f(*args)
	
def id(x): return x

# TODO: maybe flattening
def dup(*funcs, **kwargs):
	""" Allows you to split the pipe, use it[n] or it.len to get a certain value from the pipe.
>>> 'what a world'.split() |dup(len)| list
[['what', 'a', 'world'], 3]

>>> 'what a world'.split() |dup(len)| it[1]
3

>>> 'what a world'.split() |dup(lol=len)| it.lol
3

>>> 'war love war'.split() |dup(id, len, set)| (lambda x: [x.len, x.id, x.set])
[3, ['war', 'love', 'war'], set(['love', 'war'])]
	"""	
	if len(funcs) + len(kwargs) < 2:
		funcs = (id,) + funcs
	
	allfuncs = funcs + tuple(kwargs.values())
	toident = lambda x: x.__name__.strip().strip('<>')
	idents   = tuple(toident(i) for i in funcs) + tuple(kwargs.keys())
	tup = namedtuple('dup', idents)
	
	def pipe(x, f):		
		return f(tup(*(g(x) for g in allfuncs)))
	return Infix(PipeLogger(pipe))

if __name__ == '__main__':
	import doctest
	doctest.testmod()
	print Log.log.getvalue()