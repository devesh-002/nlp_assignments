import argparse
import numpy as np
import regex as re
import collections
from collections import defaultdict, Counter
import math
import sys
# import tokenizer as tokenizer


def special_cases(wiki):
    wiki=re.sub("_"," ",wiki)
    wiki=re.sub(r'"',"",wiki)
    # wiki = re.sub(r'\s+\'bout', r' about', wiki)
    wiki = re.sub(r'([a-zA-Z]+)\'t', r'\1 not', wiki)
    wiki = re.sub(r'([a-zA-Z]+)\'s', r'\1 is', wiki)
    wiki = re.sub(r'([a-zA-Z]+)\'re', r'\1 are', wiki)
    wiki = re.sub(r'([a-zA-Z]+)\'ll', r'\1 will', wiki)
    wiki = re.sub(r'([a-zA-Z]+)\'d', r'\1 would', wiki)
    wiki = re.sub(r'([a-zA-Z]+)\'ve', r'\1 have', wiki)
    wiki = re.sub(r'([iI])\'m', r'\1 am', wiki)
    wiki=re.sub(r"won\'t","will not",wiki)
    wiki=re.sub(r"can\'t","cannot",wiki)

    return wiki

def tokenizer(wiki):

    wiki = re.sub(r'[^\x00-\x7F]+', ' ', wiki)
    prefix=['@','#']
    # for sep in string.
    wiki = re.sub(r"@[A-Za-z0-9_]+", "<MENTION>", wiki) # mention
    wiki = re.sub(r"#[A-Za-z0-9_]+", "<HASHTAG>", wiki) # hashtag
    wiki = re.sub(r'(https?:\/\/|www\.)?\S+[a-zA-Z0-9]{2,}\.[a-zA-Z0-9]{2,}\S+', ' <URL> ', wiki)  #url
    # wiki = re.sub(r'(?<=\s)[\:\.]?\d*[\:\.]?\d*[\:\.]?(?=\s)', ' <NUM> ', wiki) # Number
    # wiki=  re.sub(r'\w*(!|"|\$|%|&|\'|\(|\)|\*|\+|,|-|\.|\/|:|;|<|=|>|\?|\[|\\|\]|\^|\{|\||\}|~)\1{1,}', r' ', wiki)
    return wiki

def remove_stupid_fullstop(wiki):
    wiki=re.sub("Mr\s*.","Mr",wiki)
    wiki=re.sub("Ms\s*.","Ms",wiki)
    wiki=re.sub("Mrs\s*.","Mrs",wiki)
    wiki=re.sub("Miss\s*.","Miss",wiki)

    return wiki

def detect_full_stop(data):
    # data = re.sub(r'!+', "!", data)
    # data = re.sub(r'\?+', "?", data)
    data=data.lower()
    data = re.sub(r'[^\w+^\.^\?^\!\s]', r' ', data)
    data=re.sub(r'(\.+)'," <EOS> <SOS> ",data)
    return data

class N_Grams():
    def __init__(self, n, train, unk_val) -> None:
        self.n = n
        self.train = train
        self.unk_val = unk_val
        pass

    def n_gram_former(self, sentence, n_num):
        stri = ""
        for _ in range(n_num):
            stri += "<SOS> "
        sentence = stri+sentence + " <EOS>"
        sentence = re.sub('\s+', ' ', sentence)
        sentence.lstrip()
        sentence.rstrip()
        sentence = re.split(" ", sentence)
        initial_list = sentence[0:n_num]
        ans = list()
        x = initial_list.copy()
        ans.append(x)
        for i in range(1, len(sentence)-n_num+1):
            initial_list.pop(0)
            initial_list.append(sentence[i+n_num-1])
            x = initial_list.copy()
            ans.append(x)
        finalans = []
        # for val in 842280sentence:
        #     finalans.append(val)
        for x in ans:
            finalans.append(' '.join(x))

        return finalans

    def merge_two_dicts(self, x, y):
        for val in y:
            if val in x:
                x[val] += y[val]
            else:
                x[val] = y[val]
        return x

    def n_gram_recursor(self, sentence):
        ans = {}
        sentence = re.sub(' +', ' ', sentence)
        sentence.lstrip()
        sentence.rstrip()
        n_gram = {}
        for x in range(1, self.n+1):
            local_n_gram = self.n_gram_former(sentence, x)
            # print(local_n_gram)
            for y in local_n_gram:
                if(y not in ans):
                    ans[y] = 1
                else:
                    ans[y] += 1
            # for x in local_n_gram:
                # for
        return ans

    def n_gram_main(self):
        dict_main = {}
        arr = re.findall("<SOS>(.*?)<EOS>", self.train)
        
        for sentence in arr:
            if(sentence == ""):
                continue
            x = str(sentence)
            dict_util = self.n_gram_recursor(x)
            # print(dict_util)
            # for val in x:
            #     dict_util[val]=1
            dict_main = self.merge_two_dicts(dict_main, dict_util)
        dict_main['<UNK>'] = 0
        for word in list(dict_main):
            l = re.split(" ", word)
            if(len(l) == 1):
                if(dict_main[word] < self.unk_val):
                    dict_main['<UNK>'] += dict_main[word]
                    del dict_main[word]
        d = collections.defaultdict(dict)
        for key in dict_main.keys():
            y = re.split("\s+", key)
            yy = []
            for it in y:
                yy.append(it.strip())
            d[len(yy)][key] = dict_main[key]
        return d


class Language_Model():

    def __init__(self, dictionary_main, n_num) -> None:
        self.dictionary_main = dictionary_main
        self.n_gram = n_num
        self.constant = 0.75
        pass

    def Cnt(self, sentence):
        # returns count of string in corpus

        if(len(sentence) == 0):
            return 0
        y = re.split(" ", sentence)
        if sentence in self.dictionary_main[len(y)]:
            return self.dictionary_main[len(y)][sentence]
        else:
            return 0

    def sum_of_counts(self, history):
        # return sum of history of the probablity
        ans = 0
        n_gram_length = len(re.split(" ", history))+1

        for key in self.dictionary_main[n_gram_length].keys():
            string = key
            string = string.rsplit(' ', 1)[0].strip()
            # print(string)
            if(string == history):
                ans += self.dictionary_main[n_gram_length][key]
        return ans
    # def cnt_sum(self,sentence):

    def cont_count(self, n_gram, word):
        # return sum of last word occuring
        ans = 0
        for key in self.dictionary_main[n_gram]:
            string = re.split(" ", key)[-1]
            if(string == word):
                ans += 1
        return ans

    def count_of_positives(self, history):
        # sum of all words given history
        ans = 0
        n_gram_length = len(re.split(" ", history))+1

        for key in self.dictionary_main[n_gram_length].keys():
            if(self.dictionary_main[n_gram_length][key] > 0):
                string = key
                string = string.rsplit(' ', 1)[0].strip()
                if(string == history):
                    ans += 1

        return ans

    # Cnt: count_in_main_dict, sum_of_coutns: sum_history,cont_count:count_last_word,count_of_positives:varied_counts

#     def kneser_ney(self,sentence,word,step):
#         wot=list(filter(None, (re.split(" ", sentence)) ))
#         n_gram=len(wot)+1 # CHECK this
#         print(sentence+" ",n_gram)
#         if word not in self.dictionary_main[1]:
#             return self.constant/self.dictionary_main[1]['<UNK>']
#         if n_gram==1:
#             return (1-self.constant)/len(self.dictionary_main[1])+self.constant/self.dictionary_main[1]["<UNK>"]
#         first_term=0.0
#         complete_sentence=" ".join([sentence,word])
#         if(step==0):
#             try:
#                 # print(self.count(complete_sentence))
#                 first_term=max(self.Cnt(complete_sentence)-0.75,0)/self.sum_of_counts(sentence)
#             except:
#                 pass
#         else:
#             try:
#                 first_term=max(self.cont_count(n_gram,word)-self.constant,0)/len(self.dictionary_main[n_gram])
#             except:
#                 pass
#         lamb=0.0
#         print("first term ",end="")
#         print( first_term)
#         # if(self.n_gram!=n_gram):
#         try:
#             lamb=(self.constant/self.sum_of_counts(sentence))
#         # except:
#         #     pass
#         except:
#                 return self.constant/self.dictionary_main[1]['<UNK>']
# # ASK THIS
#         # if(step==0):
#         #     lamb=0

#         cont_term=self.count_of_positives(sentence)
#         lamb*=cont_term
#         # if(self.Cnt(complete_sentence)>0):
#         #     return final_kneser_val
#         pass_history=" ".join(sentence.split()[1:])
#         backoff=lamb* self.kneser_ney(pass_history,word,step+1)

#         return first_term+ backoff

    def precede_calculation(self,sentence):
        wot = list(filter(None, (re.split(" ", sentence))))
        n_gram = len(wot)+1
        l=len(dict(filter(lambda item: sentence == " ".join(item[0].split(' ')[1:]), self.dictionary_main[n_gram].items())))
        # for key in self.dictionary_main[n_gram].keys():
        #     x=re.split(" ",key)
        #     x=" ".join(x[1:])
        #     if(x==sentence):
        #         ans+=1
        # print(l,ans)
        return l
    
    def kneser_ney(self, sentence, word):

        wot = list(filter(None, (re.split(" ", sentence))))
        n_gram = len(wot)+1
        # print(sentence+" ", n_gram)
        if word not in self.dictionary_main[1]:
            return self.constant/self.dictionary_main[1]['<UNK>']

        if(n_gram == 1):
            denom=len(self.dictionary_main[1].keys())
            
            val=self.count_of_positives(word)
            if(val==0):
                val=self.dictionary_main[1]['<UNK>']
            return val/denom
            # return (1-self.constant)/len(self.dictionary_main[1])+self.constant/self.dictionary_main[1]["<UNK>"]
        first_term=0
        complete_sentence = " ".join([sentence, word])
        if n_gram==4:
            first_term = max(self.Cnt(complete_sentence)-0.75, 0)
            num = self.Cnt(sentence)
            if(num == 0):
                num = 1e-6
            first_term = first_term/num
        else:
            first_term=max(self.precede_calculation(complete_sentence)-self.constant,0)
            denom=self.precede_calculation(sentence)
            if(denom==0):
                denom=1e-6
            first_term=first_term/denom
        count_val=self.Cnt(sentence)
        if(count_val==0):
            count_val=1e-6
        # print(n_gram)
        lamb = self.constant/count_val
        c_lamb = self.count_of_positives(sentence)
        if(c_lamb == 0):
            c_lamb = 1e-6
        lamb = lamb*c_lamb

        pass_history = " ".join(sentence.split()[1:])
        # print(str(n_gram)+" Lambda is: ", end="")
        # print(" First term is: ", end="")
        # print(first_term)
        final_val = first_term+lamb * \
            self.kneser_ney(pass_history, word)
        return final_val

    def witten_bell(self, sentence, word):

        wot = list(filter(None, (re.split(" ", sentence))))

        n_gram = len(wot)+1
        if(n_gram == 1):

            if word not in self.dictionary_main[1]:

                return self.dictionary_main[1]['<UNK>']/sum(self.dictionary_main[1].values())

            return max(1e-6, self.dictionary_main[1]['<UNK>'])/sum(self.dictionary_main[1].values())

        else:
            complete_sentence = " ".join([sentence, word])
            val = 1e-6
            if sentence in self.dictionary_main[n_gram-1]:
                val = self.dictionary_main[n_gram-1][sentence]
            pml = self.Cnt(complete_sentence)/val
            pml = pml/val
            lamb = val/(max(1, 2*val))
            pass_history = " ".join(sentence.split()[1:])
            return lamb*pml+(1-lamb)*self.witten_bell(pass_history, word)

    def witten_bell2(self,sentence,word):
        wot = list(filter(None, (re.split(" ", sentence))))
        n_gram = len(wot)+1
        if(n_gram == 1):
            if word  in self.dictionary_main[1]:
                # return self.dictionary_main[1]['<UNK>']/sum(self.dictionary_main[1].values())
                return self.Cnt(sentence)/(self.dictionary_main[1]["<UNK>"])
            return 1/len(self.dictionary_main[1])
            # return max(1e-6, self.dictionary_main[1]['<UNK>'])/sum(self.dictionary_main[1].values())

        try:
            lamb=self.count_of_positives(sentence)/(self.count_of_positives(sentence)+self.sum_of_counts(sentence))
        except:
            lamb=1/len(self.dictionary_main[n_gram])
        complete_sentence = " ".join([sentence, word])
        
        pml=self.Cnt(complete_sentence)/max(1e-6,self.sum_of_counts(sentence))
        pass_history = " ".join(sentence.split()[1:])
        return (1-lamb)*pml+lamb*self.witten_bell2(pass_history,word)

    def witten_bell3(self,sentence,word):
        wot = list(filter(None, (re.split(" ", sentence))))
        n_gram = len(wot)+1
        if(n_gram)==1:
            
            num=self.Cnt(word)
            if(num==0):
                num=max(self.dictionary_main[1]['<UNK>'],num)
            denom=sum(self.dictionary_main[1].values())
            return num/denom
        num=self.count_of_positives(sentence)
        denom=self.sum_of_counts(sentence)
        if(denom==0):
            denom=1e-6
        lamb=num/(denom+num)
        complete_sentence = " ".join([sentence, word])
        pml=max(1e-6,self.Cnt(complete_sentence))
        pml=pml/denom
        pass_history = " ".join(sentence.split()[1:])
        return lamb*(self.witten_bell3(pass_history,word))+(1-lamb)*pml

def run_language_mdel_initiater(n_gram,sentence,smoothing):
    
    ans=1
    sentence=re.sub("\s+"," ",sentence)
    arr=sentence.split(" ")

    for i in range(len(arr)-n_gram+1):
        sentence_util=arr[i:i+n_gram-1]
        # print(sentence_util)
        word=arr[i+n_gram-1].strip()

        sentence_util=" ".join(sentence_util).strip()
        # print(sentence_util)
        # print(word)
        # print(sentence_util.strip()+"    "+sentence[i+n_gram-1])
        if(smoothing=="w"):
            ans*=lm.witten_bell3(sentence_util.strip(),word)
        else:
            ans*=lm.kneser_ney(sentence_util.strip(),word)
            pass
    # print(ans)
    # if(ans==0):
    #     lm.dictionary_main[1]['<UNK>']/len(lm.dictionary_main[1])
    return ans

def get_perplexity(n, text, smooth):
    try:
        return np.power(1/run_language_mdel_initiater(n, text, smooth), 1/(len(text.split())))
    except:
        return np.inf
if __name__ == '__main__':
    n_gram=4
    sent = "or views of"
    filename="ulys_t.txt"
    f = open(filename, "r")
    smoothing="k"
    data = f.read()
    arr = re.findall("<SOS>(.*?)<EOS>", data)
    
    np.random.seed(41)
    train_split=[]
    test_split=[]
    select_id=np.random.choice(len(arr),1000,replace=True)
    
    for i,val in enumerate(arr):

        if i in select_id:
            test_split.append(val.strip())

        else:
            
            x="<SOS> "
            x+=val.strip()
            x+=" <EOS>"
            train_split.append(x)
    
    train_split=" ".join(train_split)
    train_split_arr=re.findall("<SOS>(.*?)<EOS>", train_split)
    # test_sentence<SOS> <SOS> <SOS> she had saved him from being trampled underfoot and had gone scarcely having been <EOS> 2.5505392607296598
# ="<SOS> wow this is a <EOS>"
    n_gram_model = N_Grams(n_gram, train_split, 2)
    # print(recursiveNgramsConstructor(n_gram, [sent]))
    x = n_gram_model.n_gram_main()
    lm = Language_Model(x, n_gram)
    # print(lm.dictionary_main)
    # print(get_perplexity(n_gram,"why are we still here just to suffer","k"))
    original_stdout = sys.stdout # Save a reference to the original standard output
    print("Test Set Frequencies")
    types=['Test','Train']
    # print(train_split_arr[0])
    # print(get_perplexity( 4,"<SOS> "+ train_split_arr[0]+" <EOS>","w"))

    # out_path =  "2020115005"  +"_"+"test" + "4" + "_" + smoothing +"_"+ filename
    # f = open(out_path, "w")
    # f=open(out_path,"a")
    # print("Test Set Frequencies")
    # avg=0
    # n_gram=4

    # for string in test_split:
    #         string=remove_stupid_fullstop(string)
    #         string=detect_full_stop(string)
    #         string=special_cases(string)
    #         string=tokenizer(string)
    #         stri="<SOS> "
    #         x=""
    #         for i in range(n_gram-1): 
    #             x+=stri
    #         string=x+string.strip()+" <EOS>"
    #         string=re.sub("\s+"," ",string).strip()
            
    #         print(string)

    #         val=get_perplexity(n_gram,string,smoothing)
    #         f.write(string +" ");f.write(str(val)+"\n")

    #         avg+=val
    #         print(val)

    # f.write("Average Value: ")
    # f.write(str(avg/len(test_split))+"\n")
    # print(avg/len(test_split))

    out_path =  "2020115005"  +"_"+"train" + "4" + "_" + smoothing +"_"+ filename
    f = open(out_path, "w")
    f=open(out_path,"a")
    # # # print(avg/len(test_split))
    avg=0
    print("Train Set Frequencies")
    ii=0
    
    for string in train_split_arr:
            if(ii>=1000):
                break
            ii+=1
            print(ii)
            string=remove_stupid_fullstop(string)
            string=detect_full_stop(string)
            string=special_cases(string)
            string=tokenizer(string)
            stri="<SOS> "
            x=""
            for i in range(n_gram-1): 
                x+=stri
            string=x+string.strip()+" <EOS>"
            string=re.sub("\s+"," ",string).strip()
            val=get_perplexity(n_gram,string,smoothing)
            f.write(string +" ");f.write(str(val)+"\n")
            avg+=val
            print(val)
    f.write("Average Value: ")
    f.write(str(avg/1000)+"\n")
    sys.stdout=original_stdout
    print(avg/1000)
