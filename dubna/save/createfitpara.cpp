#include </home/ubuntu/fuyuew/mrpc/MRPCProject/plotfunctions.cpp>
void createfitpara(){
  TString thisdir="dubna/";
  TString rootdatadir="../../data/"+thisdir,txtdir="../../txt/"+thisdir,plotdir="../../plot/"+thisdir;

  Int_t Nbofscan=6,filerange[2]={0,10};
  Int_t Nboffile=filerange[1]-filerange[0]+1;

  Double_t meanmeasuredpos[Nboffile],posresidual[Nboffile],fitparasummary[Nbofscan][5],truthshift[Nbofscan];

  for(Int_t scani=0;scani<Nbofscan;scani++){
	 Double_t startfitrange=3;
	 // if(scani==2) startfitrange=4;
	 // else startfitrange=3;
	 ifstream infile(txtdir+"residualposVsmeasurescan"+TString::Format("%d",scani)+".txt", ios::in);
	 TString tmpstr;
	 Double_t tmpdouble;
	 infile>>tmpstr>>tmpstr>>tmpdouble;
	 truthshift[scani]=tmpdouble;
	 for(Int_t filei=0;filei<Nboffile;filei++){
		infile>>tmpdouble; meanmeasuredpos[filei]=tmpdouble;
		infile>>tmpdouble; posresidual[filei]=tmpdouble;
	 }
	 infile.close();
	 // TF1 *fsin = new TF1("fsin"+TString::Format("%d",scani),"[0]*pow(x,0.1)*sin([1]*x+[2])+[3]",startfitrange,13.2);
	 TF1 *fpoly = new TF1("polynominal"+TString::Format("%d",scani),"[0]/x+[1]*x+[2]*pow(x,2)+[3]*pow(x,3)+[4]",startfitrange,13.2);
	 TGraph* gr=new TGraph(Nboffile,meanmeasuredpos,posresidual);
	 gr->Draw("AP");
	 gr->SetMarkerStyle(21);
	 gr->SetMarkerSize(1);
	 fpoly->SetParameters(0.297527,1.60621,-0.314309,-0.729119);
	 // fsin->Draw("same");
	 gr->Fit("polynominal"+TString::Format("%d",scani),"QR");
	 Double_t fitpara[5];
	 fpoly->GetParameters(&fitpara[0]);
	 cout<<fitpara[0]<<" "<<fitpara[1]<<" "<<fitpara[2]<<" "<<fitpara[3]<<" "<<fitpara[4]<<endl;
	 fitparasummary[scani][0]=fitpara[0];
	 fitparasummary[scani][1]=fitpara[1];
	 fitparasummary[scani][2]=fitpara[2];
	 fitparasummary[scani][3]=fitpara[3];
	 fitparasummary[scani][4]=fitpara[4];
	 plotpara p1;
	 p1.xname="Measured Position [cm]";
	 p1.yname[0]="Measured-Calibrated Position [cm]";
	 p1.textcontent="ECal: Interpolation correction scan:"+TString::Format("%d",scani);
	 p1.plotname=plotdir+"fitsin"+TString::Format("%d",scani);
	 // p1.minortext=TString::Format("%.2f",fitpara[0])+"x^{0.1}sin("+TString::Format("%.2f",fitpara[1])+"x"+TString::Format("%.2f",fitpara[2])+")"+TString::Format("%.2f",fitpara[3]);
	 p1.SetMinorTextPosition(0.4,0.88);
	 p1.SetY1range(-3,3);
	 Draw1GraphAndTF(meanmeasuredpos,posresidual,Nboffile,fpoly,p1);
  }
  ofstream outstd(txtdir+"fitpara.txt");
  outstd<<"[0]/x+[1]*x+[2]*pow(x,2)+[3]*pow(x,3)+[4]";//"[0]*pow(x,0.1)*sin([1]*x+[2])+[3]";
  for(Int_t scani=0;scani<Nbofscan;scani++){
	 outstd<<"\n";
	 for(Int_t k=0;k<5;k++)
		outstd<<fitparasummary[scani][k]<<" ";
	 outstd<<truthshift[scani]<<" ";
  }
}
