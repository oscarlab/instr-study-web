input = open('package_popularity')
output = open('package_popularity.csv', 'w+')
for line in input:
    package_name, rank, inst = line.strip().split('|')
    output.write(package_name.strip(" ") + ", " + rank.strip(" ") + "," + inst.strip(" ") + "\n")
