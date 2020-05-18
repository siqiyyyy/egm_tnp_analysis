/*****************************************************************************
 * Project: CMS detector at the CERN
 *
 * Package: PhysicsTools/TagAndProbe/RooParabolic
 *
 *
 * Authors:
 *   Nadia Adam, Princeton - neadam@princeton.edu
 *   Adam Hunt, Princeton  - ahunt@princeton.edu
 *   Kalanand Mishra, Fermilab - kalanand@fnal.gov
 *
 * Description:
 *   Defines a probability density function which has exponential decay 
 *   distribution at high mass beyond the pole position (say, Z peak)  
 *   but turns over (i.e., error function) at low mass due to threshold 
 *   effect. We use this to model the background shape in Z->ll invariant 
 *   mass.
 * History:
 *   
 *
 *****************************************************************************/

#include "RooParabolic.h"

ClassImp(RooParabolic) 

 RooParabolic::RooParabolic(const char *name, const char *title, 
                        RooAbsReal& _x,
                        RooAbsReal& _alpha,
                        RooAbsReal& _beta) :
   RooAbsPdf(name,title), 
   x("x","x",this,_x),
   alpha("alpha","alpha",this,_alpha),
   beta("beta","beta",this,_beta)
 { } 


 RooParabolic::RooParabolic(const RooParabolic& other, const char* name):
   RooAbsPdf(other,name), 
   x("x",this,other.x),
   alpha("alpha",this,other.alpha),
   beta("beta",this,other.beta)
 { } 



 Double_t RooParabolic::evaluate() const 
 { 
  // ENTER EXPRESSION IN TERMS OF VARIABLE ARGUMENTS HERE 
  
  double ret = 1 + alpha*(x/80-1) + beta*(x/100-1)*(x/100-1);
  if (ret > 0) return ret;
  else return 0;
  return 1 + alpha*(x/80-1) + beta*(x/100-1)*(x/100-1);
 } 
