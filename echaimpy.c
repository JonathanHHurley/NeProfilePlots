//ECHAIM python wrapper
#include <stdio.h>
#include <stdlib.h>
#include "ECHAIM/ECHAIM.h"
#include "ECHAIM/errorCodes.h"

double* makeAltProfile(double start,double end,int steps)
{
  double* alloc = malloc(sizeof(double)*steps);
  for (size_t i = 0; i < steps; i++) {
    alloc[i] = start + i*((end - start)/500.0);
  }
  return alloc;
}


int main(int argc, char const *argv[]) {
  // float** testvar_re = alloc_2d_array_float(2,2);
  // fortranArrayToC_2D(testvar_re,testvar,2,2);
  // printf("Test %f %f %f %f\n",testvar_re[0][0],testvar_re[0][1],testvar_re[1][0],testvar_re[1][1] );
  // double* lat_d = fortranRealToDouble(lat,1);
  // double* lon_d = fortranRealToDouble(lon,1);
  // double* year_d = fortranRealToDouble(year,1);
  // double* month_d = fortranRealToDouble(month,1);
  // double* day_d = fortranRealToDouble(day,1);
  // double* hour_d = fortranRealToDouble(hour,1);
  // double* min_d = fortranRealToDouble(min,1);
  // double* sec_d = fortranRealToDouble(sec,1);
  //double* alt_d = fortranRealToDouble(alt,*l1);
  int storm,precip,dregion;

  double lat_d,lon_d,year_d,month_d,day_d,hour_d,min_d,sec_d;
  sscanf(argv[1], "%lf", &lat_d);
  sscanf(argv[2], "%lf", &lon_d);
  sscanf(argv[3], "%lf", &year_d);
  sscanf(argv[4], "%lf", &month_d);
  sscanf(argv[5], "%lf", &day_d);
  sscanf(argv[6], "%lf", &hour_d);
  sscanf(argv[7], "%lf", &min_d);
  sscanf(argv[8], "%lf", &sec_d);
  sscanf(argv[9], "%i", &storm);
  sscanf(argv[10], "%i", &precip);
  sscanf(argv[11], "%i", &dregion);

  double* alt_d = makeAltProfile(60,560,500);

  char **er; //error output

  double **output2;
  // int storm = 1; //storm perturbation flag
  // int precip = 1; //precipitation model flag
  // int dregion = 1; //d region model flag
  //Ask the model to log possible error codes
  logErrors(1);


  output2 = densityProfile(&lat_d, &lon_d, &year_d, &month_d, &day_d, &hour_d, &min_d, &sec_d, storm, precip, dregion, 1, alt_d, 500, 0);


  // er = getErrors();
  //
  // FILE *errorlog = fopen("echaimpyerrors.txt","w");
  //
  // for (int i=0; i<1; i++)
  // {
  //   fprintf(errorlog,"Error Codes: %c%c%c%c%c%c%c%c%c%c\n", er[i][0],er[i][1],er[i][2],er[i][3], \
  //     er[i][4],er[i][5],er[i][6],er[i][7],er[i][8],er[i][9]);
  // }
  //
  // fclose(errorlog);

  for (size_t i = 0; i < 500; i++) {
    printf("%lf ",output2[0][i] );
  }

  for (int i=0; i<1; i++) {free(output2[i]);}
  free(output2);
  return 0;
}
