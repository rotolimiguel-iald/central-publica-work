# Trechos metodológicos do artigo H0DN v1

Extração local de parágrafos, sem leitura ou ajuste de centros observados.

## 1. Report GitHub Issue

B The system of equations and the covariance matrix B.1 Linearity and Gaussianity B.2 Solution procedure B.3 Equations and covariance matrix B.3.1 Optimization parameters B.3.2 Host distance equations B.3.3 Host-group equations B.3.4 Calibrator equations B.3.5 Hubble flow B.3.6 The intercept equations B.3.7 Peculiar velocities B.3.8 Special cases Direct distance estimates for sources in the Hubble flow The Fundamental Plane of elliptical galaxies and the Coma cluster An H 0 H_{0} estimate without Hubble flow SNe Ia B.4 The system of equations in matrix form

## 2. Report GitHub Issue

C Literature comparison C.1 Literature Replication and Comparison for SNe Ia C.2 Understanding differences in H 0 H_{0} for past SN Ia-based ladders C.2.1 Refitting with new, SNooPy v2.7.0 C.2.2 Differences with Calibrator Sample Size C.3 Literature comparison for other distance indicators

## 3. Report GitHub Issue

F Additional details from the Distance Network: calibration parameters and host/calibrator distances F.1 Calibration parameters F.2 Host and calibrator distances

## 4. The Local Distance Network: a community consensus report on the measurement of the Hubble constant at ∼ \sim 1% precision

The direct, empirical determination of the local value of the Hubble constant ( H 0 H_{0} ) has markedly advanced thanks to improved instrumentation, measurement techniques, and distance estimators. However, combining determinations from different estimators is non-trivial, due to their correlated calibrations and different analysis methodologies. Using covariance weighting and leveraging community expertise, we constructed a rigorous and transparent Distance Network to find a consensus value and uncertainty for the locally-measured Hubble constant. A broad and comprehensive list of experts across all relevant distance measurement domains were invited to critically review the available data sets, spanning parallaxes, detached eclipsing binaries (DEB), masers, Cepheids, the Tip of the Red Giant Branch (TRGB), Miras, carbon-rich AGB stars (JAGB), Type Ia supernovae (SNe Ia), Surface Brightness Fluctuations (SBF), Type II supernovae (SNe II), the Fundamental Plane, and Tully-Fisher relations. Before any calculations, the group voted for first-rank indicators to define a ‘baseline’ Distance Network. Other indicators were included to assess the robustness and sensitivity of the results. We provide open-source software and data products to support full transparency and future extensions of this effort. Our key conclusions are: 1) The local H 0 H_{0} is robustly determined, with first-rank indicators internally consistent within their uncertainties; 2) A covariance-weighted combination yields a relative uncertainty of 1.1% (baseline) or 0.9% (all estimators); 3) The contribution from SNe Ia is consistent across four current compilations of optical magnitudes or using NIR-only magnitudes; 4) Removing either Cepheids or TRGB has minimal effect on the central value of H 0 H_{0} ; 5) Replacing SNe Ia with galaxy-based indicators changes H 0 H_{0} by less than 0.1 km ​ s − 1 ​ Mpc − 1 \,{\rm km\,s}^{-1}{\rm\,Mpc}^{-1} , while doubling its uncertainty; 6) The baseline result is H 0 H_{0} = 73.50 ± 0.81 ​ km ​ s − 1 ​ Mpc − 1 73.50\pm 0.81\,{\rm km\,s}^{-1}{\rm\,Mpc}^{-1} . Compared to early Universe+ Λ \Lambda CDM results, our result differs by 7.1 ​ σ 7.1\sigma from the CMB anisotropies within flat Λ \Lambda CDM, 67.24 ± 0.35 ​ km ​ s − 1 ​ Mpc − 1 67.24\pm 0.35\,{\rm km\,s}^{-1}{\rm\,Mpc}^{-1} from Planck+SPT+ACT [ 35 , Eq. (54) of] and 5.0 ​ σ 5.0\sigma from BBN+BAO within flat Λ \Lambda CDM from DESI DR2 [ 1 , 68.51 ± 0.58 ​ km ​ s − 1 ​ Mpc − 1 68.51\pm 0.58\,{\rm km\,s}^{-1}{\rm\,Mpc}^{-1} ; Tab. V of] . A networked approach, such as presented here, is invaluable for enabling further progress in Hubble constant measurements, providing much needed advances in accuracy and precision without overreliance on any single method, sample or group.

## 5. I.1 The ISSI Bern Workshop setup and philosophy

This was the underlying motivation and raison d’être for the workshop 1 1 1 https://workshops.issibern.ch/hubble-constant/ “What’s under the H0od?” held at the International Space Sciences Institute (ISSI) in Bern, Switzerland, in March 2025. The goal of this workshop was to arrive at a consensus set of ‘baseline’ and ‘variant’ datasets to include, to define statistically rigorous analysis procedures that account for dataset covariance, and to begin developing the open access tools required to measure H 0 H_{0} within a networked formalism. The Local Distance Network (Fig. 1 ) extends the distance ladder concept “horizontally” by linking multiple, overlapping calibration paths. It combines the statistical advantages of consistently averaging the contributions from multiple probes with the robustness to allow for the omission of any single probe. This is possible because there are multiple indicators that can serve the same methodological role (e.g., different anchors, different intermediate calibrators, different tracers of the Hubble flow, cf. Sect. II.1.1 ), as well as some parts of the distance network that require fewer connections or steps (megamaser distances, type II supernova modeling). This ambitious program required assembling the leading experts in each of the relevant reserach areas. The workshop conveners sought to leverage worldwide expertise across multiple tools as much as possible in selecting the ∼ \sim 40 in-person attendees invited to participate in the ISSI workshop (see Section VI for a list of attendees and their respective areas of expertise). Attention was given to inviting representatives from the most active groups in the field, including competing groups using similar or identical methods, in order to build consensus on how to consistently incorporate methods within the network and evaluate the level of agreement, especially in cases considered contentious in the literature. 2 2 2 Though the overall acceptance rate was high ( > > 90%), several invitees were unable to attend or declined participation in the workshop. Following the inclusive spirit of the workshop, opportunities for remote participation via Zoom and asynchronous participation by e-mail were offered in such cases. In the case where a group declined to participate in any format, their published data were still included to preserve their scientific contributions. The group thus assembled (i.e., we, the H 0 DN collaboration) placed emphasis on the methodology of combining datasets (i.e., the “how-to”), rather than on the results themselves, which were understood to be subject to quality and consistency checks (e.g., χ 2 \chi^{2} or residuals) and to be published irrespective of the resulting value of H 0 H_{0} .

## 6. II.1 The Local Distance Network

In recognition that the tension may be indicating something profound, greater reliability has been sought through an increasing number of different methods, sources, and measurements. These provide multiple, interrelated constraints for the same or different astrophysical sources, resulting in partially independent paths to H 0 H_{0} . Many of these approaches replace certain steps with alternative methods, sources, or calibrators. For this reason, we believe it is appropriate to consider these tools in aggregate to comprise a “Distance Network,” illustrated schematically in Fig. 1 , to better convey the interdependence of these methods. While such a goal was considered “lofty” and potentially unreachable more than a decade ago [cf. 48 , and Fig. 1 therein, originally credited to R. Ciardullo 40 ] , the improvements to the systematics of several distance measurement techniques — inspired not least by the Hubble tension — now provide a wealth of robust information that allow to again “diversify” the base on which the local measurement of H 0 H_{0} rests.

## 7. II.1 The Local Distance Network

The Distance Network provides two critical advantages on the path to a more accurate measurement of H 0 H_{0} : robustness (to reduce systematic errors) and statistical advantage (to reduce statistical uncertainties). Systematic errors can be recognized by the redundancy of methods allowing for analyses that “leave one out.” At the same time, redundancy offers the means to reduce statistical fluctuations through covariance-weighted averaging. Informally, method combination and robustness has been evaluated through the display of “whisker diagrams” which separate measurements of H 0 H_{0} by the combination of techniques they employ. Intermediate measure comparisons have also been made, most importantly by comparing multiple ways to measure distances to specific SN Ia hosts, each calibrated by the same geometric source (e.g., Cepheids, TRGB, Miras, and JAGB), though these involve only a fraction of the available data [ 172 ] . Formal covariance-weighting and combining has been attempted for only a limited set of indicators [ 169 ] .

## 8. II.1.1 Nomenclature and definitions

An astronomical object used in the calibration of a Secondary Distance Indicator, such as SNe Ia, SNe II, and galaxies with luminosity estimated via TF or SBF relations. A Calibrator is in a host (or is a host, when the Secondary Distance Indicator is based on the whole galaxy), and its distance is constrained by the host distance.

## 9. II.1.1 Nomenclature and definitions

A grouping (group or cluster) of galaxies that are assumed to be at a common distance, with appropriate dispersion due to depth effects. Group membership is used to obtain a distance estimate for some Calibrators, including SBF calibrators in Virgo and Fornax and FP calibrators in Coma.

## 10. II.1.1 Nomenclature and definitions

For each measured quantity, the original sources often define an uncertainty, which can be the combination (in quadrature) of several terms. For example, the uncertainty in a TRGB-based measurement of the distance to a host galaxy (calibrator) may combine at least three terms: the uncertainty in the geometric distance to the anchor, such as NGC 4258; the uncertainty in the apparent magnitude of the TRGB in the anchor; and the uncertainty in the TRGB of the calibrator itself. However, several of these terms may be in common with other data. For example, all distance estimates anchored to NGC 4258 share the variance associated with its geometric distance measurements, and all TRGB distances estimated relative to NGC 4258 share the uncertainty of the apparent TRGB magnitude determination in this galaxy. In order to make use of more than one such measurement, these terms must be included as covariances between the relevant data, and thus added as off-diagonal elements to a full covariance matrix of the data system. More details are given in the description of the equations in Section B .

## 11. II.1.1 Nomenclature and definitions

Based on the need to define covariance and successfully leverage a broad range of distance indicators, it is necessary to restrict the use of measurements to those with direct traceability to well-defined sources. Likewise, direct linkages assume consistent measurements between sources (e.g., Cepheids in an anchor and an SN Ia host), a reasonable assumption when both employ the same telescope and instrument. In contrast, the combination of measures from different telescopes and instruments involves substantial covariance (most certainly from different zeropoints) whose characterization is rarely provided in publications and is beyond the scope of this work to define. The above serve as “quality cuts” for the inclusion of data in the distance network. As an example, we make use of TRGB measurements in hosts calibrated with NGC 4258, where both are identically measured with HST (or JWST). However, we do not combine ground-based and space-based calibrations.

## 12. II.1.1 Nomenclature and definitions

Figure 2: The complete Distance Network, with all possible pathways illustrated. Anchors are objects that establish an absolute scale based on the methods shown to their left. Primary distance indicators (Cepheids, TRGB, Miras, JAGB) transfer the absolute scale to hosts (i.e., galaxies), the ensemble of which calibrates secondary distance indicators in the Hubble flow (tracers). Exceptions are Megamasers and astrophysically modeled SNe II, both of which serve as primary distance indicators and are capable of reaching the Hubble flow without intermediate steps. Green arrows illustrate direct connections between anchors or tracers and the method used to determine the absolute scale. Blue, violet, yellow, and red arrows show which calibrators constrain host distances; line width qualitatively distinguishes the attainable precision. Among hosts, rectangles qualitatively indicate overlap among objects measured via multiple methods. Diamond shapes represent groups. Dark gray arrows tie subsets of hosts whose distance is constrained by different calibrators to tracers. Any given arrow may represent multiple data sets, e.g., HST or JWST photometry of Cepheids, or optical vs. infrared photometry of SNe Ia. The number of hosts is labeled for Cepheids, TRGB, JAGB, and Miras, with the number of hosts exclusively available to each method shown in parentheses.

## 13. II.1.2 Distance Network Architecture

Given very few assumptions, 3 3 3 We make conventional assumptions common to distance ladders: that the cosmological principle holds so that we do not live in a special place (i.e., there is no intrinsic difference in objects solely based on their separation from us); that evolution over short lookback times, of order a few hundred Myr, is negligible; and that the expansion history for z < 0.15 z<0.15 can be approximated with an expansion of a few kinematic terms, namely H 0 H_{0} , q 0 q_{0} , and j 0 j_{0} . the measures and concepts given above may be linked together as a system of equations, as we will show below and in Appendix B , which we refer to as the Distance Network. The multiplicity of data (see Sect. III and Appendix A ) means we can optimize the system by introducing free global parameters. The wealth of sources, methodologies, and distance indicators also provide important additional and complementary information which can help strengthen the distance ladder or can contribute to constrain H 0 H_{0} . For example, the distance to a given supernova host can be measured via different methods (TRGB, Cepheids, JAGB, Miras) depending on which observations are available for that galaxy, and each method can be related to a different anchor. However, these determinations are not independent, as explained under “Use of Variance and Covariance” in Sect. II.1.1 . The full Distance Network is illustrated in Fig. 2 .

## 14. II.1.2 Distance Network Architecture

Within the approximations of the present analysis, all equations are linear (or linearized), and all probability distributions are Gaussian in magnitude, distance modulus, or log 10 ⁡ ( H 0 ) \log_{10}{(H_{0})} . Due to shared calibration sources among primary or secondary distance indicators, a covariance matrix with off-diagonal elements provides a useful method for proper accounting and weighting. The optimization procedure is that of a generalized linear least squares problem. The global solution to this problem provides best-fit values for the underlying parameters of the Distance Network as well as their uncertainties, most notably the distance moduli of included host galaxies, absolute magnitude calibrations, and the Hubble constant. These parameters include log 10 ⁡ ( H 0 ) \log_{10}{(H_{0})} , the distance moduli to host systems, μ host , ℋ \mu_{\mathrm{host},\mathcal{H}} , and groups included in the host data, μ 𝒢 \mu_{\mathcal{G}} , as well as the reference magnitudes for each type of calibrator, M ref , 𝒯 M_{\mathrm{ref},\mathcal{T}} . The full description of the system of equations and the covariance matrix is given in Appendix B . The employed data sets are listed in Table 1 , described briefly in Section III , and in greater detail in Appendix A .

## 15. II.1.2 Distance Network Architecture

Note. — (a) For the measurement of calibrators within the Milky Way galaxy, its extent is quite relevant — therefore we adopt the individual measurements standardized to a 1 kpc reference distance.

## 16. II.1.3 Selecting the baseline

There was strong consensus among the workshop participants, which is also shared more broadly within the community, that not all data, measurements, and tools are viewed with equal confidence. For this reason, we decided to produce a “baseline” result based on all methods which enjoy the broadest and highest level of confidence (sometimes referred to in the literature as “gold standards”), along with variants to the baseline that incorporate additional methods or datasets, or exclude certain data in order to reflect a broad range of minority viewpoints and explore the robustness of the results. To reach a true consensus for the baseline and variants, we adopted a collaborative, methodologically inclusive approach during the ISSI workshop “What’s under the H0od.” Prior to analyzing any combined fits, we engaged in extensive discussion of the various available methods, the choice of data sets (for instance, Cepheids from HST, TRGB distances from JWST, etc.), distance calibrators, and the systematic uncertainties involved in the determination of local distances and H 0 H_{0} . These included both classical and emerging techniques, ranging from geometric anchors (e.g., megamasers, Gaia parallaxes, detached eclipsing binaries) to stellar standard candles (e.g., Cepheids, TRGB, Miras, JAGB), as well as other methodologies such as Surface Brightness Fluctuations from HST and JWST and the Fundamental Plane from DESI. We also carefully reviewed the use of Type Ia and Type II supernovae, which extend the distance ladder into the Hubble Flow. In particular, we examined various SNe Ia data sets (e.g., Pantheon+, CSP, NIR-only samples) as well as SNe II determinations based on both the standard candle method and spectral modeling.

## 17. II.1.3 Selecting the baseline

Table 2: Result from anonymous vote on “technical readiness level” of distance calibrators. Above the line the consensus is that these will be included in the baseline, below the line will be included as variations.

## 18. Add-one-in variants

include additional information that was not voted for inclusion in the baseline, introduced through a step-by-step process. This category can introduce additional anchors (i.e., the SMC), as well as primary or secondary distance indicators. For example, V01 (Baseline+JAGB) adds JWST/NIRCam distances of the JAGB in supernova hosts calibrated to that in NGC 4258. The addition of calibrators to the baseline configuration serves to explore whether these supplementary methods shift or reinforce the baseline results. Furthermore, this category includes the incorporation of alternative distance indicators in the Hubble flow, such as SNe II calibrated via the standard candle method or spectral modeling, the Fundamental Plane from DESI anchored to Coma, and the Tully-Fisher relation as implemented in the Cosmicflows-4 catalog [ 114 , CF4;] .

## 19. Leave-one-out variants

involve the exclusion of individual methods or calibrators from the baseline configuration, motivated by the hypothesis that there is an undiscovered error in a type of measurement. Each variant is constructed by removing one key element at a time—such as Cepheids, SNe Ia, TRGB, Gaia parallaxes, or NGC 4258—and observing the resulting impact on the derived H 0 H_{0} value. These tests help identify whether any individual dataset or calibrator is significantly impacting the result. This category also includes the exclusion of specific indicators in the third rung, such as SBF, SNe Ia, and masers in the Hubble flow. Since leaving out a given element can implicitly remove other elements (e.g., specific SNe Ia calibrators), we have constructed custom baselines (cf. below) to separately assess the effect of the implicit (undesired) modification relative to the baseline.

## 20. Custom baselines

The exclusion of certain measurements can also cause the exclusion of some SNe Ia calibrators; for example, when Cepheid measurements are excluded, only 35 of the 55 SNe Ia calibrators in the baseline can be included, since the other 20 only have determinations of the host distances through Cepheids. The resulting change in the H 0 H_{0} value and uncertainty is due to both the exclusion of the measurements and the change in the SNe Ia calibrator sample. To cleanly separate the two effects, we define a custom baseline that includes those measurements, but is restricted to only the SNe Ia calibrators for which other measurements are available. Custom baseline versions are not variants per se ; they are only intended to facilitate the interpretation of the results for the corresponding variants.

## 21. Additional solutions

In addition to the variant solutions described above, we also consider special solutions designed to test our methodology. These are not “variants” in the same sense as those listed previously, and do not appear in Table 4 ; they are discussed in mode detail in Sections V.3.1 , V.3.2 , and Appendix C . They include independent grouping solutions , consistency checks , and emulator solutions . Independent grouping solutions consist of configurations in which two or more fully independent paths through the distance ladder are identified, sharing no common calibrators or intermediate steps. These allow for the construction of entirely separate determinations of H 0 H_{0} , such that agreement between them provides a strong consistency check and minimizes the risk of shared systematic effects. They are the analogous to splitting the data in uncorrelated halves or thirds. Two such variants are discussed in Section V.3.1 . Consistency checks are employed to make sure that the network results are statistically self-consistent for different paths through it and are further discussed in Section V.3.2 . Emulator solutions involve a set of emulators designed to reproduce key published results, such as SH0ES, CCHP, and recent SBF analyses, within our unified framework and dataset handling. These configurations serve both as validation tests of our pipeline and as transparent benchmarks for comparison with previous literature, and they may also help explain sources of differences. These are discussed in Appendix C .

## 22. III Datasets description

The analysis presented in this work is based on a comprehensive set of local distance measurements and their corresponding calibrators, as detailed in Section II and conceptually shown in Fig. 1 . The dataset includes a broad array of distance indicators, spanning geometric anchors, calibrators, and tracers. These are combined using a statistically rigorous framework that accounts for shared systematics and covariances among measurements. To maintain clarity and readability in the main text, we provide here only a brief summary of the datasets used to construct the Distance Network, summarized also in Table 1 . Methods employed in the baseline are marked in bold. A more detailed description of the individual measurements, sources, and associated assumptions is given in Appendix A . We employ peculiar velocity corrections as described in Appendix B.3.7 .

## 23. Mira distances

Miras are high-amplitude long-period variable asymptotic giant branch stars that obey period-luminosity relations. We use a sample of 3 Mira host galaxies consisting of the geometric anchor NGC 4258 [ 93 ] and two SNe Ia calibrator galaxies, NGC 1559 and M101 [ 94 , 95 ] , hosts of SN 2005df and SN 2011fe, respectively. All observations consisted of at least 10 epochs of HST WFC3/IR time series photometry spanning a minimum of one year, and distances were obtained using the Mira period-luminosity relation in the F160W bandpass.

## 24. Type Ia Supernovae (SNe Ia)

SNe Ia are standardizable candles whose light curve information (e.g., the duration) can be related to their intrinsic magnitude. We incorporate five different SNe Ia datasets, ranging from optical to near-infrared (NIR) wavelengths and spanning different SNe Ia modeling methodologies (Spectral template PCA with SALT2, SALT3 and SNooPy v2.7, and template-free with BayesSN). Four of these datasets are used in the Hubble Flow: (1) Pantheon+ (optical) with SALT2 [ 186 , 32 ] , (2) Carnegie Supernova Project (CSP) I & II (with SNooPy v2.7; C. R. Burns et al. 33 , S. A. Uddin et al. 204 ), (3) template-independent distances in NIR [ 76 ] , (4) optical+NIR samples processed with BayesSN [ 59 ] . A fifth dataset of 13 SNe Ia is used to calibrate the distance to the Coma cluster [ 187 ] .

## 25. Type II Supernovae (SNe II)

Several methods exist to standardize SN II magnitudes and derive distances (see T. de Jaeger & L. Galbany 49 ). In particular, the Standard Candle Method (SCM; M. Hamuy & P. A. Pinto 85 ) standardizes SN II luminosities based on correlations with photospheric velocity (from H β ) and color. We use a sample of 89 SNe II in the Hubble flow at z > 0.01 z>0.01 as well as 14 calibrator supernovae from T. de Jaeger et al. [55] , T. de Jaeger et al. [50] , compiled from CSP-I, LOSS, SDSS-II, SNLS, DES-SN, and SSP-HSC [ 52 , 53 , 55 ] .

## 26. Expanding photosphere method (EPM) of Type IIP supernovae

We adopted distances of Type IIP supernovae (SNe IIP) determined by astrophysical modeling via the tailored expanding photosphere method (EPM) from C. Vogl et al. [210] . Such distances relate the angular extent of SNe IIP measured from light curves to their physical expansion determined by radiative transfer modeling of optical spectra [ 208 , 44 ] . The EPM can be applied to SNe IIP in the Hubble flow without requiring additional calibration, although it depends on the accuracy of the underlying astrophysical modeling.

## 27. Surface Brightness Fluctuations (SBF)

Spatial fluctuations in the surface brightness of an otherwise smooth galaxy arise from the statistics of the discrete number of stars per pixel. The amplitude of these fluctuations depends inversely on the distance of the galaxy, as well as on age, metallicity, and other properties of the stellar population. For galaxies with evolved stellar populations, the SBF method can be calibrated through an empirical relation between the intrinsic magnitude of the fluctuations and the galaxy’s integrated color, used as a proxy for the stellar population properties. SBF measurements in the near-infrared are particularly useful because the fluctuations are bright at these wavelengths and can be well calibrated using optical colors. For this study, we use a sample of 61 HST WFC3/IR SBF elliptical galaxy distances reaching out to 100 Mpc [ 101 , 103 , 21 ] ; distances to the 14 calibrators in the Virgo and Fornax galaxy clusters are based on TRGB; see Appendix B.3.3 .

## 28. Tully-Fisher (TF)

The Tully-Fisher relation relates the rotation velocity of spiral galaxies (determined with HI line widths) to the total intrinsic luminosity. TF data were obtained from the Cosmicflows-4 catalog [ 114 ] , which compiled HI line widths, redshifts, and photometry for ∼ 10,000 \sim 10,000 spiral galaxies across the full sky, out of which we use 3400 galaxies with complete infrared photometry (as recommended by P. Boubel 2025, priv. comm.). The TF relation zero-point has been re-calibrated within the Distance Network using calibrator galaxies identified in P. Boubel et al. [23] , with systematic corrections applied by D. Scolnic et al. [185] .

## 29. IV Baseline Results

As described in Section II.1.3 , this solution includes SNe Ia, SBF, and megamaser measurements as Tracers. The distances to hosts of SNe Ia and SBF calibrators are obtained from the solution of the full Distance Network, incorporating measurements based on TRGB and Cepheids from the sources described in Section III , with the Milky Way, LMC, and NGC 4258 as anchors for Cepheid distances. 4 4 4 Note that the current version only uses TRGB measurements for the calibration of the SBF method, in accordance with the most recent publication [ 101 ] ; in future iterations we intend to allow for arbitrary primary distance indicators for the calibration. SNe Ia measurements are from the Pantheon+ sample, and peculiar velocity corrections in the Hubble flow are based on the 2M++ model [ 38 ] . This solution has an overall χ 2 \chi^{2} of 0.9879 per degree of freedom, indicating broad agreement between the estimated uncertainties—all based on original sources—and the statistical properties of the solution. Note that the value of χ 2 \chi^{2} does not include degrees of freedom associated with SNe Ia and SBF tracers in the Hubble flow. In our methodology, we solve separately for the Hubble flow intercept for SNe Ia and SBF tracers in the Hubble Flow—as well for others that are not included in the baseline solution, such as SNe II and TF tracers—and only the intercept is included in the final Distance Network solution. It can be shown that, apart from a separation of the χ 2 \chi^{2} values, this approach is equivalent to directly including the Hubble tracer equations into the Distance Network; see also Appendix B.3.6 .

## 30. IV Baseline Results

Figure 4 shows the residuals of host distances, estimated from the network solution, grouped by methodology. Each grouping, identified by a different color, refers to a specific combination of primary distance indicator, anchor, and source, as indicated in the labels below the group. The error bars shown correspond to the uncertainty of the specific distance measurement for that host, not including terms that are covariant with the other elements of the group. For example, each Cepheid measurement is shown with the uncertainty of the Period-Luminosity intercept for that galaxy, which reflects the expected scatter of residuals within that group . The color-shaded band for each group shows instead the uncertainty associated with common error terms for that group, i.e., the anchor uncertainty and the uncertainty in the indicator measurement (TRGB magnitude or Cepheid Period-Luminosity intercept) for that anchor, combined in quadrature; this term is indicative of the likely scatter of the average of the group---shown by the corresponding horizontal line at the center of the band---with respect to zero. 5 5 5 This is a slightly simplified description of the uncertainties, as it accounts for most, but not all, covariances in the data. However, it is a useful guide to the properties of residuals, as long as the formal χ 2 \chi^{2} is consistent with the statistics of the system. As can be seen, the distribution of residuals is consistent with expectations, with no significant deviation from the published uncertainties for any subset of data.

## 31. IV Baseline Results

Figure 5 shows the distribution of residuals for objects in the Hubble flow as a function of redshift for three classes of objects. The ordinate is the offset in log 10 ⁡ ( H 0 ) \log_{10}{(H_{0})} inferred for that specific object; the error bar reflects a combination of the measurement uncertainty (photometric error, error in standardization, and/or uncertainty in the solution, as applicable), the effect of the dispersion in peculiar velocities, the uncertainty in the peculiar velocity reconstruction, and the intrinsic dispersion in the relevant distance indicator, as determined in the original sources from the dispersion in the calibrators. They do not include the calibration uncertainty, which is determined as part of the distance network calibration solution for each group when applicable. The shaded bars at the right show the measured mean and dispersion for each of the three sets of data. Again, both the dispersion in individual measurements and the mean for each subset are consistent with expectations, which represent the direct measurement uncertainties for each value—not including calibration uncertainties. Figure 6 shows the posterior distribution for the global fit parameters for this solution: the absolute magnitude calibration for SNe Ia, the offset in the SBF calibration, the estimated distances to Virgo and Fornax, and the value of H 0 H_{0} . These are based on finite-length chains extracted from the probability distribution of the solution, and the values of the parameters may be slightly different from the analytically calculated results.

## 32. V Variants

Exploring variants to the baseline solution serves multiple purposes. First, several available methods and data sets were not included in the baseline solution, for various reasons—primarily because of maturity of analysis or questions about uncertainty estimates. These data can still be used to highlight potential issues with the baseline solution, or point toward future research directions. In some cases, additional observations may eventually justify including these methods in the baseline. Second, it is informative to assess what happens to both the value and uncertainty in the Hubble constant when different categories of data are included or excluded in the solution. Third, some methods — e.g., SNe Ia — can be included in several different ways; different filters, different light curve analysis, or different redshift selections. Finally, it is useful to consider a solution that includes all available, independent data and methods to assess the potential precision achievable with existing data once the remaining analysis issues are resolved. We stress that our process determined the baseline analysis as the primary solution priori to obtaining any results on H 0 H_{0} . Variants in these categories are defined in Section V.1 , and the results discussed in Section V.2 .

## 33. V.1 Description of variants

V04 Baseline + empirically calibrated SNe II: includes all baseline methods and adds SNe II (standard candle method) both as calibrators and in the Hubble Flow. SNe II host distances are determined via the distance network.

## 34. V.1 Description of variants

Baseline + empirically calibrated SNe II: includes all baseline methods and adds SNe II (standard candle method) both as calibrators and in the Hubble Flow. SNe II host distances are determined via the distance network.

## 35. V.1 Description of variants

V06 Baseline + Tully-Fisher: includes all baseline methods and adds calibrators for the Tully-Fisher relation and Tully-Fisher galaxies in the Hubble flow. The calibrators are treated in the same way as SNe Ia hosts, and their individual distances are determined from all available measurements.

## 36. V.1 Description of variants

Baseline + Tully-Fisher: includes all baseline methods and adds calibrators for the Tully-Fisher relation and Tully-Fisher galaxies in the Hubble flow. The calibrators are treated in the same way as SNe Ia hosts, and their individual distances are determined from all available measurements.

## 37. V.1 Description of variants

V13 Baseline without SNe Ia: excludes all SNe Ia, both as calibrators and as Hubble Flow objects.

## 38. V.1 Description of variants

Baseline without SNe Ia: excludes all SNe Ia, both as calibrators and as Hubble Flow objects.

## 39. V.1 Description of variants

V18 Exclude SN 1994D and earlier: excludes 7 SNe Ia calibrators that do not have modern data, namely SN 1980N, 1981B, 1981D, 1989B, 1990N, 1992A, and 1994D.

## 40. V.1 Description of variants

Exclude SN 1994D and earlier: excludes 7 SNe Ia calibrators that do not have modern data, namely SN 1980N, 1981B, 1981D, 1989B, 1990N, 1992A, and 1994D.

## 41. V.1 Description of variants

V08B Modified baseline for the no-Cepheid variant V08. This is identical to the baseline, except that SNe Ia for which we only have Cepheid distance estimates have been removed, leaving 35 SNe Ia calibrators. Comparing V08 and V08B allows a direct estimate of the impact of removing Cepheids from the distance network, without the effect of changing the subset of SNe Ia calibrators.

## 42. V.1 Description of variants

Modified baseline for the no-Cepheid variant V08. This is identical to the baseline, except that SNe Ia for which we only have Cepheid distance estimates have been removed, leaving 35 SNe Ia calibrators. Comparing V08 and V08B allows a direct estimate of the impact of removing Cepheids from the distance network, without the effect of changing the subset of SNe Ia calibrators.

## 43. V.1 Description of variants

V09B Modified baseline for the no-TRGB variant V09. This is identical to the baseline, except that SNe Ia for which we only have TRGB distance estimates have been removed, leaving 42 SNe Ia calibrators. Comparing V09 and V09B allows a direct estimate of the impact of removing TRGB from the distance network, without the effect of changing the subset of SNe Ia calibrators. However, this custom baseline includes SBF, which are excluded from V09 because they are calibrated using TRGB distances; therefore the difference between V09 and V09B is due to both the TRGB contribution to SN calibrator distances and to the omission of SBF.

## 44. V.1 Description of variants

Modified baseline for the no-TRGB variant V09. This is identical to the baseline, except that SNe Ia for which we only have TRGB distance estimates have been removed, leaving 42 SNe Ia calibrators. Comparing V09 and V09B allows a direct estimate of the impact of removing TRGB from the distance network, without the effect of changing the subset of SNe Ia calibrators. However, this custom baseline includes SBF, which are excluded from V09 because they are calibrated using TRGB distances; therefore the difference between V09 and V09B is due to both the TRGB contribution to SN calibrator distances and to the omission of SBF.

## 45. V.1 Description of variants

V12B Modified baseline for the no-NGC 4258 variant V12. This is identical to the baseline, except that SNe Ia for which we only have distance estimates based on NGC 4258 have been removed, leaving 42 SNe Ia calibrators. This variant allows a direct estimate of the impact of removing NGC 4258 from the distance network, without the effect of changing the subset of SNe Ia calibrators. Unlike V09B, this custom baseline also excludes SBF measurements; therefore the difference between V12 and V12B is only in the contribution of NGC 4258 to the distances to SNe Ia calibrators.

## 46. V.1 Description of variants

Modified baseline for the no-NGC 4258 variant V12. This is identical to the baseline, except that SNe Ia for which we only have distance estimates based on NGC 4258 have been removed, leaving 42 SNe Ia calibrators. This variant allows a direct estimate of the impact of removing NGC 4258 from the distance network, without the effect of changing the subset of SNe Ia calibrators. Unlike V09B, this custom baseline also excludes SBF measurements; therefore the difference between V12 and V12B is only in the contribution of NGC 4258 to the distances to SNe Ia calibrators.

## 47. V.1 Description of variants

V16B Modified baseline for the no-HST variant V16. This is identical to the baseline, except that SNe Ia for which we only have HST-based distance estimates have been removed, leaving 24 SNe Ia calibrators. Comparing V16 and V16B allows a direct estimate of the impact of removing HST measurements from the distance network, without the effect of changing the subset of SNe Ia calibrators.

## 48. V.1 Description of variants

Modified baseline for the no-HST variant V16. This is identical to the baseline, except that SNe Ia for which we only have HST-based distance estimates have been removed, leaving 24 SNe Ia calibrators. Comparing V16 and V16B allows a direct estimate of the impact of removing HST measurements from the distance network, without the effect of changing the subset of SNe Ia calibrators.

## 49. V.1 Description of variants

V22 Modified baseline, with SNeIa restricted to the CSP sample fit using SNooPy v2.7 for both calibrators and tracers.

## 50. V.1 Description of variants

Modified baseline, with SNeIa restricted to the CSP sample fit using SNooPy v2.7 for both calibrators and tracers.

## 51. V.1 Description of variants

V23 Modified baseline with SNe Ia measurements fitted using BayesSN for both calibrators and Hubble flow objects.

## 52. V.1 Description of variants

Modified baseline with SNe Ia measurements fitted using BayesSN for both calibrators and Hubble flow objects.

## 53. V.1 Description of variants

V24 Modified baseline, wherein SNe Ia light curves were fitted using the SALT V3 fitter instead of SALT V2.4 (as in Pantheon+)

## 54. V.1 Description of variants

Modified baseline, wherein SNe Ia light curves were fitted using the SALT V3 fitter instead of SALT V2.4 (as in Pantheon+)

## 55. V.1 Description of variants

V25 Modified baseline that exclusively uses H-band NIR measurements for both calibrators and Hubble flow SNe Ia.

## 56. V.1 Description of variants

Modified baseline that exclusively uses H-band NIR measurements for both calibrators and Hubble flow SNe Ia.

## 57. V.1 Description of variants

V26 Modified baseline that exclusively uses J-band NIR measurements for both calibrators and Hubble flow SNe Ia.

## 58. V.1 Description of variants

Modified baseline that exclusively uses J-band NIR measurements for both calibrators and Hubble flow SNe Ia.

## 59. V.1 Description of variants

V27 Modified baseline that ignores off-diagonal covariance terms for Hubble flow SNe Ia.

## 60. V.1 Description of variants

Modified baseline that ignores off-diagonal covariance terms for Hubble flow SNe Ia.

## 61. V.1 Description of variants

Figure 8: Baseline and variants results from Table 4 . For some variants, a labeled change has a secondary consequence (i.e., removing the identified primary distance indicator also results in the loss of calibration to some SN Ia). In these cases a dashed line immediately below such variants provides a custom baseline–i.e., the same SNe are removed before the removal of the primary indicator–is shown to provide a custom reference of impact for that variant; see text for details.

## 62. V.2.1 Adding one class at a time

Including the Tully-Fisher relation raises H 0 H_{0} by almost 0.5 km ​ s − 1 ​ Mpc − 1 \,{\rm km\,s}^{-1}{\rm\,Mpc}^{-1} ( ∼ 60 % \sim 60\% of the baseline error), and yields a reduced χ 2 \chi^{2} significantly larger than unity (1.4712). The increase in H 0 H_{0} is consistent with the results of the recalibration of the Tully-Fisher relation by [ 185 ] . Inspection of the residuals shows that the anomalous value of χ 2 \chi^{2} is caused by the dispersion in predicted magnitude for Tully-Fisher calibrators, whose empirical scatter significantly exceeds the assumed intrinsic dispersion, particularly at the bright end. Uncertainties in host distances are subdominant and unlikely to play a role in this comparison. We conclude that the internal dispersion currently assumed for the Tully-Fisher relation is likely underestimated, and recommend avoiding the inclusion of Tully-Fisher results until its intrinsic dispersion can be reevaluated.

## 63. V.2.2 Leave-one-out variants

Variants V08-V18 each remove one class of measurements or a subset of data from the solution. Most variants do not change the central value of H 0 H_{0} much, with the exception of V08 (no Cepheids), which drops it by almost 1 km ​ s − 1 ​ Mpc − 1 \,{\rm km\,s}^{-1}{\rm\,Mpc}^{-1} to 72.51 km ​ s − 1 ​ Mpc − 1 \,{\rm km\,s}^{-1}{\rm\,Mpc}^{-1} , and V12 (no NGC 4258), which decreases it to 73.08 km ​ s − 1 ​ Mpc − 1 \,{\rm km\,s}^{-1}{\rm\,Mpc}^{-1} . Comparing V08 and the corresponding custom baseline (V08B) clearly identifies that the shift in the no-Cepheids variant (V08) is driven by the implicit exclusion of 20 calibrator SNe Ia rather than by the Cepheids themselves. Analogous effects on H 0 H_{0} induced by subsampling SNe Ia calibrators have been extensively discussed in A. G. Riess et al. [172] . Accounting for this effect leaves a difference of merely 0.352 0.352 km ​ s − 1 ​ Mpc − 1 \,{\rm km\,s}^{-1}{\rm\,Mpc}^{-1} ( 44 % 44\% of the baseline error) due to excluding Cepheids.

## 64. V.2.2 Leave-one-out variants

Some variants yield significantly increased uncertainties on H 0 H_{0} . Excluding Cepheids (V08) increases the uncertainty from 0.81 to 1.30 km ​ s − 1 ​ Mpc − 1 \,{\rm km\,s}^{-1}{\rm\,Mpc}^{-1} , and comparison with the uncertainty of the custom baseline V08B (0.87) reveals that this increase is truly driven by the exclusion of Cepheids rather than the implicitly removed 20 SNe Ia calibrators. More modest increases occur for the variants without NGC 4258 as anchor, or when TRGB measurements are excluded. This is simply a reflection of the reduced constraining power caused by the exclusion of a broad class of measurements. Excluding either the Milky Way or the LMC as anchors has less impact, as each exclusion leaves two anchors for Cepheids, and does not affect the TRGB, which is only calibrated via NGC 4258. The most dramatic impact is associated with the exclusion of all SNe Ia; this increases the uncertainty to 1.79 km ​ s − 1 ​ Mpc − 1 \,{\rm km\,s}^{-1}{\rm\,Mpc}^{-1} , more than a factor of 2 above the baseline, illustrating the strong constraining power of SNe Ia, which remain the most powerful way to measure the local value of the Hubble constant. When SNe Ia are excluded from the baseline, the primary constraint on H 0 H_{0} is based on the SBF measurement. Even in this case, the central value of H 0 H_{0} is changed only little, although one naturally finds a much larger uncertainty. As an illustration, the solution including all other available data but excluding SNe Ia in the Hubble flow—formally not a variant, since it does not satisfy the criteria established during the Workshop—yields 75.29 ± 0.93 ​ km ​ s − 1 ​ Mpc − 1 75.29\pm 0.93\,\,{\rm km\,s}^{-1}{\rm\,Mpc}^{-1} ; despite the higher uncertainty, this value is still 8.1 ​ σ 8.1\,\sigma away from the CMB value in flat Λ \Lambda CDM.

## 65. V.2.2 Leave-one-out variants

The two variants V16 and V17 explore the impact of excluding all calibrator data from either HST or JWST, testing potential broad systematics, such as calibration errors, that affect either facility. Note that all primary distance indicators as included used space-based data from at least one of the two facilities. Excluding HST also implies excluding the Milky Way and the LMC as anchors, since we do not yet have a calibration for Cepheids in those systems based on JWST data. The solutions with either no HST or no JWST data are not fully disjoint since they share a common anchor, NGC 4258, and many of the Hubble Flow tracers, and since the set of calibrators overlap, carrying with them any intrinsic variance in their properties. However, many of the sources of uncertainty in distance estimates are different and independent. The resulting H 0 H_{0} values bracket the baseline, as could be expected, with a difference in line with their respective uncertainties: without HST, 73.75 ± 1.33 ​ km ​ s − 1 ​ Mpc − 1 73.75\pm 1.33\,\,{\rm km\,s}^{-1}{\rm\,Mpc}^{-1} ; and without JWST, 73.00 ± 0.86 ​ km ​ s − 1 ​ Mpc − 1 73.00\pm 0.86\,\,{\rm km\,s}^{-1}{\rm\,Mpc}^{-1} . Not surprisingly, the uncertainty in the result increases more if HST is excluded, since HST results use three anchors (only NGC 4258 is available for JWST) and more HST observations are available, yet both subsets remain close to the baseline with a difference below 1 ​ km ​ s − 1 ​ Mpc − 1 1\,\,{\rm km\,s}^{-1}{\rm\,Mpc}^{-1} . The fact that the inclusion of JWST observations favors a higher value of H 0 H_{0} corroborates the conclusion based on host-to-host distance comparisons by A. G. Riess et al. [172] that H 0 H_{0} measurements based purely on HST [ 169 ] are not biased high by the limited spatial resolution of WFC3/IR (crowding).

## 66. V.2.3 Alternate treatments

Variants V22-V27 are noteworthy because they explore different treatments of SNe Ia, which drive overall precision (cf. Sect. V.2.2 ). Variants V22 and V23 consider different light curve fitters (consistently for both calibrators and tracers), namely SNooPy v2.7 in V22 and BayesSN in V23. Both variants yield slightly higher H 0 H_{0} values with slightly larger nominal uncertainties. The BayesSN variant V23 furthermore yields a higher reduced χ 2 \chi^{2} . Further detail and comparisons with published articles is provided in App. C.2 , specifically concerning SNooPy in App. C.2.1 .

## 67. V.2.3 Alternate treatments

Variants V25 and V26 rely exclusively on NIR measurements for SNe Ia [ 76 ] , in the H H and J J band respectively. These also yield slightly lower, yet consistent H 0 H_{0} results with slightly larger uncertainties due to the smaller number of calibrators and Hubble flow tracers. Note that we did not use SNe Ia measurements from multiple sources (e.g., Pantheon+ and NIR) simultaneously in any solution; doing so would lead to unreliable, likely incorrect results. First, the calibration of SN measurements in different samples are inconsistent, as they are based on different filters, fitting processes, and conventions. More importantly, different measurements of the same SN would share to a large extent the astrophysical variance of the source; therefore we expect such measurements to be significantly correlated in their deviation from the mean, to an extent that; to the best of our knowlegde, has not been sufficiently quantified. Since the SNe Ia samples overlap significantly, multiple measurements cannot be included in the same solution in a statistically satisfactory way. To avoid such issues, we take care not to include multiple measurements of the same SNe Ia—whether as local calibrators or as Hubble flow objects—in the same solution. Unless otherwise stated, all solutions exclusively consider measurements collected in the Pantheon+ system [ 186 ] .

## 68. V.2.3 Alternate treatments

Another treatment option concerns the covariance between different SNe Ia in the Hubble flow. Several collections of measurements provide covariances between different objects; these can be due to the effect of standardization parameters, or the survey from which data have been obtained. By default, we include such covariances where available. However, Variant V27 deliberately ignores these covariances and assumes (incorrectly) the stated uncertainties to be independent in order to assess the impact that the SNe Ia covariances have on the final result. This results in a miniscule decrease in H 0 H_{0} , by less than 0.1 km ​ s − 1 ​ Mpc − 1 \,{\rm km\,s}^{-1}{\rm\,Mpc}^{-1} , and analogously miniscule decrease in the nominal uncertainty. We conclude that covariances between SNe Ia measurements in the Hubble flow currently have a negligible impact on H 0 H_{0} .

## 69. V.2.4 “Everything” solution

It is naturally interesting to consider the result of including all available methods into the Distance Network. To this end, we constructed variant V99 by including all available measurements. As noted above, multiple measurements of SNe Ia cannot be combined in a statistically satisfactory way, so that V99 exclusively considered Pantheon+ SNeIa. V99 also incorporates methods with as yet insufficiently well understood systematics, such as SN II with EPM and the Tully-Fisher relation. These results are provided here for completeness, and we recommend that they not be used for further analysis. The resulting value is 73.99 ± 0.70 ​ km ​ s − 1 ​ Mpc − 1 73.99\pm 0.70\,\,{\rm km\,s}^{-1}{\rm\,Mpc}^{-1} , which lies 8.7 ​ σ 8.7\,\sigma from the Planck+ Λ \Lambda CDM solution. We recognize that this solution may not be fully reliable, as indicated by the relatively large value of reduced χ 2 \chi^{2} , namely 1.3078 1.3078 per degree of freedom; indeed, this solution deviates from the baseline more than several others, primarily because of the TF contribution. Since the TF relation contributes the most to the excess χ 2 \chi^{2} , we also include variant V99a, which is identical to V99 except for the exclusion of TF calibrators and tracers. This variant results in H 0 = 73.66 ± 0.71 ​ km ​ s − 1 ​ Mpc − 1 H_{0}=73.66\pm 0.71\,{\rm km\,s}^{-1}{\rm\,Mpc}^{-1} , very close to the baseline with a 12% smaller uncertainty (and sub-percent precision on H 0 H_{0} ), has a reasonable reduced χ 2 \chi^{2} of 0.8943, and lies 8.1 ​ σ 8.1\,\sigma from the Plank+ Λ \Lambda CDM solution.

## 70. V.2.4 “Everything” solution

The everything solution is useful to understanding how elements in the baseline solution compare to the elements not included therein, as well as any covariances among them. Three figures illustrate these points. Figure 9 shows the fit residuals of host and calibrator distances for V99 in analogy with Fig. 4 for the baseline. Figure 10 illustrates the corresponding Hubble flow residuals for V99. A corner plot illustrating covariance among the main global fit parameters of the Distance Network for V99 is shown in Fig. 11 .

## 71. V.2.4 “Everything” solution

Figure 9: Residuals for host and calibrator distances for the “everything” solution. The groupings, also distinguished by color, correspond to calibrators measured by the same authors with common method and anchor. The error bars reflect the individual calibrator errors; the shaded areas for each group indicate the combined uncertainty in the anchor distance and its reference value, which are in common for all calibrators in the same grouping.

## 72. V.3.1 Orthogonal paths

• O2:(N4258+TRGB+SBF+MM) Uses N4258 as anchor, TRGB as calibrators, and SBF as tracers, in addition to megamasers. This corresponds to a modified V07 (baseline+SMC) from which all measurements correlated with O1 have been removed. This yields H 0 = 73.45 ± 1.78 ​ km ​ s − 1 ​ Mpc − 1 H_{0}=73.45\pm 1.78\,{\rm km\,s}^{-1}{\rm\,Mpc}^{-1} , with a χ 2 = 11.2 \chi^{2}=11.2 , and a reduced χ 2 \chi^{2} of 0.4853. The low reduced χ 2 \chi^{2} indicates that the measurement uncertainties used are overestimated.

## 73. V.3.1 Orthogonal paths

O2:(N4258+TRGB+SBF+MM) Uses N4258 as anchor, TRGB as calibrators, and SBF as tracers, in addition to megamasers. This corresponds to a modified V07 (baseline+SMC) from which all measurements correlated with O1 have been removed. This yields H 0 = 73.45 ± 1.78 ​ km ​ s − 1 ​ Mpc − 1 H_{0}=73.45\pm 1.78\,{\rm km\,s}^{-1}{\rm\,Mpc}^{-1} , with a χ 2 = 11.2 \chi^{2}=11.2 , and a reduced χ 2 \chi^{2} of 0.4853. The low reduced χ 2 \chi^{2} indicates that the measurement uncertainties used are overestimated.

## 74. V.3.1 Orthogonal paths

Fig. 12 illustrates the results of these orthogonal paths compared to the baseline result. Both O1 and O2 are highly compatible with each other, deviating by only 0.17 ​ σ 0.17\sigma despite representing fully independent measurements. As previously shown in the context of V13, the significantly higher uncertainty of O2 is due to the exclusion of SNe Ia. The orthogonal nature of O1 and O2 allows to compute their weighted average, H 0 O1 + O2 = ( 73.18 ± 0.82 ) ​ km ​ s − 1 ​ Mpc − 1 H_{0}^{\mathrm{O1+O2}}=(73.18\pm 0.82)\,{\rm km\,s}^{-1}{\rm\,Mpc}^{-1} , which agrees to within 0.3 0.3\, km ​ s − 1 ​ Mpc − 1 \,{\rm km\,s}^{-1}{\rm\,Mpc}^{-1} of the baseline. The slightly offset central value and reduced precision arise due to fewer internal cross-calibrations—their combination is missing for example any N4258-anchored calibrations of SNe Ia. This underlines a key advantage of the covariance-combined approach taken by the H0DN collaboration compared to independent pursuits of H 0 H_{0} .

## 75. V.3.1 Orthogonal paths

The two extensions to O2 considered, O2_V99a and VO2_V99, add elements from the “everything” variants (V99a, V99) to improve precision. Both extensions yield H 0 H_{0} values marginally higher than O2 and fully compatible with the respective “everything” variants V99 and V99a. The weighted average H 0 O1 + O2 ​ _ ​ V99a = ( 73.45 ± 0.74 ) ​ km ​ s − 1 ​ Mpc − 1 H_{0}^{\mathrm{O1+O2\_V99a}}=(73.45\pm 0.74)\,{\rm km\,s}^{-1}{\rm\,Mpc}^{-1} agrees to within < 0.5 ​ σ <0.5\sigma with V99a and features a very similar uncertainty. Finally, the weighted average including the Tully-Fisher relation, H 0 O1 + O2 ​ _ ​ V99 = ( 73.77 ± 0.71 ) ​ km ​ s − 1 ​ Mpc − 1 H_{0}^{\mathrm{O1+O2\_V99}}=(73.77\pm 0.71)\,{\rm km\,s}^{-1}{\rm\,Mpc}^{-1} , agrees to within 0.4 0.4 km ​ s − 1 ​ Mpc − 1 \,{\rm km\,s}^{-1}{\rm\,Mpc}^{-1} with V99, with also very similar uncertainty.

## 76. V.3.2 Paths based on subsets of data

In order to verify the internal consistency of different data sets and methods relevant to determining the Hubble constant, we show below the H 0 H_{0} values obtained for a set of ‘‘paths’’ through the network, each defined by a unique combination of anchors, calibrators, and tracers. 7 7 7 In practice we construct these paths as minimal combinations, except where this might lead to ambiguities. First we use each of the possible calibrator sets (e.g. Cepheids measured with HST, or Miras, or JAGB, etc.) together with the SNe Ia as Hubble flow tracers (13 combinations), then using the SNe II (either just with the minimal calibrator set from T. de Jaeger et al. [51] or with all available calibrators) (2 combinations), the megamasers alone, the SBF anchored using any hosts anchored by NGC 4258, and the SNII tailored EPM method (each 1 path), as well as the FP method anchored only by the SBF value (to remain minimal). In total that makes 19 paths through the network. These paths are not all statistically independent by definition, since they might share, for example, a common anchor or a common set of tracer objects. However, we expect the corresponding distribution of H 0 H_{0} values to align at least as well as for independent variables, since we expect the shared data to produce positive, not negative, correlations. In this case, the corresponding test statistics can be regarded as lower bounds on the true values that would be obtained if the full correlation structure were accounted for (i.e., in plain English: “if the points sharing the same data are incompatible, that’s even worse than points not sharing the same data being incompatible”). We find that the Anderson-Darling test cannot reject the null hypothesis of the paths stemming from a Gaussian distribution at 5% confidence level, and we find p = 86.3 % p=86.3\% for the Shapiro test, both very well within acceptable bounds. We also find no visually strong ( > 2 ​ σ ) (>2\sigma) outliers among the paths shown in Figure 13 . Note that since these paths are constructed always using minimal paths through the network, they explicitly do not qualify as ‘variants’ in the sense defined above. We also note that if we were to include the Tully-Fisher case in the generation of these paths, the results worsen quite a bit, to a p ≃ 10 % p\simeq 10\% for the Anderson-Darling test and a p ≃ 5 % p\simeq 5\% for the Shapiro test, showing once again the high discrepancy of the Tully-Fisher based results within the Distance Network.

## 77. V.3.2 Paths based on subsets of data

Figure 12: The two paths starting with “O” are proper orthogonal paths and can be taken as independent measurements of the Hubble constant. Their weighted mean (red) agrees well with our baseline result despite the latter including all cross-correlations. The shortcuts of the data sets are as defined in the text. The pie charts “fraction of data kept” represent the fraction of statistical power remaining in the path. It is computed as the fraction of the variance of H 0 H_{0} for the given result (in this way multiple datasets with the same constraining power in H 0 H_{0} will be assigned equal percentages). We show the percentages relative to the baseline result (V00).

## 78. V.3.2 Paths based on subsets of data

Figure 13: The statistical consistency of various individual paths through the network. These represent a set of paths that are highly correlated, and often only take a tiny part of the network into account. They are used for a statistical consistency check and should not be interpreted as valid variants in the sense of section II.1.4 . We also show the simple weighted mean of these paths in grey purely for visual purposes, reminding that due to their correlations (and selection effects) it need not necessarily agree with the baseline result. For details on the pie charts, see Fig. 12 .

## 79. VI Conclusions and Discussion

The Distance Network framework introduced here establishes a reproducible and extensible methodology for synthesizing local distance constraints. Its transparency and modularity allow for the straightforward integration of new data, methods, or calibrators, enabling the community to track the evolution of H 0 H_{0} estimates over time. In addition to the primary distance ladder, the network already incorporates several fully independent paths to H 0 H_{0} , including the maser-based anchor, the TRGB–SBF route, and SNe II distances based on astrophysical modeling. These methods rely on distinct physical assumptions and observational systematics, yet yield results consistent with the primary solution, reinforcing the robustness of the empirical determination. While current uncertainties for these paths are larger, their future competitiveness will depend on targeted improvements in calibration, modeling, and sample size. Promising opportunities include searches for SNe II in SBF or SNe Ia host galaxies, extending TRGB and Cepheid measurements deeper into the Hubble flow using ELTs, denser tiling of NGC 4258 to refine JAGB and TRGB calibrations, and establishing additional anchors via geometric methods [ 123 , e.g., using population-II pulsating stars calibrated by parallax, e.g.,] . Strengthening these independent routes and developing new anchors will be critical for validating and advancing precision cosmology. The approach presented here serves both as a benchmark of current capabilities and as a foundation for future consensus efforts in the determination of H 0 H_{0} .

## 80. VI Conclusions and Discussion

The Distance Network presented in this work provides the most precise direct measurement to date of the Hubble constant, H 0 = 73.50 ± 0.81 ​ km ​ s − 1 ​ Mpc − 1 H_{0}=73.50\pm 0.81\,\,{\rm km\,s}^{-1}{\rm\,Mpc}^{-1} , achieving a relative uncertainty of 1.09 % 1.09\% . This value is the result of a comprehensive, covariance-weighted combination of local distance measurements incorporating multiple distance indicators, each rigorously assessed for reliability, consistency, and methodological transparency. By explicitly accounting for shared uncertainties and correlations, the Distance Network formalism surpasses the precision of previous individual or pairwise combinations and reflects a collaborative consensus on data selection, treatment, and analysis strategy.

## 81. VI Conclusions and Discussion

In constructing the distance network, certain methodological deviations from state-of-the-art analyses were necessary to achieve full covariance treatment across indicators. For example, the use of supernova intercepts for calibration simplifies network integration but does not incorporate the full cross-rung covariance present in datasets such as Pantheon+, as done in A. G. Riess et al. [169] . These tradeoffs are explicitly documented to ensure transparency and reproducibility. We are publicly releasing the full Distance Network code upon acceptance of this paper at https://github.com/StefCas789/H0DN . We are planning to additionally publish the code in the Astrophysics Source Code Library 8 8 8 https://ascl.net – the corresponding DOI will be updated and linked here in a future version of the paper.

## 82. VI Conclusions and Discussion

A central feature of our approach is the construction of a baseline solution exclusively based on top-ranked calibrators and tracers, as determined by agreement among all authors as representatives of their respective communities. This was complemented by a suite of predefined variants, decided prior to conducting the analysis, which explore the sensitivity of the result to alternative assumptions, datasets, or methodological choices. The resulting spread in H 0 H_{0} values across all variants is significantly smaller than the statistical uncertainty of any individual variant, confirming that no single dataset or technique dominates the result and that the network solution is not driven by any particular methodology or systematic effect. This is also confirmed by investigating routes through the network that are designed to not have any elements in common, leading to results that are highly consistent with the baseline analysis.

## 83. References

[10] Anderson, R. I. 2019, Towards a 1% measurement of the Hubble constant: accounting for time dilation in variable-star light curves, A&A, 631, A165, doi: 10.1051/0004-6361/201936585

## 84. References

[20] Bhardwaj, A., Ripepi, V., Testa, V., et al. 2024, Cepheid Metallicity in the Leavitt Law (C-MetaLL) survey. V. New multiband (grizJHK s ) Cepheid light curves and period-luminosity relations, A&A, 683, A234, doi: 10.1051/0004-6361/202348140

## 85. References

[32] Brout, D., Taylor, G., Scolnic, D., et al. 2022b, The Pantheon+ Analysis: SuperCal-fragilistic Cross Calibration, Retrained SALT2 Light-curve Model, and Calibration Systematic Uncertainty, ApJ, 938, 111, doi: 10.3847/1538-4357/ac8bcc

## 86. References

[33] Burns, C. R., Stritzinger, M., Phillips, M. M., et al. 2011, The Carnegie Supernova Project: Light-curve Fitting with SNooPy, AJ, 141, 19, doi: 10.1088/0004-6256/141/1/19

## 87. References

[54] de Jaeger, T., Zheng, W., Stahl, B. E., et al. 2019, The Berkeley sample of Type II supernovae: BVRI light curves and spectroscopy of 55 SNe II, MNRAS, 490, 2799, doi: 10.1093/mnras/stz2714

## 88. References

[162] Riess, A. G., Kirshner, R. P., Schmidt, B. P., et al. 1999, BVRI Light Curves for 22 Type IA Supernovae, AJ, 117, 707, doi: 10.1086/300738

## 89. References

[186] Scolnic, D., Brout, D., Carr, A., et al. 2022, The Pantheon+ Analysis: The Full Data Set and Light-curve Release, ApJ, 938, 113, doi: 10.3847/1538-4357/ac8b7a

## 90. References

[195] Taylor, G., Lidman, C., Tucker, B. E., et al. 2021, A revised SALT2 surface for fitting Type Ia supernova light curves, MNRAS, 504, 4111, doi: 10.1093/mnras/stab962

## 91. References

[213] Wilson, R. E., & Devinney, E. J. 1971, Realization of Accurate Close-Binary Light Curves: Application to MR Cygni, ApJ, 166, 605, doi: 10.1086/150986

## 92. Systematic Corrections.

Well documented systematics of GEDR3 parallaxes were corrected using the formalism by L. Lindegren et al. [130, L21] , which considers source magnitude, color, and on-sky position (sine of ecliptic latitude). It is also well documented that additional corrections (known as a residual parallax offset ϖ corr \varpi_{\rm corr} ) are required at a sample level to ensure unbiased parallaxes [ 112 , 211 , 18 , e.g.,] . A. G. Riess et al. [160] simultaneously solved for the fiducial absolute magnitude of Cepheids and for ϖ corr \varpi_{\rm corr} for a sample of 75 field Cepheids observed photometrically with HST in the SH0ES Wesenheit index (a color-corrected magnitude, m H W m_{H}^{W} ) and found ϖ corr = − 14 ​ μ \varpi_{\rm corr}=-14\,\mu arcsec. For cluster members (used to infer parallaxes of cluster Cepheids), A. G. Riess et al. [169, R22] find no evidence for a residual parallax offset: the corrections from L. Lindegren et al. [130] effectively mitigate the parallax bias, as cluster members fall within the color and magnitude range of the sources used in its calibration. The cluster parallax uncertainty is a combination of the statistical uncertainty and the small-scale angular covariance, with the latter being the dominant term. Table 1 of A. G. Riess et al. [170] presents the mean parallaxes of 17 Cluster Cepheids from GEDR3 also observed photometrically with HST.

## 93. Assumptions.

For field Cepheids, we assume that the parallax as measured by GEDR3 has a normal distribution with central value equal to the reciprocal of the true distance plus the fixed offset ϖ corr \varpi_{\rm corr} discussed above, and width given by the nominal EDR3 parallax uncertainty for each source. The calibration of Milky Way Cepheids is obtained from the aggregation of all the measured parallax values, including parallax, photometric, and systematic uncertainties, and marginalized over the solution of the offset value. The uncertainty in the offset ϖ corr \varpi_{\rm corr} thus determined is therefore included in the final calibration uncertainty. For cluster Cepheids, the distance to each cluster is estimated from the aggregation of the parallax measurements for cluster stars; as noted above, cluster stars are generally within the applicability parameters of the standard offset determined in L. Lindegren et al. [130] . However, it is important to note that parallax uncertainties within a small angular region are significantly correlated; this correlation is included in the estimate of the combined uncertainty in A. G. Riess et al. [170] . Thanks to the combination of multiple sources, individual cluster parallaxes are typically a factor of three better than the nominal uncertainty for a single bright Cepheid.

## 94. Methodological Details.

Light curves and radial velocity curves were analysed simultaneously with the updated Wilson-Devinney code [ 213 ] in order to derive masses and radii of eclipsing binary components with a precision better than 3 percent. Interstellar extinction corrected photometric indices were used to derive angular diameters of components utilizing the SBCR calibrated by [ 149 ] . The geometric distance to a particular EB results from dividing a radius of a component by its angular diameter. Reddenings were determined by three independent methods using reddening maps [ 183 , 87 ] , the sodium doublet [ 138 ] and utilizing extinction-free photometric indices derived from analysis of decomposed spectra of components.

## 95. Methodological Details.

Cepheid pulsation periods are measured from HST optical broad band light curves (in host galaxies) and from well covered ground based light curves in the Milky Way and Magellanic Clouds. The brightness of each Cepheid is measured from optical and IR observations using HST or JWST, and epoch-corrected using the estimated amplitude and phase of the light curve obtained from optical data. Periods are known at the 10 − 4 10^{-4} day level for Cepheids in the MW and Magellanic Clouds and to 1–2% precision for those determined with HST in more distant hosts. A linear relation is fitted between the logarithm of the pulsation period and Cepheid brightness, which gives the Period-Luminosity slope and intercept. Intercept differences between the period-luminosity relations in two galaxies give their relative distance.

## 96. Overview.

Mira variables are fundamentally-pulsating Asymptotic Giant Branch stars that, similar to Cepheids, follow a period-luminosity Relation. Despite not being as widely-used or as well-understood as Cepheids, Miras still have two major advantages as independent calibrators of Type Ia SNe: 1) they have larger near-infrared amplitudes than Cepheids, allowing them to be characterized and detected using only near-infrared observations and 2) they are ubiquitous since they have low-to-intermediate masses (stars with initial masses ranging from 0.8 ​ M ⊙ < M < 8 ​ M ⊙ 0.8M_{\odot}<M<8M_{\odot} are expected to undergo a Mira phase of evolution), allowing them to be detected in galaxies not reachable by Cepheids. Miras are as bright as Cepheids in the near-infrared and brighter than all of the other commonly-used stellar distances indicators such as Tip of the Red Giant Branch, J-region Asymptotic Giant Branch, and RR Lyrae.

## 97. Data Sources.

• Pantheon+ (optical): The Pantheon+ sample of 1701 light curves of 1550 spectroscopically confirmed SNe Ia compiled from 18 different surveys. The sample itself and light curves are detailed in [ 186 ] , is cross-calibrated in [ 32 ] , and host-galaxy assignments and redshifts are updated in [ 37 ] . Pantheon+ utilize the SALT2 SN Ia model from [ 195 ] and apply bias corrections to the observed light-curve quantities following [ 151 , 150 ] . The entire analysis pipeline for Pantheon+ is automated in [ 89 ] which facilitated the systematic uncertainties described in [ 31 ] that are utilized for this work.

## 98. Data Sources.

Pantheon+ (optical): The Pantheon+ sample of 1701 light curves of 1550 spectroscopically confirmed SNe Ia compiled from 18 different surveys. The sample itself and light curves are detailed in [ 186 ] , is cross-calibrated in [ 32 ] , and host-galaxy assignments and redshifts are updated in [ 37 ] . Pantheon+ utilize the SALT2 SN Ia model from [ 195 ] and apply bias corrections to the observed light-curve quantities following [ 151 , 150 ] . The entire analysis pipeline for Pantheon+ is automated in [ 89 ] which facilitated the systematic uncertainties described in [ 31 ] that are utilized for this work.

## 99. Data Sources.

• CSP-I&II (optical+NIR): The Carnegie Supernova Project (CSP; M. Hamuy et al. 86 ) obtained high-quality light-curves of SNe Ia in u ​ B ​ g ​ V ​ r ​ i ​ Y ​ J ​ H uBgVriYJH bands from two observing campaigns between 2004 and 2015. The first observing campaign (CSP-I) ran from 2004 to 2009, and the second campaign (CSP-II) ran from 2011 to 2015. Light-curves from CSP-I are published in [ 115 ] , and spectroscopic analysis is described in [ 66 ] . While CSP-I followed up SNe Ia mostly from targeted search, CSP-II followed SNe Ia that are discovered from rolling search, primarily from La Silla Quest [ 15 ] . CSP-II is described in [ 92 ] and in [ 147 ] . Spectra of SNe Ia are published in [ 137 ] , and individual light-curves will be published (N. Suntzeff et al. 2026, in preparation) soon. An extensive analysis of Hubble constant using various distance calibrators is presented in [ 204 ] , where light-curve fitting parameters obtained from SNooPy [ 33 ] max_model method are available.

## 100. Data Sources.

CSP-I&II (optical+NIR): The Carnegie Supernova Project (CSP; M. Hamuy et al. 86 ) obtained high-quality light-curves of SNe Ia in u ​ B ​ g ​ V ​ r ​ i ​ Y ​ J ​ H uBgVriYJH bands from two observing campaigns between 2004 and 2015. The first observing campaign (CSP-I) ran from 2004 to 2009, and the second campaign (CSP-II) ran from 2011 to 2015. Light-curves from CSP-I are published in [ 115 ] , and spectroscopic analysis is described in [ 66 ] . While CSP-I followed up SNe Ia mostly from targeted search, CSP-II followed SNe Ia that are discovered from rolling search, primarily from La Silla Quest [ 15 ] . CSP-II is described in [ 92 ] and in [ 147 ] . Spectra of SNe Ia are published in [ 137 ] , and individual light-curves will be published (N. Suntzeff et al. 2026, in preparation) soon. An extensive analysis of Hubble constant using various distance calibrators is presented in [ 204 ] , where light-curve fitting parameters obtained from SNooPy [ 33 ] max_model method are available.

## 101. Data Sources.

• Template-independent distances in the NIR: A compilation of all publicly available SNe Ia with NIR observations was presented in [ 76 ] . These were selected for having pre-maximum data so the peak magnitude could be derived by simple Gaussian Process fitting. The sample include 19 SNe Ia in galaxies with Cepheid-based distances from SH0ES, and 55 SNe Ia in the Hubble flow ( z > 0.01 z>0.01 ). From those, all 19 SNe Ia in the calibrator sample have J J -band light curves, however only 16 have light-curves with enough quality in the H H band. Similarly, for the Hubble-flow sample, while 52 SNe Ia have good J J -band light-curves, 40 have H H -band light-curves that permit the determination of the peak-brightness. For the H 0 H_{0} determination, an intrinsic scatter of σ i ​ n ​ t \sigma_{int} of 0.125 mag was included in quadrature to the observed peak magnitude uncertainty. From the baseline analysis presented in [ 76 ] , in this paper we removed the term accounting for the SH0ES ladder in the systematic uncertainty budget (0.51 km s -1 Mpc -1 ), so the total systematic uncertainty here is 1.35 km s -1 Mpc -1 instead of the 1.44 km s -1 Mpc -1 used in [ 76 ] .

## 102. Data Sources.

Template-independent distances in the NIR: A compilation of all publicly available SNe Ia with NIR observations was presented in [ 76 ] . These were selected for having pre-maximum data so the peak magnitude could be derived by simple Gaussian Process fitting. The sample include 19 SNe Ia in galaxies with Cepheid-based distances from SH0ES, and 55 SNe Ia in the Hubble flow ( z > 0.01 z>0.01 ). From those, all 19 SNe Ia in the calibrator sample have J J -band light curves, however only 16 have light-curves with enough quality in the H H band. Similarly, for the Hubble-flow sample, while 52 SNe Ia have good J J -band light-curves, 40 have H H -band light-curves that permit the determination of the peak-brightness. For the H 0 H_{0} determination, an intrinsic scatter of σ i ​ n ​ t \sigma_{int} of 0.125 mag was included in quadrature to the observed peak magnitude uncertainty. From the baseline analysis presented in [ 76 ] , in this paper we removed the term accounting for the SH0ES ladder in the systematic uncertainty budget (0.51 km s -1 Mpc -1 ), so the total systematic uncertainty here is 1.35 km s -1 Mpc -1 instead of the 1.44 km s -1 Mpc -1 used in [ 76 ] .

## 103. Data Sources.

• SNe Ia in Coma: A sample of 13 SNe Ia located in the Coma Cluster was recently compiled by [ 187 ] , using data from multiple modern surveys including ATLAS and YSE. These SNe Ia were selected to be hosted by passive galaxies in the Coma cluster and are located at effectively the same redshift, providing a local standard-candle ensemble. Light curves are calibrated following the Pantheon+ framework.

## 104. Data Sources.

SNe Ia in Coma: A sample of 13 SNe Ia located in the Coma Cluster was recently compiled by [ 187 ] , using data from multiple modern surveys including ATLAS and YSE. These SNe Ia were selected to be hosted by passive galaxies in the Coma cluster and are located at effectively the same redshift, providing a local standard-candle ensemble. Light curves are calibrated following the Pantheon+ framework.

## 105. Systematic Corrections.

Systematic uncertainties include photometric calibration, light-curve model assumptions, and corrections for selection biases. These are treated internally within each analysis and propagated into the final uncertainties on H 0 H_{0} .

## 106. Data Sources.

The Type-II supernova sample used to derive distances through the SCM is almost the same as that in T. de Jaeger et al. [50] . This sample consists of 89 objects with z > z> 0.01 from various surveys, including the Carnegie Supernova Project-I (CSP-I; J. P. Anderson et al. 9 ), the Lick Observatory Supernova Survey (LOSS; T. de Jaeger et al. 54 ), the Sloan Digital Sky Survey-II SN Survey (SDSS-II; C. B. D’Andrea et al. 45 ), the Supernova Legacy Survey (SNLS; P. Nugent et al. 140 ), the Dark Energy Survey Supernova Program (DES-SN; T. de Jaeger et al. 55 ), and the Subaru Hyper Suprime-Cam Survey (SSP-HSC; T. de Jaeger et al. 53 ). Filters used include multiple optical bands (e.g., B B , V V , R R , I I , g g , r r , i i ). We exclude a total of four SNe II with Cepheid distances from the list in T. de Jaeger et al. [50] . The distances to three supernovae (SN 1999em, SN 1999gi, and SN 2012aw) were based on Cepheid measurements using optical images. These objects were removed for consistency with our baseline, for which all the Cepheid distances were derived using NIR images. Furthermore, SN 2005ay (NGC 3938) was also removed from the sample because it used the Cepheid distance to NGC 3982—both galaxies are part of the Ursa Major groups but are located in different subgroups (South and North, respectively). We add SN 2023ixf [ 216 ] which exploded in M101, a galaxy for which a Cepheid distance is available [ 169 ] . Finally, the four galaxies NGC 628, NGC 5194, NGC 6946, and NGC 7793 [ 50 , 5 SNe II used by] with TRGB measurements were re-scaled to the distances from G. S. Anand et al. [4] , which uses NGC 4258 as the TRGB zeropoint. Therefore, to calibrate the SN II absolute magnitude, we use a total of ten calibrators: four objects with Cepheid measurement, five SNe II with TRGB distances, and one in NGC 4258 with geometric maser distance.

## 107. Methodological Details.

We follow the methodology of T. de Jaeger et al. [55] to derive SN velocities, magnitudes, and colors. Expansion velocities are obtained using H β absorption via cross-correlation between observed spectra and an SN II template library. Light curves are modeled using hierarchical Gaussian Processes with the George Python library, allowing accurate interpolation of magnitudes and colors at fixed epochs (43 days post-explosion).

## 108. Connection to the Network.

The SN II tailored EPM method can be used to directly determine distances to objects in the Hubble flow. Currently, there is no overlap between the host galaxies used for the distance network and the SNe II modeling approach, however, they could serve as a calibrator in the future. An overlap between the network and the modeling of SNe II can be created by either finding new SNe II in host galaxies, by estimating further precise standard candle distances to hosts of modelable SNe II, or by observing siblings of SNe Ia and SNe II in the same host galaxy. All of these options will open new avenues in the distance network and are being actively pursued.

## 109. Comments and Known Issues.

While SBF is robust for early-type galaxies, its use is limited in spiral galaxies where star formation, clumpy dust, intermediate age asymptotic giant branch and young massive stars can all affect the RGB-based SBF fluctuation signal useful for determining the distance. The accuracy of SBF distances also depends on high-quality imaging and precise knowledge of the point spread function. The SBF method is potentially sensitive to calibration systematics from ( i ) (i) the uncertainty in the slope of the stellar population correction arising from the limited number of calibrators and their color range, and ( i ​ i ) (ii) the systematic uncertainty in the zero point calibration from TRGB measured in a single anchor galaxy (NGC 4258), and the potential differences between the TRGB brightness in that spiral galaxy and in the elliptical galaxies used to calibrate SBF.

## 110. Data Sources.

The primary dataset for TF measurements is Cosmicflows-4 (CF4; E. Kourkchi et al. 114 ), which represents the largest TF catalogue to date with approximately 10 000 spiral galaxies distributed across the full sky, out of which we only use around 3 400 with complete infrared photometry (as recommended by P. Boubel 2025, priv. comm.). The CF4 sample combines data from multiple surveys, incorporating HI line widths from various sources, optical photometry from the SDSS in the i − i- band, and infrared photometry from WISE in the W1-band.

## 111. Methodological Details.

The Tully-Fisher model assumed for this dataset is typically a linear relation with a quadratic term introduced at the bright end and an intrinsic scatter that decreases linearly with rotation velocity / luminosity [ 114 , 22 ] . In the Distance Network implementation, the distances of the calibrators are solved for explicitly in the same way as all other calibrators.

## 112. Appendix B The system of equations and the covariance matrix

Critically, we do include several off-diagonal terms in the covariance matrix of all equations, reflecting the fact that their uncertainties are correlated. The solution process also returns the covariance matrix for the optimized parameters, including the Hubble constant (more precisely, its logarithm).

## 113. B.1 Linearity and Gaussianity

In our approach, we adopt equations that are linear in distance modulus and linearized in the logarithm of quantities non-linearly related to distances, such as redshifts and H 0 H_{0} . We also assume that the probability distribution function of all measured quantities is Gaussian in this description, and therefore is fully described by a (non-diagonal) covariance matrix. Unfortunately, many original papers do not provide a full PDF for the quantities they measure, and they implicitly describe the errors as Gaussian; even if asymmetric confidence intervals are given, the lack of a full description of the PDF makes it challenging to go beyond the Gaussian approximation. However, most measured quantities have small enough fractional errors that the Gaussian approximation is accurate, especially in the aggregate; those with large fractional errors (and typically more non-Gaussian profiles) contribute only little to the final results. Finally, we note that most published data are already processed, incorporating uncertainties e.g. due to the underlying anchor. Therefore, we make sure to include the appropriate (see below) covariances for the published data according to how they were obtained from the original measurements. The most direct validation we have for all of the above approximations is our ability to recover the original results for all the examples considered in Appendix C . We note that the linearization naturally implies that results going out to many > 5 ​ σ >5\sigma should be interpreted with this caveat in mind. However, only slight changes could be introduced by these approximations, and we believe that our qualitative statements remain true even in more careful implementations.

## 114. B.2 Solution procedure

Given the measured data vector 𝐘 \mathbf{Y} with its associated (non-diagonal) covariance matrix 𝐂 \mathbf{C} we can construct a likelihood function as follows

## 115. B.2 Solution procedure

for some positive-definite, symmetric weight matrix W W ; here ( ) T ()^{T} indicates the transpose. By the Gauss-Markov theorem, the result of this minimization has the lowest variance if the weight matrix 𝐖 \mathbf{W} is the inverse of the covariance matrix 𝐂 \mathbf{C} of the data [ 3 ] ; in this case the quadratic form corresponds to the usual χ 2 \chi^{2} in Equation ( B1 ).

## 116. B.2 Solution procedure

However, a difficulty can arise in that the set of these equations is generally not linearly independent. The reason is that the same measured quantities can be combined in different ways to obtain constraints (i.e., equations); if the number of constraints exceeds the number of independent measurements, some of these constraints must be equivalent to a combination of others. For example, consider the case of Cepheid-related distance constraints based on different anchors. If we have, say, 30 host galaxies with measured intercepts of the Leavitt law, and 3 calibrations based on different anchors, we have a total of 33 independently measured quantities: the apparent magnitude of the intercept in the 30 host galaxies, and the calibrated absolute magnitude of the intercept in the three anchors. However, these result in 90 separate equations for the host distances, one for each combination of host and anchor (see also Section B.3.2 below); these equations are by necessity linearly dependent. Other dependencies are more subtle, and result from using the same host distance constraint for different types of calibrators. As a result, the covariance matrix 𝐂 \mathbf{C} , as constructed, is generally singular, as evidenced by extremely small (numerically consistent with zero) elements in the diagonal matrix of its singular-value decomposition. In our baseline case, we have 255 equations, but only 183 distinct measurements, resulting in 72 superflous/overconstrained equations.

## 117. B.2 Solution procedure

To address the issue, we replace the standard matrix inversion for the covariance matrix with its Moore-Penrose inverse [ 143 ] , also called pseudoinverse, computed, e.g., via the python routine scipy.linalg.pinv (see, e.g., R. Gommers et al. 80 ). In this implementation, the Moore-Penrose inverse is computed via singular value decomposition, but the singular values that are numerically consistent with zero are ignored, i.e., their inverse is set to zero. Other languages have similar implementations, and this computation can also be implemented using LAPACK routines (see, e.g., Lapack Contributors 120 ). The effect of using the Moore-Penrose inverse of the covariance matrix in Equation B1 is to ignore linearly-dependent equations in the computation of the χ 2 \chi^{2} , and reduce the problem to only linearly independent equations; this obviates the need to carry out a detailed analysis of all constraints.

## 118. B.3 Equations and covariance matrix

The form of each equation depends on which data and which parameters are involved. We have four main types of equations: host distance equations; host-group equations; calibrator equations; and Hubble flow equations. The host distance equations (Section B.3.2 ) relate the distance of each host to several published measurements, which are typically not independent; their correlations are accounted for in the covariance matrix, as discussed in the following. Host-group equations (Section B.3.3 ) relate the distance of each host in a group to the common distance of that group (or cluster). Calibrator equations (Section B.3.4 ) relate the absolute calibration of one of the secondary distance indicators—such as SNe Ia, SNe II, Surface brightness fluctuations, Tully-Fisher relation, and so on—to the distance of a host system obtained via the primary calibration method. Hubble Flow equations (Section B.3.5 ) relate the distance (typically a luminosity or angular diameter distance) of a calibrated secondary distance indicator to its redshift, and thus provides the connection to the Hubble constant. Some methods bypass some of these equations; for example, megamaser distances are calibrated directly, and directly provide a Hubble Flow equation without intermediate steps. Similarly, astrophysically calibrated SNe II (using the Expanding Photosphere method) connect directly to the Hubble flow. In such cases, the equations are modified accordingly; for example, Hubble flow equations for directly calibrated distances will not involve a host distance—see also Section B.3.8 for these special cases.

## 119. B.3.1 Optimization parameters

The quantity μ ℋ \mu_{{\cal H}} is the distance modulus of the host ℋ {\cal H} . This is defined on the basis of the geometric luminosity distance alone; the apparent magnitude m ℋ m_{{\cal H}} is expected to follow the simple relation m ℋ = M ℋ + μ ℋ m_{{\cal H}}=M_{{\cal H}}+\mu_{{\cal H}} , with any corrections due to extinction, redshift effects, and other standardization terms absorbed in the definition of the apparent or absolute magnitude, as appropriate. The reference absolute magnitude M ref , 𝒯 M_{{\rm ref},{\cal T}} for calibrator type 𝒯 {\cal T} is defined so that for each calibrator 𝒞 {\cal C} , the observed magnitude m 𝒞 m_{{\cal C}} is expressed as

## 120. B.3.1 Optimization parameters

For a calibrator 𝒞 {\cal C} within a given host ℋ ⁡ [ 𝒞 ] {\cal H}[{\cal C}] , this equation is used to determine the μ host , ℋ ⁡ [ 𝒞 ] \mu_{\mathrm{host},{\cal H}[{\cal C}]} .

## 121. B.3.1 Optimization parameters

• M ref , 𝒯 ( 𝒯 = 1 , … , N types ) M_{\rm ref,{\cal T}}\quad({\cal T}=1,\dots,N_{\rm types}) : the reference magnitude for each type of calibrator used in the solution. Calibrator types include SNe Ia, SNe II (calibrated empirically), SBF, and Tully-Fisher. For the sake of brevity, we synonymously refer to these as M Ia ≡ M ref , SNe ​ Ia M_{\rm Ia}\equiv M_{\rm ref,SNe~Ia} , M II ≡ M ref , SNe ​ II M_{\rm II}\equiv M_{\rm ref,SNe~II} , M SBF off ≡ M ref , SBF M^{\mathrm{off}}_{\rm SBF}\equiv M_{\rm ref,SBF} , M TF off ≡ M ref , TF M^{\mathrm{off}}_{\rm TF}\equiv M_{\rm ref,TF} , respectively.

## 122. B.3.1 Optimization parameters

M ref , 𝒯 ( 𝒯 = 1 , … , N types ) M_{\rm ref,{\cal T}}\quad({\cal T}=1,\dots,N_{\rm types}) : the reference magnitude for each type of calibrator used in the solution. Calibrator types include SNe Ia, SNe II (calibrated empirically), SBF, and Tully-Fisher. For the sake of brevity, we synonymously refer to these as M Ia ≡ M ref , SNe ​ Ia M_{\rm Ia}\equiv M_{\rm ref,SNe~Ia} , M II ≡ M ref , SNe ​ II M_{\rm II}\equiv M_{\rm ref,SNe~II} , M SBF off ≡ M ref , SBF M^{\mathrm{off}}_{\rm SBF}\equiv M_{\rm ref,SBF} , M TF off ≡ M ref , TF M^{\mathrm{off}}_{\rm TF}\equiv M_{\rm ref,TF} , respectively.

## 123. B.3.1 Optimization parameters

These are collectively indicated as X j X_{j} in Equation B3 . Other parameters—e.g., those describing the metallicity dependence of a class of calibrators, or other standardization parameters—can in principle be included. However, in the spirit of this study, we generally adopt whatever conventions and standardizations have been used in the original papers, and eschew re-characterizing the behavior of calibrators.

## 124. B.3.2 Host distance equations

with correspondingly A i eq , j = δ j , ℋ ⁡ [ i eq ] A_{{i_{\rm eq}},j}=\delta_{j,{\cal H}[{i_{\rm eq}}]} for this i eq {i_{\rm eq}} , and δ i ​ j = 1 \delta_{ij}=1 if i = j i=j and 0 otherwise. In order to construct the covariance for this set of equations, we note that the uncertainty of each measurement combines the measured uncertainty of the distance indicator (e.g., the TRGB magnitude or the Cepheid intercept) in the host, σ ℋ ⁡ [ i eq ] | 𝒫 ⁡ [ i eq ] \sigma_{{\cal H}[{i_{\rm eq}}]|{\cal P}[{i_{\rm eq}}]} ; the uncertainty of the same measurement in the anchor, σ 𝒜 ⁡ [ i eq ] | ℳ ⁡ [ i eq ] \sigma_{{\cal A}[{i_{\rm eq}}]|{\cal M}[{i_{\rm eq}}]} ; and the uncertainty in the distance modulus of the anchor itself, σ 𝒜 ⁡ [ i eq ] \sigma_{{\cal A}[{i_{\rm eq}}]} . Therefore the diagonal element of the covariance matrix is:

## 125. B.3.2 Host distance equations

The covariance between different equations i eq , j eq {i_{\rm eq}},{j_{\rm eq}} depends on which elements they have in common. If the anchor is the same, then the covariance includes the anchor distance uncertainty. If the MAS ℳ {\cal M} is the same, then the uncertainty of the measurement of the distance indicator in the anchor is in common. If two equations share the same host measured by the same method and source ( 𝒫 {\cal P} ) then the covariance includes the uncertainty of the distance indicator measurement within the host. Therefore:

## 126. B.3.3 Host-group equations

In some cases, especially for the Surface Brightness Fluctuations method, a distance estimate for a calibrator or host can come from its membership in a group or cluster. Most of the SBF calibrators are either in Fornax or in Virgo; some of them have direct distance estimates from TRGB, others do not. The assumption is that all objects within each of those clusters are at approximately the same distance, with a dispersion reflecting the estimated spatial extent of the cluster.

## 127. B.3.3 Host-group equations

with correspondingly A i eq , j = δ j , ℋ ⁡ [ i eq ] − δ j , 𝒢 ⁡ [ i eq ] A_{{i_{\rm eq}},j}=\delta_{j,{\cal H}[{i_{\rm eq}}]}-\delta_{j,{\cal G}[{i_{\rm eq}}]} and Y i eq = 0 Y_{i_{\rm eq}}=0 in this case. The uncertainty associated to this equation is the estimated dispersion σ ℋ , 𝒢 \sigma_{{\cal H},{\cal G}} of the distance modulus of host ℋ {\cal H} with respect to the distance of the group 𝒢 {\cal G} . This value can in principle be different for every member of the group; however, currently we assign the same uncertainty σ 𝒢 \sigma_{\cal G} to all hosts in the group, and assume the hosts are randomly distributed within that group (no non-diagonal elements in the covariance matrix). In the current treatment, this type of equation has no covariance with any other equation.

## 128. B.3.4 Calibrator equations

For every calibrator 𝒞 {\cal C} , we include an equation relating the distance modulus of its host and the quantity being calibrated, the reference magnitude M ref , 𝒯 M_{\rm ref,{\cal T}} , with the standardized apparent magnitude m 𝒞 m_{{\cal C}} . This quantity can be the reference magnitude for TF or SBF, the standardized absolute magnitude of a SN Ia or SN II in the appropriate band, or (in the case of BayesSN) a reference magnitude for the SN. These equations have in general negligible covariance in the data, but it is critical that the intrinsic dispersion in each calibrator’s distance estimate (e.g., the intrinsic variance in SNe Ia absolute magnitude, or the internal dispersion of the TF relation) be included in the uncertainty of each source. These uncertainties are reduced by using more calibrators. Distance calibration uncertainties are propagated from the uncertainty of the host distance modulus, which is derived from the distance network, and therefore are not included in the data covariance matrix.

## 129. B.3.4 Calibrator equations

The calibrator equations have the form:

## 130. B.3.4 Calibrator equations

where μ ℋ \mu_{{\cal H}} is the distance modulus parameter of the host ℋ {\cal H} in which the calibrator 𝒞 {\cal C} is located, which will be optimized from the global solution of the generalized least-squares problem. This equation can be recast in the form of Equation B3 as follows:

## 131. B.3.4 Calibrator equations

The variance associated with these quantities includes not only the contribution from the direct measurement process, such as the photometric uncertainty, but also the variance resulting from measurements of the standardization parameters, such as color and light curve width for SNe Ia, or the velocity width for Tully-Fisher. Those uncertainties are those reported in the original papers, unless otherwise stated. Critically, the variance must also include the intrinsic dispersion in that distance indicator—e.g., the scatter in standardized SN luminosities. or the dispersion in the velocity-based luminosity indicator from Tully-Fisher. This term is not always included explicitly in the uncertainties provided by the original sources, and in such cases it must be added in quadrature to the stated uncertainties. We assume that these equations have a diagonal covariance structure.

## 132. B.3.5 Hubble flow

In principle each tracer in the Hubble flow would add its own equation, and with the potentially hundreds to thousands of objects in the Hubble flow, this would greatly increase the size of the problem. Luckily, the additional equations are highly similar, and therefore allow a great simplification of the overall problem. Since the equations for this part of the problem are uncorrelated to the remaining system of equations (the covariance matrix is block-diagonal), this sub-problem can be treated independently. Additionally, the similarity of the equations can be expressed mathematically precisely as a rank deficiency of the coefficient matrix. We therefore first analyze such rank-deficient cases in general, and then apply our knowledge to the Hubble flow tracer equations.

## 133. B.3.5 Hubble flow

This establishes the equivalence between the full problem with coefficient matrix A A , parameter vector X X and data vector Y Y with inverse covariance matrix F = C − 1 F=C^{-1} and a smaller condensed problem with coefficient vector a a and a single data point y y with inverse covariance f f . Here f = ( b T ​ F ​ b ) f=(b^{T}Fb) and y = ( b T ​ F ​ Y ) / ( b T ​ F ​ b ) y=(b^{T}FY)/(b^{T}Fb) are both scalars – the new condensed covariance matrix and data point. Additionally Δ ​ χ 2 = ( Y T ​ F ​ Y ) − f ​ y 2 \Delta\chi^{2}=(Y^{T}FY)-fy^{2} is a parameter-independent offset of the χ 2 \chi^{2} function and correspondingly does not impact the overall parameter estimation. This means that instead of solving the full problem with many data points Y Y , one can solve the reduced problem with a single data point y y . Interestingly the value of the scalar y y is the solution to the independent χ 2 \chi^{2} optimization problem

## 134. B.3.5 Hubble flow

where y ^ = a 𝒯 + 5 \hat{y}=a_{\cal T}+5 is the so-called Hubble intercept for tracer type 𝒯 {\cal T} . For these reduced equations we use in analogy with Equation B13 the full covariance matrix of the m i m_{i} with possible peculiar velocity corrections (see below). For our full problem we can then reduce the additional equation to only

## 135. B.3.5 Hubble flow

with A i eq , j = δ j , log ⁡ H 0 − 0.2 ​ δ j , 𝒯 ⁡ [ i eq ] A_{{i_{\rm eq}},j}=\delta_{j,\log H_{0}}-0.2\delta_{j,{\cal T}[{i_{\rm eq}}]} , where a 𝒯 a_{\cal T} is the solution to the Hubble intercept sub-problem and its covariance is used for the full problem according to Equation B12 . Solving the equations determining the Hubble flow then boils down to solving the Hubble flow intercept problem of Equation B15 . We quickly note that the condensation procedure can be repeated independently for the independent tracer types, leading to one additional Hubble intercept equation and one independent Hubble intercept minimization problem per tracer type 𝒯 {\cal T} ; the form of the equation will differ for SBF and TF because of the form of their luminosity calibration.

## 136. B.3.6 The intercept equations

The variance of each data item m i − 5 ​ f ​ ( z i ) m_{i}-5f(z_{i}) combines: the measurement error for the indicator (typically a photometric error); the variance in the velocity function due to the uncertainty of the redshift (including any uncertainty in the peculiar velocity corrections); and the intrinsic width of the distance indicator, expressed in magnitudes. These variances are considered uncorrelated and added together. The elements entering the different intercept equations can (and typically do) have correlated errors; for example, uncertainties in the standardization parameter will propagate to all elements i i in ways that depend on how their properties were standardized, and sources from the same survey could have survey-systematics in common. However, this information is not always available. We have included covariance terms between SNe Ia according to the prescriptions of Pantheon+, resulting in a minor impact on the results; the change in H 0 H_{0} between including and excluding off-diagonal covariance terms is less than 0.1 ​ km / s / Mpc 0.1\,\rm km/s/Mpc (see V00 vs V27 in Table 4 ). In practice, for all secondary distance indicators in use the intrinsic dispersion of the calibration is significantly larger than any systematic covariance terms; only with very large number of sources could these covariances, which are not abated by simply increasing the number of sources, come into play. The uncertainty in the absolute calibration itself is part of the distance network system and is accounted as part of the default system of equations; it need not be included explicitly in the covariance matrix of the separated intercept equations.

## 137. The Fundamental Plane of elliptical galaxies and the Coma cluster

with Coma distance modulus μ Coma \mu_{\mathrm{Coma}} , SNIa reference magnitude M Ia M_{\rm Ia} , and individual supernovae magnitudes m i eq m_{i_{\rm eq}} , where we use the following list of 13 supernovae as part of the Coma cluster: [2019bkh, 2020ags, 2021dch, 2021lxb, 2022frn, 2023aakj, 2023czd, 2023epj, 2024ana, 2021oat, 2010ai, 2013ag, ASASSN-15jt]. Their absolute magnitude uncertainties include intrinsic dispersion but we do not model their correlations within Coma or with other calibrators. Following K. Said et al. [180] , we consider only the YSE measurement of SN 2021lxb.

## 138. B.4 The system of equations in matrix form

The following equatons show formally how the equations for hosts, calibrators, and Hubble flow objects fit into the system of equations for the distance network. Which equations are included of course depends on the specific variant chosen; for simplicity, we show the case in which Hubble flow objects in the same class are grouped in via their corresponding α 𝒪 \alpha_{\cal O} value.

## 139. C.1 Literature Replication and Comparison for SNe Ia

Given the dominant role of the SNe Ia in previous claims of a Hubble tension, we focus in this part of the appendix on the agreement of the SNe Ia-derived results by exploring a broader range of SN Ia light curve fitters and SN Ia calibration samples than those included in the main variants Section V that may help explain the origin of differences in H 0 H_{0} compared to literature studies.

## 140. C.1 Literature Replication and Comparison for SNe Ia

Figure 14: Comparison of the impact of supernova type Ia calibrator samples (sets of hosts) on the Hubble constant inference H 0 H_{0} , each one relative to the baseline result, for the various light curve fitting codes. The triangle shows a case where for the bayesSN fitter only 52 out of the 55 hosts was calibrated due to several missing supernovae in the fit, and the cross one where only 32 out of 35 hosts were calibrated. For details on the pie charts, see Fig. 13 . In this case we take 100% of the pies to be the case involving all supernovae data instead of the baseline.

## 141. C.1 Literature Replication and Comparison for SNe Ia

Table 5: Comparison of Hubble constant values (in km s -1 Mpc -1 ) from different supernova sets and calibrators. Note that for the same calibrator sets differences in the uncertainty stem mostly from the number of objects in the Hubble flow. SNooPy pre v2.7 is the one used in U24/F25. ∗ In this case only 52 out of the 55 calibrators could be matched with the given set of fitted SNeIa. + In this case only 32 out of the 35 calibrators could be matched with the given set of fitted SNeIa.

## 142. C.1 Literature Replication and Comparison for SNe Ia

First, we compare our distance network in the case that we only use type Ia supernovae as secondary distance indicators and in the Hubble flow. For this case, we can compare to three references, namely [ 169 , 59 , 71 ] . This comparison is graphically summarized in Figure 14 and Figure 16 , and the corresponding numbers can be found in Tables 5 and 9 . We observe that all comparisons agree between the publication and the Distance Network emulation within less than 0.15 ​ σ 0.15\sigma on the inferred value of H 0 H_{0} . In particular, when using only the 42 calibrators of [ 169 ] for Pantheon+ supernovae and adopting only the Cepheid calibration as in that study, we find H 0 = 73.17 ± 0.96 ​ km ​ s − 1 ​ Mpc − 1 H_{0}=73.17\pm 0.96\,{\rm km\,s}^{-1}{\rm\,Mpc}^{-1} where they find H 0 = 73.15 ± 0.97 ​ km ​ s − 1 ​ Mpc − 1 H_{0}=73.15\pm 0.97\,{\rm km\,s}^{-1}{\rm\,Mpc}^{-1} ( 0.02 ​ σ 0.02\sigma difference, 1% smaller uncertainty). Note that we compared to the results of [ 170 ] , as the Distance Network also includes the cluster Cepheids that tighten the calibration in the anchors. When comparing to the Cepheid-based results of [ 59 ] based on BayesSN supernovae, we find in this case H 0 = 74.67 ± 1.14 ​ km ​ s − 1 ​ Mpc − 1 H_{0}=74.67\pm 1.14\,{\rm km\,s}^{-1}{\rm\,Mpc}^{-1} where they find H 0 = 74.82 ± 1.28 ​ km ​ s − 1 ​ Mpc − 1 H_{0}=74.82\pm 1.28\,{\rm km\,s}^{-1}{\rm\,Mpc}^{-1} ( − 0.12 ​ σ -0.12\sigma difference, 11% smaller uncertainty). In this case, there is an additional caveat that [ 59 ] only used 41 calibrators whereas with the BayesSN supernova fitter we used 42 Cepheid calibrators in this case. Finally, when comparing to the 24 TRGB-calibrated SN Ia results of [ 71 ] (from HST or JWST), we find H 0 = 70.31 ± 1.80 ​ km ​ s − 1 ​ Mpc − 1 H_{0}=70.31\pm 1.80\,{\rm km\,s}^{-1}{\rm\,Mpc}^{-1} where they find H 0 = 70.39 ± 1.22 ​ ( stat ) ± 1.33 ​ ( sys ) ± 0.70 ​ ( σ SN ) ​ km ​ s − 1 ​ Mpc − 1 H_{0}=70.39\pm 1.22\mathrm{(stat)}\pm 1.33\mathrm{(sys)}\pm 0.70\mathrm{(\sigma_{\mathrm{SN}})}\,{\rm km\,s}^{-1}{\rm\,Mpc}^{-1} ( − 0.06 ​ σ -0.06\sigma difference, 0.3% smaller uncertainty when comparing the relevant uncertainties in quadrature). We can also compare the values of the calibration in these cases, finding for [ 169 ] M B = − 19.260 ± 0.027 M_{B}=-19.260\pm 0.027 ( − 0.18 ​ σ -0.18\sigma compared to M B = − 19.253 ± 0.027 M_{B}=-19.253\pm 0.027 ), for [ 59 ] Δ ​ M B = 0.039 ± 0.027 \Delta M_{B}=0.039\pm 0.027 ( + 0.4 ​ σ +0.4\sigma compared to Δ ​ M B = 0.030 ± 0.023 \Delta M_{B}=0.030\pm 0.023 , with one additional calibrator), and for [ 71 ] M B = − 19.186 ± 0.053 M_{B}=-19.186\pm 0.053 ( − 0.11 ​ σ -0.11\sigma compared to M B = − 19.18 ± 0.04 ​ ( statonly ) M_{B}=-19.18\pm 0.04\mathrm{(statonly)} ). We thus take as a noteworthy conclusion that the DN can accurately reproduce the individual distance ladder results based on the host distances, standardized SN magnitudes, and geometric calibrations used in these studies.

## 143. C.2.1 Refitting with new, SNooPy v2.7.0

An immediate challenge to comparing and extending the SN Ia results that make use of the SNooPy fitter (used in all CSP and CCHP studies) is both the absence of many useful SN calibrators in the S. A. Uddin et al. [204] (hereafter U24) the compilation that was used in [ 71 ] (hereafter F25) as well as the update to the SNooPy fitter to version v2.7.0 or later (since Aug 27, 2024)– with the prior version which we dub “pre v2.7” (the prior release was 2.5.3 Jan 29, 2020) that was used in U24 not readily accessible nor recommended for further use by its author. According to C. Burns who supports SNooPy development (private communication, 2025) current studies are advised to use the latest, v2.7.0. The most relevant update in v2.7 involves the method used by SNooPy to extrapolate the light curve templates beyond the training sample ( s ⁡ ( B − V ) < 0.3 s(B-V)<0.3 and s ⁡ ( B − V ) > 1.27 s(B-V)>1.27 ). Such SN Ia have light curves and inferred luminosities near the extrema of the distributions (often going by the name “91bg-like” at the faint and fast side and ”91T-like” at the bright and slow/high stretch side). This has very little affect on the calibrator sample (which are often pre-selected to be normal or near the middle of the distribution, see R22). However, the Hubble flow sample, and specifically the CSPII sample has a surprising abundance of “high-stretch” or 91T-like SNe Ia (U24). We find 18 18 supernovae in CSPII and 5 5 in CSP I (so 23 in all). Such SNe Ia will generally have s ⁡ ( B − V ) ≥ 1.15 s(B-V)\geq 1.15 for which the impact from the version update is quite large. The prior SNooPy version (pre v2.7) was found to over-correct these, motivating the revision to the fitter. For the updated SNooPy v2.7, prior fits with s ⁡ ( B − V ) ∼ 1.15 s(B-V)\sim 1.15 are lowered on average to s ⁡ ( B − V ) ∼ 1.0 s(B-V)\sim 1.0 (the fitted, apparent peak magnitudes are hardly impacted) and the implied reddening in B − V B-V is increased by ∼ \sim 0.04 mag. The net change comparing old and new follows as Δ ​ m ≈ 0.9 ⋅ ( 1.15 − 1.0 ) − 2.9 ⋅ ( − 0.04 ) ≈ 0.25 \Delta m\approx 0.9\cdot(1.15-1.0)-2.9\cdot(-0.04)\approx 0.25 mag (neglecting a small quadratic term in s ⁡ ( B − V ) s(B-V) for this illustration) for the high s ⁡ ( B − V ) s(B-V) supernovae with the new standardized magnitude being brighter (since a brightness previously attributed to over-luminosity and low extinction is now reflected in the newly, brighter standardized magnitudes). Specific examples which all have s ⁡ ( B − V ) > s(B-V)> 1.1 include CSP12G, CSP13Z, CSP13aad, LSQ12agd, LSQ12gef, LSQ12hxx, LSQ13dqh, and PTF14uo which all change by 0.2-0.3 mag in the same, brighter direction. As 91T’s represent ∼ \sim 8% of the CSP sample, we might expect a mean change of ∼ \sim 0.02 mag which is similar to the actual change from the new version of ∼ \sim 0.03 mag (which includes error weighting). This appears as an increase in the Hubble flow intercept of a B = 0.6843 ± 0.0025 a_{B}=0.6843\pm 0.0025 to a B = 0.6895 ± 0.0026 a_{B}=0.6895\pm 0.0026 ( + 2 ​ σ ) (+2\sigma) . As a result H 0 H_{0} increases by 1.0 km s -1 Mpc -1 due only to the change in the measurement of the Hubble flow for CSP from the new SNooPy.

## 144. C.2.1 Refitting with new, SNooPy v2.7.0

An independent consideration is that it is also necessary to use the newer SNooPy v2.7 to fit additional SN Ia calibrators not included in the U24 compilation produced from pre v2.7 SNooPy. New SNooPy v2.7 fits were thus made by C. Burns (private communication, 2025) using the versions of the light curves in the Pantheon+ light curve database, most of which are not CSP light curves. In the process a number of discrepancies were identified from the prior SNooPy fits in U24 and W. L. Freedman et al. [73] (hereafter F19). These were either the use of an older data release when a newer and better one was available (e.g., Cfa I from A. G. Riess et al. [162] did not employ host subtraction which was applied and released in A. G. Riess et al. [163] , A. G. Riess et al. [164] ), an inconsistency in a filter function definition (i.e., when older published data were provided after transformation to the Landolt/Bessel system, not the “natural” system, e.g., 1998bu and 2002fk) or the use of a broader set of optical light curves was available.

## 145. C.2.1 Refitting with new, SNooPy v2.7.0

These differences tend to pertain to older light curves from CfA I or LOSS , with changes in either direction, as tabulated in Table 6 .

## 146. C.2.1 Refitting with new, SNooPy v2.7.0

Due to the rarity of NIR light curves for calibrators which span decades and require data before NIR observations were common, to avoid introducing a systematic error (from the difference between optical and NIR calibration) we did not include NIR data for the CSP Hubble flow (in practice we found this difference is negligible). See however V.1 for variants that specifically use only NIR information for both calibrators and Hubble flow.

## 147. C.2.1 Refitting with new, SNooPy v2.7.0

The net change from SNooPy pre-v2.7 to post-v2.7 makes the mean calibrator fainter in M B M_{B} by 0.026 mag for the F25 sample of 24 24 SNeIa and 0.019 mag for the full in-common sample of 35 35 SNeIa. Overall, compared to prior SNooPy fits, the fits of the current version (SNooPy v2.7) raise H 0 H_{0} for the same SN samples by ∼ 1.7 ​ 𝐤𝐦 ​ 𝐬 − 𝟏 ​ 𝐌𝐩𝐜 − 𝟏 \mathbf{\sim 1.7\,\mathbf{km\,s^{-1}\,Mpc^{-1}}} (e.g., from 70.31 for the F25 sample to 72.05). This difference is caused then primarily from improvements to SNooPy and to a lesser degree from better, later versions of the SN Ia calibrator data, see Table 7 .

## 148. C.2.2 Differences with Calibrator Sample Size

Lastly, within the use of every SN fitter, increasing the sample size from the smallest, selected study (the F25 sample of 24 calibrators) to the full available sample of 55 calibrators shows a clear trend towards increasing H 0 H_{0} —as evident from Figure 14 and Table 5 . It increases by 0.9 ​ km ​ s − 1 ​ Mpc − 1 0.9\,{\rm km\,s}^{-1}{\rm\,Mpc}^{-1} for Pantheon+ fitting, by 0.2 ​ km ​ s − 1 ​ Mpc − 1 0.2\,{\rm km\,s}^{-1}{\rm\,Mpc}^{-1} for SNooPy post-v2.7 fitting, by 1.0 ​ km ​ s − 1 ​ Mpc − 1 1.0\,{\rm km\,s}^{-1}{\rm\,Mpc}^{-1} for Salt 3 fitting, and by 1.4 ​ km ​ s − 1 ​ Mpc − 1 1.4\,{\rm km\,s}^{-1}{\rm\,Mpc}^{-1} for BayesSN fitting—a mean of + 0.9 ​ km ​ s − 1 ​ Mpc − 1 +0.9\,{\rm km\,s}^{-1}{\rm\,Mpc}^{-1} . This difference due to calibrator sample is even greater between the F25 sample and that from R22, about 1.2 ​ km ​ s − 1 ​ Mpc − 1 1.2\,{\rm km\,s}^{-1}{\rm\,Mpc}^{-1} in the mean, agreeing with the findings of [ 172 ] . This is shown in Figure 14 . It seems reasonable to expect greater convergence in estimates of H 0 H_{0} as sample sizes increase.

## 149. C.2.2 Differences with Calibrator Sample Size

We note that the F25 sample is not a natural sample selection from the perspective of the Distance Network—it cannot be constructed from simple cuts in redshift/distance or calibrator type. As such, we do not consider it as a variant (according to the methodology laid out in Section II.1.4 , those should be based on physical assumptions or hypotheses). We analyze it here to provide for a direct comparison with W. L. Freedman et al. [71] . We show the distribution in distance of the F25 ( N = 24 N=24 ) and full samples ( N = 55 N=55 ) according to the network in Figure 15 —which shows that 37 of the 55 objects would have to be included if a cut was made in distance modulus to retain the full F25 sample. The smaller F25 sample is at a mean distance moduli of μ host = 31.13 ± 0.85 \mu_{\mathrm{host}}=31.13\pm 0.85 , and the remaining sample is at a mean distance moduli of μ host = 32.01 ± 0.73 \mu_{\mathrm{host}}=32.01\pm 0.73 , which are thus a little further away on average (though not very significantly).

## 150. C.2.2 Differences with Calibrator Sample Size

Figure 15: The full network sample (blue) and the F25 sample of calibrator hosts (red) in comparison. The grey region marks the maximal extent of the F25 sample. The green stars mark hosts with TRGB distances available. The left hand side shows an ordered scatterplot of the distance moduli, while the right hand side shows the corresponding histogram. Note that while F25 calibrates 24 SN Ia, these are located in only 20 hosts (hence only 20 points are marked red). The 11 additional hosts marked with green stars would correspond to potentially 10 additional SNe Ia (with the 11th host NGC 1399 calibrating SBF, not SNe Ia). One additional SN Ia (2021pit) is present in an already F25-calibrated host (N5643) but not within the CSP sample. In total that makes 24+10+1=35 calibrators that are available for SNe Ia calibrated through TRGB. Even within the sample of the CSP I&II supernovae only, there would still be 4 additional CSPI&II calibrators to be gained using TRGB observations of nearby hosts within the range of the F25 sample—with 7 additional TRGB-calibratable SNe Ia not present within the CSP I&II samples. The 4 “missing” TRGB-F25 calibrators are 2012ht in NGC 3447, 1998aq in NGC 3982, 1992A in NGC 1380, and ASAS14-lp in NGC 4666.

## 151. C.2.2 Differences with Calibrator Sample Size

For this purpose we can also look at Figure 16 , which shows the differences between calibrator sets for the same supernovae standardizations and datasets. In each case we take the same supernovae to be used for calibration, but vary with which primary distance indicators the distances to their hosts are calibrated, for example using only HST Cepheids vs using all methods, or using only the TRGB (JWST and HST) vs using all methods, or using only the TRGB calibrations adopted in F25 vs using all methods. These differences are typically compatible with the uncertainty at ∼ 1 ​ σ \sim 1\sigma , with shifts around − 1 ​ km ​ s − 1 ​ Mpc − 1 -1\,{\rm km\,s}^{-1}{\rm\,Mpc}^{-1} in central value. We also see that the reduced calibrations agree nicely with the results reported in the literature.

## 152. Appendix E Code availability and reproducing our results

The code is driven by configuration files that determine which data sets are included and other processing parameters. Configuration files corresponding to all the variants presented in Table 4 and many of the other tests are provided. Summary results for each run are provided in the form of text files; in addition, the user has the option of saving the main data, equation coefficients, and covariance matrices in FITS files for more detailed perusal. 13 13 13 The IDL version can also be run using command-line parameters, and has options to provide more detailed output if desired. It is our intent to update the code and data files with new options and published measurements as they become available.

## 153. Appendix F Additional details from the Distance Network: calibration parameters and host/calibrator distances

The main result of the Distance Network analysis is of course the value and uncertainty of H 0 H_{0} , reported in Table 4 for all variants, together with the value of the total χ 2 \chi^{2} to evaluate the quality of the fit. In addition, the Distance Network process can provide more detailed information on each class of calibrators and on host and the calibrated distances.

## 154. F.1 Calibration parameters

The Distance Network approach can include several secondary distance indicators whose calibration is determined simultaneously with all other parameters of the solution; each can be used to constrain H 0 H_{0} via tracers in the Hubble Flow. For each variant, Table 11 provides the resulting calibration parameter, the Hubble Flow intercept, and the number of calibrators for each of the main secondary distance indicators: SNe Ia, SBF, SNe II, and TF. For SNe Ia and SN II, the calibration parameter is generally the reference absolute magnitude of a standardized SN in the appropriate passband; the exception is the BayesSN method, which uses a different definition. For SBF and TF, the calibration parameter is reported as the difference with respect to the published value, as described in Section A . In all cases, the reported uncertainty is marginalized over all other parameters in the Distance Network.

## 155. F.1 Calibration parameters

The Hubble Flow intercept is the parameter a 𝒯 a_{{\cal T}} defined in Equation B15 and discussed in Section B.3.5 . It is expressed in units of log ⁡ ( H 0 ) \log(H_{0}) (numerically equivalent to 0.2 mag); the reported uncertainty includes the intrinsic and measurement error for the tracers, but does not include the calibration uncertainty. For some versions of SNe Ia, the reported uncertainty includes covariance terms between different tracers, as reported in the original sources.

## 156. F.1 Calibration parameters

Note. — (a) Reference F19 claims that 1994ae used the version of the light curve from A. G. Riess et al. [163] , but C. Burns, who performed the fit, sourced the data from the Open Source Catalogue, which instead used A. G. Riess et al. [162] . We further confirm that the value in S. A. Uddin et al. [204] matches A. G. Riess et al. [162] , not A. G. Riess et al. [163]

## 157. F.2 Host and calibrator distances

One of the secondary results of the Distance Network approach is an optimized set of distance moduli for all hosts and calibrators included in the Network. These distances are based not only on the multiple measurements included in the Distance Network, but also on the consistency equations for the various classes of calibrators to which they belong. They represent the values of the distances that, together, produce the best-fitting solution to all of the Distance Network equations. As a result, the estimated distances for each host will differ slightly depending on which classes of calibrators are included in the solution, even when no additional measurements are introduced.

## 158. F.2 Host and calibrator distances

Table 12 reports the best distance estimate for each of the hosts (or host/calibrators) included in two solutions, Baseline (V00) and “Everything,” the solution including all methods (V99). Since hosts not tied to any calibrators are excluded from each solution, many of the hosts do not have a distance estimate in the Baseline version. SN calibrators are not included, since their distances are not separate parameters; they are assumed identical to the distances to their host, which as a consequence are also affected by the SN calibration via the (one or more) SNe they host. On the other hand, SBF calibrator galaxies in Fornax and Virgo are included individually; their distances are allowed to deviate from the group distance, because of depth effects, and are affected by their SBF luminosity measurements via their global calibration. The quoted distance uncertainties are marginalized over all parameters of the respective Distance Network solution, and therefore are not independent.

## 159. F.2 Host and calibrator distances

Table 12: Distance moduli and statistical uncertainties for host and calibrator systems in the Distance Network.
