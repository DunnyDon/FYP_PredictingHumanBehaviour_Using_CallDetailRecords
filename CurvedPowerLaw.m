filename ='countcredit.csv';
%filename = 'Weighted_Degree_Distribution_Data.csv';
M = csvread(filename);
count_1=1;
count_2=1;
for i = 1:length(M)
    x(count_1)=M(i,1)+1;
    y(count_1)=M(i,2)+1;
    count_1= count_1+1;
end
plot(log2(x),log2(y),'r.'),hold on
fo = fit(log2(x(:)),log2(y(:)),'power2');
plot(fo,'g'), hold on
%legend('Data',sprintf('y=%.3f{}x^{%.3f}',a,k));
ylim([-1 15])
xlim([0 13])
ylabel('Number of Credit Top Ups')
xlabel('Number of Users with that amount of Top Ups')
title('Credit Distribution, scaled to the log 2')
