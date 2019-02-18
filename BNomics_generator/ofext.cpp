//=============================================================
//(c) 2011 Distributed under MIT-style license. 
//(see LICENSE.txt or visit http://opensource.org/licenses/MIT)
//=============================================================

#include <math.h>
#include <numeric>
#include <stdio.h>
#include <iostream>
#include <algorithm>
#include <vector>
#include <iterator>

extern "C"{
double cmdl(int* in, int dsize, int* arity, int asize, int complexity)
{
	int ri=arity[0];
	int drepr[dsize]; 
	int abasis[asize]; abasis[0]=0;
	int qi=1;
	double H=0.0;
	
	if (asize>1){
		abasis[1]=1;
		std::partial_sum(arity+1,arity+asize-1, abasis+2, std::multiplies<int>());
		qi = std::accumulate(arity+1, arity+asize, 1, std::multiplies<int>());
	}
	//std::cout<<"basis"<<std::endl;
	//std::copy(abasis, abasis+asize, std::ostream_iterator<int>(std::cout," "));
	//std::cout<<std::endl;

	for(int i=0; i<dsize; i++){
		drepr[i]=std::inner_product(in+asize*i, in+asize*(i+1), abasis, 0);
	}
	//std::cout<<"inner product"<<std::endl;
	//std::copy(drepr, drepr+dsize, std::ostream_iterator<int>(std::cout," "));
	//std::copy(drepr, drepr+dsize, drepr_tmp);
	//std::cout<<std::endl;

	//std::sort(drepr_tmp, drepr_tmp+dsize);
	//int* new_end=std::unique(drepr_tmp, drepr_tmp+dsize, std::equal_to<int>());
	int unsize = *std::max_element(drepr,drepr+dsize)+1;
	

	std::vector<double> Nijk (unsize*ri,0.0);
	for (int i=0; i<dsize; i++){
		Nijk[drepr[i]*ri+in[asize*i]]+=1.0;
	}
	std::vector<double> Nij (unsize,0.0);
	for(int i=0; i<unsize; i++){
		Nij[i]=std::accumulate(Nijk.begin()+ri*i, Nijk.begin()+ri*(i+1), 0);
	}

	//std::copy(Nijk.begin(), Nijk.end(), std::ostream_iterator<double>(std::cout, " "));
	//std::cout<<std::endl;

	for(double n : Nijk){ if ( n>0 ){ H+=n*log(n);} };
	for(double n : Nij){ if ( n>0 ){ H-=n*log(n);} };

	H-=(ri-1)*qi*(log(dsize)*0.5*complexity+1-complexity);
	return H;

}

void p_score_c(int* data, int dsize, int* arity, int* p_candidates, int psize, int* group_ind, int group_size, double* tmp)
{
	int group[dsize*group_size+dsize];
	int group_arity[group_size+1];
	for(int i=0; i<group_size; i++){
		for(int j=0; j<dsize; j++){
			group[dsize*i+j] = data[dsize*group_ind[i]+j];
			group_arity[i] = arity[group_ind[i]];
		}
	}
	for(int i=0; i<psize; i++){
		for(int j=0; j<dsize; j++){
			group[group_size*dsize+j]=data[p_candidates[i]*dsize+j];
		

		group_arity[group_size]=arity[p_candidates[i]];
		tmp[p_candidates[i]]+=cmdl(group,dsize,group_arity,group_size+1,0);
		}
	}
}


void disc(double* x, double* y, int vsize, int Ngrid, double* out)
{
	double xmax= *std::max_element(x,x+vsize);
	double xmin= *std::min_element(x,x+vsize);
	double ymax= *std::max_element(y,y+vsize);
	double ymin= *std::min_element(y,y+vsize);
	double hx=(xmax-xmin)/(Ngrid-1);
	double hy=(ymax-ymin)/(Ngrid-1);
	int tmp=0, ytmp;

	
	for(int p=0; p<Ngrid; p++){
		for(int q=0; q<Ngrid; q++){
			int xcount=0, ycount=0, joint=0;
			for(int i=0; i<vsize; i++){
				if(x[i]<=xmin+p*hx){
					xcount+=1;
					ytmp=(y[i]<=ymin+q*hy);
					ycount+=ytmp;
					joint+=ytmp;
					//if(y[i]<=ymin+q*hy){
					//	joint+=1;
					//	ycount+=1;
					//}
				}
				else ycount+=(y[i]<=ymin+q*hy);

			}
			//out[p+Ngrid*q]=std::abs(vsize*joint-xcount*ycount);
			tmp=std::abs(vsize*joint-xcount*ycount);
			if(tmp>out[2]){
				out[0]=xmin+p*hx;
				out[1]=ymin+q*hx;
				out[2]=tmp;
			}

		}
	}
}
	
			
}
