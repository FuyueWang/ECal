#include </home/ubuntu/fuyuew/mrpc/MRPCProject/plotfunctions.cpp>

void drawnntest(){
  TString thisdir="nn/";
  TString rootdatadir="../../data/"+thisdir,txtdir="../../txt/"+thisdir,plotdir="../../plot/"+thisdir;

  
  Int_t Nsigma=3,scani=1;
  TString model="DNNmodels"+TString::Format("%d",scani);
 
  TH1D *residual=new TH1D("residual","",60,-3.5,4.5);
  // TH1D *residual=new TH1D("residual","",70,-3.5,4.5);
  ifstream infile(rootdatadir+"tensorflow/"+model+"/testpred1.csv", ios::in);
  TString tmpstr;
  Double_t tmpdouble1,tmpdouble2;
  Int_t tmpint;
  infile>>tmpstr>>tmpstr;

  while(!infile.eof()){
	 infile>>tmpdouble1; 
	 infile>>tmpdouble2;
	 residual->Fill(tmpdouble1-tmpdouble2);
  }
  infile.close();

  plotpara p2;
  p2.xname="Measured-Truth Position [cm]";
  p2.yname[0]="Entries";
  p2.leftmargin=0.17;
  p2.rightmargin=0.2-p2.leftmargin;
  p2.titleoffsety[0]=2;
  p2.textcontent="ECal: position residual of "+model;
  p2.SetStatsrange(0.62,0.56,0.97,0.94);
  p2.plotname=plotdir+model+"scan"+TString::Format("%d",scani)+"resihist";
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

  
}
