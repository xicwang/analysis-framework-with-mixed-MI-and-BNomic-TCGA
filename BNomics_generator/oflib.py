#//=============================================================
#//(c) 2011 Distributed under MIT-style license. 
#//(see LICENSE.txt or visit http://opensource.org/licenses/MIT)
#//=============================================================


import os

import numpy as np

class cext:
	def __init__(self):
		_path=os.path.dirname(os.path.realpath(__file__))
		self.lib = np.ctypeslib.load_library('ofext',_path)

		self.lib.cmdl.restype=np.ctypeslib.ctypes.c_double
		type_in=np.ctypeslib.ndpointer(dtype=np.int32,ndim=2,flags='C_CONTIGUOUS')
		type_out=np.ctypeslib.ndpointer(dtype=np.int32,flags='C_CONTIGUOUS')
		self.lib.cmdl.argtypes=\
			[type_in,np.ctypeslib.ctypes.c_int,
			type_out, np.ctypeslib.ctypes.c_int]


		self.lib.p_score_c.restype=None
		a=np.ctypeslib.ndpointer(dtype=np.int32,ndim=2,flags='C_CONTIGUOUS')
		b=np.ctypeslib.ndpointer(dtype=np.int32,flags='C_CONTIGUOUS')

		c=np.ctypeslib.ndpointer(dtype=np.int32,flags='C_CONTIGUOUS')
		d=np.ctypeslib.ndpointer(dtype=np.float64,flags='C_CONTIGUOUS')
		e=np.ctypeslib.ndpointer(dtype=np.int32,flags='C_CONTIGUOUS')
		self.lib.p_score_c.argtypes=\
			[a, np.ctypeslib.ctypes.c_int,\
			 b,\
			 c, np.ctypeslib.ctypes.c_int,\
			 e, np.ctypeslib.ctypes.c_int,\
			 d]

		self.lib.disc.restype=None
		disc_x=np.ctypeslib.ndpointer(dtype=np.float64,flags='C_CONTIGUOUS')
		disc_y=np.ctypeslib.ndpointer(dtype=np.float64,flags='C_CONTIGUOUS')
		disc_out=np.ctypeslib.ndpointer(dtype=np.float64,flags='C_CONTIGUOUS')
		self.lib.disc.argtypes=\
			[disc_x, disc_y,\
			np.ctypeslib.ctypes.c_int,\
			np.ctypeslib.ctypes.c_int,\
			disc_out]


	def cdisc(self,x,y,Ngrid):
		vsize=len(x)
		x=np.require(x,np.float64,'C')
		y=np.require(y,np.float64,'C')
		#out=np.zeros((Ngrid,Ngrid),dtype=np.float64)
		out=np.zeros(3,dtype=np.float64)
		self.lib.disc(x,y,vsize,Ngrid,out)
		return out

	def cmdl(self,a,b,c=0):
		""" cpp mdl objective function
			a - data
			b - arity
			c - complexity (0 for AIC or 1 for BIC)"""
		cc=c
		m,n=a.shape
		a=np.require(a,np.int32,'C')
		b=np.require(b,np.int32,'C')
		return self.lib.cmdl(a,m,b,n,cc)
		
	def cmdla(self,a,b):
		""" cpp mdl objective function
			a - data
			b - arity
			c - complexity (0 for AIC or 1 for BIC)"""
		cc=0
		m,n=a.shape
		a=np.require(a,np.int32,'C')
		b=np.require(b,np.int32,'C')
		return self.lib.cmdl(a,m,b,n,cc)

	def cmdlb(self,a,b):
		""" cpp mdl objective function
			a - data
			b - arity
			c - complexity (0 for AIC or 1 for BIC)"""
		cc=1
		m,n=a.shape
		a=np.require(a,np.int32,'C')
		b=np.require(b,np.int32,'C')
		return self.lib.cmdl(a,m,b,n,cc)

	def p_score_c(self,data,arity,p_candidates,family,tmp):
		dsize,n=data.shape
		psize=len(p_candidates)
		group_size=len(family)
		ar=np.require(arity,np.int32,'C')
		p_candidates=np.require(list(p_candidates),np.int32,'C')
		group_ind=np.require(family,np.int32,'C')
		dd=np.require(data,np.int32,'C')
		tmp=np.require(tmp,np.float64,'C')
		self.lib.p_score_c(dd,dsize,ar,p_candidates,psize,group_ind,group_size,tmp)


