[![pipeline status](https://gitlab.cs.fau.de/efe/mmda-refactor/badges/master/pipeline.svg)](https://gitlab.cs.fau.de/efe/mmda-refactor/commits/master)
[![coverage report](https://gitlab.cs.fau.de/efe/mmda-refactor/badges/master/coverage.svg)](https://gitlab.cs.fau.de/efe/mmda-refactor/commits/master)

# MMDA

The digitalisation of society and media systems has had a major impact on (political) discourses and the formation of public opinion. The purpose of this project is to investigate the transnational algorithmic public sphere, a complex phenomenon that has arisen in an era of globalised mass media and social media connectivity across national borders.

An interdisciplinary combination of computational linguistics, network visualisation, intercultural hermeneutics and communication science enables us to analyse and map the processes underlying this phenomenon. The project addresses the current political discussion on nuclear power and renewable energy in Germany and Japan following the Fukushima accident.

Project co-ordination: Prof. Dr. Stefan Evert, stefan.evert@fau.de

# Overview

This section will provide a high-level overview of the implementation.

For details on the productive deployment, see the [deployment documenation](deployment/README.md)

## Backend

For details on the Setup, see the [mmda-backend/README.md](mmda-backend/README.md)

The backend is implemented in Python using Flask. It builds upon the [IMS Open Corpus Workbench](http://cwb.sourceforge.net/) and the [UCS toolkit](http://www.collocations.de/software.html), both of these need to be installed locally or run inside a [Docker Container](https://github.com/fau-klue/docker-corpus-tool).

All low-level CWB calls are being abstracted using Python. This is mostly done using Pandas DataFrames and native Python Classes. At this stage, all collocates extracted from a corpus are being processed using computational linguistic techniques such as Word2Vec. Dimentionality reduction is done using t-SNE.

Finally, a standardized (HTTP) API is provided using Flask. This interface is used to abstract complex operations and deliver structured data to a frontend for visualisation.

## Frontend

For details on the Setup, see the [mmda-frontend/README.md](mmda-frontend/README.md)

The frontend implementation uses Vue.js. It depends on the previously described backend and is used for visualisation and interaction with the data provided. For this a modern Material Design UI was created, based on the open-source JavaScript framework Vue.js.
