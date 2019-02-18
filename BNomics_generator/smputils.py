#//=============================================================
#//(c) 2011 Distributed under MIT-style license. 
#//(see LICENSE.txt or visit http://opensource.org/licenses/MIT)
#//=============================================================


import multiprocessing as mp
import numpy as np
from time import time

def wrapper(f,arg_q,sys_q,err_q,lock):
	n,t,fargs=arg_q.get()
	try:
		print('[ %.4f ] proc %d started' %(time()-t,n))
		result=f(*fargs)
	except Exception, err:
		err_q.put(err)
		return
	print('[ %.4f ] proc %d finished' %(time()-t,n))

	sys_q.put((n,result))


def submit(jobs,sys_q,err_q,ncores,t):
	
	kill=(lambda procs: \
		[proc.terminate() for proc in procs if proc.exitcode is None])
	
	try:
		for job in jobs:
			job.start()
		for job in jobs:
			job.join()

	except Exception, err:
		kill(jobs)
		raise err
	
	if not err_q.empty():
		kill(jobs)
		raise err_q.get()

	print('[ %.4f ] query sys_q' %(time()-t))
	results=[None]*ncores
	rindx=[None]*ncores
	while not sys_q.empty():
		indx,res=sys_q.get()
		results[indx]=res
		rindx[indx]=[indx]

	print('[ %.4f ] merging resuts' %(time()-t))	
	for i in range(ncores-1):
		results[0].extend(results.pop(1))

	return results[0]

def splitter(datacol,mparts=1,psize=1):
	"""	iterator that splits datasets into either m parts or 
		into a number of parts of size=psize.
		datacol=[dataset1,dataset2,...] is a list of datasets
		of equal length ( len(dataset1)=len(dataset2) ).
		
	"""
	offset=0

	if mparts>1:
		psize=int(np.ceil(len(datacol[0])/float(mparts)))

	for i in xrange(psize,len(datacol[0]),psize):
		yield [data[offset:i] for data in datacol]
		offset=i
	yield [data[offset:] for data in datacol]


def process(f,d_args,params=[],nproc=2):
	""" d_args=[dataset1,dataset2,...] a list or a tuple of datasets 
		to be passed to the function f.
		params=[x1,x2,...] a list of parameters to be passed to f.
		nproc - a number of process/parts to break the task into.
	"""
	
	t=time()
	mn=mp.Manager()
	sys_q=mn.Queue()
	err_q=mn.Queue()
	arg_q=mn.Queue()
	lock=mn.Lock()
	print('[ %.4f ] init' %(time()-t))

	for i,part in enumerate(splitter(d_args,mparts=nproc)):
		arg_q.put(tuple([i,t,part+params]))
	print('[ %.4f ] arg_q formed' %(time()-t))

	jobs=[mp.Process( target=wrapper, args=(f,arg_q,sys_q,err_q,lock))\
		for i in range(nproc)]

	print('[ %.4f ] submiting jobs' %(time()-t))
	r=submit(jobs,sys_q,err_q,nproc,t)

	print('[ %.4f ] completed' %(time()-t))
	return r





	
	
	
	
