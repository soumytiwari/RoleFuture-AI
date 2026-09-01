"""Seed the remaining representative roles with role-specific activities and skills."""

from app.database import Base, SessionLocal, engine
from app.models import Activity, ActivityAssessment, FutureResponsibility, Process, Role, RoleSkill, Skill


ROLE_SPECS = {
    "Business Analyst": {
        "department": "Business Analysis",
        "description": "Translates business needs into requirements, process insights, and decision support.",
        "future_profile": "A business analyst who combines discovery and stakeholder judgment with AI-assisted requirements analysis, process mining, and decision support.",
        "current_skills": ["Requirements analysis", "Process mapping"],
        "future_skills": ["AI-assisted requirements analysis", "Process mining", "AI output validation"],
        "responsibilities": ["Validate AI-assisted requirements", "Identify process improvement opportunities", "Challenge AI-generated recommendations"],
        "processes": [
            ("Requirements Discovery", [
                ("Gather stakeholder requirements", "Interview stakeholders and document business needs and constraints.", "Weekly", 5, [2,4,2,5,5,1,4]),
                ("Analyse requirement patterns", "Review requirements for themes, duplication, gaps, and inconsistencies.", "Weekly", 4, [3,5,4,4,4,1,3]),
                ("Validate proposed requirements", "Check proposed requirements against business objectives and stakeholder expectations.", "Per project", 5, [2,4,3,4,5,1,5]),
            ]),
            ("Process Analysis", [
                ("Map current-state processes", "Document process steps, handoffs, inputs, outputs, and pain points.", "Per project", 4, [3,4,4,4,4,2,4]),
                ("Identify process bottlenecks", "Analyse process data and stakeholder feedback to find delays and rework.", "Monthly", 4, [4,5,4,3,4,1,3]),
                ("Prepare improvement recommendations", "Develop improvement options and communicate their expected business effects.", "Monthly", 5, [2,4,3,5,5,1,5]),
            ]),
            ("Decision Support", [
                ("Prepare analysis for decision-makers", "Turn business information into concise findings for leaders.", "Monthly", 4, [3,5,3,5,4,1,4]),
                ("Evaluate solution options", "Compare alternatives against business requirements, cost, risk, and expected value.", "Per project", 5, [2,4,3,4,5,1,5]),
                ("Explain trade-offs to stakeholders", "Communicate findings and trade-offs and support decisions.", "As needed", 5, [2,3,2,5,5,1,5]),
            ]),
        ],
    },
    "HR Analyst": {
        "department": "Human Resources",
        "description": "Analyses workforce information, HR processes, and people-related metrics for decision support.",
        "future_profile": "An HR analyst who combines workforce analytics with AI-assisted insight generation, data governance, and responsible interpretation.",
        "current_skills": ["Workforce analytics", "HR data management"],
        "future_skills": ["AI-assisted workforce analytics", "People-data governance", "Responsible AI review"],
        "responsibilities": ["Validate AI-generated workforce insights", "Monitor people-data quality", "Support responsible use of workforce analytics"],
        "processes": [
            ("Workforce Reporting", [
                ("Compile workforce metrics", "Collect headcount, movement, attendance, and workforce metrics from HR systems.", "Monthly", 2, [5,5,4,4,2,1,4]),
                ("Prepare workforce dashboards", "Prepare recurring workforce reports and dashboards for management.", "Monthly", 3, [5,5,4,5,3,1,4]),
                ("Check workforce data quality", "Identify incomplete, inconsistent, or duplicate workforce records.", "Weekly", 3, [4,5,4,3,3,1,5]),
            ]),
            ("Workforce Analysis", [
                ("Analyse workforce trends", "Identify changes in staffing, turnover, absence, and workforce composition.", "Monthly", 4, [4,5,3,4,4,1,5]),
                ("Investigate workforce anomalies", "Review unusual workforce patterns and identify possible causes.", "Monthly", 5, [3,5,3,4,5,1,5]),
                ("Support workforce planning", "Use workforce data and business assumptions to support staffing plans.", "Quarterly", 4, [3,5,3,4,5,1,5]),
            ]),
            ("HR Decision Support", [
                ("Prepare people insights", "Summarise workforce findings for HR and business leaders.", "Monthly", 4, [3,5,3,5,4,1,5]),
                ("Review policy metrics", "Track HR metrics relevant to policy effectiveness and compliance.", "Quarterly", 4, [4,5,5,3,4,1,5]),
                ("Explain workforce findings", "Communicate findings while respecting sensitive people information.", "As needed", 5, [2,4,2,5,5,1,5]),
            ]),
        ],
    },
    "Marketing Analyst": {
        "department": "Marketing",
        "description": "Analyses campaigns, customer behaviour, channels, and market information to support marketing decisions.",
        "future_profile": "A marketing analyst who combines quantitative insight with AI-assisted campaign analysis, experimentation, and customer-data governance.",
        "current_skills": ["Marketing analytics", "Campaign reporting"],
        "future_skills": ["AI-assisted campaign analysis", "Experimentation design", "Customer-data governance"],
        "responsibilities": ["Validate AI-generated campaign insights", "Monitor model-supported targeting", "Interpret customer-data risks"],
        "processes": [
            ("Campaign Reporting", [
                ("Compile campaign performance data", "Collect channel, campaign, cost, reach, and conversion information.", "Weekly", 2, [5,5,4,4,2,1,3]),
                ("Prepare campaign reports", "Summarise campaign performance and key movements for stakeholders.", "Weekly", 3, [5,5,4,5,3,1,3]),
                ("Check tracking data", "Validate campaign tracking and resolve common data-quality issues.", "Weekly", 3, [4,5,4,3,3,1,4]),
            ]),
            ("Customer and Market Analysis", [
                ("Analyse customer behaviour", "Review customer and campaign data to identify patterns and segments.", "Monthly", 4, [4,5,3,4,4,1,4]),
                ("Identify campaign anomalies", "Investigate unusual campaign results and performance shifts.", "Weekly", 4, [4,5,3,4,4,1,4]),
                ("Assess market signals", "Combine internal performance information with market observations.", "Monthly", 5, [3,4,3,4,5,1,5]),
            ]),
            ("Campaign Decision Support", [
                ("Recommend campaign improvements", "Use performance evidence to propose changes to campaigns and channels.", "Monthly", 4, [3,5,3,5,4,1,4]),
                ("Evaluate channel performance", "Compare channel results against objectives, cost, and audience response.", "Monthly", 4, [4,5,4,4,4,1,3]),
                ("Present marketing insights", "Explain findings and recommendations to marketing stakeholders.", "Monthly", 5, [2,4,2,5,5,1,5]),
            ]),
        ],
    },
    "Operations Analyst": {
        "department": "Operations",
        "description": "Monitors operational performance, analyses process data, and supports continuous improvement.",
        "future_profile": "An operations analyst who combines process expertise with AI-assisted monitoring, exception detection, and improvement planning.",
        "current_skills": ["Operational analysis", "Process improvement"],
        "future_skills": ["AI-assisted operations monitoring", "Process analytics", "Automation governance"],
        "responsibilities": ["Monitor AI-assisted operational alerts", "Validate exception patterns", "Improve automated workflows"],
        "processes": [
            ("Operational Reporting", [
                ("Collect operational metrics", "Gather service, throughput, quality, and productivity metrics.", "Daily", 2, [5,5,5,3,2,2,3]),
                ("Prepare performance reports", "Create recurring operational performance summaries.", "Weekly", 3, [5,5,4,4,3,2,3]),
                ("Validate operational data", "Check source data for missing, duplicate, or inconsistent records.", "Daily", 3, [4,5,4,2,3,2,4]),
            ]),
            ("Performance Analysis", [
                ("Analyse throughput trends", "Identify patterns in operational volume, speed, and service levels.", "Weekly", 4, [4,5,4,3,4,2,3]),
                ("Investigate operational exceptions", "Investigate unusual service or process results and determine causes.", "Daily", 5, [3,5,4,3,5,2,4]),
                ("Identify improvement opportunities", "Prioritise operational changes based on performance evidence.", "Monthly", 5, [3,4,3,3,5,2,4]),
            ]),
            ("Continuous Improvement", [
                ("Monitor process changes", "Track performance after process improvements or automation changes.", "Weekly", 4, [4,5,4,3,4,2,4]),
                ("Test improvement outcomes", "Compare results before and after operational changes.", "Monthly", 4, [4,5,4,3,4,2,3]),
                ("Recommend operational actions", "Translate findings into actions for operational managers.", "Monthly", 5, [2,4,3,4,5,2,5]),
            ]),
        ],
    },
    "Risk Analyst": {
        "department": "Risk",
        "description": "Identifies, assesses, monitors, and reports business risks and emerging issues.",
        "future_profile": "A risk analyst who combines risk judgment with AI-assisted monitoring, anomaly detection, and evidence-led escalation.",
        "current_skills": ["Risk assessment", "Risk reporting"],
        "future_skills": ["AI-assisted risk monitoring", "Model risk awareness", "Evidence-based escalation"],
        "responsibilities": ["Validate AI-detected risk signals", "Investigate exceptions", "Monitor model and data risk"],
        "processes": [
            ("Risk Monitoring", [
                ("Collect risk indicators", "Compile internal metrics and risk indicators used in ongoing monitoring.", "Weekly", 3, [5,5,4,3,3,1,5]),
                ("Update risk registers", "Maintain risk records, owners, ratings, and mitigation actions.", "Monthly", 3, [5,5,4,4,3,1,5]),
                ("Check risk data quality", "Validate risk data and supporting evidence for completeness.", "Weekly", 4, [4,5,4,3,4,1,5]),
            ]),
            ("Risk Analysis", [
                ("Analyse risk trends", "Review risk indicators to identify changing exposure and emerging patterns.", "Monthly", 5, [4,5,3,4,5,1,5]),
                ("Investigate risk exceptions", "Investigate unusual or elevated risk indicators and identify possible causes.", "Weekly", 5, [3,5,3,4,5,1,5]),
                ("Assess mitigation effectiveness", "Evaluate whether risk responses are reducing the intended exposure.", "Quarterly", 5, [3,4,3,4,5,1,5]),
            ]),
            ("Risk Reporting", [
                ("Prepare risk reporting", "Create concise reports for risk committees and management.", "Monthly", 5, [3,5,3,5,5,1,5]),
                ("Escalate significant risks", "Communicate material risks and recommended escalation paths.", "As needed", 5, [2,4,2,5,5,1,5]),
                ("Explain risk drivers", "Explain underlying drivers, uncertainty, and management implications.", "Monthly", 5, [2,4,2,5,5,1,5]),
            ]),
        ],
    },
    "Compliance Analyst": {
        "department": "Compliance",
        "description": "Supports regulatory compliance through monitoring, review, evidence collection, and reporting.",
        "future_profile": "A compliance analyst who combines regulatory interpretation with AI-assisted document review, monitoring, and exception handling.",
        "current_skills": ["Compliance monitoring", "Regulatory documentation"],
        "future_skills": ["AI-assisted compliance review", "Regulatory data literacy", "Exception governance"],
        "responsibilities": ["Validate AI-assisted compliance findings", "Review regulatory exceptions", "Maintain audit-ready evidence"],
        "processes": [
            ("Compliance Monitoring", [
                ("Collect compliance evidence", "Collect documents, records, and monitoring information for compliance reviews.", "Monthly", 3, [4,5,4,4,3,1,5]),
                ("Review compliance records", "Review records against documented policies and requirements.", "Monthly", 4, [4,5,4,5,4,1,5]),
                ("Track compliance actions", "Monitor outstanding findings, owners, and corrective actions.", "Weekly", 3, [4,5,5,3,3,1,5]),
            ]),
            ("Control Testing", [
                ("Test control evidence", "Assess whether required evidence demonstrates that controls operated as expected.", "Quarterly", 5, [3,5,3,4,5,1,5]),
                ("Investigate control exceptions", "Investigate unusual or failed control results.", "Monthly", 5, [3,5,3,4,5,1,5]),
                ("Document compliance findings", "Prepare clear findings and supporting evidence for stakeholders.", "Monthly", 5, [3,5,3,5,5,1,5]),
            ]),
            ("Compliance Reporting", [
                ("Prepare compliance reports", "Prepare status and exception reports for management.", "Monthly", 5, [4,5,4,5,4,1,5]),
                ("Summarise regulatory changes", "Review regulatory information and summarise potentially relevant changes.", "Monthly", 5, [2,4,2,5,5,1,5]),
                ("Communicate compliance priorities", "Explain findings, risks, and required actions to stakeholders.", "Monthly", 5, [2,4,2,5,5,1,5]),
            ]),
        ],
    },
    "Customer Service Representative": {
        "department": "Customer Service",
        "description": "Handles customer enquiries, resolves issues, and coordinates service outcomes.",
        "future_profile": "A customer-service professional who combines relationship management with AI-assisted triage, drafting, and knowledge support.",
        "current_skills": ["Customer communication", "Issue resolution"],
        "future_skills": ["AI-assisted customer support", "Conversation quality review", "Exception handling"],
        "responsibilities": ["Validate AI-generated responses", "Handle complex customer exceptions", "Monitor customer-service quality"],
        "processes": [
            ("Customer Enquiries", [
                ("Classify incoming enquiries", "Review incoming enquiries and route them to the appropriate service path.", "Daily", 2, [5,5,4,5,2,1,3]),
                ("Draft routine responses", "Prepare responses to common customer questions using approved information.", "Daily", 3, [5,5,4,5,3,1,4]),
                ("Update customer records", "Record customer interactions and resolution information in service systems.", "Daily", 2, [5,5,4,3,2,1,5]),
            ]),
            ("Issue Resolution", [
                ("Investigate customer issues", "Review case information and identify causes and possible resolutions.", "Daily", 4, [4,5,3,5,4,1,5]),
                ("Resolve standard service cases", "Apply documented procedures to resolve routine customer cases.", "Daily", 3, [5,5,5,4,3,1,4]),
                ("Escalate complex cases", "Recognise cases requiring additional authority, judgment, or specialist input.", "Daily", 5, [2,4,2,5,5,1,5]),
            ]),
            ("Customer Experience", [
                ("Monitor service trends", "Review service volumes, reasons for contact, and resolution patterns.", "Weekly", 3, [4,5,3,4,3,1,4]),
                ("Review response quality", "Check service interactions against quality and policy expectations.", "Weekly", 4, [3,5,3,5,4,1,5]),
                ("Communicate complex resolutions", "Explain decisions and resolutions in situations requiring human judgment.", "Daily", 5, [1,3,2,5,5,1,5]),
            ]),
        ],
    },
    "Project Coordinator": {
        "department": "Project Management",
        "description": "Coordinates project information, schedules, actions, reporting, and stakeholder communications.",
        "future_profile": "A project coordinator who uses AI for schedule support, document synthesis, action tracking, and project-risk monitoring while retaining coordination accountability.",
        "current_skills": ["Project coordination", "Status reporting"],
        "future_skills": ["AI-assisted project coordination", "Project-data governance", "AI-supported risk monitoring"],
        "responsibilities": ["Validate AI-generated project summaries", "Monitor AI-detected project risks", "Coordinate human decisions and escalations"],
        "processes": [
            ("Project Administration", [
                ("Maintain project records", "Keep project documents, actions, decisions, and status information current.", "Weekly", 2, [4,5,5,4,2,1,4]),
                ("Track project actions", "Monitor actions, owners, due dates, and completion status.", "Weekly", 3, [5,5,5,3,3,1,4]),
                ("Prepare meeting materials", "Compile agendas, status information, and supporting material for meetings.", "Weekly", 3, [4,5,3,5,3,1,4]),
            ]),
            ("Project Monitoring", [
                ("Prepare project status reports", "Summarise schedule, budget, risks, dependencies, and actions.", "Weekly", 4, [4,5,4,5,4,1,5]),
                ("Monitor project risks", "Track risks, issues, and dependencies and identify items needing attention.", "Weekly", 4, [4,5,3,4,4,1,5]),
                ("Investigate delivery exceptions", "Review delays or exceptions and coordinate information gathering.", "As needed", 5, [3,5,3,4,5,1,5]),
            ]),
            ("Stakeholder Coordination", [
                ("Coordinate project communications", "Distribute approved updates and coordinate required stakeholder actions.", "Weekly", 4, [3,5,3,5,4,1,5]),
                ("Track stakeholder decisions", "Maintain decision records and follow-up actions.", "Weekly", 4, [4,5,4,5,4,1,5]),
                ("Escalate project issues", "Identify issues needing project-manager or sponsor decisions.", "As needed", 5, [2,4,2,5,5,1,5]),
            ]),
        ],
    },
    "Supply Chain Planner": {
        "department": "Supply Chain",
        "description": "Plans supply and inventory, analyses demand and constraints, and coordinates replenishment decisions.",
        "future_profile": "A supply-chain planner who combines planning judgment with AI-assisted demand sensing, exception management, and scenario modelling.",
        "current_skills": ["Supply planning", "Inventory analysis"],
        "future_skills": ["AI-assisted demand planning", "Scenario modelling", "Supply exception management"],
        "responsibilities": ["Validate AI-assisted forecasts", "Investigate supply exceptions", "Monitor automated planning recommendations"],
        "processes": [
            ("Demand Planning", [
                ("Collect demand information", "Compile forecasts, orders, sales history, and other demand signals.", "Weekly", 3, [5,5,4,3,3,2,4]),
                ("Prepare demand forecasts", "Review demand information and produce planning forecasts.", "Weekly", 4, [4,5,3,3,5,2,4]),
                ("Review forecast exceptions", "Investigate unusually high or low demand signals.", "Weekly", 5, [3,5,3,3,5,2,4]),
            ]),
            ("Supply Planning", [
                ("Assess supply requirements", "Compare forecast demand with available supply and constraints.", "Weekly", 4, [4,5,4,3,4,2,4]),
                ("Plan replenishment", "Develop replenishment actions based on demand, inventory, and lead times.", "Weekly", 4, [4,5,4,3,4,2,4]),
                ("Investigate supply constraints", "Analyse shortages, delays, and capacity constraints requiring action.", "Daily", 5, [3,5,3,4,5,2,5]),
            ]),
            ("Planning Decisions", [
                ("Run planning scenarios", "Compare supply options under alternative demand and constraint assumptions.", "Monthly", 5, [3,5,3,4,5,2,4]),
                ("Prioritise constrained supply", "Balance demand, commercial priorities, and operational constraints.", "Daily", 5, [2,4,2,4,5,2,5]),
                ("Communicate supply decisions", "Explain planning actions, trade-offs, and exceptions to stakeholders.", "Weekly", 5, [2,4,2,5,5,2,5]),
            ]),
        ],
    },
    "Recruitment Specialist": {
        "department": "Human Resources",
        "description": "Sources candidates, coordinates recruitment processes, and supports hiring managers and candidates.",
        "future_profile": "A recruitment specialist who combines candidate and stakeholder judgment with AI-assisted sourcing, screening support, and workflow coordination.",
        "current_skills": ["Candidate sourcing", "Interview coordination"],
        "future_skills": ["AI-assisted talent sourcing", "Structured hiring evaluation", "Responsible AI awareness"],
        "responsibilities": ["Review AI-assisted candidate screening", "Monitor fairness and quality in hiring workflows", "Coordinate human hiring decisions"],
        "processes": [
            ("Candidate Sourcing", [
                ("Search candidate profiles", "Identify candidates using recruitment systems and approved sourcing channels.", "Daily", 4, [4,5,4,4,3,1,5]),
                ("Screen candidate information", "Review candidate information against role requirements.", "Daily", 4, [4,5,4,5,4,1,5]),
                ("Maintain candidate records", "Update candidate status, notes, and process information.", "Daily", 5, [5,5,5,3,2,1,5]),
            ]),
            ("Recruitment Coordination", [
                ("Coordinate interviews", "Schedule interviews, communicate logistics, and track completion.", "Daily", 3, [5,5,5,5,3,1,4]),
                ("Prepare candidate shortlists", "Organise candidate information for hiring-manager review.", "Weekly", 4, [4,5,4,5,4,1,5]),
                ("Track recruitment pipeline", "Monitor hiring stages, bottlenecks, and outstanding actions.", "Weekly", 3, [5,5,5,3,3,1,4]),
            ]),
            ("Hiring Support", [
                ("Support candidate evaluation", "Provide structured information to hiring managers during evaluation.", "Per vacancy", 5, [3,4,3,5,5,1,5]),
                ("Monitor recruitment metrics", "Track time-to-hire, funnel movement, and candidate-flow metrics.", "Monthly", 3, [4,5,4,4,3,1,4]),
                ("Communicate hiring outcomes", "Coordinate outcome communication and handle candidate questions.", "As needed", 5, [2,4,2,5,5,1,5]),
            ]),
        ],
    },
    "Payroll Specialist": {
        "department": "Finance",
        "description": "Processes payroll, validates employee pay information, and manages payroll exceptions and reporting.",
        "future_profile": "A payroll specialist who combines payroll controls with AI-assisted validation, exception detection, and employee support.",
        "current_skills": ["Payroll processing", "Payroll controls"],
        "future_skills": ["AI-assisted payroll validation", "Payroll data governance", "Exception analytics"],
        "responsibilities": ["Validate automated payroll outputs", "Investigate payroll exceptions", "Maintain payroll controls and data quality"],
        "processes": [
            ("Payroll Preparation", [
                ("Collect payroll inputs", "Compile approved pay, attendance, leave, and adjustment inputs.", "Biweekly", 2, [5,5,5,3,2,1,5]),
                ("Validate payroll inputs", "Check payroll inputs for completeness and inconsistencies.", "Biweekly", 3, [5,5,5,3,3,1,5]),
                ("Prepare payroll calculations", "Apply approved payroll rules and calculate employee pay.", "Biweekly", 3, [5,5,5,3,3,1,5]),
            ]),
            ("Payroll Control", [
                ("Review payroll exceptions", "Investigate unusual payroll results and adjustment requests.", "Biweekly", 4, [4,5,4,4,4,1,5]),
                ("Reconcile payroll totals", "Reconcile payroll results against control totals and expected movements.", "Biweekly", 3, [5,5,5,3,3,1,5]),
                ("Approve payroll changes", "Validate changes requiring appropriate review before processing.", "Biweekly", 5, [3,5,3,4,5,1,5]),
            ]),
            ("Payroll Reporting", [
                ("Prepare payroll reports", "Create recurring payroll reports for finance and HR stakeholders.", "Monthly", 3, [5,5,4,4,3,1,5]),
                ("Analyse payroll variances", "Review unusual movement in payroll costs and employee pay.", "Monthly", 4, [4,5,4,4,4,1,5]),
                ("Resolve employee payroll queries", "Investigate and explain payroll questions requiring record review.", "Daily", 5, [2,4,2,5,5,1,5]),
            ]),
        ],
    },
    "Management Accountant": {
        "department": "Finance",
        "description": "Supports management reporting, budgeting, cost analysis, and financial decision support.",
        "future_profile": "A management accountant who combines financial control and business partnering with AI-assisted analysis, scenario modelling, and insight validation.",
        "current_skills": ["Management reporting", "Cost analysis"],
        "future_skills": ["AI-assisted management reporting", "Scenario modelling", "AI output validation"],
        "responsibilities": ["Validate AI-generated management commentary", "Interpret AI-detected financial drivers", "Monitor finance automation controls"],
        "processes": [
            ("Management Reporting", [
                ("Compile management information", "Collect financial results and operational drivers for management reporting.", "Monthly", 3, [5,5,4,4,3,1,4]),
                ("Prepare management reports", "Create recurring management reports with analysis and commentary.", "Monthly", 4, [5,5,4,5,4,1,5]),
                ("Review reporting quality", "Check report completeness, consistency, and supporting data.", "Monthly", 4, [4,5,4,3,4,1,5]),
            ]),
            ("Cost and Performance Analysis", [
                ("Analyse cost movements", "Identify cost drivers and explain material changes.", "Monthly", 4, [4,5,3,4,4,1,4]),
                ("Perform profitability analysis", "Analyse performance across products, customers, or business units.", "Monthly", 5, [3,5,3,4,5,1,5]),
                ("Investigate financial anomalies", "Investigate unusual financial movements and determine business causes.", "Monthly", 5, [3,5,3,4,5,1,5]),
            ]),
            ("Planning and Decision Support", [
                ("Prepare budgets and forecasts", "Develop budgets and forecasts using financial and business assumptions.", "Quarterly", 5, [3,5,3,4,5,1,5]),
                ("Model business scenarios", "Compare financial outcomes under alternative scenarios.", "Quarterly", 5, [3,5,3,4,5,1,5]),
                ("Communicate financial implications", "Explain financial trade-offs and recommendations to business leaders.", "Monthly", 5, [2,4,2,5,5,1,5]),
            ]),
        ],
    },
    "Internal Auditor": {
        "department": "Audit",
        "description": "Evaluates controls, processes, risks, and evidence to support assurance activities.",
        "future_profile": "An internal auditor who combines assurance judgment with AI-assisted testing, anomaly detection, evidence review, and audit planning.",
        "current_skills": ["Audit testing", "Control evaluation"],
        "future_skills": ["AI-assisted audit analytics", "Continuous monitoring", "Audit evidence governance"],
        "responsibilities": ["Validate AI-assisted audit findings", "Investigate anomalies", "Maintain audit evidence quality"],
        "processes": [
            ("Audit Planning", [
                ("Gather audit information", "Collect process, control, risk, and prior-audit information.", "Per audit", 3, [4,5,4,4,3,1,5]),
                ("Assess audit scope", "Review available information to define audit scope and priorities.", "Per audit", 5, [3,4,3,4,5,1,5]),
                ("Prepare audit workpapers", "Organise planned procedures, evidence needs, and supporting documentation.", "Per audit", 4, [4,5,4,5,4,1,5]),
            ]),
            ("Audit Testing", [
                ("Test control samples", "Execute documented procedures over selected transactions or evidence.", "Per audit", 4, [5,5,5,3,3,1,5]),
                ("Analyse audit data", "Use data to identify patterns, exceptions, or unusual transactions.", "Per audit", 4, [4,5,4,3,4,1,5]),
                ("Investigate audit exceptions", "Investigate exceptions and determine whether they indicate control weaknesses.", "Per audit", 5, [3,5,3,4,5,1,5]),
            ]),
            ("Audit Reporting", [
                ("Document audit findings", "Prepare evidence-based observations and findings.", "Per audit", 5, [3,5,3,5,5,1,5]),
                ("Prepare audit reports", "Summarise audit results, risks, and recommendations.", "Per audit", 5, [3,5,3,5,5,1,5]),
                ("Discuss findings with management", "Communicate findings, challenge responses, and support agreed actions.", "Per audit", 5, [2,4,2,5,5,1,5]),
            ]),
        ],
    },
    "Contract Administrator": {
        "department": "Legal Operations",
        "description": "Maintains contracts, monitors obligations, coordinates renewals, and supports contract administration.",
        "future_profile": "A contract administrator who combines document and obligation management with AI-assisted contract review, tracking, and exception handling.",
        "current_skills": ["Contract administration", "Document control"],
        "future_skills": ["AI-assisted contract review", "Obligation tracking", "Contract data governance"],
        "responsibilities": ["Validate AI-assisted contract extraction", "Monitor obligation exceptions", "Maintain contract records and controls"],
        "processes": [
            ("Contract Records", [
                ("Register contract documents", "Record contract metadata, parties, dates, and key terms.", "Per contract", 3, [5,5,5,4,2,1,5]),
                ("Maintain contract records", "Keep contract versions, approvals, and supporting information organised.", "Weekly", 3, [5,5,5,3,3,1,5]),
                ("Check contract completeness", "Validate that expected documents and information are present.", "Per contract", 3, [4,5,5,3,3,1,5]),
            ]),
            ("Obligation Management", [
                ("Track contract obligations", "Monitor key obligations, dates, deliverables, and owners.", "Weekly", 4, [5,5,5,3,3,1,5]),
                ("Monitor renewal dates", "Track renewal, expiry, and notice dates and identify upcoming actions.", "Weekly", 3, [5,5,5,3,2,1,5]),
                ("Investigate obligation exceptions", "Review missed or unusual obligations and coordinate responses.", "As needed", 5, [3,5,3,4,5,1,5]),
            ]),
            ("Contract Reporting", [
                ("Prepare contract reports", "Summarise contract status, obligations, and upcoming actions.", "Monthly", 4, [4,5,4,5,3,1,5]),
                ("Review contract changes", "Compare updated documents to identify important changes and impacts.", "Per contract", 5, [4,5,4,5,5,1,5]),
                ("Communicate contract actions", "Coordinate contract actions with legal, commercial, and business stakeholders.", "As needed", 5, [2,4,2,5,5,1,5]),
            ]),
        ],
    },
    "Credit Analyst": {
        "department": "Finance",
        "description": "Assesses credit information, monitors exposures, and supports lending or customer-risk decisions.",
        "future_profile": "A credit analyst who combines credit judgment with AI-assisted document analysis, risk monitoring, and exception investigation.",
        "current_skills": ["Credit analysis", "Financial statement review"],
        "future_skills": ["AI-assisted credit analysis", "Model-risk awareness", "Exception-based review"],
        "responsibilities": ["Validate AI-assisted credit signals", "Investigate exceptions", "Monitor data and model risk"],
        "processes": [
            ("Credit Information", [
                ("Collect applicant information", "Compile financial, customer, and credit information for assessment.", "Per application", 3, [4,5,4,4,3,1,5]),
                ("Review financial information", "Review financial statements and supporting documents.", "Per application", 4, [4,5,3,5,4,1,5]),
                ("Validate credit data", "Check data completeness and inconsistencies before assessment.", "Per application", 3, [4,5,4,3,3,1,5]),
            ]),
            ("Credit Assessment", [
                ("Assess credit risk", "Evaluate financial position, repayment capacity, and relevant risk indicators.", "Per application", 5, [3,5,3,4,5,1,5]),
                ("Investigate credit exceptions", "Review unusual information, adverse signals, or policy exceptions.", "Per application", 5, [3,5,3,4,5,1,5]),
                ("Prepare credit recommendations", "Summarise assessment findings and recommend an appropriate decision.", "Per application", 5, [3,5,3,5,5,1,5]),
            ]),
            ("Portfolio Monitoring", [
                ("Monitor credit exposures", "Review portfolio-level indicators and changes in exposure.", "Monthly", 4, [4,5,4,3,4,1,5]),
                ("Analyse credit trends", "Identify changes in delinquency, exposure, or risk patterns.", "Monthly", 4, [4,5,3,4,5,1,5]),
                ("Escalate material credit risks", "Communicate significant credit risks requiring management attention.", "As needed", 5, [2,4,2,5,5,1,5]),
            ]),
        ],
    },
    "Research Analyst": {
        "department": "Research",
        "description": "Collects, analyses, and interprets information to answer business or market research questions.",
        "future_profile": "A research analyst who combines source evaluation and synthesis with AI-assisted research, evidence screening, and insight generation.",
        "current_skills": ["Research methods", "Data interpretation"],
        "future_skills": ["AI-assisted research", "Source validation", "Evidence synthesis"],
        "responsibilities": ["Validate AI-assisted research outputs", "Evaluate source quality", "Synthesize evidence for decisions"],
        "processes": [
            ("Research Planning", [
                ("Define research questions", "Clarify research objectives, scope, and information requirements.", "Per project", 5, [2,4,2,5,5,1,5]),
                ("Identify research sources", "Identify relevant internal and external information sources.", "Per project", 4, [3,5,3,5,4,1,5]),
                ("Plan research activities", "Define methods, analysis steps, and evidence requirements.", "Per project", 4, [3,4,3,4,5,1,5]),
            ]),
            ("Research and Analysis", [
                ("Collect research information", "Gather structured and unstructured information relevant to the research question.", "Weekly", 3, [4,5,3,5,3,1,5]),
                ("Analyse research evidence", "Review information, identify patterns, and assess evidence.", "Weekly", 5, [3,5,3,5,5,1,5]),
                ("Compare research findings", "Compare evidence across sources and identify important differences.", "Weekly", 5, [3,5,3,5,5,1,5]),
            ]),
            ("Research Reporting", [
                ("Prepare research summaries", "Synthesize research into concise findings for stakeholders.", "Per project", 5, [3,5,3,5,5,1,5]),
                ("Document research evidence", "Maintain evidence, sources, and analytical notes for traceability.", "Per project", 4, [4,5,4,5,4,1,5]),
                ("Present research implications", "Explain findings, uncertainty, and implications for decisions.", "Per project", 5, [2,4,2,5,5,1,5]),
            ]),
        ],
    },
    "Sales Operations Analyst": {
        "department": "Sales",
        "description": "Supports sales performance through data analysis, pipeline reporting, forecasting, and process coordination.",
        "future_profile": "A sales-operations analyst who combines commercial data analysis with AI-assisted forecasting, pipeline monitoring, and process optimisation.",
        "current_skills": ["Sales analytics", "Pipeline reporting"],
        "future_skills": ["AI-assisted sales forecasting", "Pipeline analytics", "CRM data governance"],
        "responsibilities": ["Validate AI-assisted pipeline insights", "Monitor forecast quality", "Improve sales automation workflows"],
        "processes": [
            ("Sales Reporting", [
                ("Compile sales pipeline data", "Collect opportunity, account, activity, and pipeline information.", "Weekly", 3, [5,5,5,3,2,1,4]),
                ("Prepare sales dashboards", "Prepare recurring sales performance dashboards and reports.", "Weekly", 3, [5,5,4,5,3,1,4]),
                ("Check CRM data quality", "Identify missing, duplicate, or inconsistent sales records.", "Weekly", 3, [4,5,5,3,3,1,4]),
            ]),
            ("Pipeline Analysis", [
                ("Analyse pipeline trends", "Review pipeline movement, conversion, ageing, and coverage.", "Weekly", 4, [4,5,4,4,4,1,4]),
                ("Identify pipeline exceptions", "Investigate unusual pipeline movements or stalled opportunities.", "Weekly", 4, [4,5,3,4,4,1,5]),
                ("Support sales forecasting", "Use pipeline data and commercial assumptions to support forecasts.", "Weekly", 5, [3,5,3,4,5,1,5]),
            ]),
            ("Sales Process Improvement", [
                ("Evaluate sales process metrics", "Analyse operational metrics to identify process bottlenecks.", "Monthly", 4, [4,5,4,3,4,1,4]),
                ("Recommend workflow improvements", "Recommend changes to sales processes and supporting tools.", "Monthly", 5, [3,4,3,5,5,1,5]),
                ("Communicate sales insights", "Explain performance findings and recommendations to sales leaders.", "Monthly", 5, [2,4,2,5,5,1,5]),
            ]),
        ],
    },
    "Administrative Officer": {
        "department": "Administration",
        "description": "Coordinates administrative records, scheduling, correspondence, and routine business support activities.",
        "future_profile": "An administrative professional who combines coordination and service judgment with AI-assisted document handling, scheduling, and workflow support.",
        "current_skills": ["Administrative coordination", "Records management"],
        "future_skills": ["AI-assisted administration", "Digital workflow management", "Information governance"],
        "responsibilities": ["Validate AI-generated administrative outputs", "Monitor automated workflows", "Handle exceptions and sensitive requests"],
        "processes": [
            ("Records and Documents", [
                ("Maintain administrative records", "Create, update, and organise administrative records and files.", "Daily", 2, [5,5,5,3,2,1,4]),
                ("Process routine documents", "Prepare and route routine documents using established procedures.", "Daily", 2, [5,5,5,5,2,1,4]),
                ("Check records completeness", "Validate that required administrative information and documents are present.", "Weekly", 3, [4,5,5,3,3,1,4]),
            ]),
            ("Scheduling and Coordination", [
                ("Coordinate meetings", "Schedule meetings, circulate materials, and track actions.", "Daily", 3, [5,5,5,5,3,1,4]),
                ("Track administrative actions", "Monitor deadlines, requests, and completion of routine actions.", "Daily", 3, [5,5,5,3,3,1,4]),
                ("Handle routine enquiries", "Respond to routine requests using approved information and procedures.", "Daily", 3, [4,5,4,5,3,1,4]),
            ]),
            ("Business Support", [
                ("Prepare administrative reports", "Compile routine administrative metrics and status information.", "Monthly", 3, [5,5,4,4,3,1,4]),
                ("Process service requests", "Review and route requests to the appropriate internal teams.", "Daily", 3, [4,5,4,4,3,1,5]),
                ("Resolve complex administrative issues", "Handle exceptions and requests requiring judgment or escalation.", "As needed", 5, [2,4,2,5,5,1,5]),
            ]),
        ],
    },
}


def get_or_create_skill(db, name: str, category: str, description: str) -> Skill:
    skill = (
        db.query(Skill)
        .filter(Skill.name == name, Skill.category == category)
        .first()
    )
    if skill is None:
        skill = Skill(name=name, category=category, description=description)
        db.add(skill)
        db.flush()
    return skill


def add_role_skill(db, role: Role, skill: Skill, importance: int, reason: str) -> None:
    exists = (
        db.query(RoleSkill)
        .filter(RoleSkill.role_id == role.id, RoleSkill.skill_id == skill.id)
        .first()
    )
    if exists is None:
        db.add(RoleSkill(role_id=role.id, skill_id=skill.id, importance=importance, reason=reason))


def seed_additional_roles() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    inserted_roles = 0
    inserted_activities = 0

    try:
        for title, spec in ROLE_SPECS.items():
            role = db.query(Role).filter(Role.title == title).first()
            if role is None:
                role = Role(
                    title=title,
                    department=spec["department"],
                    industry="Corporate Services",
                    description=spec["description"],
                    creation_source="researched_seed",
            future_profile=spec["future_profile"],
                )
                db.add(role)
                db.flush()
                inserted_roles += 1

            for skill_name in spec["current_skills"]:
                skill = get_or_create_skill(
                    db,
                    skill_name,
                    "Current",
                    f"Current capability used by {title.lower()} work.",
                )
                add_role_skill(
                    db,
                    role,
                    skill,
                    5,
                    "This capability is part of the current role profile.",
                )

            for skill_name in spec["future_skills"]:
                skill = get_or_create_skill(
                    db,
                    skill_name,
                    "Future",
                    f"Future capability relevant to {title.lower()} as AI-supported work expands.",
                )
                add_role_skill(
                    db,
                    role,
                    skill,
                    5,
                    "This capability supports effective AI adoption while retaining human review and accountability.",
                )

            existing_processes = db.query(Process).filter(Process.role_id == role.id).count()
            if existing_processes == 0:
                for process_name, activities in spec["processes"]:
                    process = Process(
                        role_id=role.id,
                        name=process_name,
                        description=f"{process_name} activities performed within the {title.lower()} role.",
                    )
                    db.add(process)
                    db.flush()

                    for name, description, frequency, _judgment, factors in activities:
                        activity = Activity(
                            process_id=process.id,
                            name=name,
                            description=description,
                            frequency=frequency,
                            human_judgment_level=factors[4],
                        )
                        db.add(activity)
                        db.flush()

                        db.add(
                            ActivityAssessment(
                                activity_id=activity.id,
                                repetitiveness=factors[0],
                                digital_data_availability=factors[1],
                                rule_based_potential=factors[2],
                                language_intensity=factors[3],
                                human_judgment_requirement=factors[4],
                                physical_dependency=factors[5],
                                sensitivity_complexity=factors[6],
                            )
                        )
                        inserted_activities += 1

            existing_responsibilities = db.query(FutureResponsibility).filter(FutureResponsibility.role_id == role.id).count()
            if existing_responsibilities == 0:
                for index, responsibility in enumerate(spec["responsibilities"]):
                    db.add(
                        FutureResponsibility(
                            role_id=role.id,
                            responsibility=responsibility,
                            description=f"Future responsibility for the {title.lower()} role as AI-supported work develops.",
                            priority=5 if index < 2 else 4,
                        )
                    )

        db.commit()
        print(f"Inserted roles: {inserted_roles}")
        print(f"Inserted activities: {inserted_activities}")
        print("Additional role seed completed successfully.")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_additional_roles()
