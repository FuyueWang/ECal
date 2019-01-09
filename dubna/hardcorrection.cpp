#include </home/ubuntu/fuyuew/mrpc/MRPCProject/plotfunctions.cpp>
void hardcorrection(){
  TString thisdir="dubna/";
  TString rootdatadir="../../data/"+thisdir,txtdir="../../txt/"+thisdir,plotdir="../../plot/"+thisdir;

  Int_t Nbofscan=6;
  Int_t filerange[2]={0,10},Nsigma=2;
  Int_t Nboffile=filerange[1]-filerange[0]+1;

  Double_t ypos[4]={14,10,6,2};
  Double_t preresi[Nboffile],calibratedpos[Nboffile],postresi[Nboffile],posttotalresi[Nbofscan],postfitresi[Nbofscan],energy[6]={1,1.2,1.4,1.6,1.8,2.0};
  TH1D* preresihist[Nboffile],* postresihist[Nboffile],*totalresihist;
  totalresihist=new TH1D("totalresihist","",70,-4,4);
  for(Int_t filei=0;filei<Nboffile;filei++){
  	 postresihist[filei]=new TH1D("postresihist"+TString::Format("%d",filei),"",100,-100,100);
  	 preresihist[filei]=new TH1D("preresihist"+TString::Format("%d",filei),"",100,-100,100);
	 calibratedpos[filei]=16-(filei+filerange[0])*0.5;
  }
  for(Int_t scani=0;scani<Nbofscan;scani++){
	 // if(scani==0) continue;
	 for(Int_t filei=0;filei<Nboffile;filei++){
		preresihist[filei]->Reset();
		postresihist[filei]->Reset();
	 }
	 
  	 TFile* infile=new TFile(rootdatadir+"rootdata/lwaveform"+TString::Format("%d",scani)+"energy.root");
	 TTree* intree=(TTree*)infile->Get("wavetree");
	 Int_t fileid;
	 Float_t intch[9];
	 intree->SetBranchAddress("intch",intch);
	 intree->SetBranchAddress("fileid",&fileid);
	 
	 Int_t nEntries=intree->GetEntries();
	 for(Int_t itr=0;itr<nEntries;itr++){
		intree->GetEntry(itr);
		if(fileid<7){
		  preresihist[fileid-filerange[0]]->Fill(((intch[0]+intch[1]+intch[2])*ypos[0]+(intch[3]+intch[4]+intch[5])*ypos[1]+(intch[6]+intch[7]+intch[8])*ypos[2])/(intch[0]+intch[1]+intch[2]+intch[3]+intch[4]+intch[5]+intch[6]+intch[7]+intch[8]));
		}
		else{
		  preresihist[fileid-filerange[0]]->Fill(((intch[0]+intch[1]+intch[2])*ypos[1]+(intch[3]+intch[4]+intch[5])*ypos[2]+(intch[6]+intch[7]+intch[8])*ypos[3])/(intch[0]+intch[1]+intch[2]+intch[3]+intch[4]+intch[5]+intch[6]+intch[7]+intch[8]));
		}
	 }
	 for(Int_t filei=0;filei<Nboffile;filei++)
		preresi[filei]=preresihist[filei]->GetMean();
		
	 for(Int_t itr=0;itr<nEntries;itr++){
		intree->GetEntry(itr);
		if(fileid<7){
		  postresihist[fileid-filerange[0]]->Fill(((intch[0]+intch[1]+intch[2])*ypos[0]+(intch[3]+intch[4]+intch[5])*ypos[1]+(intch[6]+intch[7]+intch[8])*ypos[2])/(intch[0]+intch[1]+intch[2]+intch[3]+intch[4]+intch[5]+intch[6]+intch[7]+intch[8])-preresi[fileid]);
		  totalresihist->Fill(((intch[0]+intch[1]+intch[2])*ypos[0]+(intch[3]+intch[4]+intch[5])*ypos[1]+(intch[6]+intch[7]+intch[8])*ypos[2])/(intch[0]+intch[1]+intch[2]+intch[3]+intch[4]+intch[5]+intch[6]+intch[7]+intch[8])-preresi[fileid]);
		}
		else{
		  postresihist[fileid-filerange[0]]->Fill(((intch[0]+intch[1]+intch[2])*ypos[1]+(intch[3]+intch[4]+intch[5])*ypos[2]+(intch[6]+intch[7]+intch[8])*ypos[3])/(intch[0]+intch[1]+intch[2]+intch[3]+intch[4]+intch[5]+intch[6]+intch[7]+intch[8])-preresi[fileid]);
		  totalresihist->Fill(((intch[0]+intch[1]+intch[2])*ypos[1]+(intch[3]+intch[4]+intch[5])*ypos[2]+(intch[6]+intch[7]+intch[8])*ypos[3])/(intch[0]+intch[1]+intch[2]+intch[3]+intch[4]+intch[5]+intch[6]+intch[7]+intch[8])-preresi[fileid]);
		}
	 }
	 
	 for(Int_t filei=0;filei<Nboffile;filei++)
		postresi[filei]=postresihist[filei]->GetMean();
	 posttotalresi[scani]=totalresihist->GetRMS();
	 // totalresihist->Draw();
	 plotpara p2;
	 p2.plotname=plotdir+"hardcorr"+TString::Format("%d",scani);
	 TF1 *f1 = new TF1("f1","gaus");
	 Double_t mean = totalresihist->GetMean();
	 Double_t sigma = totalresihist->GetRMS();
	 Double_t gausspara[3];
	 f1->SetRange(mean-Nsigma*sigma, mean+Nsigma*sigma); 
	 totalresihist->Fit("f1","QR");
	 f1->GetParameters(&gausspara[0]);  
	 // 2nd fit      
	 f1->SetRange(gausspara[1]-Nsigma*gausspara[2], gausspara[1]+Nsigma*gausspara[2]);  
	 totalresihist->Fit("f1","QR");                                     
	 f1->GetParameters(&gausspara[0]);                                  
	 Draw1HistogramWithTF1(totalresihist,f1,p2);
	 postfitresi[scani]=gausspara[2];
  }
  plotpara p1;
  p1.yname[0]="Position Resolution [cm]";
  p1.xname="Energy [GeV]";
  Draw1Graph(energy,posttotalresi,Nbofscan,p1);
  Draw1Graph(energy,postfitresi,Nbofscan,p1);
}
