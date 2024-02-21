# youtube-kids-ads-www24
This project involves analyzing ads that play on kids content on Youtube.
We aim to collect data from the most popular videos on Youtube and assess their appropriateness and relevance for child viewership (children under 9).

Directory Structure
```
.
├── data/
│   ├── high policy/
│   │   ├── labelled/
│   │   │   ├── usa/
|   │   │   │   ├── USA.csv 
|   │   │   │   ├── ad_Details_US.csv
│   │   |   |   └── unique_vid_US.csv
│   │   │   ├── uk/
|   │   │   │   ├── UK.csv 
|   │   │   │   ├── ad_Details_UK.csv
│   │   |   |   └── unique_vid_UK.csv
│   │   │   ├── france/
|   │   │   │   ├── France.csv 
|   │   │   │   ├── ad_Details_France.csv
│   │   |   |   └── unique_vid_France.csv
│   │   │   ├── germany/
|   │   │   │   ├── Germany.csv 
|   │   │   │   ├── ad_Details_Germany.csv
│   │   |   |   └── unique_vid_Germany.csv
│   │   │   └──sweden/
|   │   │       ├── Sweden.csv 
|   │   │       ├── ad_Details_Sweden.csv
│   │   |       └── unique_vid_Sweden.csv
│   │   │ 
│   │   └── unlabelled/
│   │       ├── usa/
|   │       │   ├── USA_unlabelled.csv 
|   │       │   ├── ad_Details_US_unlabelled.csv
│   │       |   └── unique_vid_US_unlabelled.csv
│   │       ├── uk/
|   │       │   ├── UK_unlabelled.csv 
|   │       │   ├── ad_Details_UK_unlabelled.csv
│   │       |   └── unique_vid_UK_unlabelled.csv
│   │       ├── france/
|   │       │   ├── France_unlabelled.csv 
|   │       │   ├── ad_Details_France_unlabelled.csv
│   │       |   └── unique_vid_France_unlabelled.csv
│   │       ├── germany/
|   │       │   ├── Germany_unlabelled.csv 
|   │       │   ├── ad_Details_Germany_unlabelled.csv
│   │       |   └── unique_vid_Germany_unlabelled.csv
│   │       └──sweden/
|   │           ├── Sweden_unlabelled.csv 
|   │           ├── ad_Details_Sweden_unlabelled.csv
│   │           └── unique_vid_Sweden_unlabelled.csv
│   │    
│   └──low policy/
│       ├── labelled/
│       │   ├── pakistan/
|       │   │   ├── Pakistan.csv 
|       │   │   ├── ad_Details_Pakistan.csv
│       |   |   └── unique_vid_Pakistan.csv
│       │   ├── bangladesh/
|       │   │   ├── Bangladesh.csv 
|       │   │   ├── ad_Details_Bangladesh.csv
│       |   |   └── unique_vid_Bangladesh.csv
│       │   ├── morocco/
|       │   │   ├── Morocco.csv 
|       │   │   ├── ad_Details_Morocco.csv
│       |   |   └── unique_vid_Morocco.csv
│       │   ├── sri lanka/
|       │   │   ├── SriLanka.csv 
|       │   │   ├── ad_Details_SriLanka.csv
│       |   |   └── unique_vid_SriLanka.csv
│       │   └──venezuela/
|       │       ├── Venezuela.csv 
|       │       ├── ad_Details_Venezuela.csv
│       |       └── unique_vid_Venezuela.csv
│       └──unlabelled/
│           ├── pakistan/
|           │   ├── Pakistan_unlabelled.csv 
|           │   ├── ad_Details_Pakistan_unlabelled.csv
│           |   └── unique_vid_Pakistan_unlabelled.csv
│           ├── bangladesh/
|           │   ├── Bangladesh_unlabelled.csv 
|           │   ├── ad_Details_Bangladesh_unlabelled.csv
│           |   └── unique_vid_Bangladesh_unlabelled.csv
│           ├── morocco/
|           │   ├── Morocco_unlabelled.csv 
|           │   ├── ad_Details_Morocco_unlabelled.csv
│           |   └── unique_vid_Morocco_unlabelled.csv
│           ├── sri lanka/
|           │   ├── Sir Lanka_unlabelled.csv 
|           │   ├── ad_Details_SriLanka_unlabelled.csv
│           |   └── unique_vid_SriLanka_unlabelled.csv
│           └──venezuela/
|               ├── Venezuela_unlabelled.csv 
|               ├── ad_Details_Venezuela_unlabelled.csv
│               └── unique_vid_Venezuela_unlabelled.csv
├── codebook
|    ├── labelled/
|    │   ├── Bangladesh 1.csv ~> ads tagged from Bangladesh by coder #1
|    │   ├── Bangladesh 2.csv ~> ads tagged from Bangladesh by coder #2
|    │   ├── Pakistan 1.csv
|    │   ├── Pakistan 2.csv
|    │   ├── Morocco 1.csv
|    │   ├── Morocco 2.csv
|    │   ├── Venezuela 1.csv
|    │   ├── Venezuela 2.csv
|    │   ├── Sri Lanka 1.csv
|    │   ├── Sri Lanka 2.csv
|    │   ├── US 1.csv
│    |   ├── US 2.csv
│    |   ├── UK 1.csv 
│    |   ├── UK 2.csv
│    |   ├── Sweden 1.csv
│    |   ├── Sweden 2.csv
│    |   ├── Germany 1.csv
│    |   ├── Germany 2.csv
│    |   ├── France 1.csv
│    |   └── France 2.csv
|    |   
|    ├── unlabelled/
|    │   ├── UL_Bangladesh1.csv
|    │   ├── UL_Bangladesh2.csv
|    │   ├── UL_Pakistan1.csv
|    │   ├── UL_Pakistan2.csv
|    │   ├── UL_Morocco1.csv
|    │   ├── UL_Morocco2.csv
|    │   ├── UL_Venezuela1.csv
|    │   ├── UL_Venezuela2.csv
|    │   ├── UL_Sri Lanka1.csv
|    │   ├── UL_Sri Lanka2.csv
|    │   ├── UL_US1.csv
│    |   ├── UL_US2.csv
│    |   ├── UL_UK1.csv 
│    |   ├── UL_UK2.csv
│    |   ├── UL_Sweden1.csv
│    |   ├── UL_Sweden2.csv
│    |   ├── UL_Germany1.csv
│    |   ├── UL_Germany2.csv
│    |   ├── UL_France1.csv
│    |   └── UL_France2.csv
|    |
|    └── Master Codebook Weighted.xlsx ~> excel file with all tagged ads + tag aggregates
|
└── src
    ├── 
    ├──
    └── 
```

