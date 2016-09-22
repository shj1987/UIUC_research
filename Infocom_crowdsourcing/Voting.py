'''
Huajie Shao@09/20/2016
Fun: voting for MURI project about influence
graph of social sensing
'''

import numpy as np
# from math import factorial
from copy import deepcopy
import sys


w1 = 0.3
w2 = 0.8
nk = 2
w = 0.8
cost = 60
M= 15	# Ma Carlo


#----define the huristic alg based on the reliability
# to choose the sources
def Hfun_reb(cost, new_price, k, n):
	st_num = []
	if np.sum(new_price[0:k+1]) <= cost:  # e.g k=3 there are 4 numbers
		st_num = list(range(0,k+1))
	elif np.sum(new_price[0:k]) <= cost:
		for j in range(k+1, n):
			Sum_cost = np.sum(new_price[0:k]) + new_price[j]
			if Sum_cost <= cost:
				st_num = list(range(0,k))
				st_num.append(j)
			else:
				if j < n-1:
					Sum_cost = np.sum(new_price[0:k-1]) + new_price[j] + new_price[j+1]
					if Sum_cost<cost:
						st_num = list(range(0,k-1))
						st_num.extend([j, j+1])
					else:
						st_num = list(range(0,k-1))
	return st_num


def Generate_SC(N,NumV,id_rank):   #sources'claims
	t = NumV*pr
	SC = np.zeros([NumV,N])	#assertion and number of variables
	C0 = np.random.randint(0, 1, t)
	C1 = np.random.randint(1, 2, NumV-t)
	C = np.hstack((C1,C0))
	random.shuffle(C)
	# generate the claims of each observation
	for j in range(NumV):
		if C[j] ==1:
			t = np.random.uniform(0.4,0.9)
			numt = int(N*t)   # number of SC = 1
			SC1 = np.random.randint(1, 2, numt)	    # sc = 1
			SC0 = np.random.randint(0, 1, N-numt)   # sc = 0 
			SC01 = np.concatenate((SC0,SC1))
			random.shuffle(SC01)
			SC[j,:] = SC01
		else:
			# generate the false assertion and let SC=1
			tn =  np.random.uniform(0.2,0.7)
			nt = int(N*tn)
			SC3 = np.random.randint(1, 2, nt)
			SC4 = np.random.randint(0, 1, N-nt)
			SC34 = np.concatenate((SC4,SC3))
			random.shuffle(SC34)
			SC[j,:] = SC34



def fun_reb(Ran,Rbn):
	


# define the random function
def rand_fun(N,SC,cost,prc):
	Psum = 0
	Num = []
	Rai = []
	Rbi = []
	while Psum<cost:
		ids = np.random.randint(0,N)
		if ids in Num:
			pass
		else:
			Psum += prc[ids]
			Num.append(ids)

	for ids in Num:



	return rand_err


# define function: cost-only

def cost_only(Ra,Rb,Fee,cost):
	Psum = 0
	N = len(Fee)
	nums = []
	for j in range(N):
		if Psum <= cost:
			Psum += Fee[j]
			nums.append(j)
		else:
			break

	cost_err = fun_voting

	return cost_err




def Sort_abi(ai,bi):
	dict_ai = dict()
	id_list = []
	# dict_bi = dict()
	rk_ai = sorted(ai,reverse=True)
	# print(rk_ai)
	rk_bi = np.sort(bi)
	new_bi = np.zeros(len(bi))
	for i in range(n):
		dict_ai[ai[i]] = i
	for k in range(n):
		key = rk_ai[k]   # get the key of ai
		ids = dict_ai[key]
		new_bi[ids] = rk_bi[k]
		id_list.append(ids)

	return new_bi,id_list

#-----below is the main function to compare with the baselines
rst_err1 = []
rst_err2 = []
rst_err3 = []
rst_err4 = []
for mt in range(0,M):
	print("running time is", mt)
	arr_err1 = []
	arr_err2 = []
	arr_err3 = []
	arr_err4 = []
	Assertion = np.random.uniform(0,2,)
	for n in range(50,110,10):
		ai = np.random.uniform(0.4,0.9,n)
		bi = np.random.uniform(0.1,0.3,n)
		ai = np.around(ai*1000)/1000
		bi = np.around(bi*1000)/1000
		pr = np.random.uniform(1, 5, n)  # the prices for each source
		pr = np.around(pr,decimals=3)
		bi,id_rank = Sort_abi(ai,bi)

		# ---below fun: store the [ai, id]
		dict_ai = dict()
		dict_bi = dict()
		dict_pr = dict()
		for i in range(n):
			# dict_ai[ai[i]] = i
			# dict_bi[i] = bi[i]  	# store [id: bi]
			dict_pr[pr[i]] = i
		S_ai = deepcopy(ai)  # save the original reliability
		S_bi = deepcopy(bi)
		s_prc = deepcopy(pr)
		# -----------------------------------------------------
		# --make the ai and bi similar values after sorting ai, sort first
		# -----------------------------------------------------
		for k in range(n):
			key = ai[k]   # get the key of ai
			ids = dict_ai[key]
			S_bi[k] = dict_bi[ids]

		# --- the following is to save the original ai and bi
		# it could be used for Link ** changes and W changes---
		ai = S_ai
		bi = S_bi
		pr = s_prc
		Pa = ai
		Pb = bi
		# --#function is to generate the Matrix graph ------
		SD_ancestor = Generate_graph(n,nk,id_rank)
		#---------------------
		for s in range(n):
			if s in SD_ancestor.keys():
				parent = SD_ancestor[s]
				sum_ai_anct = 0
				sum_bi_anct = 0
				for v in parent:
					sum_ai_anct += ai[v]
					sum_bi_anct += bi[v]

				length = len(parent)
				Pa[s] = (1-w)*sum_ai_anct/length + w*ai[s]
				Pb[s] = (1-w)*sum_bi_anct/length + w*bi[s]

		#----below fun: sort the reliability of sources
		Hurist_rab = 1 + ai - bi
		rab_dict = dict()
		for i in range(n):
			h_rab = Hurist_rab[i]
			rab_dict[h_rab] = i

		Rab = np.sort(Hurist_rab)  # get the most reliable sources
		Rab = sorted(Rab, reverse=True)   #get the descending order

		# -------sort the reliability based on the hurisctic rab-----
		# then we get the highest reb to lowest in order
		# as input for the Hfun_reb
		new_Ra = np.zeros(n)
		new_Rb = np.zeros(n)
		new_price = np.zeros(n)
		for j in range(n):
			abi = Rab[j]
			ids = rab_dict[abi]
			new_price[j] = pr[ids]
			new_Ra[j] = ai[ids]
			new_Rb[j] = bi[ids]

		# --based on the prices, get the maxi number of sources chosen
		ct = np.sort(pr)  # sort prices for smallest to highest
		Ra_prc = np.zeros(n)
		Rb_prc = np.zeros(n)
		# this fun: sort the prices and its corrsponding reliability
		for i in range(n):
			srt_prc = ct[i]
			ids = dict_pr[srt_prc]  # find it in dict.
			Ra_prc[i] = ai[ids]
			Rb_prc[i] = bi[ids]

		psum = 0
		nm = 0
		while psum <= cost:
			nm += 1
			psum += ct[nm]
		nm = nm-1   # get the max numbers of sources to report
		min_err1 = 1


		#------------------------------------------------
		#  Here begin to calculate the error of our method
		#  -----------------------------------------------
		for k in range(2, nm):
			st_num = Hfun_reb(cost, new_price, k, n)
			Ran = []
			Rbn = []
			ppr = []
			if len(st_num) > 0:
				for j in range(len(st_num)):
					ids = st_num[j]
					Ran.append(new_Ra[ids])
					Rbn.append(new_Rb[ids])
					ppr.append(new_price[ids])

				err1 = voting_reb(Ran,Rbn)
				if err1 < min_err1:
					min_err1 = err1
					crowd_price = ppr
					crowd_ai = Ran
					crowd_bi = Rbn

		# errors for the baselines
		err2 = rand_fun(n,SC,cost,new_price)   #same as the RA,RB in the Matlab codes
		err3 = cost_only(Ra_prc,Rb_prc,ct,cost)
		# err4 = crowdbudget(crowd_price,cost,crowd_ai, crowd_bi)

		arr_err1.append(min_err1)
		arr_err2.append(err2)
		arr_err3.append(err3)
		# arr_err4.append(err4)

	rst_err1.append(arr_err1)
	rst_err2.append(arr_err2)
	rst_err3.append(arr_err3)
	# rst_err4.append(arr_err4)

#-------------------------------------
# ----calculat the mean values---
# ------------------------------------

Err1 = np.mean(rst_err1,axis=0)
Err2 = np.mean(rst_err2,axis=0)
Err3 = np.mean(rst_err3,axis=0)
# Err4 = np.mean(rst_err4,axis=0)
print(Err1)
print(Err2)
print(Err3)
# print(Err4)
