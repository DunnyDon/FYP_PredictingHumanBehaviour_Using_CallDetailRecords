import csv
from collections import defaultdict
with open('C:\Users\Conor\Desktop\Gephi_Graphs\FYP_Partiition [Nodes].csv', 'rb') as fin: data = list(csv.reader(fin))[1:]
degree_dict = defaultdict(set)
def get_uniques():
	for id,modularity_class,weighted_indegree,weighted_outdegree,weighted_degree in data:
		degree_dict[weighted_degree] = 0
		
def count_vals():
	for id,modularity_class,weighted_indegree,weighted_outdegree,weighted_degree in data:
		for i in degree_dict:
			if i == weighted_degree:
				count = degree_dict[weighted_degree]
				degree_dict[weighted_degree] = count+1
def write_to_file():
	with open('C:\Users\Conor\Desktop\Gephi_Graphs\Degree_Distribution_Data.txt', 'w+') as fl:
		for i in degree_dict:
			print i+","+str(degree_dict[i])
			fl.write(i+","+str(degree_dict[i])+"\n")
			fl.flush()
get_uniques()
print len(degree_dict)
count_vals()
write_to_file()