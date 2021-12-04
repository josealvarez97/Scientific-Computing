library(containerit)
cr_dockerfile_plumber <- function(deploy_folder, ...){
  docker <- dockerfile(
      deploy_folder,
      image = "rstudio/plumber",
      offline = FALSE,
      cmd = Cmd("api.R"),
      maintainer = NULL,
      copy = list("./"),
      container_workdir = NULL,
      entrypoint = Entrypoint("R",
                       params = list(
        "-e",
       "pr <- plumber::plumb(commandArgs()[4]); pr$run(host='0.0.0.0', port=as.numeric(Sys.getenv('PORT')))")
       ),
      filter_baseimage_pkgs = FALSE,
      ...)

  write_to <- file.path(deploy_folder, "Dockerfile")
  
  write(docker, file = write_to)

  assert_that(
    is.readable(write_to)
  )

  message("Written Dockerfile to ", write_to, level = 3)
  print(docker)
  docker

}