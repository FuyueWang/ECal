#include </home/ubuntu/fuyuew/mrpc/MRPCProject/plotfunctions.cpp>
void extractmean(){
  TString thisdir="tradposx/";
  TString rootdatadir="../../data/"+thisdir,txtdir="../../txt/"+thisdir,plotdir="../../plot/"+thisdir+"slewing/";

  Int_t Nbofscan=2,filerange[2]={0,49};
  Int_t Nboffile=filerange[1]-filerange[0]+1;
  
  Double_t calibratedpos[Nboffile];
  for(Int_t filei=0;filei<Nboffile;filei++)
	 calibratedpos[filei]=filei*0.2;

  Double_t xpos[6]={-2,2,6,10,14,18},residualmean[Nbofscan];
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
		if(fileid<15)
		  residualhist->Fill(((intch[0]+intch[3]+intch[6])*xpos[0]+(intch[1]+intch[4]+intch[7])*xpos[1]+(intch[2]+intch[5]+intch[8])*xpos[2])/(intch[0]+intch[1]+intch[2]+intch[3]+intch[4]+intch[5]+intch[6]+intch[7]+intch[8])-calibratedpos[fileid]);
		else if(fileid<33)
		  residualhist->Fill(((intch[0]+intch[3]+intch[6])*xpos[1]+(intch[1]+intch[4]+intch[7])*xpos[2]+(intch[2]+intch[5]+intch[8])*xpos[3])/(intch[0]+intch[1]+intch[2]+intch[3]+intch[4]+intch[5]+intch[6]+intch[7]+intch[8])-calibratedpos[fileid]);
		else
		  residualhist->Fill(((intch[0]+intch[3]+intch[6])*xpos[2]+(intch[1]+intch[4]+intch[7])*xpos[3]+(intch[2]+intch[5]+intch[8])*xpos[4])/(intch[0]+intch[1]+intch[2]+intch[3]+intch[4]+intch[5]+intch[6]+intch[7]+intch[8])-calibratedpos[fileid]);
	 }
	 residualmean[scani]=residualhist->GetMean();
  }
  ofstream outstd(txtdir+"residualmeanforscans.txt");
  outstd<<"scanid residualmean\n";
  for(Int_t scani=0;scani<Nbofscan;scani++)
	 outstd<<scani<<" "<<residualmean[scani]<<"\n";
}
