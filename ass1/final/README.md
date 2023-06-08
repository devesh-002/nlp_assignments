# Run Instructions

The file contains 4 total .py files,

The language_model.py runs as instructed and gives the output 

```
python3 language_model.py k ./corpus.txt
```

There are two neural language models, one for each corpus. The pride and prejudice works in colab and is linked in code, it would be better to load it there.

The other corpus is too huge to be even loaded on colab (the dimensions are huge) and hence can be loaded on ada. But if you have that much capability locally, the model compiles as:

```
python3 neural_language_model.py ../models/trained_nlm.h5(path)
```

NOTE: To run neural language model locally you need to keep the tokenised corpus along with it in the same directory, else it will not work. They are submitted along with model in drive link

To run on ada first build an interactive session:

```
sinteractive -c 20 -g 2
python3 neural_language_model.py path
```

The Joyce corpus needs atleast 2 GPUs and 20 CPUs atleast, else the model won't load!

The training part has been commented for now, uncomment that to train.

Joyce Neural Model: https://drive.google.com/file/d/1RMxctGAoCtavHeZZTErYE6NFtueHqpty/view?usp=sharing

Pride and Prejudice Model:https://drive.google.com/file/d/1PHtyhebcSZbRIWudWKDryW40n7Lyk-OA/view?usp=sharing
