FROM public.ecr.aws/lambda/python:3.12-arm64

COPY requirements.txt  ${LAMBDA_TASK_ROOT} 

# install dependencies
RUN pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

COPY src/app ${LAMBDA_TASK_ROOT} 

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "main.handler" ]
