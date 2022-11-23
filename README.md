# The MMDA toolkit

See our [instance](https://corpora.linguistik.uni-erlangen.de/mmda) @FAU for a demo.

## Implementation Overview

### Backend

The backend is implemented in Python/Flask.

It builds upon the [IMS Open Corpus Workbench](http://cwb.sourceforge.net/), which needs to be installed locally or run inside a [Docker Container](mmda-backend/Dockerfile).

See the [README](mmda-backend/README.md) there for details on the setup.

### Frontend

The frontend is implemented in Vue.js.

See the [README](mmda-frontend/README.md) there for details on the setup.

## Deployment

For details on the productive deployment, see the [deployment documentation](deployment/README.md).
