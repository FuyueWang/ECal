#include </home/ubuntu/fuyuew/mrpc/MRPCProject/plotfunctions.cpp>
void slewingcorrection(){
  TString thisdir="tradpos/";
  TString rootdatadir="../../data/"+thisdir,txtdir="../../txt/"+thisdir,plotdir="../../plot/"+thisdir+"slewing/";
  TF1 *f1 = new TF1("f1","gaus");
  Int_t scani=1,filerange[2]={8,22},Nsigma=3,methodid=1;
  Int_t Nboffile=filerange[1]-filerange[0]+1;
  Double_t fitpara[6][4],rangefit[2]={3,14};
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
  
  Double_t truthpos[33];
  for(Int_t filei=0;filei<33;filei++)
	 truthpos[filei]=16-filei*0.5+fitpara[scani][3];
  

  Double_t uncorrectedmeasuredposarray[Nboffile],correctedmeasuredposarray[Nboffile],uncorrectedresidualarray[Nboffile],correctedresidualarray[Nboffile];
  TH1D* uncorrectedmeasuredposhist[Nboffile],*correctedmeasuredposhist[Nboffile],*uncorrectedresidualhist[Nboffile],*correctedresidualhist[Nboffile];

  for(Int_t filei=0;filei<Nboffile;filei++){
  	 uncorrectedmeasuredposhist[filei]=new TH1D("uncorrectedmeasuredposhist"+TString::Format("%d",filei),"",100,-100,100);
	 correctedmeasuredposhist[filei]=new TH1D("correctedmeasuredposhist"+TString::Format("%d",filei),"",100,-100,100);
	 uncorrectedresidualhist[filei]=new TH1D("uncorrectedresidualhist"+TString::Format("%d",filei),"",100,-100,100);
	 correctedresidualhist[filei]=new TH1D("correctedresidualhist"+TString::Format("%d",filei),"",100,-100,100);
	 // [filei]=new TH1D(""+TString::Format("%d",filei),"",100,-100,100);
  }

  TFile* inrootfile=new TFile(rootdatadir+"rootdata/lwaveform"+TString::Format("%d",scani+1)+"cutLEDless.root");
  TTree* intree=(TTree*)inrootfile->Get("wavetree");
  Int_t fileid;
  Float_t intch[9];
  intree->SetBranchAddress("intch",intch);
  intree->SetBranchAddress("fileid",&fileid);
  Int_t nEntries=intree->GetEntries();
  Double_t residual[nEntries],measuredpos[nEntries];
  Int_t filearray[nEntries];
  for(Int_t itr=0;itr<nEntries;itr++){
	 intree->GetEntry(itr);
	 if(fileid<filerange[0]||fileid>filerange[1]) continue;
	 if(fileid<15)
		measuredpos[itr]=((intch[0]+intch[1]+intch[2])*14+(intch[3]+intch[4]+intch[5])*10+(intch[6]+intch[7]+intch[8])*6)/(intch[0]+intch[1]+intch[2]+intch[3]+intch[4]+intch[5]+intch[6]+intch[7]+intch[8]);
	 else
		measuredpos[itr]=((intch[0]+intch[1]+intch[2])*10+(intch[3]+intch[4]+intch[5])*6+(intch[6]+intch[7]+intch[8])*2)/(intch[0]+intch[1]+intch[2]+intch[3]+intch[4]+intch[5]+intch[6]+intch[7]+intch[8]);
	 residual[itr]=measuredpos[itr]-truthpos[fileid];
	 filearray[itr]=fileid;
	 uncorrectedmeasuredposhist[fileid-filerange[0]]->Fill(measuredpos[itr]);
	 uncorrectedresidualhist[fileid-filerange[0]]->Fill(measuredpos[itr]-truthpos[fileid]);
  }

  Int_t iteration=0,Nbofiteration=3; 
  while (iteration<Nbofiteration){
	 TH1D* residualhist=new TH1D("residual","",70,-3.5,4.5);
	 TH2D* correctionhist=new TH2D("correction"+TString::Format("%d",iteration),"",14,1,15,70,-4,4);

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
		  residual[i]=residual[i]-cor;
		  correctedmeasuredposhist[filearray[i]-filerange[0]]->Fill(residual[i]+truthpos[filearray[i]]);
		  correctedresidualhist[filearray[i]-filerange[0]]->Fill(residual[i]);
		}
	 }
	 else{
		for(Int_t i=0;i<nEntries;i++){
		  double cor=0;
		  cor=htemp->GetBinContent(htemp->FindBin(measuredpos[i]));
		  residual[i]=residual[i]-cor;
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
	 correctionp1.plotname=plotdir+"scan"+TString::Format("%d",scani+1)+"corritr"+TString::Format("%d",iteration);
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
	 residualp1.plotname=plotdir+"scan"+TString::Format("%d",scani+1)+"timeitr"+TString::Format("%d",iteration);
	 Draw1HistogramWithTF1(residualhist,ftemp,residualp1);

	 iteration++;
  }

  for(Int_t filei=0;filei<Nboffile;filei++){
	 uncorrectedmeasuredposarray[filei]=uncorrectedmeasuredposhist[filei]->GetMean();
	 uncorrectedresidualarray[filei]=uncorrectedresidualhist[filei]->GetMean();
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
  p1.textcontent="ECal: interpolation correction method "+TString::Format("%d",methodid);
  p1.plotname=plotdir+"scan"+TString::Format("%d",scani+1)+"m"+TString::Format("%d",methodid)+"corrcompare";
  DrawNGraph(veccompareplotx,veccompareploty,2,vecNbofpoints,p1);
  


}
