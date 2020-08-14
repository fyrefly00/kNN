# k_means.py Author: Robert Walker
import random
import sys
import math
def main():
  k = sys.argv[2]
  filename = sys.argv[1]
  # Read the data points in and save them as a list of 14 points with an extra filler for the unofficial label
  file = open(filename)
  data_points = []
  for line in file:
    line = " ," + line
    data_points.append(line.strip().split(','))

  # Pick k random centroids and assign them alphabetized labels
  centroids = []
  for i in range(0,int(k)):
    centroids.append(data_points[random.randrange(0, len(open("wine.data.in").readlines()))])
    centroids[i] [0]= chr(65 + i)

  MAX_ITERATIONS = 15 
  for i in range(0,MAX_ITERATIONS):
    #Calculate the closest centroid for each individual point and label it accordingly
    for point in data_points:
      point[0] = find_nearest_centroid(point,centroids)[0]
    
    # Save a copy of the old centroids for delta comparision (needs to be deep copy)
    old_centroids = []
    for centroid in centroids:
      old_centroids.append(centroid)
    # Recalculate the position of each centroid  
    for  k in range(0, len(centroids)):
      centroids[k]= recalculate_centroid(data_points,centroids[k][0])

    # Check to see if anything has changed between the old and new centroids. If not, terminate
    match = 0
    for k in  range(len(centroids)):
      for j in range(2, len(centroid)):
        if centroids[k][j] == old_centroids[k][j]:
          match +=1
    calculate_sucess_rate(data_points, int(k))
    if match ==( (len(centroids[0]) -2) * (k + 1)) :
      print("Convergence point reached after " + str(i) + " iterations")
      sys.exit()
    input("Press Enter for next iteration")

def find_nearest_centroid(point, centroids):
  # Store the current min (start off with distance of infinity)
  min = [centroids[0],float("inf")]
  for centroid in centroids:
    distance = 0
    for i in range(2,len(point)):
      distance += math.pow(float(point[i]) - float(centroid[i]),2)
      distance = math.sqrt(distance)
    if distance < min[1]:
      min[0] = centroid
      min[1] = distance
  return(min[0])

def recalculate_centroid(points, type):
  num_points = 0
  centroid = [type,"",0,0,0,0,0,0,0,0,0,0,0,0,0] # Blank, holder centroid
  for point in points:
    if point[0] == type:
      for i in range(2, len(point)):
        centroid[i] = (str(float(centroid[i]) + float(point[i])))
      num_points +=1
  for i in range(2, len(centroid)):
    centroid[i] = str((1/num_points) * float(centroid[i]))
  return centroid

# Sort the points into groups based on their unofficial labels and calculate which percent of each group is which label
def calculate_sucess_rate(points, k):
  grouped_points= [[] for i in range(k + 1)]
  for point in points:
    grouped_points[ord(point[0]) - 65].append(point)

  for i in range(0, len(grouped_points)):
    percents = [0,0,0]
    for point in grouped_points[i]:
      percents[ord(point[1]) - 65] +=1
    print("Region " + str(i + 1))
    for j in range(0, len(percents)):
      print(chr(65 + j) + ":" + str(percents[j]) + " : " + str((percents[j] / len(grouped_points[i])) * 100) + " percent " + chr(65 + j)) 
    print()


if __name__ == '__main__':
  main()