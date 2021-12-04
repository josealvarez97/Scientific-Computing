FROM rstudio/plumber
RUN ["install2.r", "remotes"]
RUN ["installGithub.r", "liulch/bpCausal@532297e8824eed24bcf402c044611563fde3de88"]
COPY ["./", "./"]
ENTRYPOINT ["R", "-e", "pr <- plumber::plumb('api.R'); pr$run(host='0.0.0.0', port=as.numeric(Sys.getenv('PORT')))"]
CMD ["api.R"]
