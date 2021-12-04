FROM trestletech/plumber
RUN export DEBIAN_FRONTEND=noninteractive; apt-get -y update \
  && apt-get install -y git-core
RUN ["install2.r", "remotes"]
RUN ["installGithub.r", "liulch/bpCausal@532297e8824eed24bcf402c044611563fde3de88"]
COPY ["./", "./"]
ENTRYPOINT ["R", "-e", "pr <- plumber::plumb(commandArgs()[4]); pr$run(host='0.0.0.0', port=as.numeric(Sys.getenv('PORT')))"]
CMD ["api.R"]
