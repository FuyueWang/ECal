#include </home/ubuntu/fuyuew/mrpc/MRPCProject/plotfunctions.cpp>
void correction(){
  TString thisdir="tradpos/";
  TString rootdatadir="../../data/"+thisdir,txtdir="../../txt/"+thisdir,plotdir="../../plot/"+thisdir;

  Int_t scani=2;
  Int_t filerange[2]={8,22};
  Int_t Nboffile=filerange[1]-filerange[0]+1,Nsigma=3;

  for(Int_t methodid=2;methodid<5;methodid++){
  // Int_t methodid=3;
  
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
  infile.close();
  if(methodid==3)
	 fitpara[scani][0]=fitpara[scani][0]+0.17;
  TF1 *fsin = new TF1("fsin"+TString::Format("%d",scani),"[0]*pow(x,0.1)*sin([1]*x+[2])",0,24);
  fsin->SetParameters(fitpara[scani][0],fitpara[scani][1],fitpara[scani][2]);

  Double_t singlecorr[33];
  if(methodid==4){
	 infile.open(txtdir+"residualposVsmeasurescan"+TString::Format("%d",scani+1)+".txt");
	 infile>>tmpstr>>tmpstr;
	 cout<<tmpstr<<endl;
	 for(Int_t filei=0;filei<33;filei++){
		infile>>tmpdouble; singlecorr[filei]=fsin->Eval(tmpdouble);
		cout<<tmpdouble<<endl;
		infile>>tmpdouble;
	 }
  }
  Double_t uncorrectedmeasuredposarray[Nboffile],correctedmeasuredposarray[Nboffile],uncorrectedresidualarray[Nboffile],correctedresidualarray[Nboffile],truthpos[Nboffile],uncorrectedFullmeasuredposarray[33],uncorrectedFullresidualarray[33];
  TH1D* uncorrectedmeasuredposhist[Nboffile],*correctedmeasuredposhist[Nboffile],*uncorrectedresidualhist[Nboffile],*correctedresidualhist[Nboffile],*uncorrectedFullmeasuredposhist[33],*uncorrectedFullresidualhist[33],*uncorrectedAllresidualhist,*correctedAllresidualhist;

  for(Int_t filei=0;filei<Nboffile;filei++){
  	 uncorrectedmeasuredposhist[filei]=new TH1D("uncorrectedmeasuredposhist"+TString::Format("%d",filei),"",100,-100,100);
	 correctedmeasuredposhist[filei]=new TH1D("correctedmeasuredposhist"+TString::Format("%d",filei),"",100,-100,100);
	 uncorrectedresidualhist[filei]=new TH1D("uncorrectedresidualhist"+TString::Format("%d",filei),"",100,-100,100);
	 correctedresidualhist[filei]=new TH1D("correctedresidualhist"+TString::Format("%d",filei),"",100,-100,100);
	 // [filei]=new TH1D(""+TString::Format("%d",filei),"",100,-100,100);
  }
  uncorrectedAllresidualhist=new TH1D("uncorrectedAllresidualhist","",70,-3.5,4.5);
  correctedAllresidualhist=new TH1D("correctedAllresidualhist","",70,-3.5,4.5);
  
  for(Int_t filei=0;filei<33;filei++){
	 uncorrectedFullmeasuredposhist[filei]=new TH1D("uncorrectedFullmeasuredposhist"+TString::Format("%d",filei),"",100,-100,100);
	 uncorrectedFullresidualhist[filei]=new TH1D("uncorrectedFullresidualhist"+TString::Format("%d",filei),"",100,-100,100);
	 truthpos[filei]=16-filei*0.5+fitpara[scani][3];
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
	 if(fileid<15)
		tmpmeasuredpos=((intch[0]+intch[1]+intch[2])*14+(intch[3]+intch[4]+intch[5])*10+(intch[6]+intch[7]+intch[8])*6)/(intch[0]+intch[1]+intch[2]+intch[3]+intch[4]+intch[5]+intch[6]+intch[7]+intch[8]);
	 else
		tmpmeasuredpos=((intch[0]+intch[1]+intch[2])*10+(intch[3]+intch[4]+intch[5])*6+(intch[6]+intch[7]+intch[8])*2)/(intch[0]+intch[1]+intch[2]+intch[3]+intch[4]+intch[5]+intch[6]+intch[7]+intch[8]);

	 uncorrectedFullmeasuredposhist[fileid]->Fill(tmpmeasuredpos);
	 uncorrectedFullresidualhist[fileid]->Fill(tmpmeasuredpos-truthpos[fileid]);
	 if(fileid<filerange[0]||fileid>filerange[1]) continue;
	 uncorrectedAllresidualhist->Fill(tmpmeasuredpos-truthpos[fileid]);
	 if(methodid==2||methodid==3){
		uncorrectedmeasuredposhist[fileid-filerange[0]]->Fill(tmpmeasuredpos);
		uncorrectedresidualhist[fileid-filerange[0]]->Fill(tmpmeasuredpos-truthpos[fileid]);
		correctedmeasuredposhist[fileid-filerange[0]]->Fill(tmpmeasuredpos-fsin->Eval(tmpmeasuredpos));
		correctedresidualhist[fileid-filerange[0]]->Fill(tmpmeasuredpos-fsin->Eval(tmpmeasuredpos)-truthpos[fileid]);
		correctedAllresidualhist->Fill(tmpmeasuredpos-fsin->Eval(tmpmeasuredpos)-truthpos[fileid]);
	 }
	 else if(methodid==4){
		uncorrectedmeasuredposhist[fileid-filerange[0]]->Fill(tmpmeasuredpos);
		uncorrectedresidualhist[fileid-filerange[0]]->Fill(tmpmeasuredpos-truthpos[fileid]);
		correctedmeasuredposhist[fileid-filerange[0]]->Fill(tmpmeasuredpos-singlecorr[fileid]);
		correctedresidualhist[fileid-filerange[0]]->Fill(tmpmeasuredpos-singlecorr[fileid]-truthpos[fileid]);
		correctedAllresidualhist->Fill(tmpmeasuredpos-singlecorr[fileid]-truthpos[fileid]);
	 }
  }

  for(Int_t filei=0;filei<Nboffile;filei++){
	 uncorrectedmeasuredposarray[filei]=uncorrectedmeasuredposhist[filei]->GetMean();
	 uncorrectedresidualarray[filei]=uncorrectedresidualhist[filei]->GetMean();
	 correctedmeasuredposarray[filei]=correctedmeasuredposhist[filei]->GetMean();
	 correctedresidualarray[filei]=correctedresidualhist[filei]->GetMean();
  }

  for(Int_t filei=0;filei<33;filei++){
	 uncorrectedFullmeasuredposarray[filei]=uncorrectedFullmeasuredposhist[filei]->GetMean();
	 uncorrectedFullresidualarray[filei]=uncorrectedFullresidualhist[filei]->GetMean();
  }
  if(methodid==2||methodid==3){
  //fit curve
  plotpara p0;
  p0.xname="Measured Position [cm]";
  p0.yname[0]="Measured-Truth Position [cm]";
  p0.textcontent="ECal: interpolation fit method "+TString::Format("%d",methodid);
  p0.plotname=plotdir+"scan"+TString::Format("%d",scani)+"m"+TString::Format("%d",methodid)+"fitcurve";
  Draw1GraphAndTF(uncorrectedFullmeasuredposarray,uncorrectedFullresidualarray,33,fsin,p0);
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
  p1.textcontent="ECal: interpolation correction method "+TString::Format("%d",methodid);
  p1.plotname=plotdir+"scan"+TString::Format("%d",scani)+"m"+TString::Format("%d",methodid)+"corrcompare";
  DrawNGraph(veccompareplotx,veccompareploty,2,vecNbofpoints,p1);
  
  // residual histogram
  plotpara p2;
  p2.xname="#Delta y [cm]";
  p2.yname[0]="Entries";
  p2.leftmargin=0.17;
  p2.rightmargin=0.2-p2.leftmargin;
  p2.titleoffsety[0]=2;
  p2.textcontent="ECal: position residual before correction";
  p2.SetStatsrange(0.62,0.56,0.97,0.94);
  p2.plotname=plotdir+"scan"+TString::Format("%d",scani)+"m"+TString::Format("%d",methodid)+"resihistbefore";
  TF1 *f1 = new TF1("f1","gaus");
  Double_t mean = uncorrectedAllresidualhist->GetMean();
  Double_t sigma = uncorrectedAllresidualhist->GetRMS();
  Double_t gausspara[3];
  f1->SetRange(mean-Nsigma*sigma, mean+Nsigma*sigma); 
  uncorrectedAllresidualhist->Fit("f1","QR");
  f1->GetParameters(&gausspara[0]);  
  // 2nd fit      
  f1->SetRange(gausspara[1]-Nsigma*gausspara[2], gausspara[1]+Nsigma*gausspara[2]);  
  uncorrectedAllresidualhist->Fit("f1","QR");                                     
  f1->GetParameters(&gausspara[0]);                                  
  Draw1HistogramWithTF1(uncorrectedAllresidualhist,f1,p2);

  p2.textcontent="ECal: position residual after correction";
  p2.plotname=plotdir+"scan"+TString::Format("%d",scani)+"m"+TString::Format("%d",methodid)+"resihistafter";
  TF1 *f2 = new TF1("f2","gaus");
  mean = correctedAllresidualhist->GetMean();
  sigma = correctedAllresidualhist->GetRMS();
  f2->SetRange(mean-Nsigma*sigma, mean+Nsigma*sigma); 
  correctedAllresidualhist->Fit("f2","QR");
  f2->GetParameters(&gausspara[0]);  
  // 2nd fit      
  f2->SetRange(gausspara[1]-Nsigma*gausspara[2], gausspara[1]+Nsigma*gausspara[2]);  
  correctedAllresidualhist->Fit("f2","QR");                                     
  f2->GetParameters(&gausspara[0]);               
  Draw1HistogramWithTF1(correctedAllresidualhist,f2,p2);
  }
}
