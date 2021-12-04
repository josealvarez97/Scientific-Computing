# install.packages('devtools', repos = 'http://cran.us.r-project.org') # if not already installed
# devtools::install_github('liulch/bpCausal')

set.seed(1234)
library(bpCausal) 
data(bpCausal)
# ls()

## with factors
out1 <- bpCausal(data = simdata, ## simulated dataset  
                 index = c("id", "time"), ## names for unit and time index
                 Yname = "Y", ## outcome variable
                 Dname = "D", ## treatment indicator  
                 Xname = c("X1", "X2", "X3", "X4", "X5", "X6", "X7", "X8", "X9"), # covariates that have constant (fixed) effect  
                 Zname = c("X1", "X2", "X3", "X4", "X5", "X6", "X7", "X8", "X9"), # covariates that have unit-level random effect  
                 Aname = c("X1", "X2", "X3", "X4", "X5", "X6", "X7", "X8", "X9"), # covariates that have time-level random effect  
                 re = "both",   # two-way random effect: choose from ("unit", "time", "none", "both") 
                 ar1 = TRUE,    # whether the time-level random effects is ar1 process or jsut multilevel (independent)
                 r = 10,        # factor numbers 
                 niter = 150, # number of mcmc draws
                 burn = 50,   # burn-in draws 
                 xlasso = 1,    ## whether to shrink constant coefs (1 = TRUE, 0 = FALSE)
                 zlasso = 1,    ## whether to shrink unit-level random coefs (1 = TRUE, 0 = FALSE)
                 alasso = 1,    ## whether to shrink time-level coefs (1 = TRUE, 0 = FALSE)
                 flasso = 1,    ## whether to shrink factor loadings (1 = TRUE, 0 = FALSE)
                 a1 = 0.001, a2 = 0.001, ## parameters for hyper prior shrink on beta (diffuse hyper priors)
                 b1 = 0.001, b2 = 0.001, ## parameters for hyper prior shrink on alpha_i
                 c1 = 0.001, c2 = 0.001, ## parameters for hyper prior shrink on xi_t
                 p1 = 0.001, p2 = 0.001) ## parameters for hyper prior shrink on factor terms
                 
sout1 <- coefSummary(out1)  ## summary estimated parameters
# eout1 <- effSummary(out1,   ## summary treatment effects
#                     usr.id = NULL, ## treatment effect for individual treated units, if input NULL, calculate average TT
#                     cumu = FALSE,  ## whether to calculate culmulative treatment effects
#                     rela.period = TRUE) ## whether to use time relative to the occurence of treatment (1 is the first post-treatment period) or real period (like year 1998, 1999, ...)

# sout1$est.beta 
# https://stackoverflow.com/questions/49141217/using-rs-plumber-create-get-endpoint-to-host-csv-formatted-data-rather-than-j
# https://stackoverflow.com/questions/45750698/write-table-as-text-file-with-differing-number-of-rows
# https://www.rplumber.io/articles/rendering-output.html?q=json#boxed-vs-unboxed-json
# library(RJSONIO)
write(jsonlite::toJSON(sout1,auto_unbox=FALSE), file="sout1.json")
# write.csv(sout1, "sout1.csv", row.names = FALSE)

# eout1$est.eff
