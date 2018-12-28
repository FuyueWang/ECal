#include </home/ubuntu/FuyueWANG/mrpc/MRPCProject/plotfunctions.cpp>

void checknorm(){
  TString rootdir="../../data/ecalpos/rootdata/",plotdir="../../plot/ecalpos/normcheck/";
  Double_t longimap[4][8];
  for(Int_t k=0;k<8;k++) longimap[0][k]=57+k;
  for(Int_t k=0;k<8;k++) longimap[1][k]=49+k;
  for(Int_t k=0;k<8;k++) longimap[2][k]=8-k;
  for(Int_t k=0;k<8;k++) longimap[3][k]=16-k;
  vector<Double_t*> vecfilex;
  vector<Int_t> vecNbofpoint;
  Double_t filex[33];
  for(Int_t fileid=0;fileid<33;fileid++) filex[fileid]=fileid;
  vecfilex.push_back(filex);vecfilex.push_back(filex);vecfilex.push_back(filex);vecfilex.push_back(filex);
  
  vecNbofpoint.push_back(33);vecNbofpoint.push_back(33);vecNbofpoint.push_back(33);vecNbofpoint.push_back(33);
  for(Int_t scani=0;scani<6;scani++){
	 vector<Double_t*> veccenterpixel;

	 TFile *infile = new TFile(rootdir+"lwaveform"+TString::Format("%d",scani+1)+".root");
	 TTree* intree = (TTree*)infile->Get("wavetree");

	 Double_t centerpixel0[33],centerpixel1[33],centerpixel2[33],centerpixel3[33];
	 for(Int_t fileid=0;fileid<33;fileid++){
		intree->Draw("intch[1]","fileid=="+TString::Format("%d",fileid));
		centerpixel0[fileid]=intree->GetHistogram()->GetMean();
		intree->Draw("intch[4]","fileid=="+TString::Format("%d",fileid));
		centerpixel1[fileid]=intree->GetHistogram()->GetMean();
		intree->Draw("intch[7]","fileid=="+TString::Format("%d",fileid));
		centerpixel2[fileid]=intree->GetHistogram()->GetMean();
		intree->Draw("intch[10]","fileid=="+TString::Format("%d",fileid));
		centerpixel3[fileid]=intree->GetHistogram()->GetMean();
		// cout<<fileid<<" "<<centerpixel0[fileid]<<" "<<centerpixel0[fileid]<<" "<<centerpixel0[fileid]<<" "<<centerpixel0[fileid]<<endl;
	 }
	 veccenterpixel.push_back(centerpixel0);
	 veccenterpixel.push_back(centerpixel1);
	 veccenterpixel.push_back(centerpixel2);
	 veccenterpixel.push_back(centerpixel3);
	 
	 
	 plotpara p1;
	 p1.legendname.push_back(TString::Format("%.0f",longimap[0][scani+1]));
	 p1.legendname.push_back(TString::Format("%.0f",longimap[1][scani+1]));
	 p1.legendname.push_back(TString::Format("%.0f",longimap[2][scani+1]));
	 p1.legendname.push_back(TString::Format("%.0f",longimap[3][scani+1]));
	 p1.plotname=plotdir+"scan"+TString::Format("%d",scani);
	 p1.format=".png";
	 DrawNGraph(vecfilex,veccenterpixel,4,vecNbofpoint,p1);
  }
}
