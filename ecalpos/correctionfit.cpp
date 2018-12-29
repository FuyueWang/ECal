void correctionfit(){
  TString rootdatadir;

  Int_t Nbofscan=6;
  Int_t filerange[2]={8,22};
  Int_t Nboffile=filerange[1]-filerange[0]+1;

  // TH1D* measuredposhist[scanid];
  // for(Int_t filei=0;filei<Nboffile;filei++){
  // 	 measuredposhist=new TH1D

  
  for(Int_t scanid=0;scanid<Nbofscan;scanid++){
	 Double_t meanmeasuredpos[Nboffile],Nbofpointsperfile[Nboffile],calibratedpos[Nboffile],posresidual[Nboffile];
	 for(Int_t filei=0;filei<Nboffile;filei++){
		meanmeasuredpos[filei]=0;
		Nbofpointsperfile[filei]=0;
		calibratedpos[filei]=16-(filei+filerange[0])*0.5;
	 }
	 TFile* infile=new TFile(rootdatadir+"lwaveform"+TString::Format("%d",scanid+1)+"cutLED.root");
	 TTree* intree=(TTree*)infile->Get("wavetree");
	 Int_t fileid;
	 Float_t intch[9];
	 intree->SetBranchAddress("intch",intch);
	 intree->SetBranchAddress("fileid",&fileid);
	 
	 Int_t nEntries=intree->GetEntries();
	 for(Int_t itr=0;itr<nEntries;itr++){
		intree->GetEntry(itr);
		if(fileid<15){
		  meanmeasuredpos[fileid-filerange[0]]+=((intch[0]+intch[1]+intch[2])*14+(intch[3]+intch[4]+intch[5])*10+(intch[6]+intch[7]+intch[8])*6)/(intch[0]+intch[1]+intch[2]+intch[3]+intch[4]+intch[5]+intch[6]+intch[7]+intch[8]);
		  Nbofpointsperfile[fileid-filerange[0]]+=1;
		}
		else{
		  meanmeasuredpos[fileid-filerange[0]]+=((intch[0]+intch[1]+intch[2])*10+(intch[3]+intch[4]+intch[5])*6+(intch[6]+intch[7]+intch[8])*2)/(intch[0]+intch[1]+intch[2]+intch[3]+intch[4]+intch[5]+intch[6]+intch[7]+intch[8]);
		  Nbofpointsperfile[fileid-filerange[0]]+=1;
		}
	 }

	 for(Int_t filei=0;filei<Nboffile;filei++){
		meanmeasuredpos[filei]=meanmeasuredpos[filei]/Nbofpointsperfile[filei];
		posresidual[filei]=meanmeasuredpos[filei]-calibratedpos[filei];
	 }
	 ofstream outstd(outtxtdir+"threshodintot"+TString::Format("%.0f",threinindq)+".txt");
  outstd<<"thre="<<threinindq<<"fC\n";
	 
}
