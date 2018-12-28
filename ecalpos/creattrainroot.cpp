void creattrainroot(){
  TString thisdir="ecalpos/";
  TString rootdata="../../data/"+thisdir+"rootdata/",plotdir="../../plot/"+thisdir,txtdir="../../txt/"+thisdir;
  Int_t Nbofscan=6;
  for(Int_t scani=0;scani<Nbofscan;scani++){
	 Float_t ch[9],posy;
	 TFile *outfile = new TFile(rootdata+"linttraincut"+TString::Format("%d",scani+1)+".root","recreate");
	 TTree* outtree = new TTree("inttree","inttree");
	 outtree->Branch("ch",ch,"ch[12]/F");
	 outtree->Branch("posy",&posy,"posy/F");
	 TFile * infile = new TFile(rootdata+"lwaveform"+TString::Format("%d",scani+1)+".root");
	 TTree* intree = (TTree*)infile->Get("wavetree");
	 Float_t intch[12];
	 Int_t fileid;
	 intree->SetBranchAddress("intch",intch);
	 intree->SetBranchAddress("fileid",&fileid);

	 Int_t nEntries=intree->GetEntries();
	 for(Int_t itr=0;itr<nEntries;itr++){
		intree->GetEntry(itr);
		if(fileid<8||fileid>21||fileid==15) continue;
		if(fileid<15){
		  if((intch[0]+intch[1]+intch[2])<1./2000||(intch[0]+intch[1]+intch[2])>1.8) continue;
		  if((intch[3]+intch[4]+intch[5])<1./20) continue;
		  if((intch[6]+intch[7]+intch[8])<1./2000||(intch[6]+intch[7]+intch[8])>1.8) continue;
				  
		  for(Int_t k=0;k<9;k++) ch[k]=intch[k];
		  posy=1.5-fileid%8*0.5;
		}
		else{
		  if((intch[3]+intch[4]+intch[5])<1./2000||(intch[3]+intch[4]+intch[5])>1.8) continue;
		  if((intch[6]+intch[7]+intch[8])<1./20) continue;
		  if((intch[9]+intch[10]+intch[11])<1./2000||(intch[9]+intch[10]+intch[11])>1.8) continue;

		  for(Int_t k=0;k<9;k++) ch[k]=intch[3+k];
		  posy=1.5-fileid%8*0.5;
		}
		outtree->Fill();
	 }
	 outfile->cd(); 
	 outfile->Write();
	 outfile->Close();
  }
}
