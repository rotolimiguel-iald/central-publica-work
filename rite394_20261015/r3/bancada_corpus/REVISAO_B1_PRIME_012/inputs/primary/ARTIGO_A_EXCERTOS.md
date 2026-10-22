# Artigo A — excertos primários lidos

Leitura de texto, sem executar/importar o programa. Não é auditoria da derivação variacional.

## Linhas 10106–10155

```text
10106: \end{equation}
10107: The four contributions play disjoint and complementary roles, described below.
10108: 
10109: \paragraph{Matter content.}
10110: $\mathcal{L}_{\text{matter}}$ contains the usual kinetic and potential terms
10111: of the Standard Model, minimally coupled to the metric:
10112: \begin{equation}
10113: \mathcal{L}_{\text{matter}} \;=\; \bar{\psi}\,(i\gamma^{\mu}D_{\mu} - m)\,\psi
10114: \;-\; \tfrac{1}{4}F_{\mu\nu}^{a} F^{a\,\mu\nu}
10115: \;-\; \tfrac{1}{2}|D_{\mu}\phi|^{2} - V(\phi),
10116: \end{equation}
10117: where $D_{\mu}$ is the gauge covariant derivative and $V(\phi)$ includes the
10118: Higgs sector.  \TGL{} preserves this structure intact in the bulk; the entire
10119: modification takes place at the modular boundary through the term
10120: $\mathcal{L}_{\text{modular}}$.
10121: 
10122: \paragraph{Luminodynamic field.}
10123: $\mathcal{L}_{\text{field}} = -\tfrac{1}{4}\Phi_{\mu\nu}\Phi^{\mu\nu}$ with
10124: $\Phi_{\mu\nu} = \partial_{\mu}\Psi_{\nu} - \partial_{\nu}\Psi_{\mu}$ is the
10125: luminodynamic field tensor, canonically conjugate to $\Psi^{*}$.  $\Psi$ is
10126: the \emph{boundary scalar field} whose coherent excitation realizes the
10127: \emph{boundary} mode of the modular operator $\Kpartial$
10128: (Section~\ref{sec:typeIII1}).  The choice $-\tfrac{1}{4}\Phi^{2}$ guarantees
10129: $U(1)$ gauge invariance and positive-definite energy along the boundary
10130: hypersurface.
10131: 
10132: \paragraph{Non-minimal gravitational coupling.}
10133: The gravitational piece couples $\Psi$ to the Ricci scalar $R$ via
10134: \begin{equation}
10135: \mathcal{L}_{\text{grav}} \;=\; \frac{1}{2\kappa^{2}}\,R
10136: \;+\; \xi \, R \, |\Psi|^{2},
10137: \qquad
10138: \xi \;=\; \tfrac{1}{6} \quad (\text{conformal coupling}),
10139: \end{equation}
10140: with $\kappa^{2} = 8\pi G/c^{4}$.  The conformal coupling $\xi = 1/6$ is
10141: selected because it guarantees invariance under Weyl transformations in the
10142: Bisognano--Wichmann limit, identifying $\Psi$ as the natural carrier of the
10143: discretized modular generator.  This coupling is what connects the
10144: \emph{geometry} (left-hand side of the Einstein equations) to the
10145: \emph{boundary operator} (right-hand side of the Lindblad equation).
10146: 
10147: \paragraph{Modular term --- the operational piece.}
10148: The \TGL{} modification is concentrated entirely in
10149: \begin{equation}
10150: \boxed{\;
10151: \mathcal{L}_{\text{modular}} \;=\;
10152: \mathcal{L}_{\Lambda\text{CDM}} \cdot \betatgl \cdot |1 + w_{\text{eff}}(z)|,
10153: \;}
10154: \label{eq:Lmodular}
10155: \end{equation}
```

## Linhas 10156–10218

```text
10156: where $w_{\text{eff}}(z)$ is the effective equation of state of the cosmic
10157: content at redshift $z$, and
10158: \begin{equation}
10159: \boxed{\;\betatgl \;=\; \alpha \cdot \sqrt{e} \;=\; """ + beta_val + r"""\;}
10160: \label{eq:beta-definition}
10161: \end{equation}
10162: is the programme's single dimensionless invariant constant.  The two inputs
10163: are $\alpha = 7.2973525693 \times 10^{-3}$ (fine-structure constant, CODATA
10164: 2018) and $\sqrt{e} = 1.6487212707\ldots$ (pure mathematics, free of
10165: dimensional ambiguity).  The term~\eqref{eq:Lmodular} vanishes in the pure
10166: state $w_{\text{eff}} = -1$ (cosmological constant) and saturates at
10167: $\betatgl \cdot |1+w|$ away from that point.  The Miguel angle
10168: (\emph{\^angulo de Miguel}) emerges from
10169: \begin{equation}
10170: \thetaM \;=\; \arcsin \sqrt{\betatgl} \;=\; """ + theta_deg + r"""^{\circ},
10171: \qquad
10172: 1 - \betatgl \;=\; \cos^2 \thetaM \;=\; """ + one_minus_beta + r""".
10173: \label{eq:theta-M}
10174: \end{equation}
10175: 
10176: \paragraph{Why $\sqrt{e}$, and not another factor? --- selection by half-nat.}
10177: The immediate objection to $\betatgl = \alpha\sqrt{e}$ is that the product of
10178: two dimensionless numbers could be numerology: why $\sqrt{e}$, and not
10179: $\varphi$, $\sqrt{2}$ or $\sqrt{\pi}$, which live in the same numerical
10180: neighbourhood ($\alpha\varphi = 0.01181$, $\alpha\sqrt{2} = 0.01032$)?  The
10181: answer is that $\sqrt{e}$ is \emph{selected by principle}, not by fit.  In
10182: natural-base information theory (unit: \textit{nat},
10183: $S = -k_B\sum p_i\ln p_i$), the identity
10184: \begin{equation}
10185: \ln\bigl(\sqrt{e}\bigr) \;=\; \ln\bigl(e^{1/2}\bigr) \;=\; \tfrac{1}{2}\ \text{nat}
10186: \label{eq:meio-nat}
10187: \end{equation}
10188: holds; that is, $\sqrt{e}$ is the magnitude factor corresponding to
10189: \textbf{exactly half a nat of information} --- the minimal entropic cost of a
10190: boundary$\leftrightarrow$bulk parity operation (an irreducible binary flip).
10191: It is the holographic analogue of the Landauer limit: just as erasing one
10192: classical bit costs at least $k_B T\ln 2$, projecting one holographic state
10193: from boundary to bulk costs at least $\tfrac{1}{2}$ nat (the Half-Nat,
10194: \emph{Meia-Nat}).  The candidates $\varphi$, $\sqrt{2}$, $\sqrt{\pi}$
10195: correspond to no informational cost at all --- only $\sqrt{e}$ reads as half
10196: a parity operation.  In quadratic form the selection is cleaner still:
10197: $\betatgl^{2} = \alpha^{2}\,e$, with no roots, linking the electromagnetic
10198: self-interaction ($\alpha^2$) directly to the entropic cost ($e$).  The full
10199: provenance (three independent derivations converging to
10200: $\betatgl \approx 0.012$ \emph{before} the factorization) is given in
10201: Section~\ref{sec:beta-posicionamento}.
10202: 
10203: \paragraph{Equation of motion.}
10204: Varying $\delta S / \delta \Psi^{*} = 0$ yields the modified equation for
10205: $\Psi$:
10206: \begin{equation}
10207: \bigl(\Box - m_{\Psi}^{2} - \xi R\bigr) \Psi
10208: \;=\; \betatgl \, \Kpartial \, \Psi,
10209: \label{eq:eom-Psi}
10210: \end{equation}
10211: where $\Kpartial$ is the modular generator discretized by the
10212: Bisognano--Wichmann theorem.  In the bulk, far from the boundary,
10213: $\Kpartial \to 0$ and the standard conformal Klein--Gordon equation is
10214: recovered.  At the boundary, $\Kpartial$ dominates and establishes the
10215: type III\textsubscript{1} structure demonstrated in
10216: Section~\ref{sec:typeIII1}.  The presence of $\betatgl$ as the sole coupling
10217: between $\Psi$ and $\Kpartial$ is the operational signature of \TGL{}.
10218: 
```

## Linhas 10219–10249

```text
10219: \paragraph{Status of the modular-operator $\to$ source-term bridge (honesty).}
10220: Eq.~\eqref{eq:eom-Psi} couples a field $\Psi(x)$ on the manifold to the
10221: operator $\Kpartial = -\log\Delta$, which lives in a von Neumann algebra
10222: (Section~\ref{sec:typeIII1}).  The passage from the abstract modular operator
10223: to the source term on the manifold has \emph{two distinct status levels},
10224: which we declare openly:
10225: \begin{itemize}[leftmargin=*]
10226: \item \textbf{Derived.} The \emph{cosmological} consequence of this bridge
10227: --- the modified Friedmann equation
10228: $H^2 = \tfrac{8\pi G}{3}\rho\,[1 + \betatgl|1+w_{\text{eff}}|]$
10229: (Eq.~\ref{eq:H-TGL}) --- is obtained thermodynamically from first principles
10230: via $dQ = T\,dS$ on the holographic screen --- a derivation of this
10231: programme, inscribed in this paper in layers (I)--(III) of the continuous
10232: bridge and in the local coupling theorem (Section~\ref{sec:smatrix}) ---,
10233: and the term $\betatgl|1+w|$ is the \emph{observable residue of the
10234: discretization} of the modular generator.  The proportionality constant
10235: $-2\pi/\hbar$ is fixed by the Bisognano--Wichmann theorem for Rindler wedges.
10236: \item \textbf{Declared conjecture.} The rigorous identification of the full
10237: apophatic operator with $-2\pi\Kpartial/\hbar$ \emph{in the continuum
10238: limit}, extended from Rindler wedges to general cosmological horizons, rests
10239: on a modular-universality hypothesis whose closure --- the explicit embedding
10240: of the master equation in a type III\textsubscript{1} algebra --- is an open
10241: technical problem, stated precisely in Section~\ref{sec:smatrix}.  We do not
10242: present it as demonstrated: it is the programme's identified conceptual
10243: bottleneck, and its closure is future work.
10244: \end{itemize}
10245: This distinction is deliberate: the testable cosmological face of the bridge
10246: is derived and validated (Section~\ref{sec:substrate-cosmo}); the full
10247: operatorial identification remains honest conjecture, not result.
10248: 
10249: \paragraph{Free-parameter count (with the due honest qualification).}
```

