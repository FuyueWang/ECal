# this code write a loop to run mulitple network one after the other
cd ..
python ReadOriginalAndSaveAsPythonwithcut.py
cd network
for noi in $(seq 1 6)
do
	 lastnoi=`echo "$noi-1" | bc`
	 # echo $lastnoi, $noi
	 sed -i "s/scan=${lastnoi}/scan=${noi}/g" network.py
	 sed -i "s/row2/row1/g" network.py		
	 python network.py
	 cp network.py ../../../data/nn/tensorflow/CNNmodels${noi}row1/

	 sed -i "s/row1/row2/g" network.py		
	 python network.py
	 cp network.py ../../../data/nn/tensorflow/CNNmodels${noi}row2/

done
# 

# sed -i "s/scan=0/scan=1/g" network.py
# sed -i "s/row2/row1/g" network.py		
# python network.py
# cp network.py ../../../data/nn/tensorflow/CNNmodels1row1/

# sed -i "s/row1/row2/g" network.py
# python network.py
# cp network.py ../../../data/nn/tensorflow/CNNmodels1row2/


# sed -i "s/scan=1/scan=2/g" network.py
# sed -i "s/row2/row1/g" network.py		
# python network.py
# cp network.py ../../../data/nn/tensorflow/CNNmodels2row1/

# sed -i "s/row1/row2/g" network.py
# python network.py
# cp network.py ../../../data/nn/tensorflow/CNNmodels2row2/
