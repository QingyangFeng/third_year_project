#streaming API get the data from the tweet but need to stop by keyboard 
#python movemoveInto_1.py

#export the data from the mongodb
#mongoexport -d TwitterStream -c tweet_6 -o rawDataSet.json

#preprocessing the raw data set
python preprocessing_part1.py > part1_dataSet.csv

#do the machine learning part to identify the suicidal tweet
python machinelearning_part1.py

#get the timeline tweet
python timeline.py

#preprocessing the data get from the timeline
python preprocessing_part2.py > part2_dataset_1.csv

#do the machine learning part to identify the sleep related tweet
python machinelearning_part2.py
