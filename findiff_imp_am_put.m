function P = findiff_imp_am_put(S,K,r,sigma,time,no_S_steps,no_t_steps)
sigma_sqr = sigma^2;
M=no_S_steps + rem(no_S_steps,2); %MΪS�䶯�Ĳ���
delta_S = 2.0*S/double(M); %��ΪSmax = 2* S
S_values = delta_S* (1:M+1)';%S���п��ܵ�ȡֵ
N=no_t_steps;%NΪt�䶯�Ĳ���
delta_t = time/N;%��Сʱ��䶯��λ
A = zeros(M+1,M+1);%���巽��ϵ������
A(1,1)=1.0;
for j=2:M
A(j,j-1) = 0.5*j*delta_t*(r-sigma_sqr*j);
A(j,j) = 1.0 + delta_t*(r+sigma_sqr*j*j);
A(j,j+1) = 0.5*j*delta_t*(-r-sigma_sqr*j);
end %A ��ʾ��Ȩ��ֵ������ķ��̵�ϵ������
A(M+1,M+1)=1.0;
B = max(0,K-S_values);
F = inv(A)*B;%�������Ȩ���ڵ�tʱ��ÿ��S����µĵ���Ȩ��ֵ
for t=N-1:-1:1
B = F;
F = inv(A)*B;%ͨ������������м��ÿ��ʱ�̵�ÿ��S������µ���Ȩ��ֵ
F=max(F,K-S_values);%ÿ�ζ��Ƚ�����Ȩ���Ż��ǳ�������
end
P= F(M/2);%��ǰʱ�̣���ǰS�۸���������Ȩ�ļ�ֵ
end

