function c=mccall(S,X,sigma,r,T,M)
c=0;
for i=1:M
ST=S*exp((r-0.5*sigma^2)*T+sqrt(T)*sigma*randn);
c=c+max(ST-X,0);
end
c=c/M;





