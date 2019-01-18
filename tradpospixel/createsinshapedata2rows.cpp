Double_t pos[4]={14,10,6,2};
Int_t filestartid[2][2]={{8,14},{15,22}};
Int_t Nboffile[2];

void Getcalibratedposfor2rows(Double_t calibratedpos[2][8]){
  for(Int_t rowi=0;rowi<2;rowi++)
	 for(Int_t filei=0;filei<8;filei++)
		calibratedpos[rowi][filei]=16-(filei+filestartid[rowi][0])*0.5;
}
void createsinshapedata(TString rootdatadir="../../data/tradpospixel/rootdata/",TString txtdatadir="../../txt/tradpospixel/",Int_t scani=0){
  Nboffile[0]=filestartid[0][1]-filestartid[0][0];
  Nboffile[1]=filestartid[1][1]-filestartid[1][0];
  Int_t maxNboffile=max(Nboffile[0],Nboffile[1]);
  TFile* infile=new TFile(rootdatadir+"rootdata/lwaveform"+TString::Format("%d",scani+1)+"cutLED.root");
  Int_t fileid;
  Float_t intch[9];
  TTree* intree[2];
  TH1D* measuredposhist[2][maxNboffile];
  Double_t calibratedpos[2][8];
  for(Int_t rowi=0;rowi<2;rowi++)
	 for(Int_t filei=0;filei<maxNboffile;filei++)
		measuredposhist[rowi][filei]=new TH1D("measured"+TString::Format("%d%d",rowi,filei),"",100,-100,100);

  Getcalibratedposfor2rows(calibratedpos);
	
  for(Int_t rowi=0;rowi<2;rowi++){
	 intree[rowi]=(TTree*)infile->Get("wavetreerow"+TString::Format("%d",rowi+1));
	 intree[rowi]->SetBranchAddress("intch",intch);
	 intree[rowi]->SetBranchAddress("fileid",&fileid);
  
	 Int_t nEntries=intree[rowi]->GetEntries();
	 for(Int_t itr=0;itr<nEntries;itr++){
		intree[rowi]->GetEntry(itr);
		measuredposhist[rowi][fileid-filestartid[rowi][0]]->Fill(((intch[0]+intch[1]+intch[2])*pos[rowi]+(intch[3]+intch[4]+intch[5])*pos[rowi+1]+(intch[6]+intch[7]+intch[8])*pos[rowi+2])/(intch[0]+intch[1]+intch[2]+intch[3]+intch[4]+intch[5]+intch[6]+intch[7]+intch[8]));
	 }
  }
  Double_t measuredpos[2][maxNboffile],posresidual[2][maxNboffile];
  for(Int_t filei=0;filei<maxNboffile;filei++){
	 if(filei<Nboffile[0]){
		measuredpos[0][filei]=measuredposhist[0][filei]->GetMean();
		posresidual[0][filei]=measuredpos[0][filei]-calibratedpos[0][filei];
	 }
	 if(filei<Nboffile[1]){
		measuredpos[1][filei]=measuredposhist[1][filei]->GetMean();
		posresidual[1][filei]=measuredpos[1][filei]-calibratedpos[1][filei];
	 }
  }
  ofstream outstd(txtdatadir+"createsinshape"+TString::Format("%d",scani)+".txt");
  outstd<<"measuredposrow1 ";
  for(Int_t filei=0;filei<Nboffile[0];filei++) outstd<<measuredpos[0][filei]<<" ";
  outstd<<"\nresidualrow1 ";
  for(Int_t filei=0;filei<Nboffile[0];filei++) outstd<<posresidual[0][filei]<<" ";
  outstd<<"\nmeasuredposrow2 ";
  for(Int_t filei=0;filei<Nboffile[1];filei++) outstd<<measuredpos[1][filei]<<" ";
  outstd<<"\nresidualrow2 ";
  for(Int_t filei=0;filei<Nboffile[1];filei++) outstd<<posresidual[1][filei]<<" ";
  
  // plotpara p1;
  // p1.xname="Measured Position [cm]";
  // p1.yname[0]="Measured-Calibrated Position [cm]";
  // p1.textcontent="ECal: Interpolation correction";
  // p1.withline=true;
  // Draw1Graph(meanmeasuredpos,posresidual,Nboffile,p1);
}


void createfitpara(TString txtdir,Int_t scani){
  Nboffile[0]=filestartid[0][1]-filestartid[0][0];
  Nboffile[1]=filestartid[1][1]-filestartid[1][0];
  Int_t maxNboffile=max(Nboffile[0],Nboffile[1]);

  Double_t measuredpos[2][maxNboffile],posresidual[2][maxNboffile],fitparasummary[2][4];
  ifstream infile(txtdir+"createsinshape"+TString::Format("%d",scani)+".txt", ios::in);
  TString tmpstr;
  Double_t tmpdouble;
  
  infile>>tmpstr;
  for(Int_t filei=0;filei<Nboffile[0];filei++){
	 infile>>tmpdouble;
	 measuredpos[0][filei]=tmpdouble;
  }
  infile>>tmpstr;
  for(Int_t filei=0;filei<Nboffile[0];filei++){
	 infile>>tmpdouble;
	 posresidual[0][filei]=tmpdouble;
  }
  infile>>tmpstr;
  for(Int_t filei=0;filei<Nboffile[1];filei++){
	 infile>>tmpdouble;
	 measuredpos[1][filei]=tmpdouble;
  }
  infile>>tmpstr;
  for(Int_t filei=0;filei<Nboffile[1];filei++){
	 infile>>tmpdouble;
	 posresidual[1][filei]=tmpdouble;
  }
  infile.close();

  for(Int_t rowi=0;rowi<2;rowi++){
	 Double_t measure[Nboffile[rowi]],resi[Nboffile[rowi]];
	 TF1 *fsin = new TF1("fsin"+TString::Format("%d",rowi),"[0]*pow(x,0.1)*sin([1]*x+[2])+[3]",6,13.2);
	 TGraph* gr=new TGraph(Nboffile[rowi],measure,resi);
	 gr->Draw("AP");
	 gr->SetMarkerStyle(21);
	 gr->SetMarkerSize(1);
	 fsin->SetParameters(0.297527,1.60621,-0.314309,-0.729119);
	 // fsin->Draw("same");
	 gr->Fit("fsin"+TString::Format("%d",scani),"QR");
	 Double_t fitpara[4];
	 fsin->GetParameters(&fitpara[0]);
	 cout<<fitpara[0]<<" "<<fitpara[1]<<" "<<fitpara[2]<<" "<<fitpara[3]<<endl;
	 fitparasummary[rowi][0]=fitpara[0];
	 fitparasummary[rowi][1]=fitpara[1];
	 fitparasummary[rowi][2]=fitpara[2];
	 fitparasummary[rowi][3]=fitpara[3];
	 plotpara p1;
	 p1.xname="Measured Position [cm]";
	 p1.yname[0]="Measured-Calibrated Position [cm]";
	 p1.textcontent="ECal: Interpolation correction scan:"+TString::Format("%d",scani+1);
	 // p1.plotname=plotdir+"fitsin"+TString::Format("%d",scani+1);
	 p1.minortext=TString::Format("%.2f",fitpara[0])+"x^{0.1}sin("+TString::Format("%.2f",fitpara[1])+"x"+TString::Format("%.2f",fitpara[2])+")"+TString::Format("%.2f",fitpara[3]);
	 p1.SetMinorTextPosition(0.4,0.88);
	 Draw1GraphAndTF(measure,resi,Nboffile[rowi],fsin,p1);
  }
  // return fitparasummary;
  ofstream outstd(txtdir+"fitpara"+TString::Format("%d",scani)+".txt");
  outstd<<"[0]*pow(x,0.1)*sin([1]*x+[2])+[3]";
  for(Int_t rowi=0;rowi<2;rowi++){
	 outstd<<"\n";
	 for(Int_t k=0;k<4;k++) outstd<<fitparasummary[rowi][k]<<" ";
  }
}

  
