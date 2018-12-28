#include </home/ubuntu/FuyueWANG/mrpc/MRPCProject/plotfunctions.cpp>
void exploreNN(){
  
  TString thisdir="ecalpos/";
  TString datadir="../../data/"+thisdir,plotdir="../../plot/"+thisdir,txtdir="../../txt/"+thisdir;


  TH2D* hist=new TH2D("inter","",100,-1.7,1.7,20,-1.7,1.7); 
  Float_t posy,MLP;
  TFile* infile = new TFile(datadir+"rootdata/TMVAReg1.root");
  TDirectory* dir = gFile->GetDirectory("dataset");
  TTree* intree;
  dir->GetObject("TestTree", intree);

  intree->SetBranchAddress("posy",&posy);
  intree->SetBranchAddress("MLP",&MLP);

  Int_t nEntries = intree->GetEntries();
  for(Int_t itr=0;itr<nEntries;itr++){
	 intree->GetEntry(itr);
	 hist->Fill(posy,MLP);
  }

  hist->Draw("colz");
  
}
