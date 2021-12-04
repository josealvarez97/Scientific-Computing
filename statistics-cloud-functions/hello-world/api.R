set.seed(1234)
library(bpCausal) 
data(bpCausal)
test <- ls()

x1 <- "x1 string"

#' @get /hello
#' @html
function(){
  set.seed(1234)
  library(bpCausal) 
  data(bpCausal)
  test <- ls()
  # library(forecast)

  x2 <- "x2 string"

  paste0("<html><h1>creo que ls() no funciona",test, x1, x2, "ls", ls(), "</h1></html>")
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