""" Enables several functional tools for programming in an infix style.

TODO: Contact author (maybe)
pull the thing and edit it
push this to my own repository
PEP proposal for pipes?
Better examples for dup?
>>> 'mys' |dup(len)| (lambda x: x.idy * x.len) |pipe| it[0:4]
'mysm'

"""

import operator
from collections import namedtuple
from functools import wraps
import types
# from macropy.core.macros import *
# from macropy.tracing import macros, log, trace
#
# macros = Macros()
#
# @macros.expr
# def my_macro():
# 	pass

def getoperators(underscore=True):
	return ((name, '__'+name+'__', op) for name, op in operator.__dict__.iteritems()\
		if name[0]!='_')

class ItError(Exception): pass

class It(object):
	""" Shortcut for writing lambdas.
>>> it = It()
>>> (lambda x: x[0])('lol') == it[0]('lol')
True
>>> (lambda s: s.upper())('lol') == it.upper('lol')()
True
>>> (it*it)(5) == 25
True
	"""
	def __getattr__(self, v):
		return lambda y: getattr(y, v)
	# def __getitem__(self, v):		
	# 	return lambda y: y[v]
for opname, opattr, op in getoperators():
	def opfact(op):		
		return lambda self, *args: \
			lambda y: op(y, *(i if i is not self else y for i in args))
	setattr(It, opattr, opfact(op))

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
		for opname, opattr, op in getoperators(underscore=False):
			setattr(Zipw, opname, Infix(lambda La, Lb, op=op: \
								 [op(a, b) for a, b in zip(La, Lb)]))

zipw = Zipw()

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
		@wraps(f)
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
	""" f(g(x)) <=> x |pipe| f |pipe| g α
For multi-argument functions, use "S-Expression" form where each variable gets
__ i.e: ('map', it+1, __)

>>> 'lol' |pipe| len |pipe| range
[0, 1, 2]
>>> 'lol' |pipe| enumerate |pipe| (map, lambda a: (a[1], a[0])) |pipe| it[0]
('l', 0)
>>> 5 |pipe| (list, __, 2))
[5, 2]"""
	global __
	try:
		return arg(x)
	except TypeError:
		f, args = arg[0], arg[1:]
		xtup = x if '__len__' in x else tuple(x)
		args = [xtup[i['__gn__']] if '__gn__' in i else i for i in args]

		return f(*args)

def idy(x): return x

# TODO: maybe flattening
def dup(*funcs, **kwargs):
	"""
	Allows you to split a pipe, use it[n] or it.<funcname> to get a certain
	value from the pipe.
>>> 'what a world'.split() |dup(len)| list
[['what', 'a', 'world'], 3]
>>> ('what' |dup(len)| it.len) == ('what' |dup(lol=len)| it.lol)
True
>>> 'war love war'.split() |dup(idy, set)| (lambda x: [x.idy, x.set])
[['war', 'love', 'war'], set(['love', 'war'])]
	"""
	if len(funcs) + len(kwargs) < 2:
		funcs = (idy,) + funcs

	allfuncs = funcs + tuple(kwargs.values())
	toident = lambda x: x.__name__.strip().strip('<>')
	idents = tuple(toident(i) for i in funcs) + tuple(kwargs.keys())
	tup = namedtuple('dup', idents)

	def pipe(x, f):
		return f(tup(*(g(x) for g in allfuncs)))
	return Infix(PipeLogger(pipe))

if __name__ == '__main__':
	import doctest
	doctest.testmod()
	print Log.log.getvalue()