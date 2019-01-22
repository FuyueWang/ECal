Double_t pos[4]={14,10,6,2};
Int_t filerange[2][2]={{0,4},{5,10}},Nboffile=11;
Int_t Nsigma=3;
Double_t residualrange[2]={-3,3},fitrange[2]={4.2,10.8};
void Getcalibratedpos(Double_t calibratedpos[Nboffile]){
  for(Int_t filei=0;filei<Nboffile;filei++)
	 calibratedpos[filei]=16-(filei+filerange[0][0])*0.5;
}
void createsinshapedata(TString rootdatadir="../../data/tradpospixel/rootdata/",TString txtdatadir="../../txt/tradpospixel/",Int_t scani=0){
  TFile* infile=new TFile(rootdatadir+"rootdata/lwaveform"+TString::Format("%d",scani)+"energy.root");
  Int_t fileid;
  Float_t intch[9];
  TTree* intree[2];
  TH1D* measuredposhist[Nboffile];
  Double_t calibratedpos[Nboffile];
  for(Int_t filei=0;filei<Nboffile;filei++)
	 measuredposhist[filei]=new TH1D("measured"+TString::Format("%d",filei),"",100,-100,100);

  Getcalibratedpos(calibratedpos);
	
  for(Int_t rowi=0;rowi<2;rowi++){
	 intree[rowi]=(TTree*)infile->Get("wavetreerow"+TString::Format("%d",rowi+1));
	 intree[rowi]->SetBranchAddress("intch",intch);
	 intree[rowi]->SetBranchAddress("fileid",&fileid);
	 // cout<<rowi<<endl;
	 Int_t nEntries=intree[rowi]->GetEntries();
	 for(Int_t itr=0;itr<nEntries;itr++){
		intree[rowi]->GetEntry(itr);
		measuredposhist[fileid-filerange[0][0]]->Fill(((intch[0]+intch[1]+intch[2])*pos[rowi]+(intch[3]+intch[4]+intch[5])*pos[rowi+1]+(intch[6]+intch[7]+intch[8])*pos[rowi+2])/(intch[0]+intch[1]+intch[2]+intch[3]+intch[4]+intch[5]+intch[6]+intch[7]+intch[8]));
	 }
  }
  Double_t measuredpos[Nboffile],posresidual[Nboffile],meanresi=0;
  for(Int_t filei=0;filei<Nboffile;filei++){
	 measuredpos[filei]=measuredposhist[filei]->GetMean();
	 posresidual[filei]=measuredpos[filei]-calibratedpos[filei];
	 meanresi+=posresidual[filei];
  }
  for(Int_t filei=0;filei<Nboffile;filei++) posresidual[filei]-=meanresi/(Double_t)Nboffile;
  ofstream outstd(txtdatadir+"createsinshape"+TString::Format("%d",scani)+".txt");
  outstd<<"measuredpos ";
  for(Int_t filei=0;filei<Nboffile;filei++) outstd<<measuredpos[filei]<<" ";
  outstd<<"\nresidual ";
  for(Int_t filei=0;filei<Nboffile;filei++) outstd<<posresidual[filei]<<" ";
  outstd<<"\nshift "<<meanresi/(Double_t)Nboffile;
}

Double_t Getsinshape(Double_t measuredpos[15],Double_t posresidual[15],TString filename){
  Double_t shift;
  ifstream infile(filename, ios::in);
  TString tmpstr;
  Double_t tmpdouble;
  infile>>tmpstr;
  for(Int_t filei=0;filei<Nboffile;filei++){
	 infile>>tmpdouble;
	 measuredpos[filei]=tmpdouble;
  }
  infile>>tmpstr;
  for(Int_t filei=0;filei<Nboffile;filei++){
	 infile>>tmpdouble;
	 posresidual[filei]=tmpdouble;
  }
  infile>>tmpstr>>shift;
  infile.close();
  return shift;
}


void createfitpara(TString txtdir,TString plotdir,Int_t scani){
  Double_t measuredpos[Nboffile],posresidual[Nboffile],fitpara[5],shift;
  shift=Getsinshape(measuredpos,posresidual,txtdir+"createsinshape"+TString::Format("%d",scani)+".txt");

  // TF1 *fsin = new TF1("fsin"+TString::Format("%d",scani),"[0]*pow(x,0.1)*sin([1]*x+[2])+[3]",3.7,11.6);
  TF1 *fsin = new TF1("fsin"+TString::Format("%d",scani),"[0]*x+[1]*sin([2]*x+[3])+[4]",fitrange[0],fitrange[1]);
  TGraph* gr=new TGraph(Nboffile,measuredpos,posresidual);
  gr->Draw("AP");
  gr->SetMarkerStyle(21);
  gr->SetMarkerSize(1);
  fsin->SetParameters(-2.54,-11.4007,0.255518,7.56378,18.4694);
  // fsin->Draw("same");
  gr->Fit("fsin"+TString::Format("%d",scani),"QR");
  
  fsin->GetParameters(&fitpara[0]);
  cout<<fitpara[0]<<" "<<fitpara[1]<<" "<<fitpara[2]<<" "<<fitpara[3]<<" "<<fitpara[4]<<endl;

  plotpara p1;
  p1.xname="Measured Position [cm]";
  p1.yname[0]="Measured-Calibrated Position [cm]";
  p1.textcontent="ECal: Interpolation correction scan:"+TString::Format("%d",scani);
  p1.plotname=plotdir+"fitsin"+TString::Format("%d",scani);
  p1.minortext=TString::Format("%.2f",fitpara[0])+"x+"+TString::Format("%.2f",fitpara[1])+"sin("+TString::Format("%.2f",fitpara[2])+"x+"+TString::Format("%.2f",fitpara[3])+")"+TString::Format("%.2f",fitpara[4]);
  p1.SetMinorTextPosition(0.4,0.88);
  p1.SetY1range(residualrange[0],residualrange[1]);
  Draw1GraphAndTF(measuredpos,posresidual,Nboffile,fsin,p1);

  // return fitparasummary;
  ofstream outstd(txtdir+"fitpara"+TString::Format("%d",scani)+".txt");
  outstd<<"[0]*pow(x,0.1)*sin([1]*x+[2])+[3]\n";
  for(Int_t k=0;k<5;k++) outstd<<fitpara[k]<<" ";
  outstd<<shift;
}


Double_t Getfitpara(Double_t para[5],TString filename){
  ifstream infile(filename, ios::in);
  TString tmpstr;
  Double_t tmpdouble;
  infile>>tmpstr;
  infile>>tmpdouble; para[0]=tmpdouble;
  infile>>tmpdouble; para[1]=tmpdouble;
  infile>>tmpdouble; para[2]=tmpdouble;
  infile>>tmpdouble; para[3]=tmpdouble;
  infile>>tmpdouble; para[4]=tmpdouble;
  infile>>tmpdouble;
  infile.close();
  return tmpdouble;
}

Double_t correction(TString rootdatadir,TString plotdir,TString txtdir,Int_t methodid,Int_t scani){
  Int_t Nsigma=3;
  Double_t fitpara[5],shift;
  shift=Getfitpara(fitpara,txtdir+"fitpara"+TString::Format("%d",scani)+".txt");
  if(methodid==3)
	 fitpara[1]=fitpara[1]-0.5;
  TF1 *fsin = new TF1("fsin"+TString::Format("%d",scani),"[0]*x+[1]*sin([2]*x+[3])+[4]",fitrange[0]-4,fitrange[1]+4);
  // TF1 *fsin = new TF1("fsin"+TString::Format("%d",scani),"[0]*pow(x,0.1)*sin([1]*x+[2])",0,24);
  fsin->SetParameters(fitpara[0],fitpara[1],fitpara[2],fitpara[3],fitpara[4]);
  
  Double_t singlecorr[Nboffile];
  if(methodid==4){
	 Double_t measuredpos[Nboffile],posresidual[Nboffile];
	 Getsinshape(measuredpos,posresidual,txtdir+"createsinshape"+TString::Format("%d",scani)+".txt");
	 for(Int_t filei=0;filei<Nboffile;filei++)
		singlecorr[filei]=fsin->Eval(measuredpos[filei]);
  }

  Double_t uncorrectedmeasuredposarray[Nboffile],correctedmeasuredposarray[Nboffile],uncorrectedresidualarray[Nboffile],correctedresidualarray[Nboffile],truthpos[Nboffile];
  TH1D* uncorrectedmeasuredposhist[Nboffile],*correctedmeasuredposhist[Nboffile],*uncorrectedresidualhist[Nboffile],*correctedresidualhist[Nboffile],*uncorrectedAllresidualhist,*correctedAllresidualhist;
  Getcalibratedpos(truthpos);
  for(Int_t filei=0;filei<Nboffile;filei++){
  	 uncorrectedmeasuredposhist[filei]=new TH1D("uncorrectedmeasuredposhist"+TString::Format("%d",filei),"",100,-100,100);
	 correctedmeasuredposhist[filei]=new TH1D("correctedmeasuredposhist"+TString::Format("%d",filei),"",100,-100,100);
	 uncorrectedresidualhist[filei]=new TH1D("uncorrectedresidualhist"+TString::Format("%d",filei),"",100,-100,100);
	 correctedresidualhist[filei]=new TH1D("correctedresidualhist"+TString::Format("%d",filei),"",100,-100,100);
	 truthpos[filei]=truthpos[filei]+shift;
  }
  uncorrectedAllresidualhist=new TH1D("uncorrectedAllresidualhist","",70,-3.5,4.5);
  correctedAllresidualhist=new TH1D("correctedAllresidualhist","",70,-3.5,4.5);
  Int_t fileid;
  Float_t intch[9];
  Double_t correctedpos,truepos;
  TFile *outrootfile =new TFile(rootdatadir+"rootdata/correctedM"+TString::Format("%d",methodid)+"scan"+TString::Format("%d",scani)+".root","recreate");
  TTree* outtree=new TTree("correction","correction");
  outtree->Branch("fileid",&fileid,"fileid/I");
  outtree->Branch("correctedpos",&correctedpos,"correctedpos/D");
  outtree->Branch("truepos",&truepos,"truepos/D");
  TFile* inrootfile=new TFile(rootdatadir+"rootdata/lwaveform"+TString::Format("%d",scani)+"energy.root");

  TTree* intree[2];
  for(Int_t rowi=0;rowi<2;rowi++){
	 intree[rowi]=(TTree*)inrootfile->Get("wavetreerow"+TString::Format("%d",rowi+1));
	 intree[rowi]->SetBranchAddress("intch",intch);
	 intree[rowi]->SetBranchAddress("fileid",&fileid);
	 Int_t nEntries=intree[rowi]->GetEntries();
	 Double_t tmpmeasuredpos;
	 for(Int_t itr=0;itr<nEntries;itr++){
		intree[rowi]->GetEntry(itr);
	   tmpmeasuredpos=((intch[0]+intch[1]+intch[2])*pos[rowi]+(intch[3]+intch[4]+intch[5])*pos[rowi+1]+(intch[6]+intch[7]+intch[8])*pos[rowi+2])/(intch[0]+intch[1]+intch[2]+intch[3]+intch[4]+intch[5]+intch[6]+intch[7]+intch[8]);

		uncorrectedAllresidualhist->Fill(tmpmeasuredpos-truthpos[fileid-filerange[0][0]]);
		if(methodid==2||methodid==3){
		  correctedpos=tmpmeasuredpos-fsin->Eval(tmpmeasuredpos);
		  truepos=truthpos[fileid-filerange[0][0]];
		  
		  uncorrectedmeasuredposhist[fileid-filerange[0][0]]->Fill(tmpmeasuredpos);
		  uncorrectedresidualhist[fileid-filerange[0][0]]->Fill(tmpmeasuredpos-truthpos[fileid-filerange[0][0]]);
		  correctedmeasuredposhist[fileid-filerange[0][0]]->Fill(correctedpos);
		  correctedresidualhist[fileid-filerange[0][0]]->Fill(correctedpos-truepos);
		  correctedAllresidualhist->Fill(correctedpos-truepos);
		}
		else if(methodid==4){
		  correctedpos=tmpmeasuredpos-singlecorr[fileid-filerange[0][0]];
		  truepos=truthpos[fileid-filerange[0][0]];
		  uncorrectedmeasuredposhist[fileid-filerange[0][0]]->Fill(tmpmeasuredpos);
		  uncorrectedresidualhist[fileid-filerange[0][0]]->Fill(tmpmeasuredpos-truthpos[fileid-filerange[0][0]]);
		  correctedmeasuredposhist[fileid-filerange[0][0]]->Fill(correctedpos);
		  correctedresidualhist[fileid-filerange[0][0]]->Fill(correctedpos-truepos);
		  correctedAllresidualhist->Fill(correctedpos-truepos);
		}
		outtree->Fill();
	 }
  }
  outrootfile->cd();
  outtree->Write();
  outrootfile->Close();
  for(Int_t filei=0;filei<Nboffile;filei++){
	 uncorrectedmeasuredposarray[filei]=uncorrectedmeasuredposhist[filei]->GetMean();
	 uncorrectedresidualarray[filei]=uncorrectedresidualhist[filei]->GetMean();
	 correctedmeasuredposarray[filei]=correctedmeasuredposhist[filei]->GetMean();
	 correctedresidualarray[filei]=correctedresidualhist[filei]->GetMean();
	 // cout<<uncorrectedmeasuredposarray[filei]<<" "<<correctedmeasuredposarray[filei]<<endl;
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
  p2.xname="Measured-Truth Position [cm]";
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
  return gausspara[2];
}


void gaussfitTH1(TH1D* h1,Double_t gausspara[3]){
  TF1 *f1 = new TF1("f1","gaus");

  Double_t mean = h1->GetMean();
  Double_t sigma = h1->GetRMS();
  f1->SetRange(mean-Nsigma*sigma, mean+Nsigma*sigma); 
  h1->Fit("f1","QR");
  f1->GetParameters(&gausspara[0]);  
  // 2nd fit      
  f1->SetRange(gausspara[1]-Nsigma*gausspara[2], gausspara[1]+Nsigma*gausspara[2]);  
  h1->Fit("f1","QR");                                     
  f1->GetParameters(&gausspara[0]);              
}


void analysisforeverypixel(TString rootdatadir,TString plotdir,Int_t methodid,Int_t scani,Double_t reso[2]){
  Int_t fileid; 
  Double_t correctedpos,truepos;
  TFile* infile= new TFile(rootdatadir+"rootdata/correctedM"+TString::Format("%d",methodid)+"scan"+TString::Format("%d",scani)+".root");
  TTree* tree=(TTree*)infile->Get("correction");
  tree->SetBranchAddress("fileid",&fileid);
  tree->SetBranchAddress("correctedpos",&correctedpos);
  tree->SetBranchAddress("truepos",&truepos);

  TH1D* residualhist[2];
  for(Int_t k=0;k<2;k++)
	 residualhist[k]=new TH1D("residualrow"+TString::Format("%d",k),"",100,-3.5,4.5);
  Int_t nEntries = tree->GetEntries();
  for(Int_t itr=0;itr<nEntries;itr++){
	 tree->GetEntry(itr);
	 if(fileid<filerange[1][0])
		residualhist[0]->Fill(correctedpos-truepos);
	 else
		residualhist[1]->Fill(correctedpos-truepos);
  }
  plotpara p1;
  p1.xname="Measured-Truth Position [cm]";
  p1.yname[0]="Entries";
  p1.leftmargin=0.17;
  p1.rightmargin=0.2-p1.leftmargin;
  p1.titleoffsety[0]=2;
  p1.textcontent="ECal: position residual after correction";
  p1.SetStatsrange(0.62,0.56,0.97,0.94);
  for(Int_t rowi=0;rowi<2;rowi++){
	 if(plotdir!="")
		p1.plotname=plotdir+"scanrow"+TString::Format("%d%d",scani,rowi)+"m"+TString::Format("%d",methodid);
	 Double_t gausspara[3];
	 gaussfitTH1(residualhist[rowi],gausspara);
	 TF1 *f1 = new TF1("f1","gaus");
	 f1->SetParameters(gausspara[0],gausspara[1],gausspara[2]);
	 f1->SetRange(gausspara[1]-Nsigma*gausspara[2], gausspara[1]+Nsigma*gausspara[2]);
	 Draw1HistogramWithTF1(residualhist[rowi],f1,p1);
	 reso[rowi]=gausspara[2];
	 // cout<<reso[rowi]<<endl;
  }
}
Double_t analysisforeverypixel(TString rootdatadir,TString plotdir,Int_t methodid,Int_t scani){
  Int_t fileid; 
  Double_t correctedpos,truepos;
  TFile* infile= new TFile(rootdatadir+"rootdata/correctedM"+TString::Format("%d",methodid)+"scan"+TString::Format("%d",scani)+".root");
  TTree* tree=(TTree*)infile->Get("correction");
  tree->SetBranchAddress("fileid",&fileid);
  tree->SetBranchAddress("correctedpos",&correctedpos);
  tree->SetBranchAddress("truepos",&truepos);

  TH1D* residualhist=new TH1D("residual","",100,-3.5,4.5);
  // for(Int_t k=0;k<2;k++)
  // 	 residualhist[k]=new TH1D("residualrow"+TString::Format("%d",k),"",100,-3.5,4.5);
  Int_t nEntries = tree->GetEntries();
  for(Int_t itr=0;itr<nEntries;itr++){
	 tree->GetEntry(itr);
	 residualhist->Fill(correctedpos-truepos);
  }
  plotpara p1;
  p1.xname="Measured-Truth Position [cm]";
  p1.yname[0]="Entries";
  p1.leftmargin=0.17;
  p1.rightmargin=0.2-p1.leftmargin;
  p1.titleoffsety[0]=2;
  p1.textcontent="ECal: position residual after correction";
  p1.SetStatsrange(0.62,0.56,0.97,0.94);

  if(plotdir!="")
	 p1.plotname=plotdir+"scan"+TString::Format("%d",scani)+"m"+TString::Format("%d",methodid);
  Double_t gausspara[3];
  gaussfitTH1(residualhist,gausspara);
  TF1 *f1 = new TF1("f1","gaus");
  f1->SetParameters(gausspara[0],gausspara[1],gausspara[2]);
  f1->SetRange(gausspara[1]-Nsigma*gausspara[2], gausspara[1]+Nsigma*gausspara[2]);
  Draw1HistogramWithTF1(residualhist,f1,p1);
  return gausspara[2];
	 // cout<<reso[rowi]<<endl;
  
}

Double_t analysisforeveryscan(TString rootdatadir,Int_t methodid,Int_t scani){
  Int_t fileid; 
  Double_t correctedpos,truepos;
  TFile* infile= new TFile(rootdatadir+"rootdata/correctedM"+TString::Format("%d",methodid)+"scan"+TString::Format("%d",scani)+".root");
  TTree* tree=(TTree*)infile->Get("correction");
  tree->SetBranchAddress("fileid",&fileid);
  tree->SetBranchAddress("correctedpos",&correctedpos);
  tree->SetBranchAddress("truepos",&truepos);

  TH1D* residualhist=new TH1D("residual","",100,-3.5,4.5);;
  Int_t nEntries = tree->GetEntries();
  for(Int_t itr=0;itr<nEntries;itr++){
	 tree->GetEntry(itr);
	 residualhist->Fill(correctedpos-truepos);
  }
  plotpara p1;
  p1.xname="Measured-Truth Position [cm]";
  p1.yname[0]="Entries";
  p1.leftmargin=0.17;
  p1.rightmargin=0.2-p1.leftmargin;
  p1.titleoffsety[0]=2;
  p1.textcontent="ECal: position residual before correction";
  p1.SetStatsrange(0.62,0.56,0.97,0.94);

  // p1.plotname=plotdir+"scanrow"+TString::Format("%d%d",scani,rowi)+"m"+TString::Format("%d",methodid);
  Double_t gausspara[3];
  gaussfitTH1(residualhist,gausspara);
  TF1 *f1 = new TF1("f1","gaus");
  f1->SetParameters(gausspara[0],gausspara[1],gausspara[2]);
  f1->SetRange(gausspara[1]-Nsigma*gausspara[2], gausspara[1]+Nsigma*gausspara[2]);
  Draw1HistogramWithTF1(residualhist,f1,p1);
  // cout<<gausspara[2]<<endl;
  return gausspara[2];
}

Double_t analysisNN(TString NNmodeldir,TString plotdir,Int_t scani){
  TH1D* residualhist=new TH1D("residual","",100,-3.5,4.5);
  
  ifstream infile(NNmodeldir+"valpredscan"+TString::Format("%d",scani)+".csv", ios::in);
  TString tmpstr;
  Double_t tmpdouble1,tmpdouble2;
  infile>>tmpstr>>tmpstr;
  while(!infile.eof()){
	 infile>>tmpdouble1; 
	 infile>>tmpdouble1; 
	 infile>>tmpdouble2;
	 residualhist->Fill(tmpdouble1-tmpdouble2);
  }
  infile.close();
  
  plotpara p1;
  p1.xname="Measured-Truth Position [cm]";
  p1.yname[0]="Entries";
  p1.leftmargin=0.17;
  p1.rightmargin=0.2-p1.leftmargin;
  p1.titleoffsety[0]=2;
  p1.textcontent="ECal: position residual with CNN";
  p1.SetStatsrange(0.62,0.56,0.97,0.94);
 
  if(plotdir!="")
	 p1.plotname=plotdir+"scan"+TString::Format("%d",scani);
  Double_t gausspara[3];
  gaussfitTH1(residualhist,gausspara);
  TF1 *f1 = new TF1("f1","gaus");
  f1->SetParameters(gausspara[0],gausspara[1],gausspara[2]);
  f1->SetRange(gausspara[1]-Nsigma*gausspara[2], gausspara[1]+Nsigma*gausspara[2]);
  Draw1HistogramWithTF1(residualhist,f1,p1);
  return gausspara[2];
	 
}


void slewing(TString rootdatadir,TString plotdir,TString txtdir,Int_t scani,Double_t posreso[2]){
  Double_t rangefit[2]={4.2,10.8};
  Double_t preposreso[2];
  TF1 *f1 = new TF1("f1","gaus");
  Double_t fitpara[5],shift;
  shift=Getfitpara(fitpara,txtdir+"fitpara"+TString::Format("%d",scani)+".txt");
  Double_t truthpos[Nboffile];
  Getcalibratedpos(truthpos);
  for(Int_t filei=0;filei<Nboffile;filei++) truthpos[filei]=truthpos[filei]+shift;//fitpara[3];
  Double_t uncorrectedmeasuredposarray[Nboffile],correctedmeasuredposarray[Nboffile],uncorrectedresidualarray[Nboffile],correctedresidualarray[Nboffile];
  TH1D* uncorrectedmeasuredposhist[Nboffile],*correctedmeasuredposhist[Nboffile],*uncorrectedresidualhist[Nboffile],*correctedresidualhist[Nboffile];

  for(Int_t filei=0;filei<Nboffile;filei++){
  	 uncorrectedmeasuredposhist[filei]=new TH1D("uncorrectedmeasuredposhist"+TString::Format("%d",filei),"",100,-100,100);
	 correctedmeasuredposhist[filei]=new TH1D("correctedmeasuredposhist"+TString::Format("%d",filei),"",100,-100,100);
	 uncorrectedresidualhist[filei]=new TH1D("uncorrectedresidualhist"+TString::Format("%d",filei),"",100,-100,100);
	 correctedresidualhist[filei]=new TH1D("correctedresidualhist"+TString::Format("%d",filei),"",100,-100,100);
	 // [filei]=new TH1D(""+TString::Format("%d",filei),"",100,-100,100);
  }
  
  TFile* inrootfile=new TFile(rootdatadir+"rootdata/lwaveform"+TString::Format("%d",scani)+"energy.root");
  TTree* intree[2];
  Int_t fileid;
  Float_t intch[9];
  for(Int_t rowi=0;rowi<2;rowi++){
	 intree[rowi]=(TTree*)inrootfile->Get("wavetreerow"+TString::Format("%d",rowi+1));
	 intree[rowi]->SetBranchAddress("intch",intch);
	 intree[rowi]->SetBranchAddress("fileid",&fileid);

	 Int_t nEntries=intree[rowi]->GetEntries();
	 vector<Double_t> residual,measuredpos;
	 vector<Int_t> filearray;
	 for(Int_t itr=0;itr<nEntries;itr++){
		intree[rowi]->GetEntry(itr);
		measuredpos.push_back(((intch[0]+intch[1]+intch[2])*pos[rowi]+(intch[3]+intch[4]+intch[5])*pos[rowi+1]+(intch[6]+intch[7]+intch[8])*pos[rowi+2])/(intch[0]+intch[1]+intch[2]+intch[3]+intch[4]+intch[5]+intch[6]+intch[7]+intch[8]));
		residual.push_back(measuredpos[itr]-truthpos[fileid-filerange[0][0]]);
		filearray.push_back(fileid-filerange[0][0]);
		uncorrectedmeasuredposhist[fileid-filerange[0][0]]->Fill(measuredpos[itr]);
		uncorrectedresidualhist[fileid-filerange[0][0]]->Fill(measuredpos[itr]-truthpos[fileid-filerange[0][0]]);
	 }
	 Int_t iteration=0,Nbofiteration=3; 
	 while (iteration<Nbofiteration){
		TH1D* residualhist=new TH1D("residual","",70,-3.5,4.5);
		TH2D* correctionhist=new TH2D("correction"+TString::Format("%d",iteration),"",23,-3,20,70,-10,10);
		for(Int_t i=0;i<nEntries;i++){
		  residualhist->Fill(residual[i]);  
		  correctionhist->Fill(measuredpos[i],residual[i]);
		}
		gStyle->SetOptFit(111);
		gStyle->SetOptStat(1111);	
		Double_t mean = residualhist->GetMean();
		Double_t sigma = residualhist->GetRMS();
		Double_t para[3];
		f1->SetRange(mean-Nsigma*sigma, mean+Nsigma*sigma); 
		residualhist->Fit("f1","QR");
		f1->GetParameters(&para[0]);  
		// 2nd fit      
		f1->SetRange(para[1]-Nsigma*para[2], para[1]+Nsigma*para[2]);  
		residualhist->Fit("f1","QR");                                     
		f1->GetParameters(&para[0]);                                  
		f1->SetRange(para[1]-Nsigma*para[2], para[1]+Nsigma*para[2]);
		f1->GetParameters(&para[0]);  

		
		TF1 *ftemp = new TF1("ftemp","[0]*exp(-0.5*((x-[1])/[2])**2)",para[1]-Nsigma*para[2],para[1]+Nsigma*para[2]);
		ftemp->SetParameters(para[0],para[1],para[2]);
		
		correctionhist->ProfileX();
		TH1D *htemp=(TProfile *)gDirectory->Get("correction"+TString::Format("%d",iteration)+"_pfx");
		Double_t par[8];
	 
		TF1 *f2 = new TF1("f2","[0]+[1]/sqrt(x)+[2]/x+[3]*x+[4]*pow(x,2)+[5]*pow(x,3)",rangefit[0],rangefit[1]);
		
		htemp->Fit("f2","q","QRsame",rangefit[0],rangefit[1]);
		htemp->Fit("f2","q","QRsame",rangefit[0],rangefit[1]);  
		f2->GetParameters(&par[0]);


		if(iteration==Nbofiteration-1){
		  for(Int_t i=0;i<nEntries;i++){
			 double cor=0;
			 // cor=par[0]+par[1]/sqrt(TOT[i])+par[2]/TOT[i]+par[3]*TOT[i]+par[4]*pow(TOT[i],2)+par[5]*pow(TOT[i],3);
			 cor=htemp->GetBinContent(htemp->FindBin(measuredpos[i]));
			 residual.at(i)=residual.at(i)-cor;
			 correctedmeasuredposhist[filearray[i]]->Fill(residual[i]+truthpos[filearray[i]]);
			 correctedresidualhist[filearray[i]]->Fill(residual[i]);
		  }
		}
		else{
		  for(Int_t i=0;i<nEntries;i++){
			 double cor=0;
			 cor=htemp->GetBinContent(htemp->FindBin(measuredpos[i]));
			 // residual[i]=residual[i]-cor;
			 residual.at(i)=residual.at(i)-cor;
		  }
		}	
		
		plotpara residualp1,correctionp1;
		// correctionp1.format=".png";
		correctionp1.xname="Measured Position [cm]";
		correctionp1.yname[0]="Measured-Truth Position [cm]";
		correctionp1.titleoffsety[0]=1.45;
		correctionp1.rightmargin=0.11;
		correctionp1.statsxrange[0]=0.62;	correctionp1.statsxrange[1]=0.9;
		correctionp1.statsyrange[0]=0.66;	correctionp1.statsyrange[1]=0.93;
		if(plotdir!="")
		correctionp1.plotname=plotdir+"slewing/scan"+TString::Format("%d%d",scani,rowi)+"corritr"+TString::Format("%d",iteration);
		Draw1TH2DWithPfTF(correctionhist,htemp,f2,correctionp1);
		
		// residualp1.format=".png";
		residualp1.SetStatsrange(0.1287625,0.5619546,0.4899666,0.9406632);
		residualp1.titleoffsety[0]=1.85;
		residualp1.leftmargin=0.17;
		residualp1.rightmargin=0.2-residualp1.leftmargin;
		residualp1.xname="Measured-Truth Position [cm]";
		residualp1.yname[0]="Entries";
		residualp1.SetStatsrange(0.62,0.56,0.97,0.94);
		if(iteration==0) residualp1.textcontent ="MRPC Experiment: Before slew";
		else residualp1.textcontent ="MRPC Experiment: After slew";
		if(plotdir!="")
		residualp1.plotname=plotdir+"slewing/scan"+TString::Format("%d%d",scani,rowi)+"timeitr"+TString::Format("%d",iteration);
		Draw1HistogramWithTF1(residualhist,ftemp,residualp1);
		
		iteration++;
		if(iteration==Nbofiteration){
		  posreso[rowi]=para[2];////residualhist->GetRMS();
		  // posresoerror[scani]=posreso[scani]/sqrt(2*(residualhist->GetEntries()-1));
		}
		else if(iteration==1)
		  preposreso[rowi]=residualhist->GetRMS();
	 }
  }
  for(Int_t filei=0;filei<Nboffile;filei++){
	 uncorrectedmeasuredposarray[filei]=uncorrectedmeasuredposhist[filei]->GetMean();
	 uncorrectedresidualarray[filei]=uncorrectedresidualhist[filei]->GetMean();
	 // cout<<uncorrectedresidualarray[filei]<<endl;
	 correctedmeasuredposarray[filei]=correctedmeasuredposhist[filei]->GetMean();
	 correctedresidualarray[filei]=correctedresidualhist[filei]->GetMean();
  }

  vector<Double_t*> veccompareplotx,veccompareploty;
  vector<Int_t> vecNbofpoints;
  
  veccompareplotx.push_back(uncorrectedmeasuredposarray);
  veccompareploty.push_back(uncorrectedresidualarray);
  veccompareplotx.push_back(uncorrectedmeasuredposarray);
  veccompareploty.push_back(correctedresidualarray);
  
  vecNbofpoints.push_back(Nboffile);
  vecNbofpoints.push_back(Nboffile);
 
  plotpara p1;
  p1.xname="Measured Position [cm]";
  p1.yname[0]="Measured-Truth Position [cm]";
  p1.legendname.push_back("Before Correction");
  p1.legendname.push_back("After Correction");
  p1.SetY1range(-3,3);
  p1.withline="true";
  p1.textcontent="ECal: interpolation correction method";
  p1.plotname=plotdir+"slewing/scan"+TString::Format("%d",scani)+"corrcompare";
  DrawNGraph(veccompareplotx,veccompareploty,2,vecNbofpoints,p1);

  p1.textcontent="ECal: interpolation";
  if(plotdir!="")
  p1.plotname=plotdir+"slewing/scan"+TString::Format("%d",scani)+"sinshape";
  Draw1Graph(uncorrectedmeasuredposarray,uncorrectedresidualarray,Nboffile,p1);
  
  // if(savetxt&&Nbofscan==6){
  // 	 ofstream outstd(txtdir+"resoforscansslewing.txt");
  // 	 outstd<<"scanid energy reso resoerror prereso\n";
  // 	 for(Int_t scani=0;scani<Nbofscan;scani++)
  // 		outstd<<scani<<" "<<posreso[scani]<<" "<<posresoerror[scani]<<" "<<preposreso[scani]<<"\n";
  // }
}



Double_t slewing(TString rootdatadir,TString plotdir,TString txtdir,Int_t scani){
  Double_t rangefit[2]={4.2,10.8};
  Double_t preposreso,posreso;
  TF1 *f1 = new TF1("f1","gaus");
  Double_t fitpara[5],shift;
  shift=Getfitpara(fitpara,txtdir+"fitpara"+TString::Format("%d",scani)+".txt");
  Double_t truthpos[Nboffile];
  Getcalibratedpos(truthpos);
  for(Int_t filei=0;filei<Nboffile;filei++) truthpos[filei]=truthpos[filei]+shift;//fitpara[3];
  Double_t uncorrectedmeasuredposarray[Nboffile],correctedmeasuredposarray[Nboffile],uncorrectedresidualarray[Nboffile],correctedresidualarray[Nboffile];
  TH1D* uncorrectedmeasuredposhist[Nboffile],*correctedmeasuredposhist[Nboffile],*uncorrectedresidualhist[Nboffile],*correctedresidualhist[Nboffile];

  for(Int_t filei=0;filei<Nboffile;filei++){
  	 uncorrectedmeasuredposhist[filei]=new TH1D("uncorrectedmeasuredposhist"+TString::Format("%d",filei),"",100,-100,100);
	 correctedmeasuredposhist[filei]=new TH1D("correctedmeasuredposhist"+TString::Format("%d",filei),"",100,-100,100);
	 uncorrectedresidualhist[filei]=new TH1D("uncorrectedresidualhist"+TString::Format("%d",filei),"",100,-100,100);
	 correctedresidualhist[filei]=new TH1D("correctedresidualhist"+TString::Format("%d",filei),"",100,-100,100);
	 // [filei]=new TH1D(""+TString::Format("%d",filei),"",100,-100,100);
  }
  
  TFile* inrootfile=new TFile(rootdatadir+"rootdata/lwaveform"+TString::Format("%d",scani)+"energy.root");
  TTree* intree[2];
  Int_t fileid;
  Float_t intch[9];
  vector<Double_t> residual,measuredpos;
  vector<Int_t> filearray;
  for(Int_t rowi=0;rowi<2;rowi++){
	 intree[rowi]=(TTree*)inrootfile->Get("wavetreerow"+TString::Format("%d",rowi+1));
	 intree[rowi]->SetBranchAddress("intch",intch);
	 intree[rowi]->SetBranchAddress("fileid",&fileid);

	 Int_t nEntries=intree[rowi]->GetEntries();

	 for(Int_t itr=0;itr<nEntries;itr++){
		intree[rowi]->GetEntry(itr);
		measuredpos.push_back(((intch[0]+intch[1]+intch[2])*pos[rowi]+(intch[3]+intch[4]+intch[5])*pos[rowi+1]+(intch[6]+intch[7]+intch[8])*pos[rowi+2])/(intch[0]+intch[1]+intch[2]+intch[3]+intch[4]+intch[5]+intch[6]+intch[7]+intch[8]));
		residual.push_back(measuredpos[itr]-truthpos[fileid-filerange[0][0]]);
		filearray.push_back(fileid-filerange[0][0]);
		uncorrectedmeasuredposhist[fileid-filerange[0][0]]->Fill(measuredpos[itr]);
		uncorrectedresidualhist[fileid-filerange[0][0]]->Fill(measuredpos[itr]-truthpos[fileid-filerange[0][0]]);
	 }
  }
  Int_t nEntries=intree[0]->GetEntries()+intree[1]->GetEntries();
	 Int_t iteration=0,Nbofiteration=3; 
	 while (iteration<Nbofiteration){
		TH1D* residualhist=new TH1D("residual","",70,-3.5,4.5);
		TH2D* correctionhist=new TH2D("correction"+TString::Format("%d",iteration),"",23,-3,20,70,-10,10);
		for(Int_t i=0;i<nEntries;i++){
		  residualhist->Fill(residual[i]);  
		  correctionhist->Fill(measuredpos[i],residual[i]);
		}
		gStyle->SetOptFit(111);
		gStyle->SetOptStat(1111);	
		Double_t mean = residualhist->GetMean();
		Double_t sigma = residualhist->GetRMS();
		Double_t para[3];
		f1->SetRange(mean-Nsigma*sigma, mean+Nsigma*sigma); 
		residualhist->Fit("f1","QR");
		f1->GetParameters(&para[0]);  
		// 2nd fit      
		f1->SetRange(para[1]-Nsigma*para[2], para[1]+Nsigma*para[2]);  
		residualhist->Fit("f1","QR");                                     
		f1->GetParameters(&para[0]);                                  
		f1->SetRange(para[1]-Nsigma*para[2], para[1]+Nsigma*para[2]);
		f1->GetParameters(&para[0]);  

		
		TF1 *ftemp = new TF1("ftemp","[0]*exp(-0.5*((x-[1])/[2])**2)",para[1]-Nsigma*para[2],para[1]+Nsigma*para[2]);
		ftemp->SetParameters(para[0],para[1],para[2]);
		
		correctionhist->ProfileX();
		TH1D *htemp=(TProfile *)gDirectory->Get("correction"+TString::Format("%d",iteration)+"_pfx");
		Double_t par[8];
	 
		TF1 *f2 = new TF1("f2","[0]+[1]/sqrt(x)+[2]/x+[3]*x+[4]*pow(x,2)+[5]*pow(x,3)",rangefit[0],rangefit[1]);
		
		htemp->Fit("f2","q","QRsame",rangefit[0],rangefit[1]);
		htemp->Fit("f2","q","QRsame",rangefit[0],rangefit[1]);  
		f2->GetParameters(&par[0]);


		if(iteration==Nbofiteration-1){
		  for(Int_t i=0;i<nEntries;i++){
			 double cor=0;
			 // cor=par[0]+par[1]/sqrt(TOT[i])+par[2]/TOT[i]+par[3]*TOT[i]+par[4]*pow(TOT[i],2)+par[5]*pow(TOT[i],3);
			 cor=htemp->GetBinContent(htemp->FindBin(measuredpos[i]));
			 residual.at(i)=residual.at(i)-cor;
			 correctedmeasuredposhist[filearray[i]]->Fill(residual[i]+truthpos[filearray[i]]);
			 correctedresidualhist[filearray[i]]->Fill(residual[i]);
		  }
		}
		else{
		  for(Int_t i=0;i<nEntries;i++){
			 double cor=0;
			 cor=htemp->GetBinContent(htemp->FindBin(measuredpos[i]));
			 // residual[i]=residual[i]-cor;
			 residual.at(i)=residual.at(i)-cor;
		  }
		}	
		
		plotpara residualp1,correctionp1;
		// correctionp1.format=".png";
		correctionp1.xname="Measured Position [cm]";
		correctionp1.yname[0]="Measured-Truth Position [cm]";
		correctionp1.titleoffsety[0]=1.45;
		correctionp1.rightmargin=0.11;
		correctionp1.statsxrange[0]=0.62;	correctionp1.statsxrange[1]=0.9;
		correctionp1.statsyrange[0]=0.66;	correctionp1.statsyrange[1]=0.93;
		if(plotdir!="")
		correctionp1.plotname=plotdir+"slewing/scan"+TString::Format("%d",scani)+"corritr"+TString::Format("%d",iteration);
		Draw1TH2DWithPfTF(correctionhist,htemp,f2,correctionp1);
		
		// residualp1.format=".png";
		residualp1.SetStatsrange(0.1287625,0.5619546,0.4899666,0.9406632);
		residualp1.titleoffsety[0]=1.85;
		residualp1.leftmargin=0.17;
		residualp1.rightmargin=0.2-residualp1.leftmargin;
		residualp1.xname="Measured-Truth Position [cm]";
		residualp1.yname[0]="Entries";
		residualp1.SetStatsrange(0.62,0.56,0.97,0.94);
		if(iteration==0) residualp1.textcontent ="MRPC Experiment: Before slew";
		else residualp1.textcontent ="MRPC Experiment: After slew";
		if(plotdir!="")
		residualp1.plotname=plotdir+"slewing/scan"+TString::Format("%d",scani)+"timeitr"+TString::Format("%d",iteration);
		Draw1HistogramWithTF1(residualhist,ftemp,residualp1);
		
		iteration++;
		if(iteration==Nbofiteration){
		  posreso=para[2];////residualhist->GetRMS();
		  // posresoerror[scani]=posreso[scani]/sqrt(2*(residualhist->GetEntries()-1));
		}
		else if(iteration==1)
		  preposreso=residualhist->GetRMS();
	 }
  
  for(Int_t filei=0;filei<Nboffile;filei++){
	 uncorrectedmeasuredposarray[filei]=uncorrectedmeasuredposhist[filei]->GetMean();
	 uncorrectedresidualarray[filei]=uncorrectedresidualhist[filei]->GetMean();
	 // cout<<uncorrectedresidualarray[filei]<<endl;
	 correctedmeasuredposarray[filei]=correctedmeasuredposhist[filei]->GetMean();
	 correctedresidualarray[filei]=correctedresidualhist[filei]->GetMean();
  }

  vector<Double_t*> veccompareplotx,veccompareploty;
  vector<Int_t> vecNbofpoints;
  
  veccompareplotx.push_back(uncorrectedmeasuredposarray);
  veccompareploty.push_back(uncorrectedresidualarray);
  veccompareplotx.push_back(uncorrectedmeasuredposarray);
  veccompareploty.push_back(correctedresidualarray);
  
  vecNbofpoints.push_back(Nboffile);
  vecNbofpoints.push_back(Nboffile);
 
  plotpara p1;
  p1.xname="Measured Position [cm]";
  p1.yname[0]="Measured-Truth Position [cm]";
  p1.legendname.push_back("Before Correction");
  p1.legendname.push_back("After Correction");
  p1.SetY1range(-3,3);
  p1.withline="true";
  p1.textcontent="ECal: interpolation correction method";
  p1.plotname=plotdir+"slewing/scan"+TString::Format("%d",scani)+"corrcompare";
  DrawNGraph(veccompareplotx,veccompareploty,2,vecNbofpoints,p1);

  p1.textcontent="ECal: interpolation";
  if(plotdir!="")
  p1.plotname=plotdir+"slewing/scan"+TString::Format("%d",scani)+"sinshape";
  Draw1Graph(uncorrectedmeasuredposarray,uncorrectedresidualarray,Nboffile,p1);
  
  // if(savetxt&&Nbofscan==6){
  // 	 ofstream outstd(txtdir+"resoforscansslewing.txt");
  // 	 outstd<<"scanid energy reso resoerror prereso\n";
  // 	 for(Int_t scani=0;scani<Nbofscan;scani++)
  // 		outstd<<scani<<" "<<posreso[scani]<<" "<<posresoerror[scani]<<" "<<preposreso[scani]<<"\n";
  // }
  return posreso;
}



Double_t amplitudeslewing(TString rootdatadir,TString plotdir,TString txtdir,Int_t scani){
  Double_t rangefit[2]={3.7,11.6};
  Double_t preposreso,posreso;
  TF1 *f1 = new TF1("f1","gaus");
  Double_t fitpara[5],shift;
  shift=Getfitpara(fitpara,txtdir+"fitpara"+TString::Format("%d",scani)+".txt");
  Double_t truthpos[Nboffile];
  Getcalibratedpos(truthpos);
  for(Int_t filei=0;filei<Nboffile;filei++) truthpos[filei]=truthpos[filei]+shift;//+fitpara[3];
  Double_t uncorrectedmeasuredposarray[Nboffile],correctedmeasuredposarray[Nboffile],uncorrectedresidualarray[Nboffile],correctedresidualarray[Nboffile];
  TH1D* uncorrectedmeasuredposhist[Nboffile],*correctedmeasuredposhist[Nboffile],*uncorrectedresidualhist[Nboffile],*correctedresidualhist[Nboffile];

  for(Int_t filei=0;filei<Nboffile;filei++){
  	 uncorrectedmeasuredposhist[filei]=new TH1D("uncorrectedmeasuredposhist"+TString::Format("%d",filei),"",100,-100,100);
	 correctedmeasuredposhist[filei]=new TH1D("correctedmeasuredposhist"+TString::Format("%d",filei),"",100,-100,100);
	 uncorrectedresidualhist[filei]=new TH1D("uncorrectedresidualhist"+TString::Format("%d",filei),"",100,-100,100);
	 correctedresidualhist[filei]=new TH1D("correctedresidualhist"+TString::Format("%d",filei),"",100,-100,100);
	 // [filei]=new TH1D(""+TString::Format("%d",filei),"",100,-100,100);
  }
  	 vector<Double_t> residual,ratio[2];
	 vector<Int_t> filearray;
	 residual.clear();
	 ratio[0].clear();
	 ratio[1].clear();
	 filearray.clear();
  TFile* inrootfile=new TFile(rootdatadir+"rootdata/lwaveform"+TString::Format("%d",scani)+"energy.root");
  TTree* intree[2];
  Int_t fileid;
  Float_t intch[9];
  for(Int_t rowi=0;rowi<2;rowi++){
	 intree[rowi]=(TTree*)inrootfile->Get("wavetreerow"+TString::Format("%d",rowi+1));
	 intree[rowi]->SetBranchAddress("intch",intch);
	 intree[rowi]->SetBranchAddress("fileid",&fileid);

	 Int_t nEntries=intree[rowi]->GetEntries();

	 for(Int_t itr=0;itr<nEntries;itr++){
		intree[rowi]->GetEntry(itr);
		Double_t tmpmeasuredpos;
		  tmpmeasuredpos=((intch[0]+intch[1]+intch[2])*pos[rowi]+(intch[3]+intch[4]+intch[5])*pos[rowi+1]+(intch[6]+intch[7]+intch[8])*pos[rowi+2])/(intch[0]+intch[1]+intch[2]+intch[3]+intch[4]+intch[5]+intch[6]+intch[7]+intch[8]);
	

		residual.push_back(tmpmeasuredpos-truthpos[fileid-filerange[0][0]]);
		ratio[0].push_back((intch[3]+intch[4]+intch[5])/(intch[0]+intch[1]+intch[2]));
		ratio[1].push_back((intch[3]+intch[4]+intch[5])/(intch[6]+intch[7]+intch[8]));
		filearray.push_back(fileid-filerange[0][0]);
		uncorrectedmeasuredposhist[fileid-filerange[0][0]]->Fill(tmpmeasuredpos);
		uncorrectedresidualhist[fileid-filerange[0][0]]->Fill(tmpmeasuredpos-truthpos[fileid-filerange[0][0]]);
	 }
  }
  Int_t nEntries=intree[0]->GetEntries()+intree[1]->GetEntries();
	 Int_t iteration=0,Nbofiteration=4; 
	 while (iteration<Nbofiteration){
		TH1D* residualhist=new TH1D("residual","",70,-3.5,4.5);
		TH2D* correctionhist[2];
		correctionhist[0]=new TH2D("correction0"+TString::Format("%d",iteration),"",50,0,10,50,-6,6);
		correctionhist[1]=new TH2D("correction1"+TString::Format("%d",iteration),"",50,0,10,50,-6,6);
		for(Int_t i=0;i<nEntries;i++){
		  residualhist->Fill(residual[i]);  
		  correctionhist[0]->Fill(ratio[0][i],residual[i]);
		  correctionhist[1]->Fill(ratio[1][i],residual[i]);
		}
		gStyle->SetOptFit(111);
		gStyle->SetOptStat(1111);	
		Double_t mean = residualhist->GetMean();
		Double_t sigma = residualhist->GetRMS();
		Double_t para[3];
		f1->SetRange(mean-Nsigma*sigma, mean+Nsigma*sigma); 
		residualhist->Fit("f1","QR");
		f1->GetParameters(&para[0]);  
		// 2nd fit      
		f1->SetRange(para[1]-Nsigma*para[2], para[1]+Nsigma*para[2]);  
		residualhist->Fit("f1","QR");                                     
		f1->GetParameters(&para[0]);                                  
		f1->SetRange(para[1]-Nsigma*para[2], para[1]+Nsigma*para[2]);
		f1->GetParameters(&para[0]);  
		TF1 *ftemp = new TF1("ftemp","[0]*exp(-0.5*((x-[1])/[2])**2)",para[1]-Nsigma*para[2],para[1]+Nsigma*para[2]);
		ftemp->SetParameters(para[0],para[1],para[2]);
		
		for(Int_t updowni=0;updowni<2;updowni++){
	
		correctionhist[updowni]->ProfileX();
		TH1D *htemp=(TProfile *)gDirectory->Get("correction"+TString::Format("%d%d",updowni,iteration)+"_pfx");
		Double_t par[8];
	 
		TF1 *f2 = new TF1("f2","[0]+[1]/sqrt(x)+[2]/x+[3]*x+[4]*pow(x,2)+[5]*pow(x,3)",0,5000000);
		
		htemp->Fit("f2","q","QRsame",0,70);
		htemp->Fit("f2","q","QRsame",0,70);  
		f2->GetParameters(&par[0]);


		if(iteration==Nbofiteration-1&&updowni==1){
		  for(Int_t i=0;i<nEntries;i++){
			 double cor=0;
			 // cor=par[0]+par[1]/sqrt(ratio[updowni][i])+par[2]/ratio[updowni][i]+par[3]*ratio[updowni][i]+par[4]*pow(ratio[updowni][i],2)+par[5]*pow(ratio[updowni][i],3);
			 cor=htemp->GetBinContent(htemp->FindBin(ratio[updowni][i]));
			 residual.at(i)=residual.at(i)-cor;
			 correctedmeasuredposhist[filearray[i]]->Fill(residual[i]+truthpos[filearray[i]]);
			 correctedresidualhist[filearray[i]]->Fill(residual[i]);
		  }
		}
		else{
		  for(Int_t i=0;i<nEntries;i++){
			 double cor=0;
			 // cor=par[0]+par[1]/sqrt(ratio[updowni][i])+par[2]/ratio[updowni][i]+par[3]*ratio[updowni][i]+par[4]*pow(ratio[updowni][i],2)+par[5]*pow(ratio[updowni][i],3);
			 cor=htemp->GetBinContent(htemp->FindBin(ratio[updowni][i]));
			 // residual[i]=residual[i]-cor;
			 residual.at(i)=residual.at(i)-cor;
			 // measuredpos.at(i)=residual.at(i)+truthpos[filearray[i]];
		  }
		}
		
		
		plotpara residualp1,correctionp1;
		// correctionp1.format=".png";
		correctionp1.xname="Center/Top Tower";
		correctionp1.yname[0]="Measured-Truth Position [cm]";
		correctionp1.textcontent="ECal: Before 2D correction";
		if(iteration==Nbofiteration-1)
		  correctionp1.textcontent="ECal: After 2D correction";
		correctionp1.titleoffsety[0]=0.95;
		correctionp1.leftmargin=0.095;
		correctionp1.rightmargin=0.125;
		correctionp1.statsxrange[0]=0.62;	correctionp1.statsxrange[1]=0.9;
		correctionp1.statsyrange[0]=0.66;	correctionp1.statsyrange[1]=0.93;
		if(plotdir!="")
		  correctionp1.plotname=plotdir+"slewing/scan"+TString::Format("%d%d",scani,updowni)+"corritr"+TString::Format("%d",iteration);
		Draw1TH2DWithPfTF(correctionhist[updowni],htemp,f2,correctionp1);
		
		// residualp1.format=".png";
		residualp1.SetStatsrange(0.1287625,0.5619546,0.4899666,0.9406632);
		residualp1.titleoffsety[0]=1.85;
		residualp1.leftmargin=0.17;
		residualp1.rightmargin=0.2-residualp1.leftmargin;
		residualp1.xname="Measured-Truth Position [cm]";
		residualp1.yname[0]="Entries";
		residualp1.SetStatsrange(0.62,0.56,0.97,0.94);
		if(iteration==0) residualp1.textcontent ="MRPC Experiment: Before slew";
		else residualp1.textcontent ="MRPC Experiment: After slew";
		if(plotdir!="")
		  residualp1.plotname=plotdir+"slewing/scan"+TString::Format("%d%d",scani,updowni)+"timeitr"+TString::Format("%d",iteration);
		Draw1HistogramWithTF1(residualhist,ftemp,residualp1);
		}
		iteration++;
		if(iteration==Nbofiteration){
		  posreso=para[2];////residualhist->GetRMS();
		  // posresoerror[scani]=posreso[scani]/sqrt(2*(residualhist->GetEntries()-1));
		}
		else if(iteration==1)
		  preposreso=residualhist->GetRMS();
	 }
  
  for(Int_t filei=0;filei<Nboffile;filei++){
	 uncorrectedmeasuredposarray[filei]=uncorrectedmeasuredposhist[filei]->GetMean();
	 uncorrectedresidualarray[filei]=uncorrectedresidualhist[filei]->GetMean();
	 // cout<<uncorrectedresidualarray[filei]<<endl;
	 correctedmeasuredposarray[filei]=correctedmeasuredposhist[filei]->GetMean();
	 correctedresidualarray[filei]=correctedresidualhist[filei]->GetMean();
  }

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
  p1.withline="true";
  p1.textcontent="ECal: interpolation correction method";
  p1.plotname=plotdir+"slewing/scan"+TString::Format("%d",scani)+"corrcompare";
  DrawNGraph(veccompareplotx,veccompareploty,2,vecNbofpoints,p1);

  p1.textcontent="ECal: interpolation";
  if(plotdir!="")
  p1.plotname=plotdir+"slewing/scan"+TString::Format("%d",scani)+"sinshape";
  Draw1Graph(uncorrectedmeasuredposarray,uncorrectedresidualarray,Nboffile,p1);
  
  // if(savetxt&&Nbofscan==6){
  // 	 ofstream outstd(txtdir+"resoforscansslewing.txt");
  // 	 outstd<<"scanid energy reso resoerror prereso\n";
  // 	 for(Int_t scani=0;scani<Nbofscan;scani++)
  // 		outstd<<scani<<" "<<posreso[scani]<<" "<<posresoerror[scani]<<" "<<preposreso[scani]<<"\n";
  // }

  return posreso;
}
