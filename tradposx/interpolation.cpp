#include </home/ubuntu/fuyuew/mrpc/MRPCProject/plotfunctions.cpp>
#include "createsinshapedata.cpp"

TString thisdir="tradposx/";
TString rootdir="../../data/"+thisdir,txtdir="../../txt/"+thisdir,plotdir="../../plot/"+thisdir,NNmodeldir="../../data/nnx/tensorflow/",NNplotdir="../../plot/nnx/";
// Double_t beamuncertainty=3;//mm
pair<vector<Double_t*>,vector<Double_t*> > readresofromfile(Int_t Nbofrow,TString CNNmodelid,TString what2D);
void measureslewing(TString CNNmodelid);
void readandplotfinalresult(TString CNNmodelid);
void interfinalenergy(TString CNNmodelid);
void interpolationx();
void runcorrectionx();
void interpolation(){
  // interpolationx();
  // runcorrectionx();
  // plotresidualvsmeasure(txtdir,plotdir,0);
  NNcompare(txtdir,NNplotdir,"../../data/nnx/tensorflow/CNNmodelpred/dataframe/",0);
  TString CNNmodelid=""; 
  // measureslewing(CNNmodelid);
  // interfinalenergy(CNNmodelid);
  // readandplotfinalresult(CNNmodelid);
}
void readandplotfinalresult(TString CNNmodelid){
  TString what2D="mea2D";
  Int_t whichmethod[2]={2,3},whichscan[2]={0,1},whichrow[2]={1,3};
  Int_t Nbofmethod,Nbofscan;
  Nbofmethod=whichmethod[1]-whichmethod[0]+1;
  Nbofscan=whichscan[1]-whichscan[0]+1;


  plotpara p1;
  vector<Double_t*> vectowerid,vecreso1,vecreso2;
  vector<Int_t> vecNbofpoint;
  std::pair<vector<Double_t*>,vector<Double_t*> > thispair=readresofromfile(Nbofrow,CNNmodelid,what2D);
  vecreso1=thispair.first;
  vecreso2=thispair.second;
  Double_t towerid[Nbofrow];
  for(Int_t rowi=0;rowi<Nbofrow;rowi++) towerid[rowi]=rowi+1;
  for(Int_t k=0;k<vecreso1.size();k++){
  	 vectowerid.push_back(towerid);
  	 vecNbofpoint.push_back(Nbofrow);
  }
  
  p1.color[0]=4;
  p1.color[1]=3;
  p1.color[2]=1;
  p1.color[3]=2;
  p1.color[4]=6;
  p1.marker[0]=22;
  p1.marker[1]=23;	 
  p1.marker[2]=20;
  p1.marker[3]=21;
  p1.marker[4]=22;
  p1.legendname.push_back("1D Correction M1");
  p1.legendname.push_back("1D Correction M1");
  p1.legendname.push_back("2D Correction");
  p1.legendname.push_back("CNN");

  p1.SetLegendPosition(0.18,0.65,0.55,0.9);
  p1.xname="Tower ID";
  p1.yname[0]="Y Position Resolution [mm]";
  p1.SetY1range(2.5,7);

  p1.SetXrange(whichrow[0]-0.8,whichrow[1]+0.8);
  p1.textcontent="ECal: Tower in Row 1 @Energy=1.6GeV";
  p1.plotname=plotdir+"resomaprow1";
  DrawNGraph(vectowerid,vecreso1,vecreso1.size(),vecNbofpoint,p1);
  p1.textcontent="ECal: Tower in Row 2 @Energy=1.6GeV";
  p1.plotname=plotdir+"resomaprow2";
  DrawNGraph(vectowerid,vecreso2,vecreso2.size(),vecNbofpoint,p1);

}

void interfinalenergy(TString CNNmodelid){

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
  	 tmpresoarray=new Double_t[Nbofrow];
  	 for(Int_t rowi=0;rowi<Nbofrow;rowi++) tmpresoarray[rowi]=posresorow[methodid][1][rowi];
  	 vecreso2.push_back(tmpresoarray);		
  	 vectowerid.push_back(towerid);
  	 vecNbofpoint.push_back(Nbofrow);
  	 p1.legendname.push_back("1D Correction M"+TString::Format("%d",whichmethod[0]+methodid-1));
  }


  Double_t slewreso1[Nbofrow], slewreso2[Nbofrow];
  for(Int_t scani=0;scani<Nbofscan;scani++){
  	 Double_t tmpreso[3];
  	 slewing(rootdir,plotdir,txtdir,scani+whichscan[0],tmpreso);
  	 if(scani==0)
  		for(Int_t rowi=0;rowi<Nbofrow;rowi++) slewreso1[rowi]=sqrt(pow(tmpreso[rowi]*10,2)-pow(beamuncertainty,2));
  	 else
  		for(Int_t rowi=0;rowi<Nbofrow;rowi++) slewreso2[rowi]=sqrt(pow(tmpreso[rowi]*10,2)-pow(beamuncertainty,2));
  	 // cout<<"scan"<<scani<<" "<<slewreso1[scani]<<endl;
  }
  vecreso1.push_back(slewreso1);
  vecreso2.push_back(slewreso2);
  vectowerid.push_back(towerid);
  vecNbofpoint.push_back(Nbofrow);
  p1.legendname.push_back("2D Correction");

  
  NNmodeldir="../../data/nnx/tensorflow/CNNmodelpred"+CNNmodelid+"/";
  Double_t NNreso1[Nbofrow], NNreso2[Nbofrow];
  for(Int_t scani=0;scani<Nbofscan;scani++){
  	 Double_t tmpreso[3];
  	 analysisNN(NNmodeldir,NNplotdir,scani+whichscan[0],tmpreso); //NNplotdir
  	 if(scani==0)
  		for(Int_t rowi=0;rowi<Nbofrow;rowi++) NNreso1[rowi]=sqrt(pow(tmpreso[rowi]*10,2)-pow(beamuncertainty,2));
  	 else
  		for(Int_t rowi=0;rowi<Nbofrow;rowi++) NNreso2[rowi]=sqrt(pow(tmpreso[rowi]*10,2)-pow(beamuncertainty,2));
  }
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


  ofstream outstd(txtdir+"summaryofresorow1CNN"+CNNmodelid+"mea2D.txt");
  outstd<<"scanid M1 M2 2D CNN\n";
  for(Int_t k=0;k<Nbofrow;k++) outstd<<k+whichrow[0]<<" "<<vecreso1[0][k]<<" "<<vecreso1[1][k]<<" "<<vecreso1[2][k]<<" "<<vecreso1[3][k]<<"\n";
  


  ofstream outstd2(txtdir+"summaryofresorow2CNN"+CNNmodelid+"mea2D.txt");
  outstd2<<"scanid M1 M2 2D CNN\n";
  for(Int_t k=0;k<Nbofrow;k++) outstd2<<k+whichrow[0]<<" "<<vecreso2[0][k]<<" "<<vecreso2[1][k]<<" "<<vecreso2[2][k]<<" "<<vecreso2[3][k]<<"\n";
  
}




pair<vector<Double_t*>,vector<Double_t*> > readresofromfile(Int_t Nbofrow,TString CNNmodelid,TString what2D){
  vector<Double_t*> vecreso1, vecreso2;
  for(Int_t scani=0;scani<2;scani++){
	 Double_t* reso1=new Double_t[Nbofrow];
	 Double_t* reso2=new Double_t[Nbofrow];
	 Double_t* resoa2D=new Double_t[Nbofrow];
	 Double_t* resonn=new Double_t[Nbofrow];

	 ifstream infile(txtdir+"summaryofresorow"+TString::Format("%d",scani+1)+"CNN"+CNNmodelid+what2D+".txt", ios::in);
	 TString tmpstr;
	 Double_t tmpdouble;
	 infile>>tmpstr>>tmpstr>>tmpstr>>tmpstr>>tmpstr;
	 for(Int_t rowi=0;rowi<Nbofrow;rowi++){
		infile>>tmpdouble;
		infile>>tmpdouble; reso1[rowi]=tmpdouble;
		infile>>tmpdouble; reso2[rowi]=tmpdouble;
		infile>>tmpdouble; resoa2D[rowi]=tmpdouble;
		infile>>tmpdouble; resonn[rowi]=tmpdouble;
	 }
	 if(scani==0){
		vecreso1.push_back(reso1);
		vecreso1.push_back(reso2);
		vecreso1.push_back(resoa2D);
		vecreso1.push_back(resonn);
	 }
	 else{
		vecreso2.push_back(reso1);
		vecreso2.push_back(reso2);
		vecreso2.push_back(resoa2D);
		vecreso2.push_back(resonn);
	 }
  }
  return std::make_pair(vecreso1,vecreso2);
}


void measureslewing(TString CNNmodelid){
  TString what2D="";
  Int_t whichmethod[2]={2,3},whichscan[2]={0,1},whichrow[2]={1,3};
  Int_t Nbofmethod,Nbofscan;
  Nbofmethod=whichmethod[1]-whichmethod[0]+1;
  Nbofscan=whichscan[1]-whichscan[0]+1;

  plotpara p1;
  vector<Double_t*> vectowerid,vecreso1,vecreso2;
  vector<Int_t> vecNbofpoint;
  std::pair<vector<Double_t*>,vector<Double_t*> > thispair=readresofromfile(Nbofrow,CNNmodelid,what2D);
  vecreso1=thispair.first;
  vecreso2=thispair.second;
  cout<<vecreso1[0][0]<<endl;
  Double_t slewreso1[Nbofrow], slewreso2[Nbofrow],towerid[Nbofrow];
  for(Int_t rowi=0;rowi<Nbofrow;rowi++) towerid[rowi]=rowi+1;

  
  for(Int_t scani=0;scani<Nbofscan;scani++){
  	 Double_t tmpreso[3];
  	 slewing(rootdir,plotdir,txtdir,scani+whichscan[0],tmpreso);
  	 if(scani==0)
  		for(Int_t rowi=0;rowi<Nbofrow;rowi++) slewreso1[rowi]=sqrt(pow(tmpreso[rowi]*10,2)-pow(beamuncertainty,2));
  	 else
  		for(Int_t rowi=0;rowi<Nbofrow;rowi++) slewreso2[rowi]=sqrt(pow(tmpreso[rowi]*10,2)-pow(beamuncertainty,2));
  	 // cout<<"scan"<<scani<<" "<<slewreso1[scani]<<endl;
  }
  vecreso1.push_back(slewreso1);
  vecreso2.push_back(slewreso2);


  
  for(Int_t k=0;k<vecreso2.size();k++){
  	 vectowerid.push_back(towerid);
  	 vecNbofpoint.push_back(Nbofrow);
  }
  p1.color[0]=4;
  p1.color[1]=3;
  p1.color[2]=1;
  p1.color[3]=2;
  p1.color[4]=6;
  p1.marker[0]=22;
  p1.marker[1]=23;	 
  p1.marker[2]=20;
  p1.marker[3]=21;
  p1.marker[4]=22;
  p1.legendname.push_back("1D Correction M1");
  p1.legendname.push_back("1D Correction M1");
  p1.legendname.push_back("2D Correction");
  p1.legendname.push_back("CNN");
  p1.legendname.push_back("2D mea Correction");

  p1.SetLegendPosition(0.18,0.65,0.55,0.9);
  p1.xname="Tower ID";
  p1.yname[0]="Y Position Resolution [mm]";
  p1.SetY1range(2.5,7);

    p1.SetXrange(whichrow[0]-0.8,whichrow[1]+0.8);
  p1.textcontent="ECal: Tower in Row 1 @Energy=1.6GeV";
  p1.plotname=plotdir+"newresomaprow1";
  DrawNGraph(vectowerid,vecreso1,vecreso1.size(),vecNbofpoint,p1);
  p1.textcontent="ECal: Tower in Row 2 @Energy=1.6GeV";
  p1.plotname=plotdir+"newresomaprow2";
  DrawNGraph(vectowerid,vecreso2,vecreso2.size(),vecNbofpoint,p1);


  
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

  TString CNNmodelid=""; //default ""
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
  		for(Int_t rowi=0;rowi<Nbofrow;rowi++) slewreso1[rowi]=sqrt(pow(tmpreso[rowi]*10,2)-pow(beamuncertainty,2));
  	 else
  	   for(Int_t rowi=0;rowi<Nbofrow;rowi++) slewreso2[rowi]=sqrt(pow(tmpreso[rowi]*10,2)-pow(beamuncertainty,2));
  }
  vecreso1.push_back(slewreso1);
  vecreso2.push_back(slewreso2);
  vectowerid.push_back(towerid);
  vecNbofpoint.push_back(Nbofrow);
  p1.legendname.push_back("2D Correction");

  
  NNmodeldir="../../data/nnx/tensorflow/CNNmodelpred"+CNNmodelid+"/";
  Double_t NNreso1[Nbofrow], NNreso2[Nbofrow];
  for(Int_t scani=0;scani<Nbofscan;scani++){
  	 Double_t tmpreso[3];
  	 analysisNN(NNmodeldir,NNplotdir,scani+whichscan[0],tmpreso); //NNplotdir
  	 if(scani==0)
  		for(Int_t rowi=0;rowi<Nbofrow;rowi++) NNreso1[rowi]=sqrt(pow(tmpreso[rowi]*10,2)-pow(beamuncertainty,2));
  	 else
  		for(Int_t rowi=0;rowi<Nbofrow;rowi++) NNreso2[rowi]=sqrt(pow(tmpreso[rowi]*10,2)-pow(beamuncertainty,2));
  }
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


  ofstream outstd(txtdir+"summaryofresorow1CNN"+CNNmodelid+".txt");
  outstd<<"scanid M1 M2 2D CNN\n";
  for(Int_t k=0;k<Nbofrow;k++) outstd<<k+whichrow[0]<<" "<<vecreso1[0][k]<<" "<<vecreso1[1][k]<<" "<<vecreso1[2][k]<<" "<<vecreso1[3][k]<<"\n";
  


  ofstream outstd2(txtdir+"summaryofresorow2CNN"+CNNmodelid+".txt");
  outstd2<<"scanid M1 M2 2D CNN\n";
  for(Int_t k=0;k<Nbofrow;k++) outstd2<<k+whichrow[0]<<" "<<vecreso2[0][k]<<" "<<vecreso2[1][k]<<" "<<vecreso2[2][k]<<" "<<vecreso2[3][k]<<"\n";
  
  
}
