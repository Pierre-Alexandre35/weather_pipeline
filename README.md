# Technical interview : Data Engineer - Contractor

## Job description

Dear participants,

Owkin is an AI biotechnology company that uses AI to find the right treatment for every patient. We combine the best of human and artificial intelligence to answer the research questions shared by biopharma and academic researchers. By closing the translational gap between complex biology and new treatments, we bring new diagnostics and drugs to patients sooner.

### Context

As a Data Engineer, the consultant will maintain, propose and implement improvements for a data pipeline in the context of a high value data generation project. They will act on the whole chain, from data ingestion, curation, QC up to processing the generated data.

The background we are looking for is mostly Data Developer with experiences on Python applications, Data pipelines, Cloud and devops.

The main technologies used are Python, GCP, AWS, Docker, buckets

The mission duration will be from April, for 2 months, extendable to 3 months.

Note: Work can be 100% remote BUT need to be at the Paris office for the 1st day of onboarding.

### Required skills/ competences

- Python
- Experience in software engineering: http, REST API, especially in backend and data technologies
- SQL
- Assessing product requirements, working collaboratively to design and document solutions
- Knowledge of main cloud data solutions; must-have: interacting with buckets
- CI/CD: automation, test setup, artifact builds & deployment
- Docker
- Software development with a focus on code quality, simplicity, maintainability
- Debugging & Refactoring skills
- Autonomous, self-starter, quick to onboard

### Optional skills/ competences

- Kubernetes
- Knowledge of some data pipelining solutions (snakemake, luigi)
- Machine learning or BioInformatics
- Software engineering master degree

## Code description

The code in this repository is a simple data pipeline based on [Snakemake](https://snakemake.readthedocs.io/en/stable/).

The pipeline is currently composed of 1 step:

- `get_weather` : retrieves the weather data from the [OpenMeteo API](https://open-meteo.com) for a given city and stores it in a TXT file

The Python script can be run with `python -m workflow.scripts.get_weather.main` and the Snakemake pipeline can be run with `snakemake --forceall`.

## Before the interview

Please make sure that :

- [ ] You have read the job description
- [ ] You have a good internet connection
- [ ] You have a working webcam and microphone
- [ ] You are in a quiet place for the interview
- [ ] You are able to share your screen
- [ ] You have cloned this repository or can edit the code on [GitHub DEV](https://github.dev/owkin/tech-interview-data-eng-30515066101/edit/main/README.md)
- [ ] You have a working environment for Python development
  - make sure you have Python 3.12 installed : `python --version` (suggestion: use [pyenv](https://github.com/pyenv/pyenv))
  - create a virtual environment : `python -m venv .venv`
  - install requirements : `pip install -r requirements.txt`
  - you should be able to run the Python script : `python -m workflow.scripts.get_weather.main`
  - you should be able to run the Snakemake pipeline : `snakemake --forceall`
- [ ] You are familiar with the code in the repository
- [ ] You are ready to improve it following the instructions that will be given to you during the interview

## During the interview

We will ask you to improve the code in the repository in different ways to assess your skills and the way you progress in solving problems. You will have to share your screen and explain your thought process while you are working on the code.
You will be able to use any resource you need (internet, documentation, LLMs, ...) to solve the problems we will give you. And of course you can ask us any question you have about the code, the task or the job, the team and the company.

## After the interview

The HR team will contact you to give you feedback on the interview and the next steps.
