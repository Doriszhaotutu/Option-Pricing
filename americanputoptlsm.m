%最小二乘法计算美式看跌期权
function price=americanputoptlsm(s0,k,r,t,sigma,n,m)
%s0为股票价格，k为执行价，r无风险利率，t期权存续期，sigma股票收益率标准差，n时间步数，m模拟路径个数
dt=t/n;
Rp=exp((r-sigma^2/2)*dt+sigma*sqrt(dt)*randn(n,m));  %生成风险中性下的价格分布
s=cumprod([s0*ones(1,m);Rp]);
extime=(m+1)*ones(n,1);
cf=zeros(size(s));    %现金流矩阵
cf(end,:)=max(k-s(end,:),0);   %实值期权行权收益
for ii=size(s)-1:-1:2
    idx=find(s(ii,:)<k);        %发现ii时刻处于实值状态路径
    x=s(ii,idx)';
    x1=x/s0;    
    y=cf(ii+1,idx)'*exp(-r*dt);          %对现金流进行贴现
    R=[ones(size(x1)) (1-x1)  1/2*(2-4*x1-x1.^2)];
    a=R\y;       %线性回归
    c=R*a;          %线性回归预测的现金流
    jdx=max(k-x,0)>c;   %找出现在期权是最优的价格
    idxj = idx(jdx);
    nidx=setdiff((1:m),idx(jdx));
    cf(ii,idx(jdx))=max(k-x(jdx),0);
    extime(idx(jdx))=ii;
    cf(ii,nidx)=exp(-r*dt)*cf(ii+1,nidx);
   
end
price=mean(cf(2,:))*exp(-r*dt);



