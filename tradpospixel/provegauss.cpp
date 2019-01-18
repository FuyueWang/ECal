#include </home/ubuntu/fuyuew/mrpc/MRPCProject/plotfunctions.cpp>
void provegauss(){
  TString thisdir="tradpos/";
  TString plotdir="../../plot/"+thisdir;
  Int_t Nbofposi=40;
  Double_t mean[Nbofposi],estimatedmean[Nbofposi],sigma=1,startpos=-4;
  for(Int_t posi=0;posi<Nbofposi;posi++){
	 mean[posi]=startpos+0.2*posi;
	 Int_t pixelsize=4;
	 TH1D* value=new TH1D("valuehist","",1000,-12,12);
	 for(Int_t k=0;k<1000000;k++){
		value->Fill(gRandom->Gaus(mean[posi],sigma));
	 }
	 if(posi==0)
		value->Draw();	
	 estimatedmean[posi]=pixelsize*(value->Integral(value->FindBin(0.5*pixelsize),value->FindBin(1.5*pixelsize))-value->Integral(value->FindBin(-1.5*pixelsize),value->FindBin(-0.5*pixelsize)))/value->Integral()-mean[posi];
  }
  plotpara p1;
  p1.plotname=plotdir+"theorygauss";
  p1.xname="Truth Position";
  p1.yname[0]="Estimated - Truth Position";
  p1.textcontent="ECal: theoratically obtained from Gauss(0,1)";
  p1.titleoffsety[0]=1.3;
  p1.SetY1range(-1,1);
  Draw1Graph(mean,estimatedmean,Nbofposi,p1);
  // new TCanvas();
  // //TF1* f1=new TF1("f1","x",startpos,Nbofposi);
  // TF1* f1=new TF1("f1","0",startpos,Nbofposi);
  // TGraph* gr=new TGraph(Nbofposi,mean,estimatedmean);
  // gr->SetMarkerStyle(21);
  // gr->Draw("AP");
  // f1->SetLineColor(2);
  // f1->Draw("same");
  // //cout<<estimatedmean<<endl;
}
