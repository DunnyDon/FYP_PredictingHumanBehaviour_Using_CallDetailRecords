filename ='Degree_Distribution_Data.csv';
M = csvread(filename);
for i = 1:length(M)
    x(i)=M(i,1);
    y(i)=M(i,2);
end
plot(log2(x),log2(y),'r.'),hold on
title('Degree Distribution, scaled to the log 2')
xlabel('Value')
ylabel('Count')
p = polyfit(log(x),log(y),1); 
k = p(1);
a = exp(p(2));
plot(log2(x),log2(a*x.^k),'g')
legend('Data',sprintf('y=%.3f{}x^{%.3f}',a,k));

%f = fit(x,y,'b*x^m'); plot(f,'k')