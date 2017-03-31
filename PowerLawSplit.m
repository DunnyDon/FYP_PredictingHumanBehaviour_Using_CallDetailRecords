%filename ='countcredit.csv';
filename = 'Weighted_Degree_Distribution_Data.csv';
M = csvread(filename);
count_1=1;
count_2=1;
for i = 1:length(M)
    if (M(i,2)> 2^5)
        x(count_1)=M(i,1);
        y(count_1)=M(i,2);
        count_1= count_1+1;
    else
        x_2(count_2)=M(i,1);
        y_2(count_2)=M(i,2);
        count_2 = count_2+1;
    end;
end
plot(log2(x),log2(y),'r.'),hold on

title('Degree Distribution, scaled to the log 2')
xlabel('Degree Value')
ylabel('Number of Users with that Degree')
p = polyfit(log(x),log(y),1); 
k = p(1);
a = exp(p(2));
plot(log2(x),log2(a*x.^k),'g'), hold on

p_2 = polyfit(log(x_2),log(y_2),1); 
k_2 = p_2(1);
a_2 = exp(p_2(2));
plot(log2(x_2),log2(a_2*x_2.^k_2),'b'),hold on
plot(log2(x_2),log2(y_2),'r.'),hold on
legend('Data',sprintf('y=%.3f{}x^{%.3f}',a,k),sprintf('y=%.3f{}x^{%.3f}',a_2,k_2));

%f = fit(x,y,'b*x^m'); plot(f,'k')