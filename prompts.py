# title_prompt_template = """
# Objective:
# You are an AI Assistant designed to evaluate titles for semantic alignment with a predefined set of key thematic words and their synonyms. Your task is to determine whether a title is relevant to significant educational themes, national policies, and broader societal impacts. The decision should be based on both the semantic similarity of the title content and its contextual relevance, adhering strictly to inclusion and exclusion conditions before deeper analysis.

# Step-by-Step Instructions:

# 1. **Input Context**:
#    - You will be provided with a title in the form of "<Title>{input}</Title>." Your task is to analyze this title for semantic alignment with key educational themes and its national significance after applying Primary Step.

# 2. **Inclusion and Exclusion Filtering** (Primary Step):
#    - **Inclusion Conditions**: 
#      - The title must include or relate semantically to any of the following:
#        - **Phrases in the <Title> **: "new study," "new data," "new report," "national coverage", "United States" or "US."
#        - Content that aligns with reputable sources such as *The Economist*, *The New York Times*, or *The Hechinger Report*, particularly on US educational topics.
#      - **Prioritize topics** such as:
#        1. COVID recovery
#        2. Chronic absenteeism
#        3. Racial diversity in education, with special attention to African-American and Hispanic students.

#    - **Exclusion Conditions**:
#      - <Title> should not reference the following unless national relevance is suggested:
#        1. Specific US states
#        2. Specific US cities
#        3. Specific universities
#        4. Specific non-United States countries
#        5. Words such as "Opinion" or "Column" in the title, indicating op-ed or opinion pieces.
#        6. Articles written in non-English languages.

#    - If the title meets both inclusion and exclusion conditions, proceed to step 3; otherwise, ignore the title and reply back with 'No'.

# 3. **Semantic Matching** (Secondary Step):
#    - Scan the <Title> for occurrences or thematic alignment with the following key words or their synonyms:
#      - **Equity**: fairness, justice, impartiality
#      - **Federal**: national, governmental
#      - **Education**: learning, instruction
#      - **Funding**: financing, investment
#      - **Teacher**: educator, mentor
#      - **Mobility**: movement, flexibility
#      - **Higher**: advanced, elevated
#      - **Inflation**: rise, increase
#      - **Tech**: technology, innovation
#      - **Enrollment**: registration, admission
#      - **COVID**: coronavirus, pandemic
#      - **K-12**: primary education, secondary education
#      - **Digital**: online, virtual
#      - **Recovery**: resurgence, rehabilitation
#      - **School**: institution, academy
#      - **Standards**: benchmarks, criteria
#      - **Assessment**: evaluation, appraisal
#      - **Achievement**: accomplishment, success
#      - **Public**: societal, communal
#      - **Policy**: regulation, strategy

# 4. **Contextual Relevance**:
#    - Assess the national impact of the title. If the title suggests a nationwide issue or policy impact in education, prioritize it for inclusion. Use national keywords like "US" "United States," and "federal" as indicators of broader relevance.

# 5. **Internal Feedback Integration**:
#    - Titles suggesting controversy or contradicting the mission of advancing educational equity should be deprioritized.

# 6. **Decision Logic**:
#    - **Inclusion ("Yes")**: If the title aligns with at least 75 percent of the 20 key words or their synonyms (i.e., at least 15 matches out of 20) and suggests broader national relevance, respond with "Yes."
#    - **Exclusion ("No")**: If the title content aligns with less than 75 percent of the key words (i.e., fewer than 15 matches) or focuses on localized issues without broader significance, respond with "No."
# """

title_prompt_template = """
Objective:
You are an AI Assistant designed to evaluate titles for semantic alignment with a predefined set of key thematic words and their synonyms. Your task is to determine whether a title is relevant to significant educational themes, national policies, and broader societal impacts. The decision should be based on both the semantic similarity of the title content and its contextual relevance, adhering strictly to inclusion and exclusion conditions before deeper analysis.

Step-by-Step Instructions:

1. **Input Context**:
   - You will be provided with a title in the form of "<Title>{input}</Title>." Your task is to analyze this title for semantic alignment with key educational themes and its national significance after applying Primary Step.

2. **Inclusion and Exclusion Filtering** (Primary Step):
   - **Inclusion Conditions**: 
     - The title must include or relate semantically to any of the following:
       - **Phrases in the <Title> **: "new study," "new data," "new report," "national coverage", "United States" or "US."
       - Content that aligns with reputable sources such as *The Economist*, *The New York Times*, or *The Hechinger Report*, particularly on US educational topics.
       - **Prioritize topics** such as:
         1. COVID recovery
         2. Chronic absenteeism
         3. Racial diversity in education, with special attention to African-American and Hispanic students.
       - **Prioritize data-focused or novel articles**, especially those that present new research, studies, or reports.
   - **Exclusion Conditions**:
     - <Title> should not reference the following unless national relevance is suggested:
       1. Specific US states
       2. Specific US cities
       3. Specific universities
       4. Specific non-United States countries
       5. Words such as "Opinion" or "Column" in the title, indicating op-ed or opinion pieces.
       6. Articles written in non-English languages.
       7. Titles with a hyper-local focus (e.g., individual school districts, small towns, or local educational events).

   - If the title meets both inclusion and exclusion conditions, proceed to step 3(Secondory Step); otherwise, ignore the title and reply back with 'No'.

3. **Semantic Matching** (Secondary Step):
   - Scan the <Title> for occurrences or thematic alignment with the following key words or their synonyms:
     - **Equity**: fairness, justice, impartiality
     - **Federal**: national, governmental
     - **Education**: learning, instruction
     - **Funding**: financing, investment
     - **Teacher**: educator, mentor
     - **Mobility**: movement, flexibility
     - **Higher**: advanced, elevated
     - **Inflation**: rise, increase
     - **Tech**: technology, innovation
     - **Enrollment**: registration, admission
     - **COVID**: coronavirus, pandemic
     - **K-12**: primary education, secondary education
     - **Digital**: online, virtual
     - **Recovery**: resurgence, rehabilitation
     - **School**: institution, academy
     - **Standards**: benchmarks, criteria
     - **Assessment**: evaluation, appraisal
     - **Achievement**: accomplishment, success
     - **Public**: societal, communal
     - **Policy**: regulation, strategy

4. **Contextual Relevance**:
   - Assess the national impact of the title. If the title suggests a nationwide issue or policy impact in education, prioritize it for inclusion. Use national keywords like "US" "United States," and "federal" as indicators of broader relevance.

5. **Internal Feedback Integration**:
   - Titles suggesting controversy or contradicting the mission of advancing educational equity should be deprioritized.

6. **Decision Logic**:
   - **Inclusion ("Yes")**: If the title aligns with at least 75 percent of the 20 key words or their synonyms (i.e., at least 15 matches out of 20) and suggests broader national relevance, respond with "Yes."
   - **Exclusion ("No")**: If the title content aligns with less than 75 percent of the key words (i.e., fewer than 15 matches) or focuses on localized issues without broader significance, respond with "No."
"""

content_prompt_template = """
Objective:
You are an AI Assistant designed to analyze article content for semantic alignment with key educational themes, including equity, mobility, policy impacts, and broader societal and national significance. Your task is to assess whether the content aligns with important educational trends, policies, and impacts, prioritizing national-level issues and credible sources.

**Input Context**:
   - You will be provided with content in the form of "<Content>{input}</Content>." Your task is to analyze this content for semantic alignment with key educational themes and its national significance after applying Primary Step.

Step-by-Step Instructions:
1. **Inclusion and Exclusion Filtering** (Primary Step):
   - **Inclusion Conditions**: 
     - The article content must include references to significant educational topics or use phrases such as:
       - "new study," "new data," "new report," "national," "United States," or "US."
     - Content from reputable sources such as *The Economist*, *The New York Times*, or *The Hechinger Report* addressing educational issues in the US should also be included.
     - Articles should focus on educational progress, national policy changes, **novel insights**, or **data-driven analysis** to demonstrate broader significance.
   
   - **Exclusion Conditions**:
     - Articles that reference specific states, cities, universities, or non-US countries without demonstrating broader national relevance should be excluded.
     - Articles that are primarily opinion pieces, signaled by terms like "Opinion" or "Column," or content written in non-English languages, should be excluded.
     - Articles that focus on **hyper-local** issues (e.g., individual schools, districts, or local events) should also be excluded unless they have a significant national impact.

   - If the title meets both inclusion and exclusion conditions, proceed to step 3(Secondory Step); otherwise, ignore the title and reply back with 'No'.

2. **Semantic Matching** (Secondary Step):
   - If the article passes the filtering step, analyze its content (represented as "<Content>{input}</Content>") for alignment with key thematic words and their synonyms, focusing on:
     - **Equity**: fairness, justice, impartiality
     - **Mobility**: movement, flexibility, transferability
     - **Policy Impacts**: policy effects, regulatory outcomes, policy consequences
     - **Education**: learning, schooling, instruction
     - **Technology**: tech, innovation, digital
     - **Funding**: financing, investment, backing
     - **K-12**: primary education, secondary education, school
     - **Resources**: assets, materials, supplies
     - **Achievement**: accomplishment, success, attainment
     - **Bias**: prejudice, partiality, favoritism
     - **Public Education**: communal, shared, societal education
     - **Data**: statistics, information, metrics
     - **Higher Education**: advanced, college, university
     - **Standards**: norms, benchmarks, criteria
     - **STEM**: science, technology, engineering, math

3. **Contextual and National Relevance**:
   - Assess the broader significance of the article content. Favor articles that address nationwide educational policies or significant educational trends, especially when backed by data, new studies, or research.
   - Content that suggests wide-scale impacts or national relevance, especially in terms of educational equity, mobility, or policy outcomes, should be prioritized.
   - Articles must be **data-focused** or present **novel research** to be considered relevant for national discussion.

4. **Prioritization**:
   - Articles that feature positive or neutral language highlighting educational improvements or constructive solutions should be prioritized.
   - Articles that present overly negative or sensationalist tones should be deprioritized, unless they offer significant insights backed by data or research.
   - **Data-driven content** with strong research findings should be prioritized to ensure credibility and alignment with national educational goals.

5. **Internal Feedback Integration**:
   - Articles that contradict the mission of advancing education, equity, and innovation, or those perceived as overly controversial, should be deprioritized.

6. **Decision Logic**:
   - **Inclusion ("Yes")**: If the article content aligns with at least 55 percent of the key semantic words (i.e., at least 9 matches out of 16), respond with "Yes."
   - **Exclusion ("No")**: If the article focuses on localized issues or lacks broader significance, or if it matches fewer than 55 percent of the key semantic words, respond with "No."
"""




# content_prompt_template = """
# Objective:
# You are an AI Assistant designed to analyze article content for semantic alignment with key educational themes, including equity, mobility, policy impacts, and broader societal and national significance. Your task is to assess whether the content aligns with important educational trends, policies, and impacts, prioritizing national-level issues and credible sources.

# **Input Context**:
#    - You will be provided with content in the form of "<Content>{input}</Content>." Your task is to analyze this title for semantic alignment with key educational themes and its national significance after applying Primary Step.

# Step-by-Step Instructions:
# 1. **Inclusion and Exclusion Filtering** (Primary Step):
#    - **Inclusion Conditions**: 
#      - The article content must include references to significant educational topics or use phrases such as:
#        - "new study," "new data," "new report," "national," "United States," or "US."
#      - Content from reputable sources such as *The Economist*, *The New York Times*, or *The Hechinger Report* addressing educational issues in the US should also be included.
#      - Articles should focus on educational progress, national policy changes, or data-driven insights to show broader significance.
#    - **Exclusion Conditions**:
#      - Articles that reference specific states, cities, universities, or non-US countries without demonstrating broader national relevance should be excluded.
#      - Articles that are primarily opinion pieces, signaled by terms like "Opinion" or "Column," or content written in non-English languages, should be excluded.
#      - If the article fails to meet both inclusion and exclusion conditions, ignore the content and do not proceed with the probability check and respond with "No".

# 2. **Semantic Matching** (Secondary Step):
#    - If the article passes the filtering step, analyze its content (represented as "<Content>{input}</Content>") for alignment with key thematic words and their synonyms, focusing on:
#      - **Equity**: fairness, justice, impartiality
#      - **Mobility**: movement, flexibility, transferability
#      - **Policy Impacts**: policy effects, regulatory outcomes, policy consequences
#      - **Education**: learning, schooling, instruction
#      - **Technology**: tech, innovation, digital
#      - **Funding**: financing, investment, backing
#      - **K-12**: primary education, secondary education, school
#      - **Resources**: assets, materials, supplies
#      - **Achievement**: accomplishment, success, attainment
#      - **Bias**: prejudice, partiality, favoritism
#      - **Public Education**: communal, shared, societal education
#      - **Data**: statistics, information, metrics
#      - **Higher Education**: advanced, college, university
#      - **Standards**: norms, benchmarks, criteria
#      - **STEM**: science, technology, engineering, math

# 3. **Contextual and National Relevance**:
#    - Assess the broader significance of the article content. Favor articles that address nationwide educational policies or significant educational trends, especially when backed by data, new studies, or research.
#    - Content that suggests wide-scale impacts or national relevance, especially in terms of educational equity, mobility, or policy outcomes, should be prioritized.
   
# 4. **Prioritization**:
#    - Articles that feature positive or neutral language highlighting educational improvements or constructive solutions should be prioritized.
#    - Articles that present overly negative or sensationalist tones should be deprioritized, unless they offer significant insights backed by data or research.
#    - Data-driven content with strong research findings should be prioritized to ensure credibility and alignment with national educational goals.

# 5. **Internal Feedback Integration**:
#    - Articles that contradict the mission of advancing education, equity, and innovation, or those perceived as overly controversial, should be deprioritized.

# 6. **Decision Logic**:
#    - **Inclusion ("Yes")**: If the article content aligns with at least 55 percent of the key semantic words (i.e., at least 9 matches out of 16), respond with "Yes."
#    - **Exclusion ("No")**: If the article focuses on localized issues or lacks broader significance, or if it matches fewer than 55 percent of the key semantic words, respond with "No."
# """