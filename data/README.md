# Codebook

### policy.csv

| Variable Name | Description                                                  |
| ------------- | ------------------------------------------------------------ |
| STATE         | US State names                                               |
| POSTCODE      | US State abbreviations                                       |
| FIPS          | US State FIPS Codes                                          |
| STEMERG       | The first date a state declared any type of emergency declaration |
| CLSCHOOL      | The date a state closed K-12 schools statewide. Only included directives/orders. Did not include guidance or recommendations. Order must apply to entire state |
| CLDAYCR       | The date a state closed daycares statewide. Only included directives/orders. Did not include guidance or recommendations. Order must apply to entire state |
| OPNCLDCR      | The date a state reopened daycares statewide. If a state never closed daycares they will be marked as 0. |
| CLNURSHM      | The date a state banned visitors to nursing homes statewide. Only included directives/orders. Did not include guidance or recommendations. Order must apply to entire state |
| STAYHOME      | The date a state's stay at home/shelter in place order went into effect. Only included directives/orders. Did not include guidance or recommendations. Order must apply to entire state |
| END_STHM      | The date a state ended/relaxed their stay at home/shelter in place order. Order must apply to entire state |
| CLBSNS        | The date a state closed non-essential businesses statewide. Only included directives/orders. Did not include guidance or recommendations. Order must apply to entire state |
| END_BSNS      | The date a state began to reopen businesses that were previously closed due to COVID-19 statewide. Order must apply to entire state. |
| RELIGEX       | An indicator of whether or not a state exempted religious gatherings from social distancing mandates. A clear social distancing requirement is defined as a mandate that gatherings must be less than 10 people and/or adherence to CDC social distance guidelines. Must be statewide. |
| FM_ALL        | The date a state mandated face mask use in public spaces by all individuals statewide. Only included directives/orders. Did not include guidance or recommendations. Order must apply to entire state |
| FMFINE        | Whether a face mask mandate is enforced through fines. Must apply to entire state. |
| FMCITE        | Whether a face mask mandate is enforced through criminal charges/citations. Must apply to entire state. |
| FMNOENF       | Whether any legal encforcement measures of the face mask mandate are present |
| FM_EMP        | The date a state mandated that employees in public facing businessses must wear face masks statewide.  Did not include guidance or recommendations. Order must apply to entire state |
| ALCOPEN       | Whether states kept alcohol/liquor stores open during the pandemic. Must apply to entire state |
| ALCREST       | The date when states allowed restaurants to sell takeout alchol.  Must apply to entire state |
| ALCDELIV      | The date when states allowed restaurants to deliver alchol.  Must apply to entire state |
| GUNOPEN       | Whether states kept firearms sellers open. Must apply to entire state. |
| CLREST        | The date when states closed restaurants (except for takeout). Did not include guidance or recommendations. Order must apply to entire state |
| ENDREST       | The date when states reopened restaurants (for indoor and/or outdoor dining) statewide. If states never closed restaurants, they will be marked as 0. |
| RSTOUTDR      | Whether restaurants could initially reopen only for outdoor dining as part of the phased reopening process.  Did not include guidance or recommendations. Order must apply to entire state |
| CLGYM         | The date states closed indoor gyms/fitness centers.  Did not include guidance or recommendations. Order must apply to entire state |
| ENDGYM        | The date states reopened indoor gyms/fitness centers statewide.If states never closed gyms they will be marked as 0 |
| CLMOVIE       | The date states closed movie theaters.  Did not include guidance or recommendations. Order must apply to entire state |
| END_MOV       | The date states reopened movie theaters statewide. If states never closed movie theaters they will be marked as 0. |
| CLOSEBAR      | The date states closed bars statewide. Unless otherwide noted, bars are defined as establishments that derive more than 50 percent of gross revenue from the sales of alcoholic beverages.  Did not include guidance or recommendations. Order must apply to entire state |
| END_BRS       | The date states reopen bars statewide. Unless otherwide noted, bars are defined as establishments that derive more than 50 percent of gross revenue from the sales of alcoholic beverages. If states never closed bars they will be marked as 0 |
| END_HAIR      | The date states reopened hair salons barber shops statewide. If states never closed hair salons/barber shops, they will be marked as 0 |
| END_CONST     | The date states restarted non essential construction statewide. If states never stopped non-essential construction, they will be marked as 0 |
| END_RELG      | The date states reopened religious gatherings statewide. If states never closed religious gatherings, they will be marked as 0 |
| ENDRETL       | The date states reopened non essential retail statewide. If states never stopped non-essential construction, they will be marked as 0 |
| BCLBAR2       | The first date a state reclosed bars after an initial reopening. The closure can be restricted to a city or county, but must be mandated by the governor or state-level agency.  Did not include guidance or recommendations. If a state never reopened bars they will be marked as 0. |
| CLBAR2        | The date a state reclosed bars statewide after an initial opening.  Did not include guidance or recommendations. If a state never reopened bars they will be marked as 0. |
| CLMV2         | The date a state reclosed movie theaters statewide after an initial opening.  Did not include guidance or recommendations. If a state never reopened movie theaters they will be marked as 0. |
| CLGYM2        | The date a state reclosed indoor  gyms/fitness centers statewide after an initial opening.  Did not include guidance or recommendations. If a state never reopened indoor  gyms/fitness they will be marked as 0. |
| CLRST2        | The date a state reclosed indoor dining statewide after an initial opening.  Did not include guidance or recommendations. If a state never reopened indoor dining they will be marked as 0. |
| QRSOMEST      | The date a state first mandated that individuals arriving in their state from a specific state(s) must undergo quarantine.  Did not include guidance or recommendations. Order must apply to entire state. Quarantine order must apply to visitors using all forms of transportation to enter the state (not just air travel) |
| QR_ALLST      | The date a state first mandated that individuals arriving in their state from any state must undergo quarantine.  Did not include guidance or recommendations. Order must apply to entire state. Quarantine order must apply to visitors using all forms of transportation to enter the state (not just air travel) |
| QR_END        | The date a state ended all mandated quarantines for individuals arriving from out of state. If any statewide quarantines for out of state individuals is still  in effect or if the state never had a quarantine in effect  the column will bear a 0. |
| EVICINTN      | The date a state stopped the initiation of evictions (overall or due to COVID-19 related issues) statewide. This could be mandated from governors or though the state court system. Did not include guidance or recommendations. Order must apply to entire state. |
| EVICENF       | The date a state stopped the enforcement of evictions (overall or due to COVID-19 related issues) statewide. This could be mandated from governors or though the state court system. Did not include guidance or recommendations. Order must apply to entire state. |
| RNTGP         | The date a state allowed a renter grace period or the use of security deposit to pay rent. Did not include guidance or recommendations. Order must apply to entire state. |
| UTILSO        | The date a state froze utility shut offs. Utilities could include water, gas, or electricity. Did not include guidance or recommendations. Order must apply to entire state. |
| MORGFR        | The date a state froze mortgage payments. Did not include guidance or recommendations. Order must apply to entire state. |
| EVICEND       | The date a state ended eviction moratoritum orders, and allowed evictions to resume statewide. Order must apply to entire state. |
| SNAPALLO      | The date a state was approved the use of a waiver to provide many SNAP households with emergency supplementary benefits up to the maximum benefit a household can receive. |
| SNAPEBT       | The date a state was approved the use of a waiver to provide meal replacement benefits through SNAP, known as “Pandemic EBT” (for electronic benefit transfer), for households with children who attend a school that’s closed and who would otherwise receive free or reduced-price meals. |
| SNAPSUSP      | The date a state was approved the use of a waiver to temporarily suspend collection of  SNAP claims |
| SNAPTLW       | Before the pandemic, whether a state had a waiver that allowed them to provide SNAP to able-bodied adults without dependents (ABAWDs) who were not meeting work requirements. Without these waivers, states are only allowed to provide SNAP to these individuals for 3 months in a 36 month period. |
| MED1135W      | The date a state used a 1135 waiver to modify or waive Medicaid requirements |
| ACAENROL      | The date a state reopened ACA enrollment using a Special Enrollment Period (SEP). |
| PREVTLHL      | Whether a state previously allowed audio-only telehealth     |
| TLHLAUD       | The date states allowed audio only telehealth statewide. If a state previously allowed audio only telehealth, it will be marked as 1/0/1900 |
| TLHLMED       | The date states allowed or expand Medicaid telehealth coverage statewide in response to the pandemic |
| CHIPLKOT      | Whether a state had a non-payment lock-out period for CHIP as of January 2019. A lock-out period is the amount of time during which the disenrolled child is prohibited from returning to the CHIP program due to non-payment of premiums. |
| LKOTSUS       | Whether a state suspended their non-payment lock-out policy for CHIP during the pandemic. If a state did not have an existing lock-out policy, they will be marked as 0. |
| TESTANY       | If a state reported any COVID-19 testing by race/ethnicity   |
| TESTMAR       | If a state reported COVID-19 testing by race/ethnicity for the month of March |
| TESTAPR       | If a state reported COVID-19 testing by race/ethnicity for the month of April |
| TESTMAY       | If a state reported COVID-19 testing by race/ethnicity for the month of May |
| TESTJUN       | If a state reported COVID-19 testing by race/ethnicity for the month of June |
| CASEANY       | If a state reported any COVID-19 cases by race/ethnicity     |
| CASEMAR       | If a state reported COVID-19 cases by race/ethnicity for the month of March |
| CASEAPR       | If a state reported COVID-19 cases by race/ethnicity for the month of April |
| CASEMAY       | If a state reported COVID-19 cases by race/ethnicity for the month of May |
| CASEJUN       | If a state reported COVID-19 cases by race/ethnicity for the month of June |
| HOSPANY       | If a state reported any COVID-19 hospitalizations by race/ethnicity |
| HOSPMAR       | If a state reported COVID-19 hospitalizations by race/ethnicity for the month of March |
| HOSPAPR       | If a state reported COVID-19 hospitalizations by race/ethnicity for the month of April |
| HOSPMAY       | If a state reported COVID-19 hospitalizations by race/ethnicity for the month of May |
| HOSPJUN       | If a state reported COVID-19 hospitalizations by race/ethnicity for the month of June |
| DEATHANY      | If a state reported any COVID-19 deaths by race/ethnicity    |
| DEATHMAR      | If a state reported COVID-19 deaths by race/ethnicity for the month of March |
| DEATHAPR      | If a state reported COVID-19 deaths by race/ethnicity for the month of April |
| DEATHMAY      | If a state reported COVID-19 deaths by race/ethnicity for the month of May |
| DEATHJUN      | If a state reported COVID-19 deaths by race/ethnicity for the month of June |
| TST_AIAN      | If state reports data on COVID testing for American Indian/Alaska Native individuals |
| TST2_AIAN     | If state reports data on positive COVID testing for American Indian/Alaska Native individuals |
| HOSPAIAN      | If state reports data on COVID hospitalizations for American Indian/Alaska Native individuals |
| DTH_AIAN      | If state reports data on COVID deaths for American Indian/Alaska Native individuals |
| AIANRESN      | Whether a state has at least one Indian/Alaska Native Reservation |
| VISITPER      | The date personal visitation was banned at prisons statewide. Order could be from the governor or from a state agency like the department of corrections |
| VISITATT      | The date attorney visitation was banned at prisons statewide. Order could be from the governor or from a state agency like the department of corrections |
| NOCOPAY       | Before the pandemic, whether a state charged incarcerated individuals medical copays statewide. Source: Prison Policy Initiative https://www.prisonpolicy.org/blog/2017/04/19/copays/ |
| NOPAYCOV      | Whether a state waived copays for incarcerated individuals for COVID/respiratory illness related charges statewide. Source: Prison Policy Initiative https://www.prisonpolicy.org/blog/2017/04/19/copays/ |
| NOPAYALL      | Whether a state waived all copays during the pandemic for incarcerated individuals statewide. Source: Prison Policy Initiative https://www.prisonpolicy.org/blog/2017/04/19/copays/ |
| YESCOPAY      | If a state did not waive copays for incarcerated individuals during the pandemic statewide. Source: Prison Policy Initiative https://www.prisonpolicy.org/blog/2017/04/19/copays/ |
| ELECPRCR      | The date states suspended elective medical dental procedures statewide. Did not include guidance or recommendations. Order must apply to entire state. |
| ENDELECP      | The date states resumeded statewide. If states never suspended elective medical/dental procedures, they will be marked as 0 |
| WTPRD         | Prior to the pandemic, whether a state did not have a mandatory waiting period until they could receive unemployment insurance benefits, OR whether we could not find whether a state did/did not have a mandatory waiting period |
| WV_WTPRD      | The date a state waived the one week waiting period for unemployment insurance benefits. Did not include guidance or recommendations. Order must apply to entire state. |
| WV_WKSR       | If a state waived the work search requirement for unemployment insurance benefits during the pandemic. Did not include guidance or recommendations. Order must apply to entire state. |
| UIQUAR        | If a state expanded eligibility of unemployment insurance to anyone who is quarantined and/or taking care of someone who is quarantined during the pandemic. Did not include guidance or recommendations. Order must apply to entire state. |
| UIHIRISK      | If a state expanded eligibility of unemployment insurance to anyone who is at high risk for COVID-19, and is undergoing preventive quarantine during the pandemic. Did not include guidance or recommendations. Order must apply to entire state. |
| UICLDCR       | If a state expanded eligibility of unemployment insurance to those who have lost childcare during the pandemic in response to daycare/school closures. Did not include guidance or recommendations. Order must apply to entire state. |
| UIEXTND       | If a state extended the amount of time an individual can be on unemployment insurance. Did not include guidance or recommendations. Order must apply to entire state. |
| UIMAXAMT      | The weekly unemployment insurance maximum amount a state will provide |
| UIMAXEXT      | The weekly unemployment insurance maximum amount a state will provided with extra stimulus through the CARES Act (through July 21, 2020) |
| UIMAXDUR      | The maximum amount of time an individual can receive unemployment insurance (before the pandemic) |
| UIMAXCAR      | The maximum amount of time an individual can receive unemployment insurance with the Pandemic Emergency Unemployment Compensation CARES extension (weeks) |
| LMABRN        | If a state made an effor through orders or legislation during the pandemic to limit or restrict access to abortion. Did not include guidance or recommendations. Order must apply to entire state. |
| TLHlBUPR      | The date a state allowed the use of telemedicine/telephone evaluations to initiate buprenorphine prescribing. |
| EXTOPFL       | The date a state allowed patients to receive 14-28 take-home doses of opioid medication |
| HMDLVOP       | The date a state allowed home delivery of take-home medication by opioid treatment programs |
| TLHLCL24      | The date a state allowed telemedicine for schedule II-V prescriptions |
| EXCEMORP      | The date a state allowed exceptions to emergency oral precriptions |
| WVDEAREQ      | The date a state waived the requirement to obtain separate DEA registration to dispense outside of the home state |
| PDSKLV        | If a state previously mandated paid sick leave. Source: https://www.zenefits.com/workest/the-definitive-list-of-states-and-cities-with-paid-sick-leave-laws/. Often depends on business size. |
| MEDEXP        | If a state had previously expanded Medicaid. Source: Kaiser Family Foundation |
| POPDEN18      | The population density of the state in square miles          |
| POP18         | The total 2018 population. Source: WIQARS                    |
| SQML          | The total size of the state in square miles                  |
| HMLS19        | The number of homeless individuals in the state in 2019. Source: 2019 AHAR: Part 1 - PIT Estimates of Homelessness in the U.S. https://www.hudexchange.info/homelessness-assistance/ahar/#2019-reports |
| UNEMP18       | The percent unemployment in the state in 2018. Source: 2018 American Community Survey 1-year estimates (https://data.census.gov/) |
| POV18         | The percent of individuals in the state who were living under the federal poverty line in 2018. Source: 2018 American Community Survey 1-year estimates (https://data.census.gov/) |
| RISKCOV       | The percent of individuals in the state who were at risk for serious illness due to COVID. Source: Kaiser Family Foundation https://www.kff.org/global-health-policy/issue-brief/how-many-adults-are-at-risk-of-serious-illness-if-infected-with-coronavirus/ |
| DEATH18       | The people/year states alled cause statewide. If states never stopped non-essential construction, they will be marked as valid 90 |

### individual.csv

| varname                       | description                                                  |
| ----------------------------- | ------------------------------------------------------------ |
| cdc_report_dt                 | Initial case report date to CDC                              |
| pos_spec_dt                   | Date of first positive specimen collection                   |
| onset_dt                      | Symptom onset date, if symptomatic                           |
| current_status                | Case Status: Laboratory-confirmed case; Probable case        |
| sex                           | Sex: Male; Female; Unknown; Other                            |
| age_group                     | Age Group: 0 - 9 Years; 10 - 19 Years; 20 - 39 Years; 40 - 49 Years; 50 - 59 Years; 60 - 69 Years; 70 - 79 Years; 80 + Years |
| Race and ethnicity (combined) | Race and ethnicity (combined): Hispanic/Latino; American Indian / Alaska Native, Non-Hispanic; Asian, Non-Hispanic; Black, Non-Hispanic; Native Hawaiian / Other Pacific Islander, Non-Hispanic; White, Non-Hispanic; Multiple/Other, Non-Hispanic |
| hosp_yn                       | Hospitalization status                                       |
| icu_yn                        | ICU admission status                                         |
| death_yn                      | Death status                                                 |
| medcond_yn                    | Presence of underlying comorbidity or disease                |

### covid_19.csv

| Column Name     | Description                                                  |
| --------------- | ------------------------------------------------------------ |
| submission_date | Date of counts                                               |
| state           | Jurisdiction                                                 |
| tot_cases       | Total number of cases                                        |
| conf_cases      | Total confirmed cases                                        |
| prob_cases      | Total probable cases                                         |
| new_case        | Number of new cases                                          |
| pnew_case       | Number of new probable cases                                 |
| tot_death       | Total number of deaths                                       |
| conf_death      | Total number of confirmed deaths                             |
| prob_death      | Total number of probable deaths                              |
| new_death       | Number of new deaths                                         |
| pnew_death      | Number of new probable deaths                                |
| created_at      | Date and time record was created                             |
| consent_cases   | Agree: confirmed and probable cases included. Else, only total cases included. |
| consent_deaths  | Agree: confirmed and probable death included. Else, only total cases included. |

### hospital1.csv

| Varname                                                      | Description                                                  |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| state                                                        | The two digit state code                                     |
| hospital_onset_covid                                         | Total current inpatients with onset of suspected or laboratory-confirmed COVID-19 fourteen or more days after admission for a condition other than COVID-19 in this state. |
| hospital_onset_covid_coverage                                | Number of hospitals reporting "hospital_onset_covid" in this state |
| inpatient_beds                                               | Reported total number of staffed inpatient beds including all overflow and surge/expansion beds used for inpatients (includes all ICU beds) in this state |
| inpatient_beds_coverage                                      | Number of hospitals reporting "inpatient_beds" in this state |
| inpatient_beds_used                                          | Reported total number of staffed inpatient beds that are occupied in this state |
| inpatient_beds_used_coverage                                 | Number of hospitals reporting "inpatient_beds_used" in this state |
| inpatient_beds_used_covid                                    | Reported patients currently hospitalized in an inpatient bed who have suspected or confirmed COVID-19 in this state |
| inpatient_beds_used_covid_coverage                           | Number of hospitals reporting "inpatient_beds_used_covid" in this state |
| staffed_adult_icu_bed_occupancy                              | Reported total number of staffed inpatient adult ICU beds that are occupied in this state |
| staffed_adult_icu_bed_occupancy_coverage                     | Number of hospitals reporting "staffed_adult_icu_bed_occupancy" in this state |
| staffed_icu_adult_patients_confirmed_and_suspected_covid     | Reported patients currently hospitalized in an adult ICU bed who have suspected or confirmed COVID-19 in this state |
| staffed_icu_adult_patients_confirmed_and_suspected_covid_coverage | Number of hospitals reporting "staffed_icu_adult_patients_confirmed_and_suspected_covid" in this state |
| staffed_icu_adult_patients_confirmed_covid                   | Reported patients currently hospitalized in an adult ICU bed who have confirmed COVID-19 in this state |
| staffed_icu_adult_patients_confirmed_covid_coverage          | Number of hospitals reporting "staffed_icu_adult_patients_confirmed_covid" in this state |
| total_adult_patients_hospitalized_confirmed_and_suspected_covid | Reported patients currently hospitalized in an adult inpatient bed who have laboratory-confirmed or suspected COVID-19. This include those in observation beds. |
| total_adult_patients_hospitalized_confirmed_and_suspected_covid_coverage | Number of hospitals reporting "total_adult_patients_hospitalized_confirmed_and_suspected_covid" in this state |
| total_adult_patients_hospitalized_confirmed_covid            | Reported patients currently hospitalized in an adult inpatient bed who have laboratory-confirmed COVID-19. This include those in observation beds. |
| total_adult_patients_hospitalized_confirmed_covid_coverage   | Number of hospitals reporting "total_adult_patients_hospitalized_confirmed_covid" in this state |
| total_pediatric_patients_hospitalized_confirmed_and_suspected_covid | Reported patients currently hospitalized in a pediatric inpatient bed, including NICU, newborn, and nursery, who are suspected or laboratory-confirmed-positive for COVID-19. This include those in observation beds. |
| total_pediatric_patients_hospitalized_confirmed_and_suspected_covid_coverage | Number of hospitals reporting "total_pediatric_patients_hospitalized_confirmed_and_suspected_covid" in this state |
| total_pediatric_patients_hospitalized_confirmed_covid        | Reported patients currently hospitalized in a pediatric inpatient bed, including NICU, newborn, and nursery, who are laboratory-confirmed-positive for COVID-19. This include those in observation beds. |
| total_pediatric_patients_hospitalized_confirmed_covid_coverage | Number of hospitals reporting "total_pediatric_patients_hospitalized_confirmed_covid" in this state |
| total_staffed_adult_icu_beds                                 | Reported total number of staffed inpatient adult ICU beds in this state |
| total_staffed_adult_icu_beds_coverage                        | Number of hospitals reporting "total_staffed_adult_icu_beds" in this state |
| inpatient_beds_utilization                                   | Percentage of inpatient beds that are being utilized in this state. This number only accounts for hospitals in the state that report both "inpatient_beds_used" and "inpatient_beds" fields. |
| inpatient_beds_utilization_coverage                          | Number of hospitals reporting both "inpatient_beds_used" and "inpatient_beds" |
| inpatient_beds_utilization_numerator                         | Sum of "inpatient_beds_used" for hospitals reporting both "inpatient_beds_used" and "inpatient_beds" |
| inpatient_beds_utilization_denominator                       | Sum of "inpatient_beds" for hospitals reporting both "inpatient_beds_used" and "inpatient_beds" |
| percent_of_inpatients_with_covid                             | Percentage of inpatient population who have suspected or confirmed COVID-19 in this state. This number only accounts for hospitals in the state that report both "inpatient_beds_used_covid" and "inpatient_beds_used" fields. |
| percent_of_inpatients_with_covid_coverage                    | Number of hospitals reporting both "inpatient_beds_used_covid" and "inpatient_beds_used". |
| percent_of_inpatients_with_covid_numerator                   | Sum of "inpatient_beds_used_covid" for hospitals reporting both "inpatient_beds_used_covid" and "inpatient_beds_used". |
| percent_of_inpatients_with_covid_denominator                 | Sum of "inpatient_beds_used" for hospitals reporting both "inpatient_beds_used_covid" and "inpatient_beds_used". |
| inpatient_bed_covid_utilization                              | Percentage of total (used/available) inpatient beds currently utilized by patients who have suspected or confirmed COVID-19 in this state. This number only accounts for hospitals in the state that report both "inpatient_beds_used_covid" and "inpatient_beds" fields. |
| inpatient_bed_covid_utilization_coverage                     | Number of hospitals reporting both "inpatient_beds_used_covid" and "inpatient_beds". |
| inpatient_bed_covid_utilization_numerator                    | Sum of "inpatient_beds_used_covid" for hospitals reporting both "inpatient_beds_used_covid" and "inpatient_beds". |
| inpatient_bed_covid_utilization_denominator                  | Sum of "inpatient_beds" for hospitals reporting both "inpatient_beds_used_covid" and "inpatient_beds". |
| adult_icu_bed_covid_utilization                              | Percentage of total staffed adult ICU beds currently utilized by patients who have suspected or confirmed COVID-19 in this state. This number only accounts for hospitals in the state that report both "staffed_icu_adult_patients_confirmed_and_suspected_covid" and "total_staffed_adult_icu_beds" fields. |
| adult_icu_bed_covid_utilization_coverage                     | Number of hospitals reporting both both "staffed_icu_adult_patients_confirmed_and_suspected_covid" and "total_staffed_adult_icu_beds". |
| adult_icu_bed_covid_utilization_numerator                    | Sum of "staffed_icu_adult_patients_confirmed_and_suspected_covid" for hospitals reporting both "staffed_icu_adult_patients_confirmed_and_suspected_covid" and "total_staffed_adult_icu_beds". |
| adult_icu_bed_covid_utilization_denominator                  | Sum of "total_staffed_adult_icu_beds" for hospitals reporting both "staffed_icu_adult_patients_confirmed_and_suspected_covid" and "total_staffed_adult_icu_beds". |
| adult_icu_bed_utilization                                    | Percentage of staffed adult ICU beds that are being utilized in this state. This number only accounts for hospitals in the state that report both "staffed_adult_icu_bed_occupancy" and "total_staffed_adult_icu_beds" fields. |
| adult_icu_bed_utilization_coverage                           | Number of hospitals reporting both both "staffed_adult_icu_bed_occupancy" and "total_staffed_adult_icu_beds". |
| adult_icu_bed_utilization_numerator                          | Sum of "staffed_adult_icu_bed_occupancy" for hospitals reporting both "staffed_adult_icu_bed_occupancy" and "total_staffed_adult_icu_beds". |
| adult_icu_bed_utilization_denominator                        | Sum of "total_staffed_adult_icu_beds" for hospitals reporting both "staffed_adult_icu_bed_occupancy" and "total_staffed_adult_icu_beds". |
| reporting_cutoff_start                                       | Look back date start - The latest reports from each hospital is summed for this report starting with this date. |

### hospital2.csv

