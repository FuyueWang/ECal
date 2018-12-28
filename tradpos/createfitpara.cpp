#include </home/ubuntu/fuyuew/mrpc/MRPCProject/plotfunctions.cpp>
void createfitpara(){
  TString thisdir="tradpos/";
  TString rootdatadir="../../data/"+thisdir,txtdir="../../txt/"+thisdir,plotdir="../../plot/"+thisdir;

  Int_t Nbofscan=6,filerange[2]={0,32};
  Int_t Nboffile=filerange[1]-filerange[0]+1;

  Double_t meanmeasuredpos[Nboffile],posresidual[Nboffile],fitparasummary[Nbofscan][4];

  for(Int_t scani=0;scani<Nbofscan;scani++){
	 ifstream infile(txtdir+"residualposVsmeasurescan"+TString::Format("%d",scani+1)+".txt", ios::in);
	 TString tmpstr;
	 Double_t tmpdouble;
	 infile>>tmpstr>>tmpstr;
	 for(Int_t filei=0;filei<Nboffile;filei++){
		infile>>tmpdouble; meanmeasuredpos[filei]=tmpdouble;
		infile>>tmpdouble; posresidual[filei]=tmpdouble;
	 }
	 infile.close();
	 TF1 *fsin = new TF1("fsin"+TString::Format("%d",scani),"[0]*pow(x,0.1)*sin([1]*x+[2])+[3]",3,13.2);
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
