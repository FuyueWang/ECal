for iD in $(seq 1 6)
do
	 rm -r NNtrain3by3cut${iD}
	 mkdir NNtrain3by3cut${iD}
	 cd NNtrain3by3cut${iD}
	 cp ../TMVARegression.C .
	 sed "s/linttraincutID/linttraincut${iD}/g" -i TMVARegression.C
	 cd ..
done

