# Disease burden deep dive: Thailand, Myanmar, and the Kanchanaburi border, and what it means for the phrasebook

Date: 2026-10-13. Prepared by the system for the project lead. American English.
Sources: WHO TB database (2024 data from the 2025 Global TB Report), WHO Mekong malaria
summaries, Thai Department of Disease Control weekly reports, UN Myanmar Health Cluster
bulletins, Mae Tao Clinic, peer-reviewed papers via PubMed and Consensus. IHME Global Burden
of Disease country sheets blocked automated access, so GBD rankings are marked UNVERIFIED.
Kanchanaburi's own provincial health office data is not online; see "Data requests."

## Part A. The answer in one page

**What a volunteer in Kanchanaburi will most often face with a Burmese, Mon, or Karen speaker,
ranked by evidence weight:**

| Rank | Situation | Why it ranks here |
|---|---|---|
| 1 | Fever: malaria versus dengue triage, 14-day primaquine adherence for vivax, "no ibuprofen or aspirin for fever" | Kanchanaburi was the number 2 or 3 malaria province every year 2023 to 2026; 90 percent or more of cases are P. vivax; about 60 percent of cases are foreign nationals and 41 percent farm workers. Dengue deaths in Thailand are linked to NSAID self-medication and late presentation. |
| 2 | Cough over two weeks, weight loss: TB screening, sputum, directly observed treatment, HIV test | Myanmar TB incidence 482 per 100,000 with case detection down to 44 percent; migrant TB case fatality 9.5 percent and loss to follow-up 9 to 21 percent in Thai programs; an XDR-TB case in a Myanmar woman in 2024. |
| 3 | Pregnancy: antenatal booking, danger signs, delivery plan, postpartum family planning | Reproductive health is 40 percent of Mae Tao Clinic admissions; pregnancy is the number 1 inpatient reason for Myanmar patients at Samut Sakhon Hospital; antenatal care is the top migrant outpatient reason at a border hospital; 17 percent antenatal loss to follow-up. |
| 4 | Child vaccination catch-up: measles, diphtheria, polio | 1.5 million Myanmar under-fives missed basic vaccination since 2018; five unvaccinated Myanmar children with diphtheria at Mae Sot Hospital in late 2024, two died; measles in Tak in 2025. |
| 5 | Injury: cuts, machine and hand injuries, motorcycle crashes, snakebite first aid | Injury is the number 2 outpatient and inpatient category for Myanmar patients at Samut Sakhon; musculoskeletal (23 percent) and injuries (19 percent) are the commonest illnesses migrants report; 6,000 snakebites a year in Thailand, 15,000 in Myanmar. |
| 6 | Pain and "yaa chud" pill packs, antibiotic misuse | Kanchanaburi's own health surveillance site documented unlabeled packs of antibiotics plus steroids sold for about 6 baht, used mainly by migrant construction workers for pain; 28 percent antibiotic self-medication and 68 percent non-adherence among migrants in Samut Sakhon. |
| 7 | Diarrhea and cholera: oral rehydration, danger signs, hygiene | Cholera outbreak at Shwe Kokko opposite Mae Sot in December 2024 (300 cases); Myanmar nationwide cholera June 2024 to April 2025. |
| 8 | Registration, insurance, referral, cost, fear of arrest | 1.8 million migrants in irregular status cannot access insurance; 18 percent of outpatients and 38 percent of inpatients from Myanmar at Kanchanaburi's provincial hospital were uninsured; undocumented status is the top driver of unmet need. |
| 9 | Hypertension and diabetes screening and follow-up | Hypertension 28 percent in registered Myanmar workers nationally and 63 percent in a northeastern sample; stroke is the number 1 cause of lost healthy life in both countries (GBD, UNVERIFIED). |
| 10 | Stress, insomnia, alcohol, methamphetamine | 12 percent harmful drinking among Myanmar men in Mae Sot; perinatal depression 39 percent among border migrants; depression 14 percent among Shan workers. |
| 11 | Skin: scabies, fungal infection, infected wounds | Scabies with secondary infection surged in 15 Myanmar townships including Tanintharyi (opposite Kanchanaburi) in early 2026. |
| 12 | Rural fevers (leptospirosis, scrub typhus, melioidosis) and chronic infections (hepatitis B 7 to 10 percent carriage in Myanmar migrants, HIV, STIs) | Leptospirosis 2,190 cases and melioidosis 1,654 cases in Thailand by July 2026; migrants have 2.4 times the STI risk of Thai workers. |

**Coverage of the current four topics** (triage, medication, antenatal, TB and malaria):
roughly 55 to 65 percent of likely encounters, judged against the only published Thai hospital
diagnosis mix for Myanmar patients (Samut Sakhon) and Mae Tao Clinic's admission mix. The
uncovered mass is injury and first aid, child immunization, NCD follow-up, mental health and
substance use, skin and wounds, and the registration and referral conversation that precedes
most hospital visits.

**What changes in the app (done today, additive):**
1. Topic list extended from six to twelve allowed domains in the schema and builder:
   `fever` (malaria and dengue triage, split from TB), `tb` (respiratory and TB, formerly
   `tb-malaria`, kept as an alias), `injury` (first aid, snakebite), `child-health`
   (immunization, nutrition, diarrhea in children), `ncd` (already allowed), `mental-health`,
   `skin-wound`, `insurance-consent` (already allowed), `pharmacy` (drug names, doses,
   finish the course, no steroid packs, no NSAIDs with fever), `diarrhea-cholera`.
2. Priority order for the next phrase batches: fever, TB, antenatal, child immunization,
   injury, pharmacy, diarrhea, insurance and referral, NCD, mental health, skin.
3. Five "high-value single phrases" to write first, each addressing a documented harm:
   no ibuprofen or aspirin when you have a fever; take the malaria pills for all 14 days even
   when you feel well; do not buy pill packs from the shop for pain; your child needs these
   vaccines, bring the yellow book; if you are bitten by a snake, keep still, do not cut or
   suck the bite, come now.
4. Existing seed phrases stay where they are; `tb-malaria` records continue to validate.

## Part B. Peer-reviewed evidence on migrants from Myanmar in Thailand (PubMed and Consensus, pulled 2026-10-13)

According to PubMed and Consensus, with DOIs:

### Kanchanaburi itself
- 73,762 registered migrants lived in Kanchanaburi province by December 2021, 80.1% from
  Myanmar; migrants were 22.3% of the province's 24,837 COVID-19 cases in 2020-2021; one in
  five cases were under 18. Healthcare attendance by migrants rose during the pandemic.
  Healthcare (Basel) 2023, https://doi.org/10.3390/healthcare11202724
- Plasmodium vivax is about 97% of all reported malaria in Thailand, "with transmission
  persisting in endemic border regions such as Kanchanaburi Province"; 109 clinical P. vivax
  isolates were collected in Kanchanaburi in 2023-2025. Parasite 2026,
  https://doi.org/10.1051/parasite/2026055
- Kanchanaburi has enough dengue hemorrhagic fever to support monthly forecasting models
  (strong seasonality, overdispersion). PLoS Negl Trop Dis 2026,
  https://doi.org/10.1371/journal.pntd.0014270
- Older evidence: migrants in Kanchanaburi are Burmese, Karen, and Mon; barriers are legal
  status, cost, and inability to speak Thai; Karen rely more on herbal and spirit medicine
  (Isarabhakdi 2004). Malaria in Sangkhlaburi villages: 42% Mon, 48% Karen respondents, with
  30-40% reporting prior malaria (Tipmontree 2009). Kanchanaburi migrants had the highest
  Plasmodium prevalence (13.7%) in a 2011 multi-province screening.

### What migrants actually present with
- Among 355 Myanmar migrants in Chiang Rai (2024), the most common major illnesses in the past
  six months were musculoskeletal disorders (23.4%) and injuries (18.8%). BMC Public Health
  2026 (Zaw Min et al.).
- National surveillance 2011 (803,817 cases): migrant workers vs Thai workers had higher
  relative risk for TB (men 1.4, women 2.3), STIs (2.4 / 1.6), and malaria (8.3 / 11.5, and up
  to 18-25 among farm workers), and lower risk for diarrhea, food poisoning, and dengue.
  Rakprasit et al., Industrial Health 2016.
- Hypertension: 27.8% of 414 registered Myanmar migrant workers (mean age 29) were hypertensive
  in a 2017 national survey, higher than Thailand (24.7%) or Myanmar (26.4%). IJERPH 2022,
  https://doi.org/10.3390/ijerph19063511. In northeastern Thailand, 63.3% of 406 Myanmar
  migrant workers had high blood pressure (72% of men); limited health literacy and no
  insurance raised the odds. PLoS One 2024, https://doi.org/10.1371/journal.pone.0302057
- Fever is the commonest reason to seek care on the border, and its meaning has shifted as
  malaria declined; health-seeking is shaped by precarious status. BMC Infect Dis 2023,
  https://doi.org/10.1186/s12879-023-08482-8
- Malaria care-seeking among short-term migrants in Tak (2025): 60% knew to seek care for fever
  or chills, only 35% did so within 24 hours, 2% carried asymptomatic P. vivax; Karen
  ethnicity was associated with less care-seeking. Malar J 2025,
  https://doi.org/10.1186/s12936-025-05539-8. Providers link the western-Thailand malaria
  resurgence to migration after the 2021 coup and name language barriers to health education as
  a key obstacle. Malar J 2025, https://doi.org/10.1186/s12936-025-05397-4. Only 27% of 300
  migrants had adequate access to malaria services. Malar J 2024 (Sripoorote et al.).
- In Tak and Mae Hong Son, non-Thais are 20-30% of the population; malaria surged in Umphang
  and Tha Song Yang 2020-2023 and TB incidence spiked, with non-Thais 2-3 times more affected.
  BMC Health Serv Res 2025 (Hong et al.).

### Tuberculosis
- A migrant-friendly TB program on the border (2013-2017): 1,344 cases, case fatality 9.5%,
  33 of 128 deaths before treatment, 9% lost to follow-up, treatment success 79.8%; mortality
  was 90% in HIV-positive patients not on antiretrovirals. Int J Tuberc Lung Dis 2020,
  https://doi.org/10.5588/ijtld.20.0014
- Myanmar migrants with TB in a border area: 87.4% treatment success; residential care raised
  the odds of success six-fold. Int J Tuberc Lung Dis 2022, https://doi.org/10.5588/ijtld.21.0532
- National surveillance 2016-2018: migrant TB loss-to-follow-up 21.5% vs 2.3% among Thais
  (Frontiers in Public Health 2025, from the earlier dossier).

### Maternal, newborn, mental health
- Antenatal care was the top migrant outpatient diagnosis in three of four years at a border
  hospital (Tha Phraya), TB in the fourth; normal delivery was the top inpatient diagnosis every
  year (earlier dossier).
- Perinatal depression on the border: 38.6% of migrant and 47.3% of refugee women (SMRU cohort).
  Phil Trans R Soc B 2021, https://doi.org/10.1098/rstb.2020.0030. Suicidal ideation in 5.3%
  of perinatal women. J Public Health 2022, https://doi.org/10.1093/pubmed/fdab297
- Extreme neonatal jaundice is a recognized problem in border clinics with phototherapy but
  limited exchange transfusion (BMJ Paediatr Open 2020, https://doi.org/10.1136/bmjpo-2020-000641);
  G6PD deficiency is common in the region and matters for both newborn jaundice and primaquine
  treatment of P. vivax.
- Breastfeeding knowledge among Burmese migrant mothers in Samut Sakhon: 66% good knowledge;
  non-Bamar ethnicity (which includes Mon and Karen) predicted lower knowledge and attitudes.
  BMJ Open 2024, https://doi.org/10.1136/bmjopen-2024-084609
- Depression prevalence 14.4% among Shan migrant workers in Chiang Mai. Glob Public Health 2024,
  https://doi.org/10.1080/17441692.2024.2334316
- One in five women migrant workers reported discrimination during COVID-19; among them 63%
  had experienced intimate partner violence. PLoS One 2024,
  https://doi.org/10.1371/journal.pone.0300388

### Behaviors and system factors
- Under half of Myanmar workers reach beginner (A1) Thai in speaking; under 10% in reading.
  PLoS One 2024, https://doi.org/10.1371/journal.pone.0312571
- Fisheries-sector migrants "treat myself first," then trusted people, then alternative
  treatment, then biomedical care; migrant health volunteers bridge the gap. PLOS Glob Public
  Health 2026, https://doi.org/10.1371/journal.pgph.0006765
- Unmet need among migrants in Phuket: 14.9%, driven by undocumented status (34%), cost (20%),
  and language (18%). BMC Health Serv Res 2024, https://doi.org/10.1186/s12913-024-11589-6

## Part C. National and regional numbers (web survey of 2026-10-13)

### C1. Thailand
- GBD 2021 top causes of lost healthy life (UNVERIFIED, IHME sheet blocked): stroke, road
  injuries, ischemic heart disease, diabetes, COVID-19, chronic kidney disease, lower
  respiratory infections, cirrhosis, HIV, lung cancer. Top risks: high blood sugar, high blood
  pressure, smoking, air pollution.
- Hypertension 25.4 percent of adults (national survey 2019); 57 percent of hypertensive men
  undiagnosed. Diabetes 10.1 percent, only 21 percent controlled (UNVERIFIED).
  https://pmc.ncbi.nlm.nih.gov/articles/PMC10866948
- Road deaths 18,218 in 2021, 84 percent motorcyclists. https://www.who.int/thailand/our-work/road-safety
- TB 2024: incidence 104,000 (146 per 100,000), notified 81,703, deaths 11,000, 7.4 percent
  HIV-positive, 1,045 rifampicin-resistant, treatment success 82 percent.
  https://extranet.who.int/tme/generateCSV.asp?ds=estimates
- HIV end-2024: 565,598 people living with HIV, 8,124 new infections a year, prevalence 8.2
  percent among people who inject drugs, 0.5 percent in antenatal clinics.
  https://hivhub.ddc.moph.go.th/officer/Download/RRTTR/HIV_Factsheet2024_EN_edit_060868.pdf
- Dengue 2025 to August 19: 38,687 cases, 37 deaths; Tak in the top ten provinces, Kanchanaburi
  not. https://he05.tci-thaijo.org/index.php/WESR/article/download/6538/5972/12816
- Leptospirosis 2,190 cases and 30 deaths, melioidosis 1,654 cases and 77 deaths, January to
  July 21, 2026. https://www.nationthailand.com/health-wellness/40069034
- Snakebite about 6,155 a year; vipers dominate. https://www.thaipbs.or.th/news/content/281247
- Mental health screening 2023-2024: 17 percent with signs of depression, 11 percent suicide
  risk. https://www.thaipbsworld.com/world/escalating-mental-health-concerns-in-thailand
- Hepatitis B surface antigen 1.7 percent nationally (2024, UNVERIFIED).

### C2. Myanmar
- GBD 2021 (UNVERIFIED): stroke, neonatal disorders, ischemic heart disease, COVID-19,
  diabetes, lower respiratory infections, COPD, congenital defects, tuberculosis.
- Conflict and collapse: 9.3 million need essential health services; 3.8 million displaced
  (June 2026); 1,939 attacks on health care since February 2021 with 175 health workers
  killed; the March 2025 earthquake killed over 4,700 and damaged about 640 facilities; US
  funding cuts suspended 65 facilities and 38 mobile clinics in 2025.
  https://myanmar.un.org/en/node/309616 ;
  https://myanmar.un.org/sites/default/files/2026-07/Myanmar%20Health%20Cluster%20Bulletin_June2026.pdf
- TB 2024: incidence 263,000 (482 per 100,000), notified 114,359 (falling), deaths 36,000,
  case detection 44 percent, 2,272 rifampicin-resistant. WHO Myanmar reports reduced TB control
  increased transmission.
- Malaria resurgence: Karen State program positives rose from 8,756 (2020) to 43,667 (2023),
  with P. falciparum up about 12-fold and artemisinin-resistance marker R561H in 95 percent
  of genotyped samples; national quarterly counts around 42,000 cases per quarter in 2024 and
  2025, 85 to 94 percent vivax; the Health Cluster calls malaria the highest reported
  infectious disease, with Tanintharyi (opposite Kanchanaburi) over alert threshold in 2026.
  https://pmc.ncbi.nlm.nih.gov/articles/PMC12951982
- Vaccine-preventable disease: 1.5 million under-fives missed basic vaccination since 2018;
  cholera at Shwe Kokko December 2024 (300 cases, 2 deaths) with two Mae Sot residents
  hospitalized; polio (cVDPV2) in Rakhine; measles risk high.
  https://ddc.moph.go.th/uploads/publish/1675020250128094148.pdf
- Maternal mortality 179 per 100,000 (2020), second highest in the WHO South-East Asia
  region; under-five mortality 37 per 1,000 (2024, UNVERIFIED); stunting 29 percent.
- Snakebite 15,079 facility-reported bites and 630 deaths in 2014; Russell's viper 85 percent
  of admissions in Mandalay; half bitten while farming. https://pmc.ncbi.nlm.nih.gov/articles/PMC6053239
- Hepatitis B 6.5 percent, hepatitis C 2.7 percent (2015 survey, UNVERIFIED).

### C3. Border and Kanchanaburi
- Mae Tao Clinic 2024: 126,631 consultations, 8,734 admissions, 1,889 deliveries, antenatal
  visits up to 11,286, obstetric referrals up 56 percent, women 62 percent of consultations.
  https://maetaoclinic.org/health-services/
- Samut Sakhon Hospital 2012-2016: Myanmar outpatient visits rose four-fold to 151,868; top
  outpatient groups after work-permit checks were respiratory, injury, symptoms, musculoskeletal,
  digestive; top inpatient groups pregnancy, injury, infectious disease; circulatory disease in
  the top five cost groups. https://he01.tci-thaijo.org/index.php/jnkp/article/download/203117/141680/624054
- Malaria in Thailand: Kanchanaburi 945 cases to July 2023 (third), 1,102 to June 9, 2024
  (second), 251 to late April 2024 (third); 5,126 cases nationally to June 10, 2026 with Tak,
  Kanchanaburi, and Mae Hong Son highest; about 90 percent vivax; historic problem districts
  Sai Yok, Sangkhlaburi, Thong Pha Phum. https://www.pptvhd36.com/health/news/5603 ;
  https://www.thansettakij.com/health-wellness/661035
- Diphtheria at Mae Sot Hospital July to December 2024: five unvaccinated Myanmar children,
  two died. https://he04.tci-thaijo.org/index.php/TJP/article/download/3164/2446/25701
- Hepatitis B carriage among Myanmar migrants: 9.7 percent (2010) and a pooled 7.4 percent
  across six studies (UNVERIFIED).
- Yaa chud pill packs in Kanchanaburi: 3 to 5 unlabeled pills for about 6 baht containing
  antibiotics plus steroids or NSAIDs, sold through grocery and drug shops, used mainly by
  migrant construction workers for pain. https://pmc.ncbi.nlm.nih.gov/articles/PMC6647088/
- Alcohol: 12.3 percent of 512 Myanmar men in Mae Sot were harmful or hazardous drinkers.
- Insurance: the MOPH-IOM migrant health volunteer program launched December 2025 in Tak only;
  a migrant health card price of 3,800 baht was proposed in February 2025 (UNVERIFIED).

## Part D. Data requests that would sharpen this (not available online)
- Kanchanaburi Provincial Health Office: top ten outpatient and inpatient diagnoses by
  nationality, 2023-2025.
- DDC Malaria Online: cases by district (Sangkhlaburi, Thong Pha Phum, Sai Yok) 2023-2026.
- Region 5 TB subcommittee: TB notifications and outcomes for non-Thai patients in Kanchanaburi.
- Any 2024-2026 outbreak investigations in the three border districts.
- Mae Tao Clinic 2025 annual report (Google Drive link on https://maetaoclinic.org/annual-reports/).
- IHME GBD 2023 country sheets for Thailand and Myanmar, once published.

Consensus searches used in this report require this notice: Create or connect a free Consensus
account to return more than 3 results per search in Claude Code.:
https://consensus.app/sign-up/?utm_source=claude_code&auth=claude_code
