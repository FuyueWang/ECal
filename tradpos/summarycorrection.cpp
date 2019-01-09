#include </home/ubuntu/fuyuew/mrpc/MRPCProject/plotfunctions.cpp>
void summarycorrection(){
  TString thisdir="tradpos/";
  TString rootdatadir="../../data/"+thisdir,txtdir="../../txt/"+thisdir,plotdir="../../plot/"+thisdir;

  Double_t posscan1[6]={6.351,5.416,5.772,5.922,5.143,4.818};
  Double_t posscan2[6]={6.295,5.372,5.751,5.923,5.081,4.832};
  Double_t posscan3[6]={6.442,5.343,5.817,5.918,5.351,4.855};
  Double_t methodid[6]={0,1,2,3,4,5};
  vector<Double_t*> plotx,ploty;
  vector<Int_t> vecNbofpoints;
  plotx.push_back(methodid);
  plotx.push_back(methodid);
  plotx.push_back(methodid);
  ploty.push_back(posscan1);
  ploty.push_back(posscan2);
  ploty.push_back(posscan3);
  vecNbofpoints.push_back(6);
  vecNbofpoints.push_back(6);
  vecNbofpoints.push_back(6);
  
  plotpara p1;
  p1.yname[0]="Position Resolution [mm]";
  p1.textcontent="ECal: resolution with different correction method";
  p1.legendname.push_back("Scan from: 58");
  p1.legendname.push_back("Scan from: 59");
  p1.legendname.push_back("Scan from: 60");
  p1.plotname=plotdir+"correctionsummary";
  p1.SetY1range(3,13);
  p1.withline=true;
  DrawNGraph(plotx,ploty,3,vecNbofpoints,p1);
}
