"""Scope ledger to accompany the verified Lean candidate; not a scientific promotion."""
ANALYSIS={
 'classification':'PONTE PARCIAL',
 'normalization':{
  'chosen':'pPlus=E+p; pMinus=E-p; E=(pPlus+pMinus)/2; c=1 in the longitudinal module',
  'order_correction':'With normalized pPlus=(E+p)/sqrt(2), pMinus=(E-p)/sqrt(2), massSquared=2*pPlus*pMinus, not pPlus*pMinus. In four dimensions subtract transverse momentum squared.',
  'orientation':'theta(s)=existing boost(-s); therefore pPlus contracts by exp(-s). Rapidity s is not automatically the BW modular time t; BW convention involves 2*pi.',
  'dimensions':'A conversion from the numerical canonical trace to physical energy units is not experimentally calibrated here.'},
 'constructed_scope':[
  'Concrete DualScalingData on real longitudinal momenta, with actual imported boost and proven scaling.',
  'Fixed-by-every-boost implies zero pPlus via FalsidadeDaInercia; this is the stated Inertial definition, not Newtonian force-free motion.',
  'Invariant Lorentz quadratic form and observer-dependent energy; embedding uses two zero transverse coordinates in the already-chosen eta4.',
  'Explicit lift F_mu(a)=((tau(a)+mu/tau(a))/2,(tau(a)-mu/tau(a))/2) intertwines dual scaling with the boost.',
  'The lift is specialized to the existing regular-core finite-trace positive cone. Positive trace witnesses are reused, not assumed vacuous.',
  'The parameter mu remains free: distinct mu give distinct lifted masses when tau(a) is nonzero.',
  'For tau>0 and mu>=0 the lift lies in the future causal cone; outside these hypotheses the ambient real plane includes nonphysical vectors.',
  'Rest-energy identity uses a rest condition and nonnegative mass/energy. Scaling alone is not a selection of physical mass.'
 ],
 'no_go':'A positive dual-scaling weight cannot also be invariant along the same orbit. Thus it cannot equal a positive Lorentz-invariant rest mass on that orbit. A null component can scale; rest mass cannot.',
 'not_proved':[
  'The lift factors through tau; no injectivity, algebra equivalence, or identification of all core observables is proved.',
  'No equality of the dual action theta and the modular flow sigma is inferred from matching exponents.',
  'No empirically calibrated body, energy scale, transverse momentum distribution, or unique mass is selected.',
  'No new derivation of Lorentz signature from complete positivity or rank-four GKLS is supplied.',
  'No derivation of H3 or global solution of Einstein equations is supplied.'
 ],
 'clausius_named_residue':{
  'existing_flow':'ChatgptAudit.Flow020.screenHeatFlux = -rate*t*tensorQuad(T(curve(t)))(velocity(curve(t)))*inducedArea(t); constructedHeat integrates this expression.',
  'required_bridge':'A stress-energy realization of the lifted momenta with normalization, distribution, symmetric conserved tensor and identified null-screen flux.',
  'required_equilibrium':'MetricScreenClausius for every nonzero null direction at each point (the existing hclausius field), plus the hypotheses already stated by metric_einstein_from_screen_clausius.',
  'status':'OPEN in this delivery; these are named mathematical/physical requirements, not new Lean declarations or axioms.'},
 'debts_C':{
  'signature':'UNCHANGED. eta4 and its indefinite signature are inputs of the imported 4D representation. Preserving this form is not deriving it from a positive Kossakowski matrix.',
  'four':'UNCHANGED. Fin 4 is selected and the constructed momenta have zero transverse components. No theorem forces rank(c)=4 or discharges H2.'},
 'ordered_inventory':[
  {'class':1,'label':'EXISTE E ESTA LIGADO','items':'DualScalingData; existing boost; FalsidadeDaInercia; regularCoreDualScalingData; AgapeNonVacuity; eta4; boost_is_first_block. Scope: compiled candidate sandbox, not installed production.'},
  {'class':2,'label':'EXISTE NA BANCADA MAS NAO LIGADO','items':'Full mass-shell orbital transport shellMomentum_chart_shift; GeneralMetricClausius and ConstructedHeatPrimitive. A scalar trace lift does not consume their entire physical contract.'},
  {'class':3,'label':'SABIDO POR CITACAO','items':'AQFT interpretation of BW under its hypotheses, and physical interpretation of stress-energy and local-horizon equilibrium. Existing source citations are retained; this delivery does not independently audit literature.'},
  {'class':4,'label':'AUSENTE NO RECORTE CONSULTADO','items':'Canonical calibrated identification of this core trace with the momentum/stress of a specified physical body and derivation of its mass from the dual law alone. This is a scoped inventory conclusion, not a claim about the entire archive.'}
 ],
 'gate_changed':False,'production_installed':False,
 'integration':'Candidate for independent management audit; no Nos/um.py/git/site change.'}
