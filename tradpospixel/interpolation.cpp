#include </home/ubuntu/fuyuew/mrpc/MRPCProject/plotfunctions.cpp>
#include "createsinshapedata.cpp"
void interpolationy();
void plotslewing();
void plotcompare();
TString thisdir="tradpospixel/";
TString rootdir="../../data/"+thisdir,txtdir="../../txt/"+thisdir,plotdir="../../plot/"+thisdir,NNmodeldir="../../data/nn/tensorflow/",NNplotdir="../../plot/nn/";

void interpolation(){
  // interpolationy();
  // plotslewing();
  // plotcompare();
  NNcompare(txtdir,NNplotdir,"../../data/nn/tensorflow/CNNmodelpred2/dataframe/",1);
}
void plotcompare(){
  Double_t resoof2rows[3][6];
  for(Int_t scani=1;scani<7;scani++){
  	 for(Int_t methodid=2;methodid<4;methodid++)
  	 	resoof2rows[methodid-2][scani-1]=correction(rootdir,plotdir,txtdir,methodid,scani);
  }
}


void plotslewing(){
  Double_t tmpreso[2];
  amplitudeslewing(rootdir,plotdir,txtdir,1,tmpreso);

}
void interpolationy(){
  Double_t beamuncertainty=3;//mm
  // Double_t resoof2rows[3][6];
  // for(Int_t scani=1;scani<7;scani++){
  // 	 // createsinshapedata(rootdir,txtdir,scani);
  // 	 // createfitpara(txtdir,plotdir,scani);
  // 	 for(Int_t methodid=2;methodid<4;methodid++)
  // 	 	resoof2rows[methodid-2][scani-1]=correction(rootdir,plotdir,txtdir,methodid,scani);
  // }

  // Double_t tmpreso[2];
  // analysisforeverypixel(rootdir,"",4,5,tmpreso);
  // cout<<tmpreso[0]<<endl;


  // Double_t tmpreso[2];
  // analysisforeverypixel(rootdir,plotdir,4,2,tmpreso);
  // cout<<tmpreso[0]<<endl;



  // Double_t tmpreso[2];
  // amplitudeslewing(rootdir,plotdir,txtdir,1,tmpreso);








  

  // NNmodeldir="../../data/nn/tensorflow/CNNmodelpred1/";
  // plotpara p0;
  
  // vector<Double_t*> vecmergetowerid,vecmergereso;
  // vector<Int_t> vecmergeNbofpoint;

  // Double_t mergetowerid[6];
  // for(Int_t scani=0;scani<6;scani++) mergetowerid[scani]=scani+1;

  // Double_t NNreso1[6], NNreso2[6];
  // for(Int_t scani=0;scani<6;scani++){
  // 	 Double_t tmpreso[2];
  // 	 analysisNN(NNmodeldir,NNplotdir,scani+1,tmpreso); //NNplotdir
  // 	 NNreso1[scani]=tmpreso[0]*10;
  // 	 NNreso2[scani]=tmpreso[1]*10;
  // 	 // cout<<"scan"<<scani<<" "<<NNreso1[scani]<<endl;
  // }
  // vecmergereso.push_back(NNreso1);
  // vecmergetowerid.push_back(mergetowerid);
  // vecmergeNbofpoint.push_back(6);
  // p0.legendname.push_back("CNN");
 
  // Double_t* tmpmresoarray=new Double_t[6];
  // for(Int_t methodid=0;methodid<3;methodid++){
  // 	 Double_t* tmpmresoarray=new Double_t[6];
  // 	 for(Int_t scani=0;scani<6;scani++) tmpmresoarray[scani]=resoof2rows[3-1-methodid][scani]*10;
  // 	 vecmergereso.push_back(tmpmresoarray);
  // 	 vecmergetowerid.push_back(mergetowerid);
  // 	 vecmergeNbofpoint.push_back(6);
  // 	 p0.legendname.push_back("Correction M"+TString::Format("%d",3-methodid));
  // }
  // p0.SetLegendPosition(0.15,0.65,0.48,0.9);
  // p0.xname="Tower ID";
  // p0.yname[0]="Y Position Resolution [mm]";
  // p0.SetY1range(3,8);
  // p0.SetXrange(0.2,6.8);
  // p0.textcontent="ECal: Towers";
  // p0.plotname=plotdir+"resomaprow";
  // DrawNGraph(vecmergetowerid,vecmergereso,vecmergeNbofpoint.size(),vecmergeNbofpoint,p0);











  
  
  Int_t whichmethod[2]={2,3},whichscan[2]={1,6};
  Int_t Nbofmethod,Nbofscan;
  Nbofmethod=whichmethod[1]-whichmethod[0]+1;
  Nbofscan=whichscan[1]-whichscan[0]+1;
  
  Double_t towerid[Nbofscan],posresorow1[Nbofmethod][Nbofscan],posresorow2[Nbofmethod][Nbofscan];
  for(Int_t scani=0;scani<Nbofscan;scani++) towerid[scani]=scani+whichscan[0];
  for(Int_t methodid=0;methodid<Nbofmethod;methodid++){
  	 for(Int_t scani=0;scani<Nbofscan;scani++){
  		Double_t tmpreso[2];
  		analysisforeverypixel(rootdir,plotdir,methodid+whichmethod[0],scani+whichscan[0],tmpreso);
  		posresorow1[methodid][scani]=sqrt(pow(tmpreso[0]*10,2)-pow(beamuncertainty,2));
  		posresorow2[methodid][scani]=sqrt(pow(tmpreso[1]*10,2)-pow(beamuncertainty,2));
  	 }
  }

  plotpara p1;
  vector<Double_t*> vectowerid,vecreso1,vecreso2;
  vector<Int_t> vecNbofpoint;


  Double_t tmpresoarray[Nbofscan];
  for(Int_t methodid=0;methodid<Nbofmethod;methodid++){
  	 Double_t* tmpresoarray=new Double_t[Nbofscan];
  	 for(Int_t scani=0;scani<Nbofscan;scani++) tmpresoarray[scani]=posresorow1[methodid][scani];
  	 vecreso1.push_back(tmpresoarray);
  	 tmpresoarray=new Double_t[Nbofscan];
  	 for(Int_t scani=0;scani<Nbofscan;scani++) tmpresoarray[scani]=posresorow2[methodid][scani];
  	 vecreso2.push_back(tmpresoarray);		
  	 vectowerid.push_back(towerid);
  	 vecNbofpoint.push_back(Nbofscan);
  	 p1.legendname.push_back("1D Correction M"+TString::Format("%d",methodid+whichmethod[0]-1));
  }
  
  Double_t slewreso1[Nbofscan], slewreso2[Nbofscan];
  for(Int_t scani=0;scani<Nbofscan;scani++){
  	 Double_t tmpreso[2];
  	 amplitudeslewing(rootdir,plotdir,txtdir,scani+whichscan[0],tmpreso);
  	 slewreso1[scani]=sqrt(pow(tmpreso[0]*10,2)-pow(beamuncertainty,2));
  	 slewreso2[scani]=sqrt(pow(tmpreso[1]*10,2)-pow(beamuncertainty,2));
  	 // cout<<"scan"<<scani<<" "<<slewreso1[scani]<<endl;
  }
  vecreso1.push_back(slewreso1);
  vecreso2.push_back(slewreso2);
  vectowerid.push_back(towerid);
  vecNbofpoint.push_back(Nbofscan);
  p1.legendname.push_back("2D Correction");
  
  NNmodeldir="../../data/nn/tensorflow/CNNmodelpred2/";
  Double_t NNreso1[Nbofscan], NNreso2[Nbofscan];
  for(Int_t scani=0;scani<Nbofscan;scani++){
  	 Double_t tmpreso[2];
  	 analysisNN(NNmodeldir,NNplotdir,scani+whichscan[0],tmpreso); //NNplotdir
  	 NNreso1[scani]=sqrt(pow(tmpreso[0]*10,2)-pow(beamuncertainty,2));
  	 NNreso2[scani]=sqrt(pow(tmpreso[1]*10,2)-pow(beamuncertainty,2));
  	 cout<<"CNN scan"<<scani<<" "<<NNreso2[scani]<<endl;
  }
  vecreso1.push_back(NNreso1);
  vecreso2.push_back(NNreso2);
  vectowerid.push_back(towerid);
  vecNbofpoint.push_back(Nbofscan);
  p1.legendname.push_back("CNN");
  p1.color[0]=4;
  p1.color[1]=3;
  p1.color[2]=1;
  p1.color[3]=2;
  p1.marker[0]=22;
  p1.marker[1]=23;	 
  p1.marker[2]=20;
  p1.marker[3]=21;
  p1.SetLegendPosition(0.18,0.65,0.55,0.9);
  p1.xname="Tower ID";
  p1.yname[0]="Y Position Resolution [mm]";
  p1.SetY1range(2.5,7);
  p1.SetXrange(0.2,6.8);
  p1.textcontent="ECal: Tower in Row 1 @Energy=1.6GeV";
  p1.plotname=plotdir+"resomaprow1";
  DrawNGraph(vectowerid,vecreso1,vecreso1.size(),vecNbofpoint,p1);
  p1.textcontent="ECal: Tower in Row 2 @Energy=1.6GeV";
  p1.plotname=plotdir+"resomaprow2";
	 
  DrawNGraph(vectowerid,vecreso2,vecreso2.size(),vecNbofpoint,p1);

}
