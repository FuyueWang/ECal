for i in $(seq 5 5)
do
	 cp ../../data/dubnann/tensorflow/CNNmodels${i}/valpred.csv ../../data/dubnann/tensorflow/CNNmodelpred1/dataframe/valpredscan${i}.csv
	 cp ../../data/dubnann/tensorflow/CNNmodels${i}/valpred.csv ../../data/dubnann/tensorflow/CNNmodelpred1/valpredscan${i}.csv
	 sed -i 's/,/ /g' ../../data/dubnann/tensorflow/CNNmodelpred1/valpredscan${i}.csv
done

	 
# sed -i 's/ /,/g' /home/ubuntu/fuyuew/ecal/data/dubnann/tensorflow/CNNmodelpred/dataframe/*
# sed -i 's/,/ /g' /home/ubuntu/fuyuew/ecal/data/dubnann/tensorflow/CNNmodels0/valpred.csv
# sed -i 's/,/ /g' /home/ubuntu/fuyuew/ecal/data/dubnann/tensorflow/CNNmodels1/valpred.csv
# sed -i 's/,/ /g' /home/ubuntu/fuyuew/ecal/data/dubnann/tensorflow/CNNmodels2/valpred.csv
# sed -i 's/,/ /g' /home/ubuntu/fuyuew/ecal/data/dubnann/tensorflow/CNNmodels3/valpred.csv
# sed -i 's/,/ /g' /home/ubuntu/fuyuew/ecal/data/dubnann/tensorflow/CNNmodels4/valpred.csv
# sed -i 's/,/ /g' /home/ubuntu/fuyuew/ecal/data/dubnann/tensorflow/CNNmodels5/valpred.csv
