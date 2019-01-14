FROM registry.ng.bluemix.net/livelo/stretch_python3:latest

LABEL 'company'='Livelo' \
	  'creator'='Gustavo Toledo' \
	  'maintainer'='Unknow'

COPY dist/easy_kubernetes /bin/easy_kubernetes
COPY easy_kubernetes/resources/token.yaml /etc/easy_kubernetes/token.yaml

# Set tools and file R/X permissions
RUN chmod a+x /bin/easy_kubernetes &&\
    chmod a+r /etc/easy_kubernetes/token.yaml

# Define a entrypoint as app
ENTRYPOINT ["bash"]

# End of file