#include </home/ubuntu/fuyuew/mrpc/MRPCProject/plotfunctions.cpp>
void drawmultipixels();
void draw3by3pixels();
void drawvisualpoint(){
  // drawmultipixels();
  draw3by3pixels();
}

void draw3by3pixels(){
  TString thisdir="tradposx/";
  TString rootdatadir="../../data/"+thisdir,txtdir="../../txt/"+thisdir,plotdir="../../plot/"+thisdir;

  Int_t Nbofscan=2,Nboffile=50;
  TH2D* integralhist[Nbofscan][Nboffile];

  for(Int_t scani=0;scani<Nbofscan;scani++){
	 for(Int_t filei=0;filei<Nboffile;filei++)
		integralhist[scani][filei]=new TH2D("int"+TString::Format("%d%d",scani,filei),"",3,0,3,3,0,3);
	 TFile* inrootfile=new TFile(rootdatadir+"rootdata/lwaveform"+TString::Format("%d",scani)+"energyless.root");
	 TTree* intree=(TTree*)inrootfile->Get("wavetree");
	 Int_t fileid;
	 Float_t intch[9];
	 intree->SetBranchAddress("intch",intch);
	 intree->SetBranchAddress("fileid",&fileid);
	 Int_t nEntries=intree->GetEntries();
	 for(Int_t itr=0;itr<nEntries;itr++){
		intree->GetEntry(itr);
		for(Int_t k=0;k<9;k++)
		  integralhist[scani][fileid]->SetBinContent(k%3+1,3-k/3,integralhist[scani][fileid]->GetBinContent(k%3+1,3-k/3)+intch[k]);
	 }
  
	 TCanvas *c1 = new TCanvas("c1","Plot",0,0,780,600);
	 c1->Divide(6,9);
	 gStyle->SetOptStat(0);	
	 for(Int_t k=0;k<Nboffile;k++){
	 	c1->cd(k+1);
	 	integralhist[scani][k]->Draw("colz");
		// cout<<k<<" "<<integralhist[scani][k]->GetBinContent(1,2)<<" "<<integralhist[scani][k]->GetBinContent(2,2)<<" "<<integralhist[scani][k]->GetBinContent(3,2)<<" "<<integralhist[scani][k]->GetBinContent(4,2)<<" "<<integralhist[scani][k]->GetBinContent(5,2)<<" "<<integralhist[scani][k]->GetBinContent(6,2)<<" "<<integralhist[scani][k]->GetBinContent(7,2)<<endl;
	 }
	 c1->SaveAs(plotdir+"integral2Dscan3by3"+TString::Format("%d",scani)+".pdf");
  }
}


void drawmultipixels(){
  TString thisdir="tradposx/";
  TString rootdatadir="../../data/"+thisdir,txtdir="../../txt/"+thisdir,plotdir="../../plot/"+thisdir;

  Int_t Nbofscan=2,Nboffile=50;
  TH2D* integralhist[Nbofscan][Nboffile];

  for(Int_t scani=0;scani<Nbofscan;scani++){
	 for(Int_t filei=0;filei<Nboffile;filei++)
		integralhist[scani][filei]=new TH2D("int"+TString::Format("%d%d",scani,filei),"",6,0,6,3,0,3);
	 TFile* inrootfile=new TFile(rootdatadir+"rootdata/lwaveform"+TString::Format("%d",scani)+"energy3by6.root");
	 TTree* intree=(TTree*)inrootfile->Get("wavetree");
	 Int_t fileid;
	 Float_t intch[18];
	 intree->SetBranchAddress("intch",intch);
	 intree->SetBranchAddress("fileid",&fileid);
	 Int_t nEntries=intree->GetEntries();
	 for(Int_t itr=0;itr<nEntries;itr++){
		intree->GetEntry(itr);
		for(Int_t k=0;k<18;k++)
		  integralhist[scani][fileid]->SetBinContent(k%6+1,3-k/6,integralhist[scani][fileid]->GetBinContent(k%6+1,3-k/6)+intch[k]);
	 }
  
	 TCanvas *c1 = new TCanvas("c1","Plot",0,0,780,600);
	 c1->Divide(6,9);
	 gStyle->SetOptStat(0);	
	 for(Int_t k=0;k<Nboffile;k++){
	 	c1->cd(k+1);
	 	integralhist[scani][k]->Draw("colz");
		cout<<k<<" "<<integralhist[scani][k]->GetBinContent(1,2)<<" "<<integralhist[scani][k]->GetBinContent(2,2)<<" "<<integralhist[scani][k]->GetBinContent(3,2)<<" "<<integralhist[scani][k]->GetBinContent(4,2)<<" "<<integralhist[scani][k]->GetBinContent(5,2)<<" "<<integralhist[scani][k]->GetBinContent(6,2)<<" "<<integralhist[scani][k]->GetBinContent(7,2)<<endl;
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
