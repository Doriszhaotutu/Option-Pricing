function p=mcput(S,X,sigma,r,T,M)
p=0;
for i=1:M
ST=S*exp((r-0.5*sigma^2)*T+sqrt(T)*sigma*randn);
p=p+max(X-ST,0);
end
p=p/M;

