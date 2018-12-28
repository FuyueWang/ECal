void writerootdata(){
  TString thisdir="ecalpos/";
  TString datadir="../../data/"+thisdir;

  Double_t posy,pixelvalue[9];
  Int_t centerTowerId,Nbof0pixel;
  TFile* outfile=new TFile(datadir+"rootdata/scanfrom60.root","recreate");
  TTree* outtree=new TTree("scantree","scantree");
  outtree->Branch("posy",&posy);
  outtree->Branch("pixelvalue",pixelvalue,"pixelvalue[9]/F");
  outtree->Branch("centerTowerId",&centerTowerId);
  outtree->Branch("Nbof0pixel",&Nbof0pixel);
	 
  Int_t Nbofentries=918440;
  TString tmpstr;
  Double_t tmpdouble;
  ifstream infile(datadir+"dfdata/scanfrom60Intdfblank.csv", ios::in);
  cout<<datadir+"dfdata/scanfrom60Intdfblank.csv"<<endl;
  for(Int_t k=0;k<12;k++)
	 infile>>tmpstr;
  for(Int_t itr=0;itr<Nbofentries;itr++){
	 infile>>tmpstr;
	 for(Int_t k=0;k<9;k++){
		infile>>tmpdouble;
		pixelvalue[k]=tmpdouble;
	 }
	 infile>>centerTowerId>>Nbof0pixel>>posy;
	 // cout<<pixelvalue[0]<<" "<<pixelvalue[1]<<" "<<pixelvalue[8]<<" "<<centerTowerId<<" "<<Nbof0pixel<<" "<<posy<<endl;
	 outtree->Fill();
  }
  outfile->cd();
  outtree->Write();
  outfile->Close();
}
