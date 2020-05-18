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

#ifndef ROO_PARABOLIC
#define ROO_PARABOLIC

#include "RooAbsPdf.h"
#include "RooRealProxy.h"
#include "RooAbsReal.h"
#include "TMath.h"
#include "RooMath.h"

class RooParabolic : public RooAbsPdf {
public:
  RooParabolic() {};
  RooParabolic(const char *name, const char *title,
	      RooAbsReal& _x,
	      RooAbsReal& _alpha,
	      RooAbsReal& _beta);

  RooParabolic(const RooParabolic& other, const char* name);
  inline virtual TObject* clone(const char* newname) const { return new RooParabolic(*this,newname); }
  inline ~RooParabolic() {}
  Double_t evaluate() const ;
  

  ClassDef(RooParabolic,2);

protected:

  RooRealProxy x ;
  RooRealProxy alpha ;
  RooRealProxy beta ;
  
};
 
#endif
