set.seed(1234)
library(bpCausal) 
data(bpCausal)
test <- ls()

library(plumber)

x1 <- "x1 string"

#' @post /hello
function(req, res) {
  data <- tryCatch(jsonlite::parse_json(req$postBody, simplifyVector=TRUE), error = function(e) NULL)
  if (is.null(data)) {
    res$status <- 400
    return(list(error = "No data submitted"))
  }
  print(data)
  
  set.seed(1234)
  library(bpCausal) 
  data(bpCausal)

  # x2 <- "x2 string"
  
  out1 <- bpCausal(data = simdata, ## simulated dataset  
                index = data$index, #c("id", "time"), ## names for unit and time index
                Yname = data$Yname, #"Y", ## outcome variable
                Dname = data$Dname, #"D", ## treatment indicator  
                Xname = data$Xname, #c("X1", "X2", "X3", "X4", "X5", "X6", "X7", "X8", "X9"), # covariates that have constant (fixed) effect  
                Zname = data$Zname, #c("X1", "X2", "X3", "X4", "X5", "X6", "X7", "X8", "X9"), # covariates that have unit-level random effect  
                Aname = data$Aname, #c("X1", "X2", "X3", "X4", "X5", "X6", "X7", "X8", "X9"), # covariates that have time-level random effect  
                re = data$re, #"both",   # two-way random effect: choose from ("unit", "time", "none", "both") 
                ar1 = data$ar1, #TRUE,    # whether the time-level random effects is ar1 process or jsut multilevel (independent)
                r = data$r, #10,        # factor numbers 
                niter = data$niter, #15000, # number of mcmc draws
                burn = data$burn, #5000,   # burn-in draws 
                xlasso = data$xlasso, #1,    ## whether to shrink constant coefs (1 = TRUE, 0 = FALSE)
                zlasso = data$zlasso, #1,    ## whether to shrink unit-level random coefs (1 = TRUE, 0 = FALSE)
                alasso = data$alasso, #1,    ## whether to shrink time-level coefs (1 = TRUE, 0 = FALSE)
                flasso = data$flasso, #1,    ## whether to shrink factor loadings (1 = TRUE, 0 = FALSE)
                a1 = data$a1, a2 = data$a2, #0.001, a2 = 0.001, ## parameters for hyper prior shrink on beta (diffuse hyper priors)
                b1 = data$a1, b2 = data$b2, #0.001, b2 = 0.001, ## parameters for hyper prior shrink on alpha_i
                c1 = data$c1, c2 = data$c2, #0.001, c2 = 0.001, ## parameters for hyper prior shrink on xi_t
                p1 = data$p1, p2 = data$p2) #0.001, p2 = 0.001) ## parameters for hyper prior shrink on factor terms

  sout1 <- coefSummary(out1)  ## summary estimated parameters
  # eout1 <- effSummary(out1,   ## summary treatment effects
  #                     usr.id = NULL, ## treatment effect for individual treated units, if input NULL, calculate average TT
  #                     cumu = FALSE,  ## whether to calculate culmulative treatment effects
  #                     rela.period = TRUE) ## whether to use time relative to the occurence of treatment (1 is the first post-treatment period) or real period (like year 1998, 1999, ...)
  
  # sout1$est.beta
  print(plumber::registered_serializers())
  # print(sout1)
  # as_attachment(sout1, filename = "sout1.json")
  
  write(jsonlite::toJSON(sout1,auto_unbox=FALSE), file="sout1.json")
  zip("result.zip", "sout1.json")

  include_file("result.zip", res, content_type = "application/octet-stream")
  # as_attachment("result.zip", filename="result.zip")

  # paste0("<html><h1>creo que ls() no funciona", x1, x2, "ls", ls(), sout1$est.beta, "</h1></html>")
  # "<html><h1>testing body</h1></html>"
}

#' Echo the parameter that was sent in
#' @param msg The message to echo back.
#' @get /echo
function(msg=""){
  list(msg = paste0("The message is: '", msg, "'"))
}

#' Plot out data from the iris dataset
#' @param spec If provided, filter the data to only this species (e.g. 'setosa')
#' @get /plot
#' @png
function(spec){
  myData <- iris
  title <- "All Species"

  # Filter if the species was specified
  if (!missing(spec)){
    title <- paste0("Only the '", spec, "' Species")
    myData <- subset(iris, Species == spec)
  }

  plot(myData$Sepal.Length, myData$Petal.Length,
       main=title, xlab="Sepal Length", ylab="Petal Length")
}