FROM public.ecr.aws/lambda/python:3.12
MAINTAINER Jaroslav Bezdek

# Copy function code
COPY function.py ${LAMBDA_TASK_ROOT}

# Add local dependencies
COPY . ${LAMBDA_TASK_ROOT}

# Install the function's dependencies using file requirements.txt
COPY requirements.txt  .
RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Set the CMD to your handler
CMD [ "function.handler" ]
