#include </home/ubuntu/FuyueWANG/mrpc/MRPCProject/plotfunctions.cpp>
void plotresidual(){
  TString outplotdir="../../plot/ecalpos/";
  Float_t posy,spec1,MLP;
  TFile * infile = new TFile("TMVAReg1.root");
  TDirectory* dir = gFile->GetDirectory("dataset");
  TTree* intree;
  dir->GetObject("TestTree", intree);
  intree->SetBranchAddress("posy",&posy);
  intree->SetBranchAddress("spec1",&spec1);
  intree->SetBranchAddress("MLP",&MLP); 
  // intree->Draw("MLP");
  TH1D* residualhist[2];
  residualhist[0]=new TH1D("Interpolation","",60,-2.5,2.5);
  residualhist[1]=new TH1D("NN","",60,-2.5,2.5);
  
  Int_t nEntries=intree->GetEntries();
  for(Int_t itr=0;itr<nEntries;itr++){
  	 intree->GetEntry(itr);
  	 residualhist[0]->Fill(spec1-posy);
  	 residualhist[1]->Fill(MLP-posy);
  }

  plotpara p1;
  p1.leftmargin=0.16;
  p1.rightmargin=0.2-p1.leftmargin;
  p1.titleoffsety[0]=1.95;
  p1.SetY1range(0,35000);//23000
  p1.SetStatsrange(0.68,0.75,0.96,0.94);
  p1.xname="Residual [cm]";
  p1.yname[0]="Counts";
  p1.textcontent="ECal: Position Resolution";
  p1.plotname=outplotdir+"residual";
  // DrawNHistogramWithStats(residualhist,2,p1);
  Draw2HistogramWithStats(residualhist,2,p1);
	 
}
