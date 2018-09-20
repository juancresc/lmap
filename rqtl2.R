list.of.packages <- c("qtl2")
new.packages <- list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
if(length(new.packages)) install.packages(new.packages, repos="http://rqtl.org/qtl2cran")

list.of.packages <- c("devtools", "yaml", "jsonlite", "data.table", "RcppEigen", "RSQLite", "qtl")
new.packages <- list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
if(length(new.packages)) install.packages(new.packages)

library(devtools)
install_github("rqtl/qtl2")
