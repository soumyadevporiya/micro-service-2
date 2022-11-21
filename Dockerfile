FROM python:3.9
WORKDIR ./
COPY ./requirement.txt ./requirement.txt
RUN pip install -r requirement.txt
COPY ./three_types_of_micro_service_comms.py ./three_types_of_micro_service_comms.py
CMD ["python3","./three_types_of_micro_service_comms.py"]
