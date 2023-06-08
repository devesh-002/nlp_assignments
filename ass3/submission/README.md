# README

In the given assignment, I have implemented frequency-based modelling approaches, such as Singular Value Decomposition (SVD), and comparing it with the embeddings obtained using one of the variants of Word2vec, such as CBOW implementation with Negative Sampling.

It is highly recommended you use the colab notebook referenced here because it requires atleast 9 GB of RAM and 6 GB of GPU to train it. The link here is:

https://colab.research.google.com/drive/1E5k_wTsSXhWwcWqxJVFoHrmthIt9ut1k?usp=sharing

If you insist on using the file then run it simply as 

```
python3 file.py
```

The link for pretrained model can be found here:

Model 1:

https://drive.google.com/file/d/15m04TKRq_GaibXn6Jl9s0wT88-Z63sEB/view?usp=share_link

Model 2:

https://drive.google.com/file/d/11pZkWewi5vlvlZ4dMsfOJc7jZ2QBPRXz/view?usp=share_link

Model 1 is an implementation of the model specified by [here](https://jalammar.github.io/illustrated-word2vec/) by taking the dot product in batchnorm after summing them up.

Model 2: The second is an interesting approach. I have reduced the problem to a binary classification problem. It
involves training the embedding layer by first calculating embeddings and then putting three basic linear layers to output a
probability which denotes whether the sample is negative or positive. We have the actual labels of them and then can train
the binary classification model simply using Binary Cross Entropy Loss function.