#include </home/ubuntu/fuyuew/mrpc/MRPCProject/plotfunctions.cpp>

void drawnntest(){
  TString thisdir="nnx/";
  TString rootdatadir="../../data/"+thisdir,txtdir="../../txt/"+thisdir,plotdir="../../plot/"+thisdir;

  
  Int_t scani=0;//{1,2,3}
  Double_t Nsigma=2.5;
  TString model="CNNmodels"+TString::Format("%d",scani),dir="x";
 
  TH1D *residual=new TH1D("residual","",60,-3.5,4.5);
  TH1D *resovspos=new TH1D("resopos","",18,9.9,13.5);
  Double_t meanresoarray[18],meanresiarray[18],pos[18];
  TH1D* meanreso[18];
  for(Int_t k=0;k<18;k++) meanreso[k]=new TH1D("meanreso"+TString::Format("%d",k),"",100,-3.5,4.5);
  ifstream infile(rootdatadir+"tensorflow/"+model+"/valpred.csv", ios::in);
  TString tmpstr;
  Double_t tmpdouble1,tmpdouble2;
  Int_t tmpint;
  infile>>tmpstr>>tmpstr;

  while(!infile.eof()){
	 infile>>tmpdouble1; 
	 infile>>tmpdouble1; 
	 infile>>tmpdouble2;
	 residual->Fill(tmpdouble1-tmpdouble2);
	 // cout<<tmpdouble1<<" "<<tmpdouble2<<endl;
	 resovspos->Fill(tmpdouble1);
	 meanreso[resovspos->FindBin(tmpdouble1)-1]->Fill(tmpdouble1-tmpdouble2);
  }
  infile.close();

  plotpara p2;
  p2.xname="Measured-Truth Position [cm]";
  p2.yname[0]="Entries";
  p2.leftmargin=0.17;
  p2.rightmargin=0.2-p2.leftmargin;
  p2.titleoffsety[0]=2;
  p2.textcontent="ECal: "+dir+" position residual of "+model;
  p2.SetStatsrange(0.62,0.56,0.97,0.94);
  p2.minortext="Gauss Fit "+TString::Format("%.1f",Nsigma)+" #sigma";
  p2.SetMinorTextPosition(0.65,0.5);
  p2.plotname=plotdir+model+"resihist"+dir;
  TF1 *f1 = new TF1("f1","gaus");
  Double_t mean = residual->GetMean();
  Double_t sigma = residual->GetRMS();
  Double_t gausspara[3];
  f1->SetRange(mean-Nsigma*sigma, mean+Nsigma*sigma); 
  residual->Fit("f1","QR");
  f1->GetParameters(&gausspara[0]);  
  // 2nd fit      
  f1->SetRange(gausspara[1]-Nsigma*gausspara[2], gausspara[1]+Nsigma*gausspara[2]);  
  residual->Fit("f1","QR");                                     
  f1->GetParameters(&gausspara[0]);                                  
  Draw1HistogramWithTF1(residual,f1,p2);

 

  // for(Int_t k=0;k<18;k++){
  // 	 meanresoarray[k]=meanreso[k]->GetRMS();
  // 	 meanresiarray[k]=meanreso[k]->GetMean();
  // 	 pos[k]=k*0.2;
  // 	 TF1 *ff1 = new TF1("ff1","gaus");
  // 	 Double_t fmean = meanreso[k]->GetMean();
  // 	 Double_t fsigma = meanreso[k]->GetRMS();
  // 	 Double_t fgausspara[3];
  // 	 ff1->SetRange(fmean-Nsigma*fsigma, fmean+Nsigma*fsigma); 
  // 	 meanreso[k]->Fit("ff1","QR");
  // 	 ff1->GetParameters(&fgausspara[0]);  
  // 	 // 2nd fit      
  // 	 ff1->SetRange(fgausspara[1]-Nsigma*fgausspara[2], fgausspara[1]+Nsigma*fgausspara[2]);  
  // 	 meanreso[k]->Fit("ff1","QR");                                     
  // 	 ff1->GetParameters(&fgausspara[0]); 
  // 	 meanresoarray[k]=fgausspara[2];	 
  // }
  // plotpara p1;
  // p1.legendname.push_back("resolution");
  // p1.legendname.push_back("mean");
  // p1.xname="position [cm]";
  // p1.yname[0]="Position Resolution [cm]";
  // p1.yname[1]="Position residual mean [cm]";
  // p1.SetY1range(0.2,0.7);
  // p1.SetY2range(-1,1);
  // p1.SetXrange(-1,10);
  // DrawGraphWith2Axis(pos,meanresoarray,pos,meanresiarray,18,18,p1);
  
}
