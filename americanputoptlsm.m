%��С���˷�������ʽ������Ȩ
function price=americanputoptlsm(s0,k,r,t,sigma,n,m)
%s0Ϊ��Ʊ�۸�kΪִ�мۣ�r�޷������ʣ�t��Ȩ�����ڣ�sigma��Ʊ�����ʱ�׼�nʱ�䲽����mģ��·������
dt=t/n;
Rp=exp((r-sigma^2/2)*dt+sigma*sqrt(dt)*randn(n,m));  %���ɷ��������µļ۸�ֲ�
s=cumprod([s0*ones(1,m);Rp]);
extime=(m+1)*ones(n,1);
cf=zeros(size(s));    %�ֽ�������
cf(end,:)=max(k-s(end,:),0);   %ʵֵ��Ȩ��Ȩ����
for ii=size(s)-1:-1:2
    idx=find(s(ii,:)<k);        %����iiʱ�̴���ʵֵ״̬·��
    x=s(ii,idx)';
    x1=x/s0;    
    y=cf(ii+1,idx)'*exp(-r*dt);          %���ֽ�����������
    R=[ones(size(x1)) (1-x1)  1/2*(2-4*x1-x1.^2)];
    a=R\y;       %���Իع�
    c=R*a;          %���Իع�Ԥ����ֽ���
    jdx=max(k-x,0)>c;   %�ҳ�������Ȩ�����ŵļ۸�
    idxj = idx(jdx);
    nidx=setdiff((1:m),idx(jdx));
    cf(ii,idx(jdx))=max(k-x(jdx),0);
    extime(idx(jdx))=ii;
    cf(ii,nidx)=exp(-r*dt)*cf(ii+1,nidx);
   
end
price=mean(cf(2,:))*exp(-r*dt);



