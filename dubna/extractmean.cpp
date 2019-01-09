#include </home/ubuntu/fuyuew/mrpc/MRPCProject/plotfunctions.cpp>
void extractmean(){
  TString thisdir="dubna/";
  TString rootdatadir="../../data/"+thisdir,txtdir="../../txt/"+thisdir,plotdir="../../plot/"+thisdir+"slewing/";

  Int_t Nbofscan=6,filerange[2]={0,10};
  Int_t Nboffile=filerange[1]-filerange[0]+1;
  
  Double_t calibratedpos[11];
  for(Int_t filei=0;filei<11;filei++)
	 calibratedpos[filei]=16-filei*0.5;

  Double_t ypos[4]={14,10,6,2},residualmean[Nbofscan];
  TH1D* residualhist=new TH1D("residual","",500,-100,100);
  for(Int_t scani=0;scani<Nbofscan;scani++){
	 residualhist->Reset();
	 TFile* infile=new TFile(rootdatadir+"rootdata/lwaveform"+TString::Format("%d",scani)+"energyless.root");
	 TTree* intree=(TTree*)infile->Get("wavetree");
	 Int_t fileid;
	 Float_t intch[9];
	 intree->SetBranchAddress("intch",intch);
	 intree->SetBranchAddress("fileid",&fileid);
	 
	 Int_t nEntries=intree->GetEntries();
	 for(Int_t itr=0;itr<nEntries;itr++){
		intree->GetEntry(itr);
		if(fileid<filerange[0]||fileid>filerange[1]) continue;
		if(fileid<7)
		  residualhist->Fill(((intch[0]+intch[1]+intch[2])*ypos[0]+(intch[3]+intch[4]+intch[5])*ypos[1]+(intch[6]+intch[7]+intch[8])*ypos[2])/(intch[0]+intch[1]+intch[2]+intch[3]+intch[4]+intch[5]+intch[6]+intch[7]+intch[8])-calibratedpos[fileid]);
		else
		  residualhist->Fill(((intch[0]+intch[1]+intch[2])*ypos[1]+(intch[3]+intch[4]+intch[5])*ypos[2]+(intch[6]+intch[7]+intch[8])*ypos[3])/(intch[0]+intch[1]+intch[2]+intch[3]+intch[4]+intch[5]+intch[6]+intch[7]+intch[8])-calibratedpos[fileid]);
	 }
	 residualmean[scani]=residualhist->GetMean();
  }
  ofstream outstd(txtdir+"residualmeanforscans.txt");
  outstd<<"scanid residualmean\n";
  for(Int_t scani=0;scani<Nbofscan;scani++)
	 outstd<<scani<<" "<<residualmean[scani]<<"\n";
}
