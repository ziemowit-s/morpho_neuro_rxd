  : setpointer syn.cp, precell.bouton.cai(0.5)

  NEURON {
      POINT_PROCESS SynACh
      RANGE g, tau
  }

  UNITS {
      (nA) = (nanoamp)
      (mV) = (millivolt)
      (uS) = (microsiemens)
  }

  PARAMETER {
      tau = 2000 (ms) <1e-9, 1e9>
  }

  ASSIGNED {

  }

  STATE {
      g (uS)
  }

  INITIAL {
      g = 0
  }

  BREAKPOINT {
      SOLVE state METHOD cnexp
      if(g > 1.0) {
  		g = 1.0
  	}
  	if(g < 0.0) {
  		g = 0.0
  	}
  }

  DERIVATIVE state {
      g' = -g/tau
  }

  NET_RECEIVE(weight (uS)) {
      g = g + weight
  }