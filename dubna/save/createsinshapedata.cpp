#include </home/ubuntu/fuyuew/mrpc/MRPCProject/plotfunctions.cpp>
void createsinshapedata(){
  TString thisdir="dubna/";
  TString rootdatadir="../../data/"+thisdir,txtdir="../../txt/"+thisdir,plotdir="../../plot"+thisdir;

  Int_t Nbofscan=6;
  Int_t filerange[2]={0,10};
  Int_t Nboffile=filerange[1]-filerange[0]+1;

  Double_t ypos[4]={14,10,6,2};
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
	 
	 TFile* infile=new TFile(rootdatadir+"rootdata/lwaveform"+TString::Format("%d",scani)+"energy.root");
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
		if(fileid<7){
		  measuredposhist[fileid-filerange[0]]->Fill(((intch[0]+intch[1]+intch[2])*ypos[0]+(intch[3]+intch[4]+intch[5])*ypos[1]+(intch[6]+intch[7]+intch[8])*ypos[2])/(intch[0]+intch[1]+intch[2]+intch[3]+intch[4]+intch[5]+intch[6]+intch[7]+intch[8]));
		}
		else{
		  measuredposhist[fileid-filerange[0]]->Fill(((intch[0]+intch[1]+intch[2])*ypos[1]+(intch[3]+intch[4]+intch[5])*ypos[2]+(intch[6]+intch[7]+intch[8])*ypos[3])/(intch[0]+intch[1]+intch[2]+intch[3]+intch[4]+intch[5]+intch[6]+intch[7]+intch[8]));
		}
	 }
	 for(Int_t filei=0;filei<Nboffile;filei++){
		meanmeasuredpos[filei]=measuredposhist[filei]->GetMean();
		posresidual[filei]=meanmeasuredpos[filei]-calibratedpos[filei];
		cout<<filei<<" "<<meanmeasuredpos[filei]<<" "<<posresidual[filei]<<" "<<measuredposhist[filei]->GetRMS()<<endl;
	 }

	 Double_t mean=0;
	 for(Int_t filei=0;filei<Nboffile;filei++)
		mean+=posresidual[filei];
	 mean=mean/Nboffile;
	 ofstream outstd(txtdir+"residualposVsmeasurescan"+TString::Format("%d",scani)+".txt");
	 outstd<<"measuredpos residual "<<mean<<"\n";
	 for(Int_t filei=0;filei<Nboffile;filei++) outstd<<meanmeasuredpos[filei]<<" "<<posresidual[filei]-mean<<"\n";
	 plotpara p1;
	 p1.xname="Measured Position [cm]";
	 p1.yname[0]="Measured-Calibrated Position [cm]";
	 p1.textcontent="ECal: Interpolation correction";
	 p1.withline=true;
	 Draw1Graph(meanmeasuredpos,posresidual,Nboffile,p1);
	 
  }
}
