#include </home/ubuntu/fuyuew/mrpc/MRPCProject/plotfunctions.cpp>
#include "createsinshapedata.cpp"
void interpolationy();
void interpolationenergy();
vector<Double_t*> readresofromfile(Int_t Nbofscan,TString CNNmodelid);
void measureslewing(TString CNNmodelid);
void readandplotfinalresult(TString CNNmodelid);
void interfinalenergy(TString CNNmodelid);
TString thisdir="dubna/";
TString rootdir="../../data/"+thisdir,txtdir="../../txt/"+thisdir,plotdir="../../plot/"+thisdir,NNmodeldir="../../data/dubnann/tensorflow/",NNplotdir="../../plot/dubnann/";
Double_t beamuncertainty=3;//mm
void interpolation(){
  // interpolationenergy();

  TString CNNmodelid="1"; //default "1"
  // measureslewing(CNNmodelid);
  // interfinalenergy(CNNmodelid);
  readandplotfinalresult(CNNmodelid);
}

void readandplotfinalresult(TString CNNmodelid){
  Int_t whichmethod[2]={2,3},whichscan[2]={0,5};
  Int_t Nbofmethod,Nbofscan;
  Nbofmethod=whichmethod[1]-whichmethod[0]+1;
  Nbofscan=whichscan[1]-whichscan[0]+1;

  plotpara p1;
  vector<Double_t*> vectowerid;
  vector<Int_t> vecNbofpoint;
  vector<Double_t*> vecreso=readresofromfile(Nbofscan,CNNmodelid);
  Double_t towerid[Nbofscan];
  for(Int_t scani=0;scani<Nbofscan;scani++) towerid[scani]=1+scani*0.2; //energy
  for(Int_t k=0;k<vecreso.size();k++){
  	 vectowerid.push_back(towerid);
  	 vecNbofpoint.push_back(Nbofscan);
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
  p1.SetY1range(2,9);
  p1.SetXrange(0.81,2.19);
  p1.textcontent="ECal: Tower in Row 1 @Energy=1.6GeV";
  p1.plotname=plotdir+"newresomaprow1";
  DrawNGraph(vectowerid,vecreso,vecreso.size(),vecNbofpoint,p1);

}


void interfinalenergy(TString CNNmodelid){
  
  Double_t beamuncertainty=3;//mm
  Int_t whichmethod[2]={2,3},whichscan[2]={0,5};
  Int_t Nbofmethod,Nbofscan;
  Nbofmethod=whichmethod[1]-whichmethod[0]+1;
  Nbofscan=whichscan[1]-whichscan[0]+1;
  
  Double_t resoof2rows[Nbofmethod][Nbofscan];
  for(Int_t scani=0;scani<6;scani++){
  	 // createsinshapedata(rootdir,txtdir,scani);
  	 // createfitpara(txtdir,plotdir,scani);
  	 for(Int_t methodid=2;methodid<5;methodid++)
  	 	resoof2rows[methodid-whichmethod[0]][scani-whichscan[0]]=correction(rootdir,"",txtdir,methodid,scani);
  }

  
  plotpara p1;
  Double_t towerid[Nbofscan];
  for(Int_t scani=0;scani<Nbofscan;scani++) towerid[scani]=1+scani*0.2;
  vector<Double_t*> vecmergetowerid,vecmergereso;
  vector<Int_t> vecmergeNbofpoint;

  Double_t tmpresoarray[Nbofscan];
  for(Int_t methodid=0;methodid<Nbofmethod;methodid++){
	 Double_t* tmpresoarray=new Double_t[Nbofscan];
  	 for(Int_t scani=0;scani<Nbofscan;scani++)
		tmpresoarray[scani]=sqrt(pow(resoof2rows[methodid][scani]*10,2)-pow(beamuncertainty,2));		
	 vecmergereso.push_back(tmpresoarray);
	 vecmergetowerid.push_back(towerid);
  	 vecmergeNbofpoint.push_back(Nbofscan);
  	 p1.legendname.push_back("1D Correction M"+TString::Format("%d",methodid+whichmethod[0]-1));
  }


  Double_t slewreso[Nbofscan];
  for(Int_t scani=0;scani<Nbofscan;scani++)
  	 slewreso[scani]=sqrt(pow(slewing(rootdir,plotdir,txtdir,scani+whichscan[0])*10,2)-pow(beamuncertainty,2));

  vecmergereso.push_back(slewreso);
  vecmergetowerid.push_back(towerid);
  vecmergeNbofpoint.push_back(Nbofscan);
  p1.legendname.push_back("2D Correction");

  NNmodeldir="../../data/dubnann/tensorflow/CNNmodelpred"+CNNmodelid+"/";
  Double_t NNreso[Nbofscan];
  for(Int_t scani=0;scani<Nbofscan;scani++){
  	 NNreso[scani]=sqrt(pow(analysisNN(NNmodeldir,NNplotdir,scani+whichscan[0])*10,2)-pow(beamuncertainty,2)); //NNplotdir
  }
  vecmergereso.push_back(NNreso);
  vecmergetowerid.push_back(towerid);
  vecmergeNbofpoint.push_back(Nbofscan);
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
  p1.xname="Energy [GeV]";
  p1.yname[0]="Y Position Resolution [mm]";
  p1.SetY1range(2,9);
  p1.SetXrange(0.7,2.3);
  p1.textcontent="ECal: Energy Scan";
  p1.plotname=plotdir+"resomaprow";
  DrawNGraph(vecmergetowerid,vecmergereso,vecmergereso.size(),vecmergeNbofpoint,p1);
 
  ofstream outstd(txtdir+"summaryofresoCNN"+CNNmodelid+".txt");
  outstd<<"scanid M1 M2 2D CNN\n";
  for(Int_t k=0;k<Nbofscan;k++) outstd<<k+whichscan[0]<<" "<<vecmergereso[0][k]<<" "<<vecmergereso[1][k]<<" "<<vecmergereso[2][k]<<" "<<vecmergereso[3][k]<<"\n";
  

}


vector<Double_t*> readresofromfile(Int_t Nbofscan,TString CNNmodelid){
  vector<Double_t*> vecreso1;
  Double_t* reso1=new Double_t[Nbofscan];
  Double_t* reso2=new Double_t[Nbofscan];
  Double_t* resoa2D=new Double_t[Nbofscan];
  Double_t* resonn=new Double_t[Nbofscan];

  ifstream infile(txtdir+"summaryofresoCNN"+CNNmodelid+".txt", ios::in);
  TString tmpstr;
  Double_t tmpdouble;
  infile>>tmpstr>>tmpstr>>tmpstr>>tmpstr>>tmpstr;
  for(Int_t scani=0;scani<Nbofscan;scani++){
	 infile>>tmpdouble;
	 infile>>tmpdouble; reso1[scani]=tmpdouble;
	 infile>>tmpdouble; reso2[scani]=tmpdouble;
	 infile>>tmpdouble; resoa2D[scani]=tmpdouble;
	 infile>>tmpdouble; resonn[scani]=tmpdouble;
  }
  vecreso1.push_back(reso1);
  vecreso1.push_back(reso2);
  vecreso1.push_back(resoa2D);
  vecreso1.push_back(resonn);
  return vecreso1;
}


void measureslewing(TString CNNmodelid){
  Int_t whichmethod[2]={2,3},whichscan[2]={0,5};
  Int_t Nbofmethod,Nbofscan;
  Nbofmethod=whichmethod[1]-whichmethod[0]+1;
  Nbofscan=whichscan[1]-whichscan[0]+1;

  plotpara p1;
  vector<Double_t*> vectowerid;
  vector<Int_t> vecNbofpoint;
  vector<Double_t*> vecreso=readresofromfile(Nbofscan,CNNmodelid);

  Double_t slewreso[Nbofscan],towerid[Nbofscan];
  for(Int_t scani=0;scani<Nbofscan;scani++) towerid[scani]=1+scani*0.2;
  
  for(Int_t scani=0;scani<Nbofscan;scani++)
  	 slewreso[scani]=sqrt(pow(slewing(rootdir,plotdir,txtdir,scani+whichscan[0])*10,2)-pow(beamuncertainty,2));
  for(Int_t scani=0;scani<Nbofscan;scani++) cout<<slewreso[scani]<<endl;
  vecreso.push_back(slewreso);
  
  for(Int_t k=0;k<vecreso.size();k++){
  	 vectowerid.push_back(towerid);
  	 vecNbofpoint.push_back(Nbofscan);
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
  p1.SetY1range(2,9);
  p1.SetXrange(0.7,2.3);
  p1.textcontent="ECal: Tower in Row 1 @Energy=1.6GeV";
  p1.plotname=plotdir+"newresomaprow1";
  DrawNGraph(vectowerid,vecreso,vecreso.size(),vecNbofpoint,p1);


  
}

void interpolationenergy(){
  TString CNNmodelid="1"; //default "1"
  Double_t beamuncertainty=3;//mm
  Int_t whichmethod[2]={2,3},whichscan[2]={0,5};
  Int_t Nbofmethod,Nbofscan;
  Nbofmethod=whichmethod[1]-whichmethod[0]+1;
  Nbofscan=whichscan[1]-whichscan[0]+1;
  
  Double_t resoof2rows[Nbofmethod][Nbofscan];
  for(Int_t scani=0;scani<6;scani++){
  	 // createsinshapedata(rootdir,txtdir,scani);
  	 // createfitpara(txtdir,plotdir,scani);
  	 for(Int_t methodid=2;methodid<5;methodid++)
  	 	resoof2rows[methodid-whichmethod[0]][scani-whichscan[0]]=correction(rootdir,"",txtdir,methodid,scani);
  }

  
  plotpara p1;
  Double_t towerid[Nbofscan];
  for(Int_t scani=0;scani<Nbofscan;scani++) towerid[scani]=1+scani*0.2;
  vector<Double_t*> vecmergetowerid,vecmergereso;
  vector<Int_t> vecmergeNbofpoint;

  Double_t tmpresoarray[Nbofscan];
  for(Int_t methodid=0;methodid<Nbofmethod;methodid++){
	 Double_t* tmpresoarray=new Double_t[Nbofscan];
  	 for(Int_t scani=0;scani<Nbofscan;scani++)
		tmpresoarray[scani]=sqrt(pow(resoof2rows[methodid][scani]*10,2)-pow(beamuncertainty,2));		
	 vecmergereso.push_back(tmpresoarray);
	 vecmergetowerid.push_back(towerid);
  	 vecmergeNbofpoint.push_back(Nbofscan);
  	 p1.legendname.push_back("1D Correction M"+TString::Format("%d",methodid+whichmethod[0]-1));
  }
  Double_t slewreso[Nbofscan];
  for(Int_t scani=0;scani<Nbofscan;scani++){
  	 slewreso[scani]=sqrt(pow(amplitudeslewing(rootdir,plotdir,txtdir,scani+whichscan[0])*10,2)-pow(beamuncertainty,2));//plotdir
  	 // cout<<"scan"<<scani<<" "<<slewreso1[scani]<<endl;
  }
  vecmergereso.push_back(slewreso);
  vecmergetowerid.push_back(towerid);
  vecmergeNbofpoint.push_back(Nbofscan);
  p1.legendname.push_back("2D Correction");

  NNmodeldir="../../data/dubnann/tensorflow/CNNmodelpred"+CNNmodelid+"/";
  Double_t NNreso[Nbofscan];
  for(Int_t scani=0;scani<Nbofscan;scani++){
  	 NNreso[scani]=sqrt(pow(analysisNN(NNmodeldir,NNplotdir,scani+whichscan[0])*10,2)-pow(beamuncertainty,2)); //NNplotdir
  }
  vecmergereso.push_back(NNreso);
  vecmergetowerid.push_back(towerid);
  vecmergeNbofpoint.push_back(Nbofscan);
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
  p1.xname="Energy [GeV]";
  p1.yname[0]="Y Position Resolution [mm]";
  p1.SetY1range(2,9);
  p1.SetXrange(0.7,2.3);
  p1.textcontent="ECal: Energy Scan";
  p1.plotname=plotdir+"resomaprow";
  DrawNGraph(vecmergetowerid,vecmergereso,vecmergereso.size(),vecmergeNbofpoint,p1);
 
  ofstream outstd(txtdir+"summaryofresoCNN"+CNNmodelid+".txt");
  outstd<<"scanid M1 M2 2D CNN\n";
  for(Int_t k=0;k<Nbofscan;k++) outstd<<k+whichscan[0]<<" "<<vecmergereso[0][k]<<" "<<vecmergereso[1][k]<<" "<<vecmergereso[2][k]<<" "<<vecmergereso[3][k]<<"\n";
  
  
}


void interpolationenergyforrow(){
 Int_t whichmethod[2]={2,3},whichscan[2]={0,5};
  Int_t Nbofmethod,Nbofscan;
  Nbofmethod=whichmethod[1]-whichmethod[0]+1;
  Nbofscan=whichscan[1]-whichscan[0]+1;
  
  Double_t resoof2rows[3][6];
  for(Int_t scani=0;scani<6;scani++){
  	 // createsinshapedata(rootdir,txtdir,scani);
  	 // createfitpara(txtdir,plotdir,scani);
  	 for(Int_t methodid=2;methodid<5;methodid++)
  	 	resoof2rows[methodid-whichmethod[0]][scani-whichscan[0]]=correction(rootdir,plotdir,txtdir,methodid,scani);
  }





  

  
//   Double_t towerid[Nbofscan],posreso[Nbofmethod][Nbofscan];
//   for(Int_t scani=0;scani<Nbofscan;scani++) towerid[scani]=scani+whichscan[0]+1;
//   for(Int_t methodid=0;methodid<Nbofmethod;methodid++){
//   	 for(Int_t scani=0;scani<Nbofscan;scani++){
//   		posreso[methodid][scani]=analysisforeverypixel(rootdir,plotdir,methodid+whichmethod[0],scani+whichscan[0])*10;
//   	 }
//   }
//   // NNmodeldir="../../data/nn/tensorflow/CNNmodelpred2/";
//   plotpara p1;
//   vector<Double_t*> vectowerid,vecreso;
//   vector<Int_t> vecNbofpoint;
//   // Double_t NNreso1[Nbofscan], NNreso2[Nbofscan];
//   // for(Int_t scani=0;scani<Nbofscan;scani++){
//   // 	 Double_t tmpreso[2];
//   // 	 analysisNN(NNmodeldir,NNplotdir,scani+whichscan[0],tmpreso); //NNplotdir
//   // 	 NNreso1[scani]=tmpreso[0]*10;
//   // 	 NNreso2[scani]=tmpreso[1]*10;
//   // 	 // cout<<"scan"<<scani<<" "<<NNreso1[scani]<<endl;
//   // }
//   // vecreso1.push_back(NNreso1);
//   // vecreso2.push_back(NNreso2);
//   // vectowerid.push_back(towerid);
//   // vecNbofpoint.push_back(Nbofscan);
//   // p1.legendname.push_back("CNN");
 
//   Double_t tmpresoarray[Nbofscan];
//   for(Int_t methodid=0;methodid<Nbofmethod;methodid++){
//   	 Double_t* tmpresoarray=new Double_t[Nbofscan];
//   	 for(Int_t scani=0;scani<Nbofscan;scani++) tmpresoarray[scani]=posreso[Nbofmethod-1-methodid][scani];
//   	 vecreso.push_back(tmpresoarray);	
//   	 vectowerid.push_back(towerid);
//   	 vecNbofpoint.push_back(Nbofscan);
//   	 p1.legendname.push_back("Correction M"+TString::Format("%d",whichmethod[1]-methodid-1));
//   }
//   Double_t slewreso[Nbofscan];
//   for(Int_t scani=0;scani<Nbofscan;scani++){
//   	 slewreso[scani]=amplitudeslewing(rootdir,plotdir,txtdir,scani+whichscan[0])*10;//plotdir
//   	 // cout<<"scan"<<scani<<" "<<slewreso1[scani]<<endl;
//   }
//   vecreso.push_back(slewreso);

//   vectowerid.push_back(towerid);
//   vecNbofpoint.push_back(Nbofscan);
//   p1.legendname.push_back("Correction M1");
//   p1.SetLegendPosition(0.15,0.65,0.48,0.9);
//   p1.xname="Tower ID";
//   p1.yname[0]="Y Position Resolution [mm]";
//   p1.SetY1range(3,12);
//   p1.SetXrange(0.2,6.8);
//   p1.textcontent="ECal: ";
//   p1.plotname=plotdir+"resomaprow";
//   DrawNGraph(vectowerid,vecreso,vecreso.size(),vecNbofpoint,p1);
//   // p1.textcontent="ECal: Tower in Row 2";
//   // p1.plotname=plotdir+"resomaprow2";
//   // DrawNGraph(vectowerid,vecreso2,Nbofmethod+1,vecNbofpoint,p1);



  
// }

// void interpolationy(){
//   // for(Int_t scani=1;scani<7;scani++){
//   // 	 // createsinshapedata(rootdir,txtdir,scani);
//   // 	 // createfitpara(txtdir,plotdir,scani);
//   // 	 for(Int_t methodid=2;methodid<5;methodid++)
//   // 		correction(rootdir,plotdir,txtdir,methodid,scani);
//   // }
//   Double_t reso[2];
//   // analysisforeverypixel(rootdir,plotdir,2,1,reso);

//   // Double_t re=analysisforeveryscan(rootdir,plotdir,2,1);
//   // analysisNN(NNmodeldir,NNplotdir,1,reso);
//   // slewing(rootdir,plotdir,txtdir,1,reso);
//   // cout<<reso[0]<<" "<<reso[1]<<endl;


  
//   Int_t whichmethod[2]={2,4},whichscan[2]={1,6};
//   Int_t Nbofmethod,Nbofscan;
//   Nbofmethod=whichmethod[1]-whichmethod[0]+1;
//   Nbofscan=whichscan[1]-whichscan[0]+1;
  
//   Double_t towerid[Nbofscan],posresorow1[Nbofmethod][Nbofscan],posresorow2[Nbofmethod][Nbofscan];
//   for(Int_t scani=0;scani<Nbofscan;scani++) towerid[scani]=scani+whichscan[0];
//   for(Int_t methodid=0;methodid<Nbofmethod;methodid++){
//   	 for(Int_t scani=0;scani<Nbofscan;scani++){
//   		Double_t tmpreso[2];
//   		analysisforeverypixel(rootdir,"",methodid+whichmethod[0],scani+whichscan[0],tmpreso);
//   		posresorow1[methodid][scani]=tmpreso[0]*10;
//   		posresorow2[methodid][scani]=tmpreso[1]*10;
//   	 }
//   }
//   NNmodeldir="../../data/nn/tensorflow/CNNmodelpred2/";
//   plotpara p1;
//   vector<Double_t*> vectowerid,vecreso1,vecreso2;
//   vector<Int_t> vecNbofpoint;
//   Double_t NNreso1[Nbofscan], NNreso2[Nbofscan];
//   for(Int_t scani=0;scani<Nbofscan;scani++){
//   	 Double_t tmpreso[2];
//   	 analysisNN(NNmodeldir,NNplotdir,scani+whichscan[0],tmpreso); //NNplotdir
//   	 NNreso1[scani]=tmpreso[0]*10;
//   	 NNreso2[scani]=tmpreso[1]*10;
//   	 // cout<<"scan"<<scani<<" "<<NNreso1[scani]<<endl;
//   }
//   vecreso1.push_back(NNreso1);
//   vecreso2.push_back(NNreso2);
//   vectowerid.push_back(towerid);
//   vecNbofpoint.push_back(Nbofscan);
//   p1.legendname.push_back("CNN");
 
//   Double_t tmpresoarray[Nbofscan];
//   for(Int_t methodid=0;methodid<Nbofmethod;methodid++){
//   	 Double_t* tmpresoarray=new Double_t[Nbofscan];
//   	 for(Int_t scani=0;scani<Nbofscan;scani++) tmpresoarray[scani]=posresorow1[Nbofmethod-1-methodid][scani];
//   	 vecreso1.push_back(tmpresoarray);
//   	 tmpresoarray=new Double_t[Nbofscan];
//   	 for(Int_t scani=0;scani<Nbofscan;scani++) tmpresoarray[scani]=posresorow2[Nbofmethod-1-methodid][scani];
//   	 vecreso2.push_back(tmpresoarray);		
//   	 vectowerid.push_back(towerid);
//   	 vecNbofpoint.push_back(Nbofscan);
//   	 p1.legendname.push_back("Correction M"+TString::Format("%d",whichmethod[1]-methodid));
//   }
//   Double_t slewreso1[Nbofscan], slewreso2[Nbofscan];
//   for(Int_t scani=0;scani<Nbofscan;scani++){
//   	 Double_t tmpreso[2];
//   	 slewing(rootdir,"",txtdir,scani+whichscan[0],tmpreso);
//   	 slewreso1[scani]=tmpreso[0]*10;
//   	 slewreso2[scani]=tmpreso[1]*10;
//   	 // cout<<"scan"<<scani<<" "<<slewreso1[scani]<<endl;
//   }
//   vecreso1.push_back(slewreso1);
//   vecreso2.push_back(slewreso2);
//   vectowerid.push_back(towerid);
//   vecNbofpoint.push_back(Nbofscan);
//   p1.legendname.push_back("Correction M1");
//   p1.SetLegendPosition(0.15,0.65,0.48,0.9);
//   p1.xname="Tower ID";
//   p1.yname[0]="Y Position Resolution [mm]";
//   p1.SetY1range(3,8);
//   p1.SetXrange(0.2,6.8);
//   p1.textcontent="ECal: Tower in Row 1";
//   p1.plotname=plotdir+"resomaprow1";
//   DrawNGraph(vectowerid,vecreso1,Nbofmethod+2,vecNbofpoint,p1);
//   p1.textcontent="ECal: Tower in Row 2";
//   p1.plotname=plotdir+"resomaprow2";
//   DrawNGraph(vectowerid,vecreso2,Nbofmethod+2,vecNbofpoint,p1);

}
