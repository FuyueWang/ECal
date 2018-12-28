#include </home/ubuntu/fuyuew/mrpc/MRPCProject/plotfunctions.cpp>
void correction(){
  TString thisdir="tradpos/";
  TString rootdatadir="../../data/"+thisdir,txtdir="../../txt/"+thisdir,plotdir="../../plot"+thisdir;

  Int_t scani=0;
  Int_t filerange[2]={8,22};
  Int_t Nboffile=filerange[1]-filerange[0]+1;
  Int_t methodid=2;
  
  Double_t fitpara[6][4];
  ifstream infile(txtdir+"fitpara.txt", ios::in);
  TString tmpstr;
  Double_t tmpdouble;
  infile>>tmpstr;
  for(Int_t scanid=0;scanid<6;scanid++){
		infile>>tmpdouble; fitpara[scanid][0]=tmpdouble;
		infile>>tmpdouble; fitpara[scanid][1]=tmpdouble;
		infile>>tmpdouble; fitpara[scanid][2]=tmpdouble;
		infile>>tmpdouble; fitpara[scanid][3]=tmpdouble;
  }
  TF1 *fsin = new TF1("fsin"+TString::Format("%d",scani),"[0]*pow(x,0.1)*sin([1]*x+[2])",0,24);
  fsin->SetParameters(fitpara[scani][0],fitpara[scani][1],fitpara[scani][2]);
  
  Double_t uncorrectedmeasuredposarray[Nboffile],correctedmeasuredposarray[Nboffile],uncorrectedresidualarray[Nboffile],correctedresidualarray[Nboffile],truthpos[Nboffile];
  TH1D* uncorrectedmeasuredposhist[Nboffile],*correctedmeasuredposhist[Nboffile],*uncorrectedresidualhist[Nboffile],*correctedresidualhist[Nboffile],*uncorrectedAllresidualhist,*correctedAllresidualhist;
  for(Int_t filei=0;filei<Nboffile;filei++){
  	 uncorrectedmeasuredposhist[filei]=new TH1D("uncorrectedmeasuredposhist"+TString::Format("%d",filei),"",100,-100,100);
	 correctedmeasuredposhist[filei]=new TH1D("correctedmeasuredposhist"+TString::Format("%d",filei),"",100,-100,100);
	 uncorrectedresidualhist[filei]=new TH1D("uncorrectedresidualhist"+TString::Format("%d",filei),"",100,-100,100);
	 correctedresidualhist[filei]=new TH1D("correctedresidualhist"+TString::Format("%d",filei),"",100,-100,100);
	 // [filei]=new TH1D(""+TString::Format("%d",filei),"",100,-100,100);
	 truthpos[filei]=16-(filei+filerange[0])*0.5+fitpara[scani][3];
  }
  
  TFile* inrootfile=new TFile(rootdatadir+"rootdata/lwaveform"+TString::Format("%d",scani+1)+"cutLED.root");
  TTree* intree=(TTree*)inrootfile->Get("wavetree");
  Int_t fileid;
  Float_t intch[9];
  intree->SetBranchAddress("intch",intch);
  intree->SetBranchAddress("fileid",&fileid);
  Double_t tmpmeasuredpos;
  Int_t nEntries=intree->GetEntries();
  for(Int_t itr=0;itr<nEntries;itr++){
	 intree->GetEntry(itr);
	 if(fileid<filerange[0]||fileid>filerange[1]) continue;
	 if(fileid<15)
		tmpmeasuredpos=((intch[0]+intch[1]+intch[2])*14+(intch[3]+intch[4]+intch[5])*10+(intch[6]+intch[7]+intch[8])*6)/(intch[0]+intch[1]+intch[2]+intch[3]+intch[4]+intch[5]+intch[6]+intch[7]+intch[8]);
	 else
		tmpmeasuredpos=((intch[0]+intch[1]+intch[2])*10+(intch[3]+intch[4]+intch[5])*6+(intch[6]+intch[7]+intch[8])*2)/(intch[0]+intch[1]+intch[2]+intch[3]+intch[4]+intch[5]+intch[6]+intch[7]+intch[8]);
	 uncorrectedAllresidualhist->Fill(tmpmeasuredpos-truthpos[fileid-filerange[0]]);
	 if(methodid==2){
		uncorrectedmeasuredposhist[fileid-filerange[0]]->Fill(tmpmeasuredpos);
		uncorrectedresidualhist[fileid-filerange[0]]->Fill(tmpmeasuredpos-truthpos[fileid-filerange[0]]);
		correctedmeasuredposhist[fileid-filerange[0]]->Fill(tmpmeasuredpos-fsin->Eval(tmpmeasuredpos));
		correctedresidualhist[fileid-filerange[0]]->Fill(tmpmeasuredpos-fsin->Eval(tmpmeasuredpos)-truthpos[fileid-filerange[0]]);
		correctedAllresidualhist->Fill(tmpmeasuredpos-fsin->Eval(tmpmeasuredpos)-truthpos[fileid-filerange[0]]);
	 }
  }

  for(Int_t filei=0;filei<Nboffile;filei++){
	 uncorrectedmeasuredposarray[filei]=uncorrectedmeasuredposhist[filei]->GetMean();
	 uncorrectedresidualarray[filei]=uncorrectedresidualhist[filei]->GetMean();
	 correctedmeasuredposarray[filei]=correctedmeasuredposhist[filei]->GetMean();
	 correctedresidualarray[filei]=correctedresidualhist[filei]->GetMean();
  }

  //compare
  vector<Double_t*> veccompareplotx,veccompareploty;
  vector<Int_t> vecNbofpoints;

  veccompareplotx.push_back(uncorrectedmeasuredposarray);
  veccompareploty.push_back(uncorrectedresidualarray);
  veccompareplotx.push_back(correctedmeasuredposarray);
  veccompareploty.push_back(correctedresidualarray);
  
  vecNbofpoints.push_back(Nboffile);
  vecNbofpoints.push_back(Nboffile);
 
  plotpara p1;
  p1.xname="Measured Position [cm]";
  p1.yname[0]="Measured-Truth Position [cm]";
  p1.legendname.push_back("Before Correction");
  p1.legendname.push_back("After Correction");
  p1.SetY1range(-3,3);
  p1.textcontent="ECal: Interpolation Correction Method "+TString::Format("%d",methodid);
  p1.plotname=plotdir+"m"+TString::Format("%d",methodid)+"corrcompare";
  DrawNGraph(veccompareplotx,veccompareploty,2,vecNbofpoints,p1);

  plotpara p2;
  

  TF1 *f1 = new TF1("f1","gaus");
  Double_t mean = uncorrrectedAllresidualhist->GetMean();
  Double_t sigma = uncorrrectedAllresidualhist->GetRMS();
  Double_t gausspara[3];
  f1->SetRange(mean-Nsigma*sigma, mean+Nsigma*sigma); 
  uncorrrectedAllresidualhist->Fit("f1","QR");
  f1->GetParameters(&para[0]);  
  // 2nd fit      
  f1->SetRange(para[1]-Nsigma*para[2], para[1]+Nsigma*para[2]);  
  uncorrrectedAllresidualhist->Fit("f1","QR");                                     
  f1->GetParameters(&para[0]);                                  
  
  
}
