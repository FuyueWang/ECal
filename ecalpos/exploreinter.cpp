#include </home/ubuntu/FuyueWANG/mrpc/MRPCProject/plotfunctions.cpp>
void exploreinter(){
  
  TString thisdir="ecalpos/";
  TString datadir="../../data/"+thisdir,plotdir="../../plot/"+thisdir,txtdir="../../txt/"+thisdir;


  TH2D* hist=new TH2D("inter","",100,-1.7,1.7,100,-3.7,3.7); 
  Float_t posy,intposy;
  TFile* infile = new TFile(datadir+"rootdata/train1.root");
  TTree* intree = (TTree*)infile->Get("traintree");

  intree->SetBranchAddress("posy",&posy);
  intree->SetBranchAddress("intposy",&intposy);

  Int_t nEntries = intree->GetEntries();
  for(Int_t itr=0;itr<nEntries;itr++){
	 intree->GetEntry(itr);
	 hist->Fill(posy,intposy);
  }

  hist->Draw();
  
}
