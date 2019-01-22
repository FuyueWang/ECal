#include </home/ubuntu/fuyuew/mrpc/MRPCProject/plotfunctions.cpp>
#include "createsinshapedata.cpp"

TString thisdir="tradposx/";
TString rootdir="../../data/"+thisdir,txtdir="../../txt/"+thisdir,plotdir="../../plot/"+thisdir,NNmodeldir="../../data/nnx/tensorflow/",NNplotdir="../../plot/nnx/";
void interpolationx();
void interpolationy();
void runcorrectionx();
void interpolation(){
  // interpolationy();
  // interpolationx();
  // runcorrectionx();
  // plotresidualvsmeasure(txtdir,plotdir,0);
  NNcompare(txtdir,NNplotdir,"../../data/nnx/tensorflow/CNNmodelpred/dataframe/",0);
}

void runcorrectionx(){
  for(Int_t scani=0;scani<2;scani++){
  	 // createsinshapedata(rootdir,txtdir,scani);
  	 // createfitpara(txtdir,plotdir,scani);
  	 for(Int_t methodid=2;methodid<4;methodid++)
  	 	correction(rootdir,plotdir,txtdir,methodid,scani);
  }


}

void interpolationx(){
  Double_t beamuncertainty=3;//mm
  // for(Int_t scani=0;scani<1;scani++){
  // 	 createsinshapedata(rootdir,txtdir,scani);
  // 	 createfitpara(txtdir,plotdir,scani);
  // 	 // for(Int_t methodid=4;methodid<5;methodid++)
  // 	 // 	correction(rootdir,plotdir,txtdir,methodid,scani);
  // }

  // Double_t tmpreso[3];
  // amplitudeslewing(rootdir,plotdir,txtdir,0,tmpreso);




  
  Int_t whichmethod[2]={2,3},whichscan[2]={0,1},whichrow[2]={1,3};
  Int_t Nbofmethod,Nbofscan,Nbofrow;
  Nbofmethod=whichmethod[1]-whichmethod[0]+1;
  Nbofscan=whichscan[1]-whichscan[0]+1;
  Nbofrow=whichrow[1]-whichrow[0]+1;
  Double_t towerid[Nbofrow],posresorow[Nbofmethod][Nbofscan][Nbofrow];
  for(Int_t rowi=0;rowi<Nbofrow;rowi++) towerid[rowi]=rowi+whichrow[0];
  for(Int_t methodid=0;methodid<Nbofmethod;methodid++){
  	 for(Int_t scani=0;scani<Nbofscan;scani++){
  		Double_t tmpreso[Nbofrow];
  		analysisforeverypixel(rootdir,plotdir,methodid+whichmethod[0],scani+whichscan[0],tmpreso);
  		for(Int_t rowi=0;rowi<Nbofrow;rowi++) posresorow[methodid][scani][rowi]=sqrt(pow(tmpreso[rowi]*10,2)-pow(beamuncertainty,2));
  	 }
  }
  
  plotpara p1;
  vector<Double_t*> vectowerid,vecreso1,vecreso2;
  vector<Int_t> vecNbofpoint;

  
  Double_t tmpresoarray[Nbofscan];
  for(Int_t methodid=0;methodid<Nbofmethod;methodid++){
  	 Double_t* tmpresoarray=new Double_t[Nbofrow];
  	 for(Int_t rowi=0;rowi<Nbofrow;rowi++) tmpresoarray[rowi]=posresorow[methodid][0][rowi];
  	 vecreso1.push_back(tmpresoarray);
  	 // cout<<"1mid"<<Nbofmethod-1-methodid<<" methodid="<<whichmethod[1]-methodid<<" "<<"row1reso="<<tmpresoarray[0]<<" "<<tmpresoarray[1]<<" "<<tmpresoarray[2]<<endl;
  	 tmpresoarray=new Double_t[Nbofrow];
  	 for(Int_t rowi=0;rowi<Nbofrow;rowi++) tmpresoarray[rowi]=posresorow[methodid][1][rowi];
  	 // cout<<"2mid"<<Nbofmethod-1-methodid<<" methodid="<<whichmethod[1]-methodid<<" "<<"row1reso="<<tmpresoarray[0]<<" "<<tmpresoarray[1]<<" "<<tmpresoarray[2]<<endl;
  	 vecreso2.push_back(tmpresoarray);		
  	 vectowerid.push_back(towerid);
  	 vecNbofpoint.push_back(Nbofrow);
  	 p1.legendname.push_back("1D Correction M"+TString::Format("%d",whichmethod[0]+methodid-1));
  }


  Double_t slewreso1[Nbofrow], slewreso2[Nbofrow];
  for(Int_t scani=0;scani<Nbofscan;scani++){
  	 Double_t tmpreso[Nbofrow];
  	 amplitudeslewing(rootdir,plotdir,txtdir,scani+whichscan[0],tmpreso);
  	 if(scani==0)
  		for(Int_t rowi=0;rowi<Nbofrow;rowi++) slewreso1[rowi]=sqrt(pow(tmpreso[0]*10,2)-pow(beamuncertainty,2));
  	 else
  	   for(Int_t rowi=0;rowi<Nbofrow;rowi++) slewreso2[rowi]=sqrt(pow(tmpreso[1]*10,2)-pow(beamuncertainty,2));
  }
  cout<<"scan0 "<<slewreso1[0]<<" "<<slewreso1[1]<<" "<<slewreso1[2]<<endl;
  cout<<"scan1 "<<slewreso2[0]<<" "<<slewreso2[1]<<" "<<slewreso2[2]<<endl;
  vecreso1.push_back(slewreso1);
  vecreso2.push_back(slewreso2);
  vectowerid.push_back(towerid);
  vecNbofpoint.push_back(Nbofrow);
  p1.legendname.push_back("2D Correction");

  
  NNmodeldir="../../data/nnx/tensorflow/CNNmodelpred/";
  Double_t NNreso1[Nbofrow], NNreso2[Nbofrow];
  for(Int_t scani=0;scani<Nbofscan;scani++){
  	 Double_t tmpreso[3];
  	 analysisNN(NNmodeldir,NNplotdir,scani+whichscan[0],tmpreso); //NNplotdir
  	 if(scani==0)
  		for(Int_t rowi=0;rowi<Nbofrow;rowi++) NNreso1[rowi]=sqrt(pow(tmpreso[0]*10,2)-pow(beamuncertainty,2));
  	 else
  		for(Int_t rowi=0;rowi<Nbofrow;rowi++) NNreso2[rowi]=sqrt(pow(tmpreso[1]*10,2)-pow(beamuncertainty,2));
  }
  cout<<"scan0 "<<NNreso1[0]<<" "<<NNreso1[1]<<" "<<NNreso1[2]<<endl;
  cout<<"scan1 "<<NNreso2[0]<<" "<<NNreso2[1]<<" "<<NNreso2[2]<<endl;
  vecreso1.push_back(NNreso1);
  vecreso2.push_back(NNreso2);
  vectowerid.push_back(towerid);
  vecNbofpoint.push_back(Nbofrow);
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
  p1.yname[0]="X Position Resolution [mm]";
  p1.SetY1range(2.5,6.5);
  p1.SetXrange(whichrow[0]-0.8,whichrow[1]+0.8);
  p1.textcontent="ECal: Tower in Row 1 @Energy=1.6GeV";
  p1.plotname=plotdir+"resomaprow1";
  p1.format=".pdf";
  DrawNGraph(vectowerid,vecreso1,Nbofmethod+2,vecNbofpoint,p1);
  p1.textcontent="ECal: Tower in Row 2 @Energy=1.6GeV";
  p1.plotname=plotdir+"resomaprow2";
  DrawNGraph(vectowerid,vecreso2,Nbofmethod+2,vecNbofpoint,p1);












  
  
}

void interpolationy(){
  for(Int_t scani=1;scani<7;scani++){
  	 createsinshapedata(rootdir,txtdir,scani);
  	 // createfitpara(txtdir,plotdir,scani);
  	 // for(Int_t methodid=2;methodid<5;methodid++)
  	 // 	correction(rootdir,plotdir,txtdir,methodid,scani);
  }
  Double_t reso[2];
  // analysisforeverypixel(rootdir,plotdir,2,1,reso);

  // Double_t re=analysisforeveryscan(rootdir,plotdir,2,1);
  // analysisNN(NNmodeldir,NNplotdir,1,reso);
  // slewing(rootdir,plotdir,txtdir,1,reso);
  // cout<<reso[0]<<" "<<reso[1]<<endl;


  
  Int_t whichmethod[2]={2,4},whichscan[2]={1,6};
  Int_t Nbofmethod,Nbofscan;
  Nbofmethod=whichmethod[1]-whichmethod[0]+1;
  Nbofscan=whichscan[1]-whichscan[0]+1;
  
  Double_t towerid[Nbofscan],posresorow1[Nbofmethod][Nbofscan],posresorow2[Nbofmethod][Nbofscan];
  for(Int_t scani=0;scani<Nbofscan;scani++) towerid[scani]=scani+whichscan[0];
  for(Int_t methodid=0;methodid<Nbofmethod;methodid++){
  	 for(Int_t scani=0;scani<Nbofscan;scani++){
  		Double_t tmpreso[2];
  		analysisforeverypixel(rootdir,"",methodid+whichmethod[0],scani+whichscan[0],tmpreso);
  		posresorow1[methodid][scani]=tmpreso[0]*10;
  		posresorow2[methodid][scani]=tmpreso[1]*10;
  	 }
  }
  NNmodeldir="../../data/nn/tensorflow/CNNmodelpred2/";
  plotpara p1;
  vector<Double_t*> vectowerid,vecreso1,vecreso2;
  vector<Int_t> vecNbofpoint;
  Double_t NNreso1[Nbofscan], NNreso2[Nbofscan];
  for(Int_t scani=0;scani<Nbofscan;scani++){
  	 Double_t tmpreso[2];
  	 analysisNN(NNmodeldir,NNplotdir,scani+whichscan[0],tmpreso); //NNplotdir
  	 NNreso1[scani]=tmpreso[0]*10;
  	 NNreso2[scani]=tmpreso[1]*10;
  	 // cout<<"scan"<<scani<<" "<<NNreso1[scani]<<endl;
  }
  vecreso1.push_back(NNreso1);
  vecreso2.push_back(NNreso2);
  vectowerid.push_back(towerid);
  vecNbofpoint.push_back(Nbofscan);
  p1.legendname.push_back("CNN");
 
  Double_t tmpresoarray[Nbofscan];
  for(Int_t methodid=0;methodid<Nbofmethod;methodid++){
  	 Double_t* tmpresoarray=new Double_t[Nbofscan];
  	 for(Int_t scani=0;scani<Nbofscan;scani++) tmpresoarray[scani]=posresorow1[Nbofmethod-1-methodid][scani];
  	 vecreso1.push_back(tmpresoarray);
  	 tmpresoarray=new Double_t[Nbofscan];
  	 for(Int_t scani=0;scani<Nbofscan;scani++) tmpresoarray[scani]=posresorow2[Nbofmethod-1-methodid][scani];
  	 vecreso2.push_back(tmpresoarray);		
  	 vectowerid.push_back(towerid);
  	 vecNbofpoint.push_back(Nbofscan);
  	 p1.legendname.push_back("Correction M"+TString::Format("%d",whichmethod[1]-methodid));
  }
  Double_t slewreso1[Nbofscan], slewreso2[Nbofscan];
  for(Int_t scani=0;scani<Nbofscan;scani++){
  	 Double_t tmpreso[2];
  	 slewing(rootdir,"",txtdir,scani+whichscan[0],tmpreso);
  	 slewreso1[scani]=tmpreso[0]*10;
  	 slewreso2[scani]=tmpreso[1]*10;
  	 // cout<<"scan"<<scani<<" "<<slewreso1[scani]<<endl;
  }
  vecreso1.push_back(slewreso1);
  vecreso2.push_back(slewreso2);
  vectowerid.push_back(towerid);
  vecNbofpoint.push_back(Nbofscan);
  p1.legendname.push_back("Correction M1");
  p1.SetLegendPosition(0.15,0.65,0.48,0.9);
  p1.xname="Tower ID";
  p1.yname[0]="Y Position Resolution [mm]";
  p1.SetY1range(3,8);
  p1.SetXrange(0.2,6.8);
  p1.textcontent="ECal: Tower in Row 1";
  p1.plotname=plotdir+"resomaprow1";
  DrawNGraph(vectowerid,vecreso1,Nbofmethod+2,vecNbofpoint,p1);
  p1.textcontent="ECal: Tower in Row 2";
  p1.plotname=plotdir+"resomaprow2";
  DrawNGraph(vectowerid,vecreso2,Nbofmethod+2,vecNbofpoint,p1);

}
