# Pin the base image by digest, not a floating tag, so the build is
# byte-for-byte reproducible.
#
# TODO (must be done on a machine with Docker + network access, which this
# sandbox does not have): resolve the digest for the tag you want and paste
# it in below, e.g.:
#
#   docker pull python:3.12-slim
#   docker inspect --format='{{index .RepoDigests 0}}' python:3.12-slim
#
# then replace the placeholder line with the real
# python:3.12-slim@sha256:<digest> value it prints.
FROM python:3.12-slim@sha256:57cd7c3a7a273101a6485ba99423ee568157882804b1124b4dd04266317710de

RUN pip install --no-cache-dir pytest==8.4.1 pytest-json-ctrf==0.3.5

WORKDIR /app

COPY access.log /app/access.log

# NOTE: solution_hint.py (a reference implementation) used to be COPY'd
# into this image. That leaked the answer straight into the agent's
# environment and has been removed. The reference solution now lives only
# under solution/, which Harbor injects for oracle runs and never exposes
# to the agent.
