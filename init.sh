#!/bin/bash

cd model

if !(git rev-parse --show-toplevel | grep model); then
    git init --initial-branch=main
    git remote add -f origin https://huggingface.co/sentence-transformers/use-cmlm-multilingual

    git config core.sparsecheckout true

    echo 1_Pooling/ >> .git/info/sparse-checkout
    echo config_sentence_transformers.json >> .git/info/sparse-checkout
    echo config.json >> .git/info/sparse-checkout
    echo model.safetensors >> .git/info/sparse-checkout
    echo modules.json >> .git/info/sparse-checkout
    echo sentence_bert_config.json >> .git/info/sparse-checkout
    echo special_tokens_map.json >> .git/info/sparse-checkout
    echo tokenizer_config.json >> .git/info/sparse-checkout
    echo tokenizer.json >> .git/info/sparse-checkout
    echo vocab.txt >> .git/info/sparse-checkout
fi

git pull origin main
