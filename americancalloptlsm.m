%最小二乘法计算美式看涨期权
function price=americancalloptlsm(s0,k,r,t,sigma,n,m)
%s0为股票价格，k为执行价，r无风险利率，t期权存续期，sigma股票收益率标准差，n时间步数，m模拟路径个数
dt=t/n;
Rp=exp((r-sigma^2/2)*dt+sigma*sqrt(dt)*randn(n,m));  %生成风险中性下的价格
s=cumprod([s0*ones(1,m);Rp]);%生成m条路径的S的价格
extime=(m+1)*ones(n,1);
cf=zeros(size(s));    %现金流矩阵
cf(end,:)=max(s(end,:)-k,0);   %最终时刻的回报的值（1时刻），cf里面存的是在ii时刻在的期权的价值数据
for ii=size(s)-1:-1:2 %ii表示的是时间刻度，从时间0.8到时间0.6 再到0.4。
    idx=find(s(ii,:)>k);        %发现ii时刻处于实值状态路径
    x=s(ii,idx)'; %时间刻度为ii的实值路径的股票的价格
    x1=x/s0;    
    y=cf(ii+1,idx)'*exp(-r*dt);          %上一时刻的回报现金流在ii时刻的贴现值（如ii是0.8时刻，则将1时刻的现金流贴现到0.8时刻）
    R=[ones(size(x1)) (1-x1)  1/2*(2-4*x1-x1.^2)];
    a=R\y;       %使用最小二乘计算出方程的系数（该方程的y是未来一期的回报的贴现值 x是当前时刻ii的股票价格）
    c=R*a;          %在ii时刻在当时的股票价格下，计算持有该期权所带来的现金流
    jdx=max(x-k,0)>c;   %对比立即行权的收益与继续持有期权带来的收益，找出应该行权的路径jdx
    nidx=setdiff((1:m),idx(jdx));%nidx为m条路径中，在ii时刻不选择行权的路径
    cf(ii,idx(jdx))=max(x(jdx)-k,0);%各个路径在ii时刻的收益，如果是正值表示该路径发生的行权，如果是0表示该路径不行权（如果ii -1及之前的时刻没有执行的话）
    extime(idx(jdx))=ii;%记录行权时间
    cf(ii,nidx)=exp(-r*dt)*cf(ii+1,nidx);%无论在ii时刻是否是实值，在ii时刻选择不行权的路径，现金流使用下一期的现金流的贴现值
end
price=mean(cf(2,:))*exp(-r*dt);%将最终得到的回报矩阵求平均并继续向前贴现一期

