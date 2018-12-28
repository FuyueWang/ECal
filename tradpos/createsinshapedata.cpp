#include </home/ubuntu/fuyuew/mrpc/MRPCProject/plotfunctions.cpp>
void createsinshapedata(){
  TString thisdir="tradpos/";
  TString rootdatadir="../../data/"+thisdir,txtdir="../../txt/"+thisdir,plotdir="../../plot"+thisdir;

  Int_t Nbofscan=6;
  Int_t filerange[2]={0,32};
  Int_t Nboffile=filerange[1]-filerange[0]+1;

  Double_t meanmeasuredpos[Nboffile],calibratedpos[Nboffile],posresidual[Nboffile];
  TH1D* measuredposhist[Nboffile];
  for(Int_t filei=0;filei<Nboffile;filei++){
  	 measuredposhist[filei]=new TH1D("measuredhist"+TString::Format("%d",filei),"",100,-100,100);
	 calibratedpos[filei]=16-(filei+filerange[0])*0.5;
  }
  for(Int_t scani=0;scani<Nbofscan;scani++){
	 // if(scani==0) continue;
	 for(Int_t filei=0;filei<Nboffile;filei++)
		measuredposhist[filei]->Reset();
	 
	 TFile* infile=new TFile(rootdatadir+"rootdata/lwaveform"+TString::Format("%d",scani+1)+"cutLED.root");
	 TTree* intree=(TTree*)infile->Get("wavetree");
	 Int_t fileid;
	 Float_t intch[9];
	 intree->SetBranchAddress("intch",intch);
	 intree->SetBranchAddress("fileid",&fileid);
	 
	 Int_t nEntries=intree->GetEntries();
	 for(Int_t itr=0;itr<nEntries;itr++){
		intree->GetEntry(itr);
		// if(intch[3]+intch[4]+intch[5]<1/2000) continue;
		if(fileid<filerange[0]||fileid>filerange[1]) continue;
		if(fileid<15){
		  measuredposhist[fileid-filerange[0]]->Fill(((intch[0]+intch[1]+intch[2])*14+(intch[3]+intch[4]+intch[5])*10+(intch[6]+intch[7]+intch[8])*6)/(intch[0]+intch[1]+intch[2]+intch[3]+intch[4]+intch[5]+intch[6]+intch[7]+intch[8]));
		}
		else{
		  measuredposhist[fileid-filerange[0]]->Fill(((intch[0]+intch[1]+intch[2])*10+(intch[3]+intch[4]+intch[5])*6+(intch[6]+intch[7]+intch[8])*2)/(intch[0]+intch[1]+intch[2]+intch[3]+intch[4]+intch[5]+intch[6]+intch[7]+intch[8]));
		}
	 }
	 for(Int_t filei=0;filei<Nboffile;filei++){
		meanmeasuredpos[filei]=measuredposhist[filei]->GetMean();
		posresidual[filei]=meanmeasuredpos[filei]-calibratedpos[filei];
		// cout<<filei<<" "<<meanmeasuredpos[filei]<<" "<<posresidual[filei]<<endl;
	 }
	 
	 ofstream outstd(txtdir+"residualposVsmeasurescan"+TString::Format("%d",scani+1)+".txt");
	 outstd<<"measuredpos residual\n";
	 for(Int_t filei=0;filei<Nboffile;filei++) outstd<<meanmeasuredpos[filei]<<" "<<posresidual[filei]<<"\n";
	 plotpara p1;
	 p1.xname="Measured Position [cm]";
	 p1.yname[0]="Measured-Calibrated Position [cm]";
	 p1.textcontent="ECal: Interpolation correction";
	 p1.withline=true;
	 Draw1Graph(meanmeasuredpos,posresidual,Nboffile,p1);
	 
  }
}
