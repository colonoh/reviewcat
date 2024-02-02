FROM public.ecr.aws/lambda/python:3.12

COPY requirements.txt  ${LAMBDA_TASK_ROOT} 

# install dependencies
RUN pip3 install --user -r requirements.txt

COPY src/app ${LAMBDA_TASK_ROOT} 

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "main.handler" ]
