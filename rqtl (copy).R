#Install qtl only if necessary
list.of.packages <- c("qtl")
new.packages <- list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
if(length(new.packages)) install.packages(new.packages)

args <- commandArgs(trailingOnly = TRUE)
minlod <- args[1]
maxrf <- args[2]

library(qtl)
#setwd(dirname(rstudioapi::getActiveDocumentContext()$path));
mapthis <- read.cross("csv", getwd(), "rqtl.csv", crosstype = "riself", estimate.map= FALSE)

#crea grupos de ligamiento, tarda mucho...
mapthis <- est.rf(mapthis)
mapthis <- formLinkageGroups(mapthis, max.rf=maxrf, min.lod=minlod, reorgMarkers=TRUE)
mapthis <- orderMarkers(mapthis, map.function = 'haldane', error.prob=0.05,maxit=500,use.ripple = FALSE)

#mapthis

#order <- compareorder(mapthis, chr=1, c(11:1,12:19), error.prob=0.005)
#mapthis <- switch.order(mapthis, chr=1, c(1:num_rows), error.prob=0.005)  

write.csv(pull.map(mapthis, as.table = TRUE), file = "map.csv")

#for(current_lg in unique(lg$LG)){
#mapthis <- orderMarkers(mapthis, map.function = 'haldane', chr=current_lg, error.prob=0.005)
#  num_rows <- nrow(lg[lg$LG==current_lg,])
#  if(num_rows < 2){
#    next
#  }
#  order <- compareorder(mapthis, chr=current_lg, c(1:num_rows), error.prob=0.005)
#  if(order->orig < order->new){
#    mapthis <- switch.order(mapthis, chr=current_lg, c(1:num_rows), error.prob=0.005)  
#  }
#}

