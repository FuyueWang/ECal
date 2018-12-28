struct modulemap{
  Int_t towerID[8][4]={{16,8,49,57},{15,7,50,58},{14,6,51,59},{13,5,52,60},{12,4,53,61},{11,3,54,62},{10,2,55,63},{9,1,56,64}};


}
void readtxtfile(){
  TString thisdir="ecalpos/";
  TString infiledir="../../data/"+thisdir,outdatadir="../../data/"+thisdir,outplotdir ="../../plot/"+thisdir,outtxtdir="../../txt/"+thisdir;
  
  Int_t NbofscanID=3,scanID[3]={59,60,61},startfileID[3]={179926,183015,191430},endfileID[3]={182152,185151,194436};


  for(Int_t scani=0;scani<NbofscanID;scani++){

	 for(Int_t fi=startfileID[scani];fi<endfileID[scani]+1;fi++){
		ifstream intxtfile(infiledir+"txtdata/"+"076d3e83_20180824_"+TString::Format("%d",fi));
		if(infiledir){

		}

  }










  
  Double_t waveform[60];
  Int_t moduleID;









if(!fin.eof())


  
ifstream fin(str.c_str());
 if(!fin)
 {
  cout <<"no such file,please check the file name!/n";
  exit(0);
 }
}
