void createfitpara(TString txtdir,Int_t scani){
  Int_t filestartid[2][2]={{8,14},{15,22}};
  Int_t Nboffile[2];
  Nboffile[0]=filestartid[0][1]-filestartid[0][0];
  Nboffile[1]=filestartid[1][1]-filestartid[1][0];


  Double_t meausredpos[2][maxNboffile],posresidual[2][maxNboffile];
  ifstream infile(txtdir+"createsinshape"+TString::Format("%d",scani)+".txt", ios::in);
  TString tmpstr;
  Double_t tmpdouble;
  
  infile>>tmpstr;
  for(Int_t filei=0;filei<Nboffile[0];filei++){
	 infile<<tmpdouble;
	 meanmeasuredpos[0][filei]=tmpdouble;
  }
  infile>>tmpstr;
  for(Int_t filei=0;filei<Nboffile[0];filei++){
	 infile<<tmpdouble;
	 posresidual[0][filei]=tmpdouble;
  }
  infile>>tmpstr;
  for(Int_t filei=0;filei<Nboffile[1];filei++){
	 infile<<tmpdouble;
	 meanmeasuredpos[1][filei]=tmpdouble;
  }
  infile>>tmpstr;
  for(Int_t filei=0;filei<Nboffile[1];filei++){
	 infile<<tmpdouble;
	 posresidual[1][filei]=tmpdouble;
  }

  









  
  TString thisdir="tradpos/";
  TString rootdatadir="../../data/"+thisdir,txtdir="../../txt/"+thisdir,plotdir="../../plot/"+thisdir;

  Int_t Nbofscan=6,filerange[2]={0,32};
  Int_t Nboffile=filerange[1]-filerange[0]+1;

  Double_t meanmeasuredpos[Nboffile],posresidual[Nboffile],fitparasummary[Nbofscan][4];

  for(Int_t scani=0;scani<Nbofscan;scani++){
	 Double_t startfitrange=3;
	 if(scani==2) startfitrange=4;
	 else startfitrange=3;
	 ifstream infile(txtdir+"residualposVsmeasurescan"+TString::Format("%d",scani+1)+".txt", ios::in);
	 TString tmpstr;
	 Double_t tmpdouble;
	 infile>>tmpstr>>tmpstr;
	 for(Int_t filei=0;filei<Nboffile;filei++){
		infile>>tmpdouble; meanmeasuredpos[filei]=tmpdouble;
		infile>>tmpdouble; posresidual[filei]=tmpdouble;
	 }
	 infile.close();
	 TF1 *fsin = new TF1("fsin"+TString::Format("%d",scani),"[0]*pow(x,0.1)*sin([1]*x+[2])+[3]",startfitrange,13.2);
	 TGraph* gr=new TGraph(Nboffile,meanmeasuredpos,posresidual);
	 gr->Draw("AP");
	 gr->SetMarkerStyle(21);
	 gr->SetMarkerSize(1);
	 fsin->SetParameters(0.297527,1.60621,-0.314309,-0.729119);
	 // fsin->Draw("same");
	 gr->Fit("fsin"+TString::Format("%d",scani),"QR");
	 Double_t fitpara[4];
	 fsin->GetParameters(&fitpara[0]);
	 cout<<fitpara[0]<<" "<<fitpara[1]<<" "<<fitpara[2]<<" "<<fitpara[3]<<endl;
	 fitparasummary[scani][0]=fitpara[0];
	 fitparasummary[scani][1]=fitpara[1];
	 fitparasummary[scani][2]=fitpara[2];
	 fitparasummary[scani][3]=fitpara[3];
	 plotpara p1;
	 p1.xname="Measured Position [cm]";
	 p1.yname[0]="Measured-Calibrated Position [cm]";
	 p1.textcontent="ECal: Interpolation correction scan:"+TString::Format("%d",scani+1);
	 p1.plotname=plotdir+"fitsin"+TString::Format("%d",scani+1);
	 p1.minortext=TString::Format("%.2f",fitpara[0])+"x^{0.1}sin("+TString::Format("%.2f",fitpara[1])+"x"+TString::Format("%.2f",fitpara[2])+")"+TString::Format("%.2f",fitpara[3]);
	 p1.SetMinorTextPosition(0.4,0.88);
	 Draw1GraphAndTF(meanmeasuredpos,posresidual,Nboffile,fsin,p1);
  }
  ofstream outstd(txtdir+"fitpara.txt");
  outstd<<"[0]*pow(x,0.1)*sin([1]*x+[2])+[3]";
  for(Int_t scani=0;scani<Nbofscan;scani++){
	 outstd<<"\n";
	 for(Int_t k=0;k<4;k++)
		outstd<<fitparasummary[scani][k]<<" ";
  }
}
