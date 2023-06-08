import regex as re
filename="/home/devesh/projects/nlp/ass1/final/2020115005_train4_w_ulys_t.txt"
f=open(filename,"r")
data=f.read()
arr=re.findall("<EOS> (.*?)\n<SOS>",data)
print(arr)
sum=0
l=[]
for val in arr:
    sum+=float(val.strip())
print(sum/len(arr))
