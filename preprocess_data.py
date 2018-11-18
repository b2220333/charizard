import json
import os
import sys
import nltk
import random
import math
nltk.download('punkt')
if sys.version_info[0] < 3:
  raise Exception('You need to run this with Python 3.')

train_split, dev_split, test_split = 0.8, 0.1, 0.1
extraction_field = 'selftext'
path_prefix = "results_"
path_postfix = ".json"
pairs = [('learnpython', 'cpp'), ('Republican', 'Democrat'), ('mac', 'windows'),
         ('askmen', 'askwomen'), ('redpill', 'bluepill'),
         ('pokemon', 'digimon'), ('funny', 'sad'), ('stanford', 'berkeley'),
         ('bitcoin', 'ethereum'), ('ps3', 'xbox'), ('android', 'ios'),
         ('nike', 'adidas'), ('prolife', 'prochoice')]
input_dir = 'data/'
output_dir = 'preprocessed_data/'

if not os.path.exists(input_dir):
  raise ValueError('Data directory (%s) does not exist.' % input_dir)

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for pair in pairs:
  pair_output_dir = os.path.join(output_dir, '%s + %s' % (pair[0], pair[1]))
  if  not os.path.exists(pair_output_dir):
    os.makedirs(pair_output_dir)
  for i, name in enumerate(pair):
    print(name)

    input_filename = path_prefix + name + path_postfix
    data = json.loads(open(os.path.join(input_dir, input_filename),
      encoding='utf-8').read())

    output_data = []
    for thread in data:
      if (extraction_field in thread and thread[extraction_field] and
          '[removed]' not in thread[extraction_field] and
          '[deleted]' not in thread[extraction_field]):
        output_data.append(nltk.word_tokenize(thread[extraction_field].lower()))

    print(len(output_data))
    random.shuffle(output_data)
    train_data = output_data[:int(math.floor(len(output_data) * train_split))]
    dev_data = output_data[int(math.floor(len(output_data) * train_split)):
      int(math.floor(len(output_data) * (train_split + dev_split)))]
    test_data = output_data[int(math.floor(len(output_data) *
      (train_split + dev_split))):]
    assert len(output_data) == len(train_data) + len(dev_data) + len(test_data)

    for split_data, split in [(train_data, "train"), (dev_data, "dev"),
                              (test_data, "test")]:
      output_filename = 'data.%s.%s' % (split, str(i))
      with open(os.path.join(pair_output_dir, output_filename), 'w') as file:
        for data in split_data:
          try:
            file.write(' '.join(data) + '\n')
          except:
            pass