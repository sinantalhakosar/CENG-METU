import random
import matplotlib.pyplot as plt
random.seed(1234)  # fix randomness

def normalize_data(somedataset):
    returnlist = list()
    for line in somedataset:
        feature_list = [float(x) for x in line[0].split(" ")]
        returnlist.append([tuple(feature_list)])
    return returnlist

def load_dataset(somefilename):
	dataset = list()
	with open(somefilename, 'r') as file:
		dataset = [[line.strip()] for line in file]
	return normalize_data(dataset)

def single(list1, list2):
    min_dist = 99999.
    for i in range(len(list1)):
        for j in range(len(list2)):
            distance = .0
            for x in range(len(list1[i])):
                distance += (list1[i][x] - list2[j][x])**2
            sqrt_dist = distance**(1/2)
            if sqrt_dist < min_dist:
                min_dist = sqrt_dist        
    return min_dist

def complete(list1, list2):
    max_dist = .0
    for i in range(len(list1)):
        for j in range(len(list2)):
            distance = .0
            for x in range(len(list1[i])):
                distance += (list1[i][x] - list2[j][x])**2
            sqrt_dist = distance**(1/2)
            if sqrt_dist > max_dist:
                max_dist = sqrt_dist        
    return max_dist

def average(list1, list2):
    total = .0
    for i in range(len(list1)):
        for j in range(len(list2)):
            distance = .0
            for x in range(len(list1[i])):
                distance += (list1[i][x] - list2[j][x])**2
            sqrt_dist = distance**(1/2)
            total += sqrt_dist     
    return total/(len(list1)*len(list2))

def centroid(list1, list2):
    list1_avg = tuple(map(lambda y: sum(y) / float(len(y)), zip(*list1)))
    list2_avg = tuple(map(lambda y: sum(y) / float(len(y)), zip(*list2)))
    distance = .0
    for x in range(len(list1_avg)):
        distance += (list1_avg[x] - list2_avg[x])**2
    sqrt_dist = distance**(1/2)
    return sqrt_dist

def algorithm(dataset,method,limit):
    while len(dataset) > limit:
        print(len(dataset))       
        min_dist = 99999
        my_list = list()
        for i in range(len(dataset)):
            for j in range(len(dataset)):
                if i==j:
                    continue
                dist = method(dataset[i],dataset[j])
                if dist < min_dist:
                    min_dist = dist
                    data1 = dataset[i]
                    data2 = dataset[j]
        my_list += data1 + data2
        dataset.remove(data1)
        dataset.remove(data2)
        dataset.append(my_list)
    return dataset

def generate_random_color(i):
    if i == 0:
        return '#FF0000'
    if i == 1:
        return '#00FF00'
    if i == 2:
        return '#0000FF'
    if i == 3:
        return '#000000'
def plot_graph(dataset,title):
    for i in range(0, len(dataset)):
        colx = tuple(x[0] for x in dataset[i])
        coly = tuple(x[1] for x in dataset[i])
        cluster_color = generate_random_color(i)
        plt.scatter(colx,coly, color=cluster_color)
        plt.title(title)
    plt.show()

dataset1 = load_dataset('dataset1.txt')
dataset2 = load_dataset('dataset2.txt')
dataset3 = load_dataset('dataset3.txt')
dataset4 = load_dataset('dataset4.txt')


single_dataset1 = algorithm(dataset1,single,2)
plot_graph(single_dataset1,"Dataset1 Single Linkage")
# complete_dataset1 = algorithm(dataset1,complete,2)
# plot_graph(complete_dataset1,"Dataset1 Complete Linkage")
# average_dataset1 = algorithm(dataset1,average,2)
# plot_graph(average_dataset1,"Dataset1 Average Linkage")
# centroid_dataset1 = algorithm(dataset1,centroid,2)
# plot_graph(centroid_dataset1,"Dataset1 Centroid Linkage")

# single_dataset2 = algorithm(dataset2,single,2)
# plot_graph(single_dataset2,"Dataset2 Single Linkage")
# complete_dataset2 = algorithm(dataset2,complete,2)
# plot_graph(complete_dataset2,"Dataset2 Complete Linkage")
# average_dataset2 = algorithm(dataset2,average,2)
# plot_graph(average_dataset2,"Dataset2 Average Linkage")
# centroid_dataset2 = algorithm(dataset2,centroid,2)
# plot_graph(centroid_dataset2,"Dataset2 Centroid Linkage")

# single_dataset3 = algorithm(dataset3,single,2)
# plot_graph(single_dataset3,"Dataset3 Single Linkage")
# complete_dataset3 = algorithm(dataset3,complete,2)
# plot_graph(complete_dataset3,"Dataset3 Complete Linkage")
# average_dataset3 = algorithm(dataset3,average,2)
# plot_graph(average_dataset3,"Dataset3 Average Linkage")
# centroid_dataset3 = algorithm(dataset3,centroid,2)
# plot_graph(centroid_dataset3,"Dataset3 Centroid Linkage")

# single_dataset4 = algorithm(dataset4,single,4)
# plot_graph(single_dataset4,"Dataset4 Single Linkage")
# complete_dataset4 = algorithm(dataset4,complete,4)
# plot_graph(complete_dataset4,"Dataset4 Complete Linkage")
# average_dataset4 = algorithm(dataset4,average,4)
# plot_graph(average_dataset4,"Dataset4 Average Linkage")
# centroid_dataset4 = algorithm(dataset4,centroid,4)
# plot_graph(centroid_dataset4,"Dataset4 Centroid Linkage")

