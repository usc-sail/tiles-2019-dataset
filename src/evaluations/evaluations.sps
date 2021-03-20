* Encoding: UTF-8.
***Attending evaluations***

**Patient Care and Procedural Skills**
*Compute means across evaluations*

COMPUTE micuattn_pcps_mean=MEAN(micuattn_pcps.1, micuattn_pcps.2, micuattn_pcps.3). 
EXECUTE.

**Medical Knowledge**
*Compute means across evaluations*

COMPUTE micuattn_mk_mean=MEAN(micuattn_mk.1, micuattn_mk.2, micuattn_mk.3). 
EXECUTE.

**System-Based Practices**
*Compute means across evaluations*

COMPUTE micuattn_sbp_mean=MEAN(micuattn_sbp.1, micuattn_sbp.2, micuattn_sbp.3). 
EXECUTE.

**Practice-Based Learning and Improvement**
*Compute means across evaluations*

COMPUTE micuattn_pbli_mean=MEAN(micuattn_pbli.1, micuattn_pbli.2, micuattn_pbli.3). 
EXECUTE.

**Professionalism**
*Compute means across evaluations*

COMPUTE micuattn_prof_mean=MEAN(micuattn_prof.1, micuattn_prof.2, micuattn_prof.3). 
EXECUTE.

**Interpersonal and Communication Skills**
*Compute means across evaluations*

COMPUTE micuattn_ics_mean=MEAN(micuattn_ics.1, micuattn_ics.2, micuattn_ics.3). 
EXECUTE.

***Peer Evaluations***
**Interpersonal and Communication Skills 1**
*Recode 0s into missing (0 = no interaction) for Peer Evaluation 1*

RECODE micupeer_ics1.1 (1=1) (2=2) (3=3) (4=4) (5=5) (0=SYSMIS) INTO micupeer_ics1.1r. 
VARIABLE LABELS  micupeer_ics1.1r 'micupeer_ics1.1 recoded'. 
EXECUTE.

*Recode 0s into missing (0 = no interaction) for Peer Evaluation 2*

RECODE micupeer_ics1.2 (1=1) (2=2) (3=3) (4=4) (5=5) (0=SYSMIS) INTO micupeer_ics1.2r. 
VARIABLE LABELS  micupeer_ics1.2r 'micupeer_ics1.2 recoded'. 
EXECUTE.

*Recode 0s into missing (0 = no interaction) for Peer Evaluation 3*

RECODE micupeer_ics1.3 (1=1) (2=2) (3=3) (4=4) (5=5) (0=SYSMIS) INTO micupeer_ics1.3r. 
VARIABLE LABELS  micupeer_ics1.3r 'micupeer_ics1.3 recoded'. 
EXECUTE.

*Recode 0s into missing (0 = no interaction) for Peer Evaluation 4*

RECODE micupeer_ics1.4 (1=1) (2=2) (3=3) (4=4) (5=5) (0=SYSMIS) INTO micupeer_ics1.4r. 
VARIABLE LABELS  micupeer_ics1.4r 'micupeer_ics1.4 recoded'. 
EXECUTE.

*Recode 0s into missing (0 = no interaction) for Peer Evaluation 5*

RECODE micupeer_ics1.5 (1=1) (2=2) (3=3) (4=4) (5=5) (0=SYSMIS) INTO micupeer_ics1.5r. 
VARIABLE LABELS  micupeer_ics1.5r 'micupeer_ics1.5 recoded'. 
EXECUTE.

*Recode 0s into missing (0 = no interaction) for Peer Evaluation 6*

RECODE micupeer_ics1.6 (1=1) (2=2) (3=3) (4=4) (5=5) (0=SYSMIS) INTO micupeer_ics1.6r. 
VARIABLE LABELS  micupeer_ics1.6r 'micupeer_ics1.6 recoded'. 
EXECUTE.

*Recode 0s into missing (0 = no interaction) for Peer Evaluation 7*

RECODE micupeer_ics1.7 (1=1) (2=2) (3=3) (4=4) (5=5) (0=SYSMIS) INTO micupeer_ics1.7r. 
VARIABLE LABELS  micupeer_ics1.7r 'micupeer_ics1.7 recoded'. 
EXECUTE.

*Recode 0s into missing (0 = no interaction) for Peer Evaluation 8*

RECODE micupeer_ics1.8 (1=1) (2=2) (3=3) (4=4) (5=5) (0=SYSMIS) INTO micupeer_ics1.8r. 
VARIABLE LABELS  micupeer_ics1.8r 'micupeer_ics1.8 recoded'. 
EXECUTE.

*Recode 0s into missing (0 = no interaction) for Peer Evaluation 9*

RECODE micupeer_ics1.9 (1=1) (2=2) (3=3) (4=4) (5=5) (0=SYSMIS) INTO micupeer_ics1.9r. 
VARIABLE LABELS  micupeer_ics1.9r 'micupeer_ics1.9 recoded'. 
EXECUTE.

*Compute means across evaluations*

COMPUTE micupeer_ics1_mean=MEAN(micupeer_ics1.1_r, micupeer_ics1.2_r, micupeer_ics1.3_r, micupeer_ics1.4_r, micupeer_ics1.5_r, micupeer_ics1.6_r, micupeer_ics1.7_r, 
    micupeer_ics1.8_r, micupeer_ics1.9_r). 
EXECUTE.


**Interpersonal Skills and Communication 2**
*Recode 0s into missing (0 = no interaction) for Peer Evaluation 1*

RECODE micupeer_ics2.1 (1=1) (2=2) (3=3) (4=4) (5=5) (0=SYSMIS) INTO micupeer_ics2.1r. 
VARIABLE LABELS  micupeer_ics2.1r 'micupeer_ics2.1 recoded'. 
EXECUTE.

*Recode 0s into missing (0 = no interaction) for Peer Evaluation 2*

RECODE micupeer_ics2.2 (1=1) (2=2) (3=3) (4=4) (5=5) (0=SYSMIS) INTO micupeer_ics2.2r. 
VARIABLE LABELS  micupeer_ics2.2r 'micupeer_ics2.2 recoded'. 
EXECUTE.

*Recode 0s into missing (0 = no interaction) for Peer Evaluation 3*

RECODE micupeer_ics2.3 (1=1) (2=2) (3=3) (4=4) (5=5) (0=SYSMIS) INTO micupeer_ics2.3r. 
VARIABLE LABELS  micupeer_ics2.3r 'micupeer_ics2.3 recoded'. 
EXECUTE.

*Recode 0s into missing (0 = no interaction) for Peer Evaluation 4*

RECODE micupeer_ics2.4 (1=1) (2=2) (3=3) (4=4) (5=5) (0=SYSMIS) INTO micupeer_ics2.4r. 
VARIABLE LABELS  micupeer_ics2.4r 'micupeer_ics2.4 recoded'. 
EXECUTE.

*Recode 0s into missing (0 = no interaction) for Peer Evaluation 5*

RECODE micupeer_ics2.5 (1=1) (2=2) (3=3) (4=4) (5=5) (0=SYSMIS) INTO micupeer_ics2.5r. 
VARIABLE LABELS  micupeer_ics2.5r 'micupeer_ics2.5 recoded'. 
EXECUTE.

*Recode 0s into missing (0 = no interaction) for Peer Evaluation 6*

RECODE micupeer_ics2.6 (1=1) (2=2) (3=3) (4=4) (5=5) (0=SYSMIS) INTO micupeer_ics2.6r. 
VARIABLE LABELS  micupeer_ics2.6r 'micupeer_ics2.6 recoded'. 
EXECUTE.

*Recode 0s into missing (0 = no interaction) for Peer Evaluation 7*

RECODE micupeer_ics2.7 (1=1) (2=2) (3=3) (4=4) (5=5) (0=SYSMIS) INTO micupeer_ics2._r. 
VARIABLE LABELS  micupeer_ics2.7r 'micupeer_ics2.7 recoded'. 
EXECUTE.

*Recode 0s into missing (0 = no interaction) for Peer Evaluation 8*

RECODE micupeer_ics2.8 (1=1) (2=2) (3=3) (4=4) (5=5) (0=SYSMIS) INTO micupeer_ics2.8r. 
VARIABLE LABELS  ics2.8r 'ics2.8 recoded'. 
EXECUTE.

*Recode 0s into missing (0 = no interaction) for Peer Evaluation 9*

RECODE micupeer_ics2.9 (1=1) (2=2) (3=3) (4=4) (5=5) (0=SYSMIS) INTO micupeer_ics2.9r. 
VARIABLE LABELS  micupeer_ics2.9r 'micupeer_ics2.9 recoded'. 
EXECUTE.

*Compute means across evaluations*

COMPUTE micupeer_ics2_mean=MEAN(micupeer_ics2.1_r, micupeer_ics2.2_r, micupeer_ics2.3_r, micupeer_ics2.4_r, micupeer_ics2.5_r, micupeer_ics2.6_r, micupeer_ics2.7_r, 
    micupeer_ics2.8_r, micupeer_ics2.9_r). 
EXECUTE.

**Intepersonal and Communication Skills 3**
*Recode 0s into missing (0 = no interaction) for Peer Evaluation 1*

RECODE micupeer_ics3.1 (1=1) (2=2) (3=3) (4=4) (5=5) (0=SYSMIS) INTO micupeer_ics3.1r. 
VARIABLE LABELS  micupeer_ics3.1r 'micupeer_ics3.1 recoded'. 
EXECUTE.

*Recode 0s into missing (0 = no interaction) for Peer Evaluation 2*

RECODE micupeer_ics3.2 (1=1) (2=2) (3=3) (4=4) (5=5) (0=SYSMIS) INTO micupeer_ics3.2r. 
VARIABLE LABELS  micupeer_ics3.2r 'micupeer_ics3.2 recoded'. 
EXECUTE.

*Recode 0s into missing (0 = no interaction) for Peer Evaluation 3*

RECODE micupeer_ics3.3 (1=1) (2=2) (3=3) (4=4) (5=5) (0=SYSMIS) INTO micupeer_ics3.3r. 
VARIABLE LABELS  micupeer_ics3.3r 'micupeer_ics3.3 recoded'. 
EXECUTE.

*Recode 0s into missing (0 = no interaction) for Peer Evaluation 4*

RECODE micupeer_ics3.4 (1=1) (2=2) (3=3) (4=4) (5=5) (0=SYSMIS) INTO micupeer_ics3.4r. 
VARIABLE LABELS  micupeer_ics3.4r 'micupeer_ics3.4 recoded'. 
EXECUTE.

*Recode 0s into missing (0 = no interaction) for Peer Evaluation 5*

RECODE micupeer_ics3.5 (1=1) (2=2) (3=3) (4=4) (5=5) (0=SYSMIS) INTO micupeer_ics3.5r. 
VARIABLE LABELS  micupeer_ics3.5r 'micupeer_ics3.5 recoded'. 
EXECUTE.

*Recode 0s into missing  (0 = no interaction) for Peer Evaluation 6*

RECODE micupeer_ics3.6 (1=1) (2=2) (3=3) (4=4) (5=5) (0=SYSMIS) INTO micupeer_ics3.6r. 
VARIABLE LABELS  micupeer_ics3.6r 'micupeer_ics3.6 recoded'. 
EXECUTE.

*Recode 0s into missing (0 = no interaction) for Peer Evaluation 7*

RECODE micupeer_ics3.7 (1=1) (2=2) (3=3) (4=4) (5=5) (0=SYSMIS) INTO micupeer_ics3.7r. 
VARIABLE LABELS  micupeer_ics3.7r 'micupeer_ics3.7 recoded'. 
EXECUTE.

*Recode 0s into missing (0 = no interaction) for Peer Evaluation 8*

RECODE micupeer_ics3.8 (1=1) (2=2) (3=3) (4=4) (5=5) (0=SYSMIS) INTO micupeer_ics3.8r. 
VARIABLE LABELS  micupeer_ics3.8r 'micupeer_ics3.8 recoded'. 
EXECUTE.

*Recode 0s into missing (0 = no interaction) for Peer Evaluation 9*

RECODE micupeer_ics3.9 (1=1) (2=2) (3=3) (4=4) (5=5) (0=SYSMIS) INTO micupeer_ics3.9r. 
VARIABLE LABELS  micupeer_ics3.9r 'micupeer_ics3.9 recoded'. 
EXECUTE.

*Compute means across evaluations*

COMPUTE micupeer_ics3_mean=MEAN(micupeer_ics3.1_r, micupeer_ics3.2_r, micupeer_ics3.3_r, micupeer_ics3.4_r, micupeer_ics3.5_r, micupeer_ics3.6_r, micupeer_ics3.7_r, 
    micupeer_ics3.8_r, micupeer_ics3.9_r). 
EXECUTE.

**Patient Care and Procedural Skills**
*Recode 0s into missing (0 = no interaction) for Peer Evaluation 1*

RECODE micupeer_pcps.1 (1=1) (2=2) (3=3) (4=4) (5=5) (0=SYSMIS) INTO micupeer_pcps.1r. 
VARIABLE LABELS  pcps.1r 'pcps.1 recoded'. 
EXECUTE.

*Recode 0s into missing (0 = no interaction) for Peer Evaluation 2*

RECODE micupeer_pcps.2 (1=1) (2=2) (3=3) (4=4) (5=5) (0=SYSMIS) INTO micupeer_pcps.2r. 
VARIABLE LABELS  micupeer_pcps.2r 'micupeer_pcps.2 recoded'. 
EXECUTE.

*Recode 0s into missing (0 = no interaction) for Peer Evaluation 3*

RECODE micupeer_pcps.3 (1=1) (2=2) (3=3) (4=4) (5=5) (0=SYSMIS) INTO micupeer_pcps.3r. 
VARIABLE LABELS  micupeer_pcps.3r 'micupeer_pcps.3 recoded'. 
EXECUTE.

*Recode 0s into missing (0 = no interaction) for Peer Evaluation 4*

RECODE micupeer_pcps.4 (1=1) (2=2) (3=3) (4=4) (5=5) (0=SYSMIS) INTO micupeer_pcps.4r. 
VARIABLE LABELS  micupeer_pcps.4r 'micupeer_pcps.4 recoded'. 
EXECUTE.

*Recode 0s into missing (0 = no interaction) for Peer Evaluation 5*

RECODE micupeer_pcps.5 (1=1) (2=2) (3=3) (4=4) (5=5) (0=SYSMIS) INTO micupeer_pcps.5r. 
VARIABLE LABELS  micupeer_pcps.5r 'micupeer_pcps.5 recoded'. 
EXECUTE.

*Recode 0s into missing (0 = no interaction) for Peer Evaluation 6*

RECODE micupeer_pcps.6 (1=1) (2=2) (3=3) (4=4) (5=5) (0=SYSMIS) INTO micupeer_pcps.6r. 
VARIABLE LABELS  micupeer_pcps.6r 'micupeer_pcps.6 recoded'. 
EXECUTE.

*Recode 0s into missing (0 = no interaction) for Peer Evaluation 7*

RECODE micupeer_pcps.7 (1=1) (2=2) (3=3) (4=4) (5=5) (0=SYSMIS) INTO micupeer_pcps.7r. 
VARIABLE LABELS  micupeer_pcps.7r 'micupeer_pcps.7 recoded'. 
EXECUTE.

*Recode 0s into missing (0 = no interaction) for Peer Evaluation 8*

RECODE micupeer_pcps.8 (1=1) (2=2) (3=3) (4=4) (5=5) (0=SYSMIS) INTO micupeer_pcps.8r. 
VARIABLE LABELS  micupeer_pcps.8r 'micupeer_pcps.8 recoded'. 
EXECUTE.

*Recode 0s into missing (0 = no interaction) for Peer Evaluation 9*

RECODE micupeer_pcps.9 (1=1) (2=2) (3=3) (4=4) (5=5) (0=SYSMIS) INTO micupeer_pcps.9r. 
VARIABLE LABELS  micupeer_pcps.9r 'micupeer_pcps.9 recoded'. 
EXECUTE.

*Compute means across evaluations*

COMPUTE micupeer_pcps_mean=MEAN(micupeer_pcps.1r, micupeer_pcps.2r, micupeer_pcps.3r, micupeer_pcps.4r, micupeer_pcps.5r, micupeer_pcps.6r, micupeer_pcps.7r, micupeer_pcps.8r, 
    micupeer_pcps.9r). 
EXECUTE.  

**Professionalism 1**
*Recode 0s into missing (0 = no interaction) for Peer Evaluation 1*

RECODE micupeer_prof1.1 (1=1) (2=2) (3=3) (4=4) (5=5) (0=SYSMIS) INTO micupeer_prof1.1r. 
VARIABLE LABELS  micupeer_prof1.1r 'micupeer_prof1.1 recoded'. 
EXECUTE.

*Recode 0s into missing (0 = no interaction) for Peer Evaluation 2*

RECODE micupeer_prof1.2 (1=1) (2=2) (3=3) (4=4) (5=5) (0=SYSMIS) INTO micupeer_prof1.2r. 
VARIABLE LABELS  micupeer_prof1.2r 'micupeer_prof1.2 recoded'. 
EXECUTE.

*Recode 0s into missing (0 = no interaction) for Peer Evaluation 3*

RECODE micupeer_prof1.3 (1=1) (2=2) (3=3) (4=4) (5=5) (0=SYSMIS) INTO micupeer_prof1.3r. 
VARIABLE LABELS  micupeer_prof1.3r micupeer_'prof1.3 recoded'. 
EXECUTE.

*Recode 0s into missing (0 = no interaction) for Peer Evaluation 4*

RECODE micupeer_prof1.4 (1=1) (2=2) (3=3) (4=4) (5=5) (0=SYSMIS) INTO micupeer_prof1.4r. 
VARIABLE LABELS  micupeer_prof1.4r 'micupeer_prof1.4 recoded'. 
EXECUTE.

*Recode 0s into missing (0 = no interaction) for Peer Evaluation 5*

RECODE micupeer_prof1.5 (1=1) (2=2) (3=3) (4=4) (5=5) (0=SYSMIS) INTO micupeer_prof1.5r. 
VARIABLE LABELS  micupeer_prof1.5r 'micupeer_prof1.5 recoded'. 
EXECUTE.

*Recode 0s into missing (0 = no interaction) for Peer Evaluation 6*

RECODE micupeer_prof1.6 (1=1) (2=2) (3=3) (4=4) (5=5) (0=SYSMIS) INTO micupeer_prof1.6r. 
VARIABLE LABELS  micupeer_prof1.6r 'micupeer_prof1.6 recoded'. 
EXECUTE.

*Recode 0s into missing (0 = no interaction) for Peer Evaluation 7*

RECODE micupeer_prof1.7 (1=1) (2=2) (3=3) (4=4) (5=5) (0=SYSMIS) INTO micupeer_prof1.7r. 
VARIABLE LABELS  micupeer_prof1.7r 'micupeer_prof1.7 recoded'. 
EXECUTE.

*Recode 0s into missing (0 = no interaction) for Peer Evaluation 8*

RECODE micupeer_prof1.8 (1=1) (2=2) (3=3) (4=4) (5=5) (0=SYSMIS) INTO micupeer_prof1.8r. 
VARIABLE LABELS  micupeer_prof1.8r 'micupeer_prof1.8 recoded'. 
EXECUTE.

*Recode 0s into missing (0 = no interaction) for Peer Evaluation 9*

RECODE prof1.9 (1=1) (2=2) (3=3) (4=4) (5=5) (0=SYSMIS) INTO prof1.9r. 
VARIABLE LABELS  prof1.9r 'prof1.9 recoded'. 
EXECUTE.

*Compute means across evaluations*

COMPUTE micupeer_prof1_mean=MEAN(micupeer_prof1.1r, micupeer_prof1.2r, micupeer_prof1.3r, micupeer_prof1.4r, micupeer_prof1.5r, micupeer_prof1.6r, micupeer_prof1.7r, 
    micupeer_prof1.8r, micupeer_prof1.9r). 
EXECUTE.

**Professionalism 2**
*Recode 0s into missing (0 = no interaction) for Peer Evaluation 1*

RECODE micupeer_prof2.1 (1=1) (2=2) (3=3) (4=4) (5=5) (0=SYSMIS) INTO micupeer_prof2.1r. 
VARIABLE LABELS  micupeer_prof2.1r 'micupeer_prof2.1 recoded'. 
EXECUTE.

*Recode 0s into missing (0 = no interaction) for Peer Evaluation 2*

RECODE micupeer_prof2.2 (1=1) (2=2) (3=3) (4=4) (5=5) (0=SYSMIS) INTO micupeer_prof2.2r. 
VARIABLE LABELS  micupeer_prof2.2r 'micupeer_prof2.2 recoded'. 
EXECUTE.

*Recode 0s into missing (0 = no interaction) for Peer Evaluation 3*

RECODE micupeer_prof2.3 (1=1) (2=2) (3=3) (4=4) (5=5) (0=SYSMIS) INTO micupeer_prof2.3r. 
VARIABLE LABELS  micupeer_prof2.3r 'micupeer_prof2.3 recoded'. 
EXECUTE.

*Recode 0s into missing (0 = no interaction) for Peer Evaluation 4*

RECODE micupeer_prof2.4 (1=1) (2=2) (3=3) (4=4) (5=5) (0=SYSMIS) INTO micupeer_prof2.4r. 
VARIABLE LABELS  micupeer_prof2.4r 'micupeer_prof2.4 recoded'. 
EXECUTE.

*Recode 0s into missing (0 = no interaction) for Peer Evaluation 5*

RECODE micupeer_prof2.5 (1=1) (2=2) (3=3) (4=4) (5=5) (0=SYSMIS) INTO micupeer_prof2.5r. 
VARIABLE LABELS  micupeer_prof2.5r 'micupeer_prof2.5 recoded'. 
EXECUTE.

*Recode 0s into missing (0 = no interaction) for Peer Evaluation 6*

RECODE micupeer_prof2.6 (1=1) (2=2) (3=3) (4=4) (5=5) (0=SYSMIS) INTO micupeer_prof2.6r. 
VARIABLE LABELS  micupeer_prof2.6r 'micupeer_prof2.6 recoded'. 
EXECUTE.

*Recode 0s into missing (0 = no interaction) for Peer Evaluation 7*


RECODE micupeer_prof2.7 (1=1) (2=2) (3=3) (4=4) (5=5) (0=SYSMIS) INTO micupeer_prof2.7r. 
VARIABLE LABELS  micupeer_prof2.7r 'micupeer_prof2.7 recoded'. 
EXECUTE.

*Recode 0s into missing (0 = no interaction) for Peer Evaluation 8*

RECODE micupeer_prof2.8 (1=1) (2=2) (3=3) (4=4) (5=5) (0=SYSMIS) INTO micupeer_prof2.8r. 
VARIABLE LABELS  micupeer_prof2.8r 'micupeer_prof2.8 recoded'. 
EXECUTE.

*Recode 0s into missing (0 = no interaction) for Peer Evaluation 9*

RECODE micupeer_prof2.9 (1=1) (2=2) (3=3) (4=4) (5=5) (0=SYSMIS) INTO micupeer_prof2.9r. 
VARIABLE LABELS  micupeer_prof2.9r 'micupeer_prof2.9 recoded'. 
EXECUTE.

*Compute means across evaluations*

COMPUTE micupeer_prof2_mean=MEAN(micupeer_prof2.1r, micupeer_prof2.2r, micupeer_prof2.3r, micupeer_prof2.4r, micupeer_prof2.5r, micupeer_prof2.6r, micupeer_prof2.7r, 
    micupeer_prof2.8r, micupeer_prof2.9r). 
EXECUTE.

**Professionalism 3**
*Recode 0s into missing (0 = no interaction) for Peer Evaluation 1*

RECODE micupeer_prof3.1 (1=1) (2=2) (3=3) (4=4) (5=5) (0=SYSMIS) INTO micupeer_prof3.1r. 
VARIABLE LABELS  micupeer_prof3.1r 'micupeer_prof3.1 recoded'. 
EXECUTE.

*Recode 0s into missing (0 = no interaction) for Peer Evaluation 2*

RECODE micupeer_prof3.2 (1=1) (2=2) (3=3) (4=4) (5=5) (0=SYSMIS) INTO micupeer_prof3.2r. 
VARIABLE LABELS  micupeer_prof3.2r 'micupeer_prof3.2 recoded'. 
EXECUTE.

*Recode 0s into missing (0 = no interaction) for Peer Evaluation 3*

RECODE micupeer_prof3.3 (1=1) (2=2) (3=3) (4=4) (5=5) (0=SYSMIS) INTO micupeer_prof3.3r. 
VARIABLE LABELS  micupeer_prof3.3r 'micupeer_prof3.3 recoded'. 
EXECUTE.

*Recode 0s into missing (0 = no interaction) for Peer Evaluation 4*

RECODE micupeer_prof3.4 (1=1) (2=2) (3=3) (4=4) (5=5) (0=SYSMIS) INTO micupeer_prof3.4r. 
VARIABLE LABELS  micupeer_prof3.4r 'micupeer_prof3.4 recoded'. 
EXECUTE.

*Recode 0s into missing (0 = no interaction) for Peer Evaluation 5*

RECODE micupeer_prof3.5 (1=1) (2=2) (3=3) (4=4) (5=5) (0=SYSMIS) INTO micupeer_prof3.5r. 
VARIABLE LABELS  micupeer_prof3.5r 'micupeer_prof3.5 recoded'. 
EXECUTE.

*Recode 0s into missing (0 = no interaction) for Peer Evaluation 6*

RECODE micupeer_prof3.6 (1=1) (2=2) (3=3) (4=4) (5=5) (0=SYSMIS) INTO micupeer_prof3.6r. 
VARIABLE LABELS  micupeer_prof3.6r micupeer_'prof3.6 recoded'. 
EXECUTE.

*Recode 0s into missing (0 = no interaction) for Peer Evaluation 7*

RECODE micupeer_prof3.7 (1=1) (2=2) (3=3) (4=4) (5=5) (0=SYSMIS) INTO micupeer_prof3.7r. 
VARIABLE LABELS  micupeer_prof3.7r 'micupeer_prof3.7 recoded'. 
EXECUTE.

*Recode 0s into missing (0 = no interaction) for Peer Evaluation 8*

RECODE micupeer_prof3.8 (1=1) (2=2) (3=3) (4=4) (5=5) (0=SYSMIS) INTO micupeer_prof3.8r. 
VARIABLE LABELS  micupeer_prof3.8r 'micupeer_prof3.8 recoded'. 
EXECUTE.

*Recode 0s into missing (0 = no interaction) for Peer Evaluation 9*

RECODE micupeer_prof3.9 (1=1) (2=2) (3=3) (4=4) (5=5) (0=SYSMIS) INTO micupeer_prof3.9r. 
VARIABLE LABELS  micupeer_prof3.9r 'micupeer_prof3.9 recoded'. 
EXECUTE.

*Compute means across evaluations*

COMPUTE micupeer_prof3_mean=MEAN(micupeer_prof3.1r, micupeer_prof3.2r, micupeer_prof3.3r, micupeer_prof3.4r, micupeer_prof3.5r, micupeer_prof3.6r, micupeer_prof3.7r, 
    micupeer_prof3.8r, micupeer_prof3.9r). 
EXECUTE.



