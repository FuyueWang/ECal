#include </home/ubuntu/fuyuew/mrpc/MRPCProject/plotfunctions.cpp>
void drawvisualpoint(){
  TString thisdir="dubna/";
  TString rootdatadir="../../data/"+thisdir,txtdir="../../txt/"+thisdir,plotdir="../../plot/"+thisdir;

  Int_t Nbofscan=6,Nboffile=11;
  TH2D* integralhist[Nbofscan][Nboffile];

  for(Int_t scani=0;scani<Nbofscan;scani++){
	 for(Int_t filei=0;filei<Nboffile;filei++)
		integralhist[scani][filei]=new TH2D("int"+TString::Format("%d%d",scani,filei),"",3,0,3,4,0,4);
	 TFile* inrootfile=new TFile(rootdatadir+"rootdata/lwaveform"+TString::Format("%d",scani)+"energy3by4.root");
	 TTree* intree=(TTree*)inrootfile->Get("wavetree");
	 Int_t fileid;
	 Float_t intch[12];
	 intree->SetBranchAddress("intch",intch);
	 intree->SetBranchAddress("fileid",&fileid);
	 Int_t nEntries=intree->GetEntries();
	 for(Int_t itr=0;itr<nEntries;itr++){
		intree->GetEntry(itr);
		for(Int_t k=0;k<12;k++)
		  integralhist[scani][fileid]->SetBinContent(k%3+1,4-k/3,integralhist[scani][fileid]->GetBinContent(k%3+1,4-k/3)+intch[k]);
	 }
  
	 TCanvas *c1 = new TCanvas("c1","Plot",0,0,780,600);
	 c1->Divide(4,3);
	 gStyle->SetOptStat(0);	
	 for(Int_t k=0;k<Nboffile;k++){
	 	c1->cd(k+1);
	 	integralhist[scani][k]->Draw("colz");
	 }
	 c1->SaveAs(plotdir+"integral2Dscan"+TString::Format("%d",scani)+".pdf");
  }


  // Int_t whichscan=1,whichfile=8;
  // plotpara p1;
  // p1.leftmargin=0.07;
  // p1.rightmargin=0.2-p1.leftmargin;
  // p1.bottommargin=0.05;
  // p1.canvassize[0]=500;
  // p1.textcontent="ECal: scan"+TString::Format("%d",whichscan+1)+", file ID:"+TString::Format("%d",whichfile);
  // p1.plotname=plotdir+"integral2d"+TString::Format("%d%d",whichscan,whichfile);
  // Draw1TH2D(integralhist[whichscan][whichfile],p1);
  
  // whichfile=15;
  // p1.textcontent="ECal: scan"+TString::Format("%d",whichscan+1)+", file ID:"+TString::Format("%d",whichfile);
  // p1.plotname=plotdir+"integral2d"+TString::Format("%d%d",whichscan,whichfile);
  // Draw1TH2D(integralhist[whichscan][whichfile],p1);
	 
}
