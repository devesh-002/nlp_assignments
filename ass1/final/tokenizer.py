import re
import argparse

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
    wiki=re.sub(r' [0-9]+ '," <NUM> ",wiki)
    wiki=re.sub(r' [0-9]+ '," <NUM> ",wiki)
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
    data=re.sub(r'(\.+)|(\?+)|(!+)'," <EOS> <SOS> ",data)
    return data

if __name__=="__main__":

    parser=argparse.ArgumentParser()
    parser.add_argument('--path',type=str,required=True)
    parser.add_argument('--n_gram',type=int,required=True)

    args=parser.parse_args()
    path=args.path
    n_gram=args.n_gram
    wiki="<SOS> "
    with open(path,"r") as fp:
        wiki=fp.readlines()
    wiki="\n".join(wiki)
    wiki=re.sub("\n+"," ",wiki)
    wiki=remove_stupid_fullstop(wiki)
    wiki=detect_full_stop(wiki)
    stri=" <SOS> "
    # for i in range(n_gram-1):
    #     stri+="<SOS> "
    wiki=stri+wiki
    wiki=wiki+" <EOS>"
    wiki=special_cases(wiki)
    wiki=tokenizer(wiki)
    print(wiki)
    pass
    
# print(special_cases("_devesh_ """))