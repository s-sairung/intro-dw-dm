import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Imports data
df = pd.read_csv("03_clustering/Chapter06Exercise.csv")
print(df.head())

# Drops unused columns
df = df.drop(columns=["Student_ID", "First_Name", "Last_Name"])
print(df.head())

# Performs The Elbow Method, and choose k = 3
inertias = []
k_range = range(1, 10)
for k in k_range:
    model = KMeans(n_clusters=k)
    model.fit(df)
    inertias.append(model.inertia_)

f1 = plt.figure(1)
plt.plot(k_range, inertias, marker="o")
plt.xlabel("Number of Clusters k")
plt.ylabel("Total Within Sum of Square")
plt.title("The Elbow Method showing the optimal k")

# Run model and plot graph
model = KMeans(n_clusters=3)
model.fit(df)
df["cluster"] = model.predict(df)

f2 = plt.figure(2)
pd.plotting.parallel_coordinates(df, "cluster")
plt.title("k-Means result")
plt.show()