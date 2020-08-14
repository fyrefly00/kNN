import matplotlib.pyplot as plt
import math
import operator
import sys
out = open("output.txt","w")

def main():
    data_points = read_data("iris.data.training")
    test_points = read_data("iris.data.testing")
    out.write("CLASSIFICATION OUTPUT: " + sys.argv[2] + " ATTRIBUTES\n")
    fig, ax = plt.subplots(nrows=2, ncols=2) 
    for row in ax:
        for col in row:
            #List comprehension!
            col.plot([element.petal_length for element in data_points if element.name == "Iris-setosa"], [element.petal_width for element in data_points if element.name == "Iris-setosa"], 'bo')
            col.plot([element.petal_length for element in data_points if element.name == "Iris-versicolor"], [element.petal_width for element in data_points if element.name == "Iris-versicolor"], 'ro')
            col.plot([element.petal_length for element in data_points if element.name == "Iris-virginica"], [element.petal_width for element in data_points if element.name == "Iris-virginica"], 'go')

    k_vals = [1,3,5,10]
    for k in k_vals:
        output = []
        out.write("VALUES FOUND WITH K OF " + str(k) + "\n")
        for flower in test_points:
            nearest_neighbors = []
            for known_flower in data_points:
                distance = 0
                if(sys.argv[2] == "4"):
                    distance = math.sqrt(  math.pow((flower.sepal_length - known_flower.sepal_length),2)  + math.pow((flower.sepal_width - known_flower.sepal_width),2) + math.pow((flower.petal_length - known_flower.petal_length),2)  + math.pow((flower.petal_width - known_flower.petal_width),2))
                elif(sys.argv[2] == "2"):
                    distance = math.sqrt(math.pow((flower.petal_length - known_flower.petal_length),2)  + math.pow((flower.petal_width - known_flower.petal_width),2))
                if distance > 0:
                    nearest_neighbors.append((known_flower,distance))
            
            #Sort the list from least to greatest distance and choose k of the closest values to calculate one resultant three dimensional vector that leans towards one category
            nearest_neighbors.sort(key = operator.itemgetter(1))
            vector = calculate_vector(nearest_neighbors,k)

            #This one section is kinda jank but I can't think of a cleaner way to relate a specific k value with a specific subplot
            if(k == 1):
                row = 0
                col = 0
            if(k == 3):
                row = 0
                col = 1
            if(k == 5):
                row = 1
                col = 0
            if(k == 10):
                row = 1
                col = 1

            ax[row][col].set_title("Classification with k value of " + str(k))
            #Kind of a messy solution but I couldn't find a simple way to associate the dimensions of the vector to the categories
            if(vector[0] > vector[1] and vector[0]> vector [2]):
                output.append("Iris-virginica")
                ax[row][col].plot(flower.petal_length, flower.petal_width, 'gv')
            elif(vector[1] > vector[0]  and vector[1] > vector[2]):
                output.append("Iris-versicolor")
                ax[row][col].plot(flower.petal_length, flower.petal_width, 'rv')
            elif(vector[2] > vector[0] and vector[2] > vector[1]):
                output.append("Iris-setosa")
                ax[row][col].plot(flower.petal_length, flower.petal_width, 'bv')
        write_results(output,test_points)
    if(sys.argv[2] == "2"):
        plt.show()

  
class  Flower:
    sepal_length = 0
    sepal_width = 0
    petal_length = 0
    petal_width = 0
    name = ""
    def __init__ (self, sepal_length, sepal_width, petal_length, petal_width, name):
        self.sepal_length = sepal_length
        self.sepal_width = sepal_width
        self.petal_length = petal_length
        self.petal_width = petal_width
        self.name = name

def read_data(filename):
    training = open(filename)
    data_points = []
    for line in training:
        if not line.strip() == "":
            data = line.strip().split(",")
            data_points.append(Flower(float(data[0]), float(data[1]), float(data[2]), float(data[3]), data[4]))
    return data_points

#Take the top k values and weight them using 1/d in the correct category
# def calculate_vector(nearest_neighbors, k):
#     composite = [("Iris-virginica",0),("Iris-versicolor",0),("Iris-setosa",0)]
#     i = 0
#     for key,val in nearest_neighbors:
#         for el in composite:
#             if key.name == el[0]:
#                 el[1]+=(1/val)


#     return composite
#         # if(key.name == "Iris-virginica"):
#         #     composite[0] +=(1/val)
#         # elif (key.name == "Iris-versicolor"):
#         #     composite[1] +=(1/val)
#         # elif (key.name == "Iris-setosa"):
#         #     composite[2] +=(1/val)
#         # i +=1
#         # if(i == k):
#         #     return composite

def write_results(output,test_points):
    score = len(output)
    for i in range( len(output)):
        out.write(output[i] + "\n")
        if not output[i] == test_points[i].name:
            score -=1
    out.write("Test Results: " + str(score/len(output) * 100) + " % Correct\n" )
    
if __name__ == '__main__':
  main()


  def calculate_vector(nearest_neighbors, k):
    composite = ["Iris-virginica"0,0,0]
    i = 0
    for key,val in nearest_neighbors:
        if(key.name == "Iris-virginica"):
            composite[0] +=(1/val)
        elif (key.name == "Iris-versicolor"):
            composite[1] +=(1/val)
        elif (key.name == "Iris-setosa"):
            composite[2] +=(1/val)
        i +=1
        if(i == k):
            return composite
