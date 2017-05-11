function P = findiff_imp_am_put(S,K,r,sigma,time,no_S_steps,no_t_steps)
sigma_sqr = sigma^2;
M=no_S_steps + rem(no_S_steps,2); %M为S变动的步数
delta_S = 2.0*S/double(M); %认为Smax = 2* S
S_values = delta_S* (1:M+1)';%S所有可能的取值
N=no_t_steps;%N为t变动的步数
delta_t = time/N;%最小时间变动单位
A = zeros(M+1,M+1);%定义方程系数矩阵
A(1,1)=1.0;
for j=2:M
A(j,j-1) = 0.5*j*delta_t*(r-sigma_sqr*j);
A(j,j) = 1.0 + delta_t*(r+sigma_sqr*j*j);
A(j,j+1) = 0.5*j*delta_t*(-r-sigma_sqr*j);
end %A 表示期权价值算满足的方程的系数矩阵
A(M+1,M+1)=1.0;
B = max(0,K-S_values);
F = inv(A)*B;%求出在期权到期的t时刻每种S情况下的的期权价值
for t=N-1:-1:1
B = F;
F = inv(A)*B;%通过迭代，求出中间的每个时刻的每种S的情况下的期权价值
F=max(F,K-S_values);%每次都比较是行权最优还是持有最优
end
P= F(M/2);%当前时刻，当前S价格的情况下期权的价值
end

