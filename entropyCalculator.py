from pandas import read_csv
import math

df = read_csv('data.csv')

def H_Y(data):
    n = data.shape[0]
    x = data.loc[data['Class'] == 1].shape[0]
    h = -((x / n) * math.log2(x / n) + ((n - x) / n) * math.log2((n - x) / n))
    return round(h, 3)

def H(data, X, x):
    rows = data.loc[data[X] == x]
    n = rows.shape[0]
    x = rows.loc[rows['Class'] == 1].shape[0]
    if(n == 0 or x == 0): return 0
    elif((n-x) == 0): return round((-((x/n)*math.log2(x/n))), 3)
    else:
        return round((-((x/n)*math.log2(x/n) + ((n-x)/n)*math.log2((n-x)/n))), 3)

def P(data, X, x):
    rows = data.loc[data[X] == x]
    n = rows.shape[0]
    if(data.shape[0] == 0):return 0
    p = n/data.shape[0]
    return round(p, 3)

def I(data, hy, X):
    vals = data[X].unique()
    sum = 0
    for val in vals:
        sum += P(data, X, val)*H(data, X, val)
    i = hy - sum
    return round(i, 3)

print("PART (A)")
hy = H_Y(df)
#iterate through all headers (except class) and hash respective gains
gains1 = {}
for header in list(df):
    if header == 'Class': continue
    for val in df[header].unique():
        h = H(df, header, val)
        p = P(df, header, val)
        print("{:25}".format(header + "," + val) + "H: {:.3f} P: {:.3f}".format(h, p))

    i = I(df, hy, header)
    print("{:25}".format("Gain:" + header) + "{}".format(i))
    gains1[header] = i

#select header with highest gain to become child node
key = max(gains1, key = lambda k: gains1[k])
#select the value of the header to be expanded (alphabetically)
value = min(df[key].unique())
hy = H(df, key, value)

print("\nPART (B)")
print("\nExpanding: " + key + " with value => " + value + "\n")

#create new dataframe using only rows where key has given value
df1 = df.loc[df[key] == value]

gains2 = {}
for header in list(df):
    if header == 'Class' or header == key: continue
    for val in df[header].unique():
        h = H(df1, header, val)
        p = P(df1, header, val)
        print("{:25}".format(header + "," + val) + "H: {:.3f} P: {:.3f}".format(h, p))

    i = I(df1, hy, header)
    print("{:25}".format("Gain:" + header) + "{}".format(i))
    gains2[header] = i

#select header with highest gain to become child node
key2 = max(gains2, key = lambda k: gains2[k])
#select the value of the header to be expanded (alphabetically)
value2 = min(df[key2].unique())
hy = H(df1, key2, value2)

print("\nPART (C)")
print("\nExpanding: " + key2 + " with value => " + value2 + "\n")
#create new dataframe using only rows where key has given value
df2 = df1.loc[df1[key2] == value2]

gains3 = {}
for header in list(df):
    if header == 'Class' or header == key or header == key2: continue
    for val in df[header].unique():
        h = H(df2, header, val)
        p = P(df2, header, val)
        print("{:25}".format(header + "," + val) + "H: {:.3f} P: {:.3f}".format(h, p))

    i = I(df2, hy, header)
    print("{:25}".format("Gain:" + header) + "{}".format(i))
    gains3[header] = i

print("\nPART (D)")
#same header as last node, 2nd value
ls = list(df[key2].unique())
ls.remove(min(ls))
value3 = min(ls)
hy = H(df1, key2, value3)
print("\nExpanding: " + key2 + " with value => " + value3 + "\n")

df3 = df1.loc[df1[key2] == value3]

gains4 = {}
for header in list(df):
    if header == 'Class' or header == key or header == key2: continue
    for val in df[header].unique():
        h = H(df3, header, val)
        p = P(df3, header, val)
        print("{:25}".format(header + "," + val) + "H: {:.3f} P: {:.3f}".format(h, p))

    i = I(df3, hy, header)
    print("{:25}".format("Gain:" + header) + "{}".format(i))
    gains4[header] = i

print("\nPART (E)")
#select header with highest gain to become child node
key3 = max(gains1, key = lambda k: gains1[k])
#select the value of the header to be expanded (alphabetically)
ls = list(df[key3].unique())
ls.remove(min(ls))
ls.remove(min(ls))
value4 = min(ls)
hy = H(df, key3, value4)

print("\nExpanding: " + key3 + " with value => " + value4 + "\n")

#create new dataframe using only rows where key has given value
df4 = df.loc[df[key3] == value4]

gains5 = {}
for header in list(df):
    if header == 'Class' or header == key3: continue
    for val in df[header].unique():
        h = H(df4, header, val)
        p = P(df4, header, val)
        print("{:25}".format(header + "," + val) + "H: {:.3f} P: {:.3f}".format(h, p))

    i = I(df4, hy, header)
    print("{:25}".format("Gain:" + header) + "{}".format(i))
    gains5[header] = i