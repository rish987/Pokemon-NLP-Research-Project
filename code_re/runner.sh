#!/bin/bash

for i in {1..116}; do
   if [ $i -lt 10 ]; then
      str="00$i";
   else
      if [ $i -lt 100 ]; then
         str="0$i";
      else
         str="$i";
      fi
   fi

   echo "Processing episode: $str";

   cd ~/Programming/stanford-corenlp-full-2018-02-27;

   java -mx4g -cp "*" edu.stanford.nlp.naturalli.OpenIE ~/Research/pokemon_nlp/code_relation_extraction/data/text/$str >> ~/Research/pokemon_nlp/code_relation_extraction/;
done
